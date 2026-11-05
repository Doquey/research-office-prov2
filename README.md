# OfficeQA Pro V2 — source-document research

**19 verified source PDFs, 3,726 pages, 168.5 MB. The pilot contains 14 documents in three collections.** Research and collection only: no synthetic QA and no claimed model failures.

| Deliverable | Contents |
|---|---|
| [officeqa_corpus_research.md](officeqa_corpus_research.md) | Benchmark taxonomy, ranked repositories, observed evidence and limitations |
| [document_candidates.json](document_candidates.json) | Metadata, publisher/download URLs, pages, checksums and FM1–FM5 feature mappings for 19 documents |
| [pilot_corpus.json](pilot_corpus.json) | Ten government reports and four BNSF filings |
| [collection_strategy.md](collection_strategy.md) | Expansion, parsing, deduplication, contamination and quality-control workflow |

## Source documents

- **Pilot A:** [Treasurer reports, 1927–1931](documents/treasurer/) — scanned federal receipts/expenditures, foldouts and explicit category changes.
- **Pilot B:** [U.S. Financial Reports, FY2020–FY2024](documents/usfr/) — original/restated figures, category changes and agency financial statements.
- **Pilot C:** [Four BNSF Form 10-K PDFs](documents/bnsf/) — consecutive statement coverage from FY2013 to FY2024. [Eight rendered pages, 36 checked figures and calculation](evidence/bnsf/README.md).
- **Expansion:** [Federal Reserve Board reports, 1930–1934](documents/frb/) — historical bank-level tables, units, earnings and accounting footnotes.
- **Benchmark reference:** [Three public benchmark illustrations](benchmark_reference_only/README.md), isolated from training sources.

Use [ingestion_allowlist.json](ingestion_allowlist.json) rather than scanning the whole repository. [Page text](extracted/) is supplied for all PDFs; OCR is not certified ground truth. [Rendered evidence](evidence/) shows selected difficult pages and revisions.

## Reproducibility

The BNSF PDFs, rendered evidence, and page text are committed here. The government collection indexes link the publisher PDFs. To materialize the government pilot reports locally, install `requirements.txt` and run `python scripts/download_sources.py`. To reproduce the full 19-document audit, include the five expansion reports after reviewing their source-use terms:

```bash
python scripts/download_sources.py --all
python scripts/audit_corpus.py
```

The downloader skips verified existing files and checks downloaded bytes against pinned hashes. [Download records](provenance/download_log.json), [deduplication audit](provenance/deduplication_report.json), and [Publisher source files](provenance/source_files.json) are included.

**Contamination limit:** the public benchmark filename inventory was checked; full benchmark byte/text/image comparison was not possible because files are gated and public hashes are masked. Distinct series are not a guarantee of no shared evidence. See the report before claiming a decontaminated training dataset.

Source works retain their respective rights and notices. No blanket licence is asserted for all assets. Benchmark illustrations and metadata are reference-only.
