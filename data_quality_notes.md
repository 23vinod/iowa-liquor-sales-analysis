# Iowa Liquor Sales Analysis — Data Quality Notes

## 1. Project Overview

**Dataset:** Iowa Liquor Sales — 2024  
**Total Records:** 2,590,975  
**Total Columns:** 24  
**Net Sales:** $447,235,413.62  
**Purpose:** Evaluate the reliability of transaction-level sales data before building business intelligence dashboards.

## 2. Sales Reconciliation

The original and cleaned datasets were compared to verify that the cleaning process preserved transaction counts and sales totals.

**Results:**
- Raw records: 2,590,975
- Cleaned records: 2,590,975
- Raw net sales: $447,235,413.62
- Cleaned net sales: $447,235,413.62
- Difference: $0.00

**Conclusion:** Record counts and sales totals reconcile successfully. This confirms that the cleaning process preserved these totals, but does not independently validate every transaction.

## 3. Product Category Conflicts

**Finding:** 132 unique item numbers have more than one recorded product category.

**Example:** Crown Royal Blackberry (Item 10785) appears under:
- Canadian Whiskies
- Temporary & Specialty Packages

**Business Impact:** Inconsistent category assignments can affect category-level revenue analysis, comparisons, and product classification.

**Action Taken:** Preserved original transaction-level category information and generated `category_conflict_audit.csv`.

**Recommendation:** Investigate classification history before assigning a single standardized category to each affected product.

## 4. Bottle-Size Conflicts

**Finding:** Six item numbers have multiple recorded bottle sizes.

Examples include:
- Arrogant Bastard Whiskey: 700 mL and 750 mL
- Baileys Original Irish Cream Mini: 50 mL and 1,000 mL
- Codigo 1530 Combo Mini: 50 mL and 150 mL

**Business Impact:** Inconsistent bottle sizes can affect volume reporting and product-level comparisons if size is inferred from item number alone.

**Action Taken:** Retained recorded transaction-level bottle sizes and generated a bottle-size conflict report.

**Recommendation:** Verify affected products against authoritative item or product-master records before correcting sizes.

## 5. Negative Sales Adjustments

**Finding:**
- Negative transactions: 2,983
- Total negative sales adjustments: −$445,368.30

**Business Impact:** Excluding negative transactions could overstate net sales and distort financial reporting.

**Action Taken:** Retained negative transactions in net sales calculations and generated adjustment reports by month and category.

**Recommendation:** Confirm adjustment types with the data owner before interpreting all negative records as returns.

## 6. Missing Geographic Information

**Finding:**
- Records with missing geography: 422
- Percentage of total records: 0.0163%
- Net sales affected: $60,180.35

**Business Impact:** Geographic dashboards may exclude these records when grouping by county or ZIP code.

**Action Taken:** Preserved affected transactions and generated `missing_geography_records.csv`.

**Recommendation:** Report the affected sales separately as Unknown Geography rather than silently excluding them.

## 7. Sales Volume Reconciliation

**Reported Sales Liters:** 23,308,430.63 L  
**Calculated Sales Liters:** 23,308,642.68 L  
**Difference:** −212.05 L

The discrepancy is approximately 0.00091% of calculated sales liters.

Individual row-level differences are consistent with rounding of reported liters to two decimal places. No row exceeded a difference of 0.01 L.

**Action Taken:** Retained both reported and calculated values for validation.

**Recommendation:** Document the rounding behavior and use a consistent volume definition in dashboards.

## 8. Bottle-Size Revenue Validation

The bottle-size analysis was reconciled against total net sales.

**Results:**
- Bottle-size revenue shares total: 100%
- Sales reconciliation: Passed
- Bottle-count reconciliation: Passed

The leading revenue-generating sizes were:
- 750 mL: 43.57%
- 1,750 mL: 22.95%
- 1,000 mL: 16.18%

**Conclusion:** The bottle-size report reconciles with the cleaned transaction data.

## 9. Overall Data Quality Assessment

The dataset is suitable for exploratory sales analysis and dashboard development, provided that identified limitations are disclosed.

**Validated:**
- Transaction-count reconciliation
- Net-sales reconciliation
- Bottle-count reconciliation
- Bottle-size revenue-share reconciliation

**Issues requiring attention:**
- Product category inconsistencies
- Bottle-size inconsistencies
- Missing geographic attributes
- Interpretation of negative transactions
- Reported-versus-calculated liters rounding

## 10. Final Recommendation

Use the cleaned dataset for sales performance dashboards while preserving original transaction-level attributes.

Do not silently remove conflicting records, overwrite product classifications, or exclude negative adjustments.

Maintain the generated audit reports and document unresolved data-quality limitations alongside management dashboards.