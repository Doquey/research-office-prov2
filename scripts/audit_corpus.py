"""Read-only PDF validation and reproducible duplicate/overlap audit.

Run from the repository root: python scripts/audit_corpus.py
Outputs provenance/deduplication_report.json. Requires PyMuPDF.
Similarity is a screening signal, not proof of semantic identity.
"""
from pathlib import Path
import collections
import hashlib
import itertools
import json
import re
import fitz

ROOT = Path(__file__).resolve().parents[1]

def norm(text):
    # Keep digits, units and signs: changing financial values must not vanish.
    return re.sub(r'\s+', ' ', text.casefold()).strip()

def audit():
    docs = json.loads((ROOT/'document_candidates.json').read_text())['candidates']
    missing = [d['verification']['local_pdf'] for d in docs
               if not (ROOT / d['verification']['local_pdf']).is_file()]
    if missing:
        raise SystemExit(
            f"{len(missing)} PDF(s) missing, including {missing[0]}. "
            "Run python scripts/download_sources.py --all before auditing the full corpus."
        )
    hashes, text_hashes, source_ids, urls = (collections.defaultdict(list) for _ in range(4))
    page_hashes = collections.defaultdict(list)
    shingles = {}
    checked = []
    for d in docs:
        id = d['id']; path = ROOT/d['verification']['local_pdf']
        data = path.read_bytes(); sha = hashlib.sha256(data).hexdigest()
        assert data.startswith(b'%PDF-'), id
        assert sha == d['verification']['sha256'], id
        with fitz.open(path) as pdf:
            assert len(pdf) == d['page_count'], id
        pages = [json.loads(line) for line in (ROOT/d['verification']['local_page_text']).read_text().splitlines()]
        assert len(pages) == d['page_count'], id
        assert [p['pdf_page'] for p in pages] == list(range(1,len(pages)+1)), id
        text = norm(' '.join(p['text'] for p in pages))
        th = hashlib.sha256(text.encode()).hexdigest()
        hashes[sha].append(id); text_hashes[th].append(id)
        source_ids[(d['collection'],d['reporting_year'],d['title'].casefold())].append(id)
        urls[d['pdf_url']].append(id)
        tokens = re.findall(r'[a-z]+|[+-]?\d[\d,.]*', text)
        shingles[id] = set(' '.join(tokens[i:i+5]) for i in range(len(tokens)-4))
        for p in pages:
            normalized = norm(p['text'])
            if len(normalized) >= 500:
                page_hashes[hashlib.sha256(normalized.encode()).hexdigest()].append({'document_id':id,'pdf_page':p['pdf_page']})
        checked.append({'id':id,'bytes':len(data),'pages':len(pages),'sha256':sha,'normalized_text_sha256':th})
    pairs = []
    for a,b in itertools.combinations(shingles,2):
        A,B=shingles[a],shingles[b]
        overlap=len(A&B)
        pairs.append({'a':a,'b':b,'jaccard':round(overlap/len(A|B),4),'containment_of_smaller':round(overlap/min(len(A),len(B)),4)})
    pairs.sort(key=lambda p:p['jaccard'],reverse=True)
    duplicates=lambda groups:[ids for ids in groups.values() if len(ids)>1]
    repeated=[v for v in page_hashes.values() if len({x['document_id'] for x in v})>1]
    manifest=json.loads((ROOT/'provenance/benchmark_pdf_manifest.json').read_text())
    entries=manifest['entries']
    usable_lfs=[e for e in entries if re.fullmatch(r'[0-9a-f]{64}',e.get('lfs',{}).get('oid',''))]
    report={
        'documents_checked':checked,
        'exact_pdf_duplicate_groups':duplicates(hashes),
        'exact_normalized_text_duplicate_groups':duplicates(text_hashes),
        'same_series_year_title_groups':duplicates(source_ids),
        'same_pdf_url_groups':duplicates(urls),
        'near_document_duplicate_threshold':0.85,
        'near_document_duplicate_candidates':[p for p in pairs if p['jaccard']>=0.85],
        'top_content_overlap_pairs':pairs[:20],
        'cross_document_exact_normalized_page_matches_min_500_chars':repeated,
        'method':'SHA-256 bytes; exact normalized full text; title+series+report year; canonical resolved URL; five-token shingle Jaccard with numbers retained; exact long-page text hashes.',
        'limitations':['Jaccard threshold is heuristic and not calibrated to this corpus.','No perceptual image deduplication or fuzzy table-cell alignment was performed.','Similar annual reports and explicit restatements are retained as distinct vintages; do not erase changed values.','No actual benchmark PDF or full-text comparison was possible.'],
        'benchmark_check':{'manifest_pdf_count':len(entries),'usable_lfs_sha256_count':len(usable_lfs),'identity_matches':[{'id':d['id'],'matches':d['contamination_check']['package_id_matches']} for d in docs if d['contamination_check']['package_id_matches']], 'full_byte_text_dedup_status':'not performed; gated bytes and masked public LFS hashes'},
        'decision':'Use ingestion_allowlist.json for generation. Retain distinct reporting vintages and keep overlapping evidence in the same future split.'
    }
    target=ROOT/'provenance/deduplication_report.json'
    target.write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps({'pdfs':len(docs),'pages':sum(d['page_count'] for d in docs),'exact_duplicates':len(report['exact_pdf_duplicate_groups']),'near_duplicate_candidates':len(report['near_document_duplicate_candidates']),'repeated_page_groups':len(repeated),'highest_jaccard':pairs[0] if pairs else None,'benchmark_hashes_usable':len(usable_lfs)},indent=2))

if __name__ == '__main__':
    audit()
