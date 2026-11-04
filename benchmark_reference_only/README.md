# Public benchmark examples — REFERENCE ONLY

**Do not ingest these files into training or synthetic-question generation.** They illustrate the evaluation target and are excluded by `../ingestion_allowlist.json`.

Source: Databricks AI Research, [OfficeQA Pro V2 announcement, Example Questions](https://www.databricks.com/blog/introducing-officeqa-pro-v2-new-benchmark-enterprise-grounded-reasoning), published 6 August 2026.

| Public example | Included illustration | Brief paraphrase |
|---|---|---|
| Historical payments | [example_1_historical_payments.jpg](example_1_historical_payments.jpg) | Select the relevant 1793 John Jay payments and their warrants; interpret ditto notation. |
| Medicare trend | [example_2_medicare_outlays.png](example_2_medicare_outlays.png) | Assemble revised annual outlays for 1990–1994 and fit a linear trend. |
| Agency forecast | [example_3_agency_outlays.jpg](example_3_agency_outlays.jpg) | Combine agency outlays across eight years and apply the specified forecasting procedure. |

These are the publicly posted source-page illustrations with short summaries, **not a copy of the gated QA dataset or answer key**. See the linked announcement for the full published question wording. No new training questions have been generated here.

`image_sources.json` preserves the exact image URLs, checksums and attribution. The underlying pages are federal records; the blog's annotations/layout may have separate rights. No blanket training or redistribution licence is asserted for Databricks-authored presentation elements. Preserve this attribution and reference-only designation.
