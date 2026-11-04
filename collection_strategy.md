# Collection and expansion strategy

## Immediate pilot

Use the ten PDF paths in `ingestion_allowlist.json`. `pilot_corpus.json` includes the full metadata for both five-year groups; `document_candidates.json` adds five Federal Reserve alternatives. Retain originals and page-level JSONL. Every cited PDF page is 1-based; printed page labels may differ.

Do not generate from the benchmark-reference folder, research report, or download manifest. These contain evaluation context and are not source documents for training. No QA generation has been performed in this collection.

## Scale in coherent blocks

1. **GovInfo first:** extend Treasurer annual reports in adjacent five-to-ten-year blocks. Discover records through title/agency/SuDoc metadata and package IDs; inspect each issue. Next consider other Treasury, Comptroller and agency accounting series only after confirming their numerical sections and benchmark exclusion. Use [GovInfo API/sitemaps](https://www.govinfo.gov/developers), not guessed PDF names.
2. **Treasury next:** extend the [Financial Report archive](https://fiscal.treasury.gov/accounting/us-financial-report/previous-reports), then trace restatement notes to the corresponding agency financial reports. Pair the original and revised vintages, and keep unchanged comparison years for context. Avoid collecting every agency merely to inflate document count.
3. **Historical financial records:** use [FRASER's collections](https://fraser.stlouisfed.org/title/117) to identify recurring Federal Reserve/banking series. Review individual rights and service terms; request an appropriate permitted acquisition route before bulk automated/commercial collection. Prefer original agency or GovInfo copies when available, recording the alternative-scan relation rather than creating duplicate documents. [FRASER terms](https://fraser.stlouisfed.org/terms-of-use)
4. **GAO and SEC later:** GAO audit reports can explain accounting changes but often overlap Treasury appendices. EDGAR provides corporate transfer data with revision histories; it is a lower-similarity extension, not the core corpus. [GAO example](https://www.gao.gov/products/gao-25-107421), [SEC API documentation](https://www.sec.gov/search-filings/edgar-application-programming-interfaces)

Suggested planning stages, not discovered inventory: validate ~50 documents across several coherent periods, scale to ~250 after measuring QA-generation yield, then consider ~1,000 only if enough distinct series and evidence survive quality/contamination review. A thousand files are not necessarily a thousand independent sources.

## Download and parsing

- Resolve the publisher landing page first. Preserve requested URL, redirect target, retrieval timestamp, HTTP result, byte length, SHA-256 and format signature. Pin content versions; changed bytes require a new version entry.
- `python scripts/download_sources.py` verifies existing pilot PDFs or retrieves missing ones against pinned hashes. `--all` includes expansion candidates. A checksum mismatch must not silently overwrite the pinned source.
- Keep original PDF bytes. Store extracted text page-by-page, not as a single undifferentiated passage. Prefer layout-aware extraction with coordinates, cell spans, headers, units, footnotes, section labels and original printed-page labels.
- OCR only where needed. Render rotated/foldout pages at sufficient resolution and tile wide tables with overlap; join cells only with verified header continuity. Preserve raw OCR alongside corrected transcriptions.
- Store figures and unit/sign conventions. Parentheses, dashes, blanks, ditto marks, superscripts and footnote markers must not become interchangeable. Do not turn a missing cell into zero.
- Throttle and cache requests, respect source restrictions, retry transient failures with bounded backoff, and verify the complete PDF after download. Never save an HTML error response with a `.pdf` extension.

## Metadata requirements

Each document needs: stable local ID; exact title; originating institution and hosting repository; series; publication date separate from reporting period; original/revised vintage; canonical publisher/package ID; all download URLs and redirects; checksum; bytes; pages; language; scan/text/layout flags; rights evidence; acquisition timestamp; extraction tool/version; page-map; provenance-linked numerical sections; revision relationships; duplicate cluster; benchmark match status; and split assignment.

Each evidence item needs: document/version, PDF page, printed page if established, table/row/column, unit, sign, period, accounting basis, entity scope, footnote references, and confidence/reviewer status. Record both original and corrected OCR; do not substitute model inference for a printed value.

## Deduplication without destroying revisions

The supplied `scripts/audit_corpus.py` performs byte hashes, normalized-text hashes, series/year/title and resolved-URL checks, five-token document-overlap screening, and exact long-page text matching. Its numerical tokens are retained. The report states the threshold and limitations; no image-level or fuzzy cell-level duplicate clearance is claimed.

For expansion, add page-image perceptual hashes and layout-aware text alignment to find alternate scans, reprints, excerpts and reports embedded in other reports. Use MinHash/LSH or a comparable retrieval index to shortlist pairs, then compare titles, page sequences, tables, values and footnotes. Inspect borderline pairs rather than deleting based on a score alone.

Maintain `work_id`, `edition_id`, `scan_id`, `table_id`, `observation_period` and `publication_vintage`. Alternate scans of one edition may share a canonical record. A real restatement remains a separate edition linked by `revises`; retain changed numbers and notes. Shared templates/boilerplate do not establish duplicate financial evidence. Identical tables repeated across later reports should share an evidence lineage even when the surrounding documents differ.

Build split groups from overlapping documents, tables and revision chains. Keep connected evidence families together; do not randomly split neighboring years containing repeated prior-year tables between training and evaluation. For scale, use non-overlapping series or periods with a reviewed boundary and inspect repeated historical series crossing that boundary.

## Benchmark contamination checks

The cached public benchmark manifest contains all 1,435 PDF paths. No matching candidate Treasury package ID was found, but benchmark PDF bytes were unavailable and LFS hashes were masked. This is identity screening only.

With legitimately authorized dataset access, build an evaluation-document exclusion inventory from corpus metadata; avoid loading answer keys into the training pipeline. Compare candidate bytes, normalized text, page images and distinctive table fragments against the **whole** evaluation corpus, not only the 249 cited documents. Exclude alternate scans, renamed copies, embedded exact pages and near-duplicate benchmark prompts. Preserve match evidence and explicit unresolved cases.

The three public benchmark illustrations are reference-only. Their filenames, hashes and URLs are recorded in `benchmark_reference_only/image_sources.json`; `training_allowed` is false. Do not ingest gated QA/answer data, and follow the [dataset's stated access conditions](https://huggingface.co/datasets/databricks/officeqa-pro-v2).

## Source use and quality gates

GovInfo's policy distinguishes government works from embedded third-party copyright. [Policy](https://www.govinfo.gov/about/policies) The inspected FRASER title has a No Copyright–United States label, but that does not replace the service's access restrictions. Corporate SEC filings and benchmark-blog figures should not inherit a blanket government-work licence. Keep source-specific attribution; do not apply one repository licence indiscriminately to all source assets.

Before admitting a new document: verify its URL, actual title, year, full download, page count, text availability, rights note, numerical section and duplicate/benchmark status. Inspect at least one difficult table and its notes. Prefer coherent annual sequences over unrelated easy PDFs.

Before calling a future sample a model failure: independently reconstruct its answer from source cells, specify cutoff/vintage, reconcile units and scopes, check alternative interpretations, and confirm answerability. Evaluate with the declared model/version, harness, modalities, tool budget and repeated attempts. Separate retrieval, parsing, temporal/category, arithmetic and infrastructure failures. Do not manufacture ambiguity or remove necessary evidence to depress model accuracy.
