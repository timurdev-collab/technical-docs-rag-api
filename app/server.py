from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from urllib.parse import urlparse,parse_qs
from pathlib import Path
import json
from app.retrieval import Retriever

INDEX=Retriever(Path(__file__).resolve().parents[1]/'docs')

class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        parsed=urlparse(self.path)
        qs=parse_qs(parsed.query)
        if parsed.path=='/health':
            data={'status':'ok','documents':len(INDEX.records)}
            status=200
        elif parsed.path=='/search':
            try:
                k=int(qs.get('k',['3'])[0])
                query=qs.get('q',[''])[0]
                data={'query':query,'results':INDEX.search(query,k)}
                status=200
            except ValueError:
                data={'error':'k must be an integer'}
                status=400
        else:
            data={'error':'not found'}
            status=404
        body=json.dumps(data).encode()
        self.send_response(status)
        self.send_header('Content-Type','application/json')
        self.send_header('Content-Length',str(len(body)))
        self.end_headers()
        self.wfile.write(body)

if __name__=='__main__':
    print('Listening at http://localhost:8000')
    ThreadingHTTPServer(('127.0.0.1',8000),Handler).serve_forever()
