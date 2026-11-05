# BNSF statement evidence

The four issuer PDFs report 12 fiscal years in four separate three-year windows. Page numbers below count from the first PDF page. Click a page number to inspect the full rendered page.

| Form 10-K | Statement years | Consolidated income | Consolidated cash flows | Independent copy |
|---|---|---|---|---|
| [2015](../../documents/bnsf/bnsf_2015.pdf) | FY2013–FY2015 | [PDF p. 19](2015_income.png) | [PDF p. 22](2015_cash_flows.png) | [SEC filing](https://www.sec.gov/Archives/edgar/data/934612/000093461216000034/llc12312015-10k.htm) |
| [2018](../../documents/bnsf/bnsf_2018.pdf) | FY2016–FY2018 | [PDF p. 19](2018_income.png) | [PDF p. 22](2018_cash_flows.png) | [SEC filing](https://www.sec.gov/Archives/edgar/data/934612/000093461219000005/llc12311810k.htm) |
| [2021](../../documents/bnsf/bnsf_2021.pdf) | FY2019–FY2021 | [PDF p. 22](2021_income.png) | [PDF p. 25](2021_cash_flows.png) | [SEC filing](https://www.sec.gov/Archives/edgar/data/934612/000093461222000005/bni-20211231.htm) |
| [2024](../../documents/bnsf/bnsf_2024.pdf) | FY2022–FY2024 | [PDF p. 22](2024_income.png) | [PDF p. 25](2024_cash_flows.png) | [SEC filing](https://www.sec.gov/Archives/edgar/data/934612/000093461225000003/bni-20241231.htm) |

## Verified figures and arithmetic

[Download the 12 annual observations](statement_values.csv). For each fiscal year we matched three numbers in the issuer PDF to the corresponding SEC HTML table. All 36 cells matched. Both documents describe Burlington Northern Santa Fe, LLC and subsidiaries. All monetary values are USD millions. The cash-flow columns preserve the filing’s negative sign for cash spent.

For FY2013–FY2024, consolidated revenue sums to **273,158**. Cash spent on capital expenditures excluding equipment sums to **38,950**, and cash spent acquiring equipment sums to **6,847**. Defining the numerator as the positive sum of those two investing outflows gives **(38,950 + 6,847) / 273,158 = 16.7658%**. This definition excludes noncash investment. A simple average of the 12 yearly percentages weights small and large revenue years equally and answers a different question.

This is a source reconciliation for reviewers. Model performance has not been tested.
