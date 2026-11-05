# OfficeQA Pro V2: source-corpus research

Government corpus research dated 4 November 2026. The [corporate addendum](evidence/bnsf/README.md) was added on 5 November. Deliverable: **15 downloaded, inspected candidates (3,479 PDF pages); a 10-document pilot in two coherent collections**. No training questions, answers or model rollouts were generated. Evidence locations and verified download metadata are in [document_candidates.json](document_candidates.json).

## 1. What the benchmark actually contains

**Confirmed from the official dataset card:** Pro V2 contains 90 questions over 1,435 federal receipts-and-expenditures PDFs, covering 1793–2024 and 211 distinct years. Its principal series are Treasury Combined Statements and earlier Congressional serial-set receipts documents. Median source count is 5.5 per question, range 1–24; 249 documents are cited by the questions. The distributed corpus includes original PDFs and parsed JSON with element types, tables, bounding boxes and page metadata. The CSV stores answers and source-page provenance. Corpus access is gated; the card prohibits training evaluated models on answer keys. [Dataset card](https://huggingface.co/datasets/databricks/officeqa-pro-v2)

**Version distinction:** Treasury Bulletins are the corpus for OfficeQA Pro/Full, not Pro V2. The GitHub repository supplies code and corpus tooling; large dataset files are hosted on Hugging Face. [Official repository](https://github.com/databricks/officeqa)

The following era tendencies are **reported by Databricks**, not an independently completed census of every benchmark PDF. Treasury is the originating accounting institution; Congressional publications provide earlier records. [Benchmark announcement](https://www.databricks.com/blog/introducing-officeqa-pro-v2-new-benchmark-enterprise-grounded-reasoning)

| Corpus layer | Observed/reported document characteristics | Numerical interpretation burden |
|---|---|---|
| Late 1700s/early 1800s | Individual payments, warrants, long-s typography, ditto notation, landscape foldouts | Carry-forward labels; payment versus date/identifier |
| Mid-1800s | T-accounts and ruled tables; calendar/fiscal-period transitions | Opposing account sides and period boundaries |
| Early 1900s | Opening/closing balances, appropriations, surplus/deficit conventions | Stocks versus flows; account scope |
| Late 1900s onward | Annual Combined Statements and appendices; later digital documents and charts | Agency/account hierarchy, units and revised prior-year columns |

Databricks reports roughly 120,000 pages and a mean of 6.7 sources per question. Reported difficulties include parsing fidelity, temporal reconciliation and entity/category scope. **FM1–FM5 remain hypotheses for this new collection**; observing a document feature does not establish that Astra, Fable or Kimi fails on it. [Announcement](https://www.databricks.com/blog/introducing-officeqa-pro-v2-new-benchmark-enterprise-grounded-reasoning)

## 2. Repository comparison

Ranking below is our inference about similarity and usefulness for this pilot, not a benchmark-author ranking. Stable-looking identifiers are evidence of reproducibility today, not a guarantee against future URL changes.

| Rank / repository | Similarity and historical coverage | Access, text, recurring series and limitations |
|---|---|---|
| **1. GovInfo** | Historical Treasury receipts/expenditures and governmental accounting. Verified Treasurer series: 1927–1931. | Individual package IDs, PDF, text and descriptive metadata; consecutive annual reports. [1930 record](https://www.govinfo.gov/app/details/GOVPUB-T-605cd93d3b25243e27afc459aac55a91) exposes all these formats and a government-work rights statement. Package-based URLs plus API/sitemaps support scaling; the API uses a key. [Developer hub](https://www.govinfo.gov/developers) |
| **2. Treasury / Fiscal Service** | Closest modern federal-accounting analogue. Verified Financial Reports: FY2020–FY2024; publication years 2021–2025. Accrual Financial Reports differ from Combined Statements. | Whole PDFs, section downloads and HTML contents; selectable text, comparative statements and notes. [2024 contents](https://fiscal.treasury.gov/accounting/us-financial-report/2024), [archive](https://fiscal.treasury.gov/accounting/us-financial-report/previous-reports). Paths are less canonical than GovInfo package IDs; retain resolved URLs and checksums. |
| **3. FRASER / St. Louis Fed** | Strong historical scan/table match, but central-bank accounts differ from federal spending accounts. Annual-report collection lists 1914–2024; verified candidates cover 1930–1934. | Item URLs, PDF downloads, automatically extracted full text and consecutive issues. [Collection and rights](https://fraser.stlouisfed.org/title/117), [OCR example](https://fraser.stlouisfed.org/title/annual-report-board-governors-federal-reserve-system-117/1932-2490/fulltext). This collection is labelled No Copyright–United States; service terms separately restrict automated/commercial use. [Terms](https://fraser.stlouisfed.org/terms-of-use) |
| **4. GAO** | Valuable audit explanations and accounting-scope evidence; less uniform as a historical numerical corpus. Government-wide reporting discussed in the inspected record begins with FY1997. | Product IDs, reports and accessible PDF variants. [FY2024/2023 audit](https://www.gao.gov/products/gao-25-107421). Can duplicate audit material already embedded in Treasury reports; do not count wrappers as new independent evidence. Broad search page returned 403 during this run, but the product page resolved. |
| **5. SEC EDGAR** | Useful corporate statement/restatement transfer set; weaker match to historical federal accounting. Modern XBRL is not a substitute for old scanned reports. | Filing identities, HTML/inline-XBRL, submission and fact JSON; annual/quarterly sequences. XBRL requirement began in 2009; bulk JSON is available. [Official API guide](https://www.sec.gov/search-filings/edgar-application-programming-interfaces). PDF availability varies; corporate submissions are not automatically U.S. government works. |

For government documents, distinguish the underlying work from third-party material embedded in it; preserve attribution and notices. GovInfo explains that government publications can include copyrighted components. [Policy](https://www.govinfo.gov/about/policies) FRASER is a discovery priority for historical records, but expansion must respect its separate service terms rather than assume unrestricted scraping.

## 3. Best collections and evidence

The pilot deliberately retains difficult scans and explicit accounting changes. Its selection is **5 Treasurer reports (1927–1931) + 5 U.S. Financial Reports (FY2020–FY2024)**. Federal Reserve annual reports 1930–1934 are retained as five verified expansion candidates. Full metadata and grouping are in [pilot_corpus.json](pilot_corpus.json).

| Priority feature | Concrete inspected evidence | Status / use |
|---|---|---|
| Historical category correction | [Treasurer 1930, PDF p11](https://www.govinfo.gov/content/pkg/GOVPUB-T-605cd93d3b25243e27afc459aac55a91/pdf/GOVPUB-T-605cd93d3b25243e27afc459aac55a91.pdf#page=11): French debt-settlement receipts transferred from interest to principal | **Confirmed FM3/FM4 feature.** Annual and monthly categories must follow the footnote. [Rendered detail](evidence/treasurer_1930_p11_footnote.png) |
| Institutional reorganization | [Treasurer 1931, PDF p13](https://www.govinfo.gov/content/pkg/GOVPUB-T-f151a087ee13443487af0236d2cf70f3/pdf/GOVPUB-T-f151a087ee13443487af0236d2cf70f3.pdf#page=13): July 1930 expenditures reassigned from Interior/War to Veterans Administration for comparison | **Confirmed FM3/FM4 feature.** The scan says 1930; OCR misreads that year in one place. [Rendered detail](evidence/treasurer_1931_p13_footnote.png) |
| Actual versus statement totals | [Treasurer 1929, PDF pp11,13](https://www.govinfo.gov/content/pkg/GOVPUB-T-90d60562805b848788b86c614091c9cf/pdf/GOVPUB-T-90d60562805b848788b86c614091c9cf.pdf#page=11): monthly totals, clearing adjustments and revised annual amounts | **Confirmed within-report reconciliation.** This alone does not prove a cross-publication restatement. |
| Original versus restated fiscal year | [FY2020 report, PDF p74](https://fiscal.treasury.gov/system/files/files/reports-statements/financial-report/2020/fr-03-25-2021-(final).pdf#page=74) and [FY2021 report, PDF p72](https://fiscal.treasury.gov/system/files/files/reports-statements/financial-report/2021/fr-02-17-2022-(final).pdf#page=72); explanation on FY2021 p88 | **Confirmed FM3 feature.** Both vintages inspected; revised labels and changed cells are visible. [Side-by-side evidence](evidence/reconciliation.png) |
| Accounting category without total change | [FY2022 report, PDF p150](https://fiscal.treasury.gov/system/files/files/reports-statements/financial-report/2022/02-16-2023-FR-(Final).pdf#page=150): Smithsonian funds moved between dedicated and other categories without changing total net position; p105 explains GSE gain presentation | **Confirmed FM3/FM4 feature.** Pair with FY2021 report for earlier presentation. |
| Comparative presentation changes | [FY2023 p86](https://fiscal.treasury.gov/system/files/files/reports-statements/financial-report/2023/02-15-2024-FR-(final).pdf#page=86) and [FY2024 p88](https://fiscal.treasury.gov/system/files/files/reports-statements/financial-report/2024/01-16-2025-FR-(Final).pdf#page=88) | **Confirmed FM3 feature:** unmatched-transactions presentation and payroll/leave liability categories. Do not relabel these as material error corrections. |
| Similar names, mixed units | [Federal Reserve 1933, PDF p69](https://fraser.stlouisfed.org/files/docs/publications/arfr/1930s/arfr_1933.pdf#page=69): comparative table in thousands and bank-level table in dollars | **Confirmed FM2/FM4 feature.** Useful expansion; model failure untested. |

FM1 and FM5 are **Potential** at task level: annual/monthly evidence exists, but no question has been designed to establish that multiple documents are necessary. Several tables already repeat previous years; a future task must not accidentally be solvable from one summary table. Historical scans visibly break ordinary text extraction order; the extracted JSONL files are search aids, not certified table transcriptions.

## 4. Target models and experiment implications

Moonshot's supplied Kimi K3.1 Pro card reports OfficeQA Pro V2 scores of **64.4 for Kimi K3.1 Pro, 54.5 for Claude Fable 5.1 and 54.4 for GPT-6 Astra**. These are provider-reported results, not experiments conducted here. The card specifies page-image input without machine-readable text; Astra uses Codex, the others Claude Code. Its comparison headers include max effort and fallback qualifications. [Model card and evaluation footnotes](https://huggingface.co/moonshotai/Kimi-K3.1-Pro)

For the intended 5–10 future samples, start with the explicitly evidenced revisions above, then combine them with retrieval and numerical operations only where evidence requires it. Evaluate raw-page and parsed-text conditions separately with fixed tool budgets. A failure in one attempt is not proof a model cannot solve the task; repeat runs and inspect the evidence/ground truth before calling it a model failure.

## 5. Deduplication, contamination and limits

The reproducible audit validates PDF signatures, page counts, SHA-256 values, normalized text, series/year/title identities, resolved URLs and document/page overlap. Results: [deduplication_report.json](provenance/deduplication_report.json). Distinct annual vintages are preserved; similar templates are not deleted merely because they look alike.

We recovered the complete **1,435-path public PDF manifest** and checked package identities. Candidate series differ from the named benchmark series, and no Treasurer package ID matched. **This is not a complete contamination clearance:** benchmark bytes were gated and the public LFS hashes were masked, so exact-hash, alternate-scan and full-text overlap against the benchmark remain untested. Some underlying federal statistics can naturally recur across series. Keep this limitation with any downstream dataset claim.

Only a sample of relevant pages in each PDF was inspected; no exhaustive cell audit or model evaluation was performed. The pilot does not cover 18th-century typography, all possible Treasury account-symbol hierarchies, or the entire benchmark retrieval scale. Modern reports also have audit limitations; ground future answers in explicitly identified reported figures rather than claim those figures establish economic truth.

Public benchmark illustrations are isolated in [benchmark_reference_only/](benchmark_reference_only/README.md); no gated QA file or answer key was obtained. The [ingestion allowlist](ingestion_allowlist.json) excludes them from generation.
