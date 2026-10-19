import unittest
from pathlib import Path
from app.retrieval import Retriever,tokenize,chunks

class RetrievalTests(unittest.TestCase):
    def test_tokenize(self):
        self.assertEqual(tokenize('Pressure-Loss!'),['pressure','loss'])
    def test_chunks(self):
        self.assertEqual(chunks('one two three',2),['one two','three'])
    def test_search(self):
        index=Retriever(Path(__file__).resolve().parents[1]/'docs')
        found=index.search('pressure loss')
        self.assertTrue(found)
        self.assertTrue(all(row['score']>0 for row in found))

if __name__=='__main__':
    unittest.main()
