import copy, datetime as dt, sys, tempfile, unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "skills" / "pmdaa" / "scripts"))
import portfolio as pf

TODAY = dt.date(2026, 10, 13)


def project(pid, **kw):
    p = {"id": pid, "name": pid, "visibility": "public", "north_star": "n", "state": "doing", "rag": "green",
         "rag_evidence": "ci ok", "milestone": {"id": "M0", "exit_test": "pytest passes"},
         "next_actions": [{"action": "a"}], "owner": "o", "last_verified": "2026-10-13"}
    p.update(kw)
    return p


def ledger(*projects, **kw):
    return {"portfolio": "t", "north_star": "n", "wip_limit": 3, "projects": list(projects), **kw}


class Check(unittest.TestCase):
    def errs(self, lg, **kw):
        return pf.check(lg, now=TODAY, **kw)

    def test_valid(self):
        self.assertEqual(self.errs(ledger(project("a"), project("b", depends_on=["a"]))), ([], []))

    def test_rules(self):
        bad = [project("a", rag="blue"), project("b", milestone={"id": "M1"}), project("c", next_actions=[1, 2, 3, 4]),
               project("d", state="blocked"), project("e", depends_on=["zz"]), project("f", rag_evidence="")]
        errors, _ = self.errs(ledger(*bad))
        for needle in ("a: rag", "b: current milestone", "c: at most 3", "d: state blocked", "e: depends_on unknown", "f: a RAG"):
            self.assertTrue(any(e.startswith(needle) for e in errors), needle)

    def test_cycle(self):
        errors, _ = self.errs(ledger(project("a", depends_on=["b"]), project("b", depends_on=["a"])))
        self.assertTrue(any("cycle" in e for e in errors))

    def test_stale_and_live(self):
        p = project("a", last_verified="2026-09-01", evidence={"head": "abc1234"},
                    live={"head": "def567890", "ci": "failure", "visibility": "private"})
        errors, warnings = self.errs(ledger(p, project("b"), project("c"), project("d")))
        self.assertTrue(any("GitHub says private" in e for e in errors))
        for needle in ("STALE, last verified", "STALE CLAIM", "UNVERIFIED", "WIP 4 > limit 3"):
            self.assertTrue(any(needle in w for w in warnings), needle)

    def test_public_safety(self):
        secret = project("x", visibility="private")
        errors, _ = self.errs(ledger(secret), public=True)
        self.assertTrue(any("x: private project in a public ledger" in e for e in errors))
        safe = {"id": "x", "name": "X", "visibility": "private", "one_line": "building", "rag": "green", "state": "doing"}
        self.assertEqual(self.errs(ledger(safe), public=True), ([], []))

    def test_pair(self):
        pair = {"public": "o/plan", "private": "o/build"}
        ok = project("p", repos=pair, evidence={"public": {"head": "abc1234"}},
                     live={"public": {"visibility": "public", "head": "abc1234ff"},
                           "private": {"visibility": "private", "head": "0000000", "ci": "failure"}})
        self.assertEqual(self.errs(ledger(ok))[0], [])
        self.assertTrue(any("p [private]: UNVERIFIED" in w for w in self.errs(ledger(ok))[1]))
        swapped = project("p", repos=pair, live={"public": {"visibility": "private"}})
        self.assertTrue(any("p [public]: ledger says public but GitHub says private" in e for e in self.errs(ledger(swapped))[0]))
        for bad in (project("p", repos={"secret": "o/x"}), project("p", repos=pair, repo="o/plan"),
                    project("p", repos={"private": "o/build"})):  # private-only pair must be a private project
            self.assertTrue(self.errs(ledger(bad))[0], bad)

    def test_pair_public_ledger_names_private_repo_only(self):
        named = project("p", repos={"public": "o/plan", "private": "o/build"}, live={"public": {"visibility": "public"}})
        self.assertEqual(self.errs(ledger(named), public=True), ([], []))
        leaky = project("p", repos={"public": "o/plan", "private": "o/build"}, live={"private": {"head": "abc", "ci": "failure"}})
        errors, warnings = self.errs(ledger(leaky), public=True)
        self.assertTrue(any("name the private repo only" in e for e in errors))
        self.assertFalse(any("[private]" in w for w in warnings))

    def test_refresh_pair_and_single(self):
        seen = []
        def fake(*args):
            seen.append(args[2] if args[0] == "repo" else None)
            if args[0] == "repo":
                return {"visibility": "PRIVATE" if "build" in args[2] else "PUBLIC", "defaultBranchRef": {"name": "main"}}
            if args[0] == "api":
                return {"sha": "f" * 40, "commit": {"committer": {"date": "d"}, "message": "m"}}
            return []
        real, pf.gh = pf.gh, fake
        try:
            lg = ledger(project("p", repos={"public": "o/plan", "private": "o/build"}), project("s", repo="o/single"))
            pf.refresh(lg)
            self.assertEqual({k: v["visibility"] for k, v in lg["projects"][0]["live"].items()}, {"public": "public", "private": "private"})
            self.assertEqual(lg["projects"][1]["live"]["visibility"], "public")
            pub = ledger(project("p", repos={"public": "o/plan", "private": "o/build"}), public=True)
            seen.clear(); pf.refresh(pub)
            self.assertEqual(list(pub["projects"][0]["live"]), ["public"])
            self.assertNotIn("o/build", seen)
        finally:
            pf.gh = real

    def test_critical_path_skips_done(self):
        ps = [project("a", state="done"), project("b", depends_on=["a"]), project("c", depends_on=["b"]), project("d")]
        self.assertEqual(pf.critical_path(ps), ["b", "c"])

    def test_ci_summary(self):
        ok = {"status": "completed", "conclusion": "success"}
        self.assertEqual(pf.ci_summary([]), "none")
        self.assertEqual(pf.ci_summary([ok]), "success")
        self.assertEqual(pf.ci_summary([ok, {"status": "in_progress", "conclusion": ""}]), "pending")
        self.assertEqual(pf.ci_summary([ok, {"status": "completed", "conclusion": "failure"}]), "failure")

    def test_board(self):
        with tempfile.TemporaryDirectory() as d:
            pf.render(ledger(project("a"), project("b", depends_on=["a"])), d)
            self.assertIn("critical path: a → b", (Path(d) / "BOARD.md").read_text())
            self.assertIn("<table>", (Path(d) / "board.html").read_text())
            self.assertTrue((Path(d) / "status" / "b.md").is_file())


class Example(unittest.TestCase):
    def test_example_is_public_safe(self):
        import yaml
        root = Path(__file__).resolve().parents[1]
        for f in (root / "examples").glob("*/PORTFOLIO.yaml"):
            errors, _ = pf.check(yaml.safe_load(f.read_text()), public=True, stale_days=10**6)
            self.assertEqual(errors, [], f)


if __name__ == "__main__":
    unittest.main()
