"""Tiny transparent retrieval sanity evaluation; not a generalizable benchmark."""
from pathlib import Path
from app.retrieval import Retriever
cases=[('pressure loss','pressure-loss.md'),
       ('sensor calibration','sensor-maintenance.md'),
       ('flow assurance','flow-assurance.md')]
index=Retriever(Path(__file__).resolve().parents[1]/'docs')
correct=sum(bool(index.search(q,k=1)) and index.search(q,k=1)[0]['source']==expected
            for q,expected in cases)
print(f'Sample top-1 accuracy: {correct}/{len(cases)}')
print('These three hand-authored queries do not establish production quality.')
