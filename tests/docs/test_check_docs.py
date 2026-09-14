"""Behavioral tests for the documentation validator, using synthetic files only."""
from __future__ import annotations

import importlib.util
import json
import tempfile
import unittest
from pathlib import Path

SCRIPT = Path(__file__).resolve().parents[2] / "scripts" / "check_docs.py"
# The test file lives in tests/docs; the repository root is parents[2].


class DocumentationChecksTest(unittest.TestCase):
    def setUp(self) -> None:
        self.assertTrue(SCRIPT.is_file(), "documentation validator has not been implemented")
        spec = importlib.util.spec_from_file_location("check_docs", SCRIPT)
        self.assertIsNotNone(spec)
        assert spec is not None and spec.loader is not None
        self.checker = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(self.checker)
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)

    def write(self, path: str, content: str) -> Path:
        target = self.root / path
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(content, encoding="utf-8")
        return target

    def skill(self, name: str = "appops-example") -> Path:
        return self.write(
            f".agents/skills/{name}/SKILL.md",
            f"---\nname: {name}\ndescription: Use when testing a synthetic example.\n---\n\n# Example\n",
        )

    def catalog(self, entries: list[dict[str, str]] | None = None) -> None:
        items = entries if entries is not None else [
            {"name": "appops-example", "path": ".agents/skills/appops-example/SKILL.md"}
        ]
        self.write(".agents/skills/catalog.json", json.dumps({"schema_version": 1, "skills": items}) + "\n")

    def scenarios(self, skill: str = "appops-example") -> None:
        self.write("tests/skills/scenarios.json", json.dumps({
            "schema_version": 1, "execution_status": "NOT_RUN", "scenarios": [{
                "id": "SK01", "skill": skill, "prompt": "Synthetic pressure prompt",
                "expected": ["Preserve the invariant"], "forbidden": ["Bypass the invariant"]
            }]
        }) + "\n")

    def test_existing_local_link_is_accepted(self) -> None:
        self.write("docs/target.md", "# Target\n")
        source = self.write("README.md", "# Start\n\n[Target](docs/target.md#section)\n")
        self.assertEqual(self.checker.check_markdown(source, self.root), [])

    def test_missing_local_link_is_reported(self) -> None:
        source = self.write("README.md", "[Missing](docs/missing.md)\n")
        self.assertTrue(any("missing link" in item for item in self.checker.check_markdown(source, self.root)))

    def test_outside_repository_link_is_rejected(self) -> None:
        source = self.write("README.md", "[Outside](../private.md)\n")
        self.assertTrue(any("outside repository" in item for item in self.checker.check_markdown(source, self.root)))

    def test_external_links_and_fenced_examples_are_not_fetched(self) -> None:
        source = self.write("README.md", "[Web](https://example.invalid/x)\n\n```text\n[Example](missing.md)\n```\n")
        self.assertEqual(self.checker.check_markdown(source, self.root), [])

    def test_whitespace_and_missing_final_newline_are_reported(self) -> None:
        source = self.write("README.md", "# Title  ")
        errors = self.checker.check_markdown(source, self.root)
        self.assertTrue(any("trailing whitespace" in item for item in errors))
        self.assertTrue(any("final newline" in item for item in errors))

    def test_valid_skill_is_accepted(self) -> None:
        self.assertEqual(self.checker.check_skill(self.skill()), [])

    def test_skill_name_must_match_directory(self) -> None:
        source = self.skill()
        source.write_text(source.read_text().replace("name: appops-example", "name: wrong-name"))
        self.assertTrue(any("directory" in item for item in self.checker.check_skill(source)))

    def test_skill_requires_description(self) -> None:
        source = self.write(".agents/skills/appops-example/SKILL.md", "---\nname: appops-example\n---\n# Example\n")
        self.assertTrue(any("description" in item for item in self.checker.check_skill(source)))

    def test_valid_catalog_is_accepted(self) -> None:
        self.skill()
        self.catalog()
        self.assertEqual(self.checker.check_catalog(self.root), [])

    def test_duplicate_catalog_entries_are_rejected(self) -> None:
        self.skill()
        entry = {"name": "appops-example", "path": ".agents/skills/appops-example/SKILL.md"}
        self.catalog([entry, entry])
        self.assertTrue(any("duplicate" in item for item in self.checker.check_catalog(self.root)))

    def test_uncatalogued_skill_is_reported(self) -> None:
        self.skill()
        self.catalog([])
        self.assertTrue(any("not in catalog" in item for item in self.checker.check_catalog(self.root)))

    def test_valid_pressure_scenario_is_accepted_without_claiming_execution(self) -> None:
        self.skill()
        self.catalog()
        self.scenarios()
        self.assertEqual(self.checker.check_scenarios(self.root), [])

    def test_unknown_scenario_skill_and_missing_coverage_are_reported(self) -> None:
        self.skill()
        self.catalog()
        self.scenarios("unknown-skill")
        errors = self.checker.check_scenarios(self.root)
        self.assertTrue(any("unknown skill" in item for item in errors))
        self.assertTrue(any("no pressure scenario" in item for item in errors))

    def test_malformed_catalog_is_reported_not_crashed(self) -> None:
        self.write(".agents/skills/catalog.json", "{not json}\n")
        self.assertTrue(any("invalid JSON" in item for item in self.checker.check_catalog(self.root)))


if __name__ == "__main__":
    unittest.main()
