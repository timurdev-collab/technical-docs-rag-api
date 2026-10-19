import tempfile
import unittest
from pathlib import Path
from app.retrieval import Retriever

class RetrievalQualityTests(unittest.TestCase):
    def test_empty_query_returns_no_passages(self):
        with tempfile.TemporaryDirectory() as directory:
            (Path(directory) / "a.md").write_text("pressure sensor maintenance")
            self.assertEqual(Retriever(directory).search("   "), [])

    def test_ranking_and_source_attribution(self):
        with tempfile.TemporaryDirectory() as directory:
            (Path(directory) / "pressure.md").write_text("pressure pressure leak pressure sensor")
            (Path(directory) / "flow.md").write_text("flow pump monitoring")
            matches = Retriever(directory).search("pressure leak", k=2)
            self.assertEqual(matches[0]["source"], "pressure.md")
            self.assertGreater(matches[0]["score"], 0)
            self.assertEqual(matches[0]["chunk"], 0)

    def test_index_is_independent_of_file_creation_order(self):
        with tempfile.TemporaryDirectory() as directory:
            (Path(directory) / "z.md").write_text("zinc sensor")
            (Path(directory) / "a.md").write_text("alpha sensor")
            self.assertEqual([r["source"] for r in Retriever(directory).records], ["a.md", "z.md"])

if __name__ == "__main__":
    unittest.main()
