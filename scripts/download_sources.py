"""Re-download the manifest PDFs with checksum validation (pilot by default).

python scripts/download_sources.py [--all]
No benchmark-reference files are downloaded or used for training.
"""
from pathlib import Path
import argparse
import hashlib
import json
import time
import urllib.request

ROOT = Path(__file__).resolve().parents[1]

def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('--all',action='store_true',help='Include the five Federal Reserve expansion reports; review their service-use terms before new bulk collection.')
    args=parser.parse_args()
    docs=json.loads((ROOT/'document_candidates.json').read_text())['candidates']
    for d in docs:
        if not args.all and not d['selected_for_pilot']: continue
        path=ROOT/d['verification']['local_pdf'];expected=d['verification']['sha256']
        if path.exists():
            if hashlib.sha256(path.read_bytes()).hexdigest()!=expected:
                raise ValueError(f'Existing file checksum mismatch: {path}; preserve and investigate.')
            print(d['id'],'already verified');continue
        path.parent.mkdir(parents=True,exist_ok=True)
        part=path.with_suffix('.pdf.part')
        for attempt in range(3):
            try:
                request=urllib.request.Request(d['pdf_url'],headers={'User-Agent':'OfficeQA-Source-Research/1.0'})
                with urllib.request.urlopen(request,timeout=90) as response, part.open('wb') as output:
                    while chunk:=response.read(1024*1024):output.write(chunk)
                data=part.read_bytes()
                if not data.startswith(b'%PDF-') or hashlib.sha256(data).hexdigest()!=expected:
                    raise ValueError('Downloaded content differs from the pinned PDF; inspect before accepting a new version.')
                part.replace(path);print(d['id'],'downloaded and verified');break
            except ValueError:
                raise
            except Exception:
                if attempt==2:raise
                time.sleep(2**attempt)
        time.sleep(1)

if __name__=='__main__':main()
