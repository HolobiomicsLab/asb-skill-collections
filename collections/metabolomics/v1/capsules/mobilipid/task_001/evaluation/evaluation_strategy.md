# Evaluation Strategy

## Direct Checks

- Verify file 'DTCCSN2_library.csv' (or equivalent lipid library file with .csv, .xlsx, .rda, or .txt extension) exists in github:FelinaHildebrand__MobiLipid repository root or designated data directory
- Verify file format is consistent with tabular structure (row_count_equals at least 1 header row plus data rows; field_present for columns: lipid_identifier, CCS_value, lipid_class, isotope_label)
- Verify field 'isotope_label' contains substring 'U13C' or '13C' for all library entries (robust to case variation)
- Value of field 'CCS_value' is in_range and numeric (non-null, parseable as float); no canonical answer for absolute range without instrument metadata — expert review required for physical plausibility
- Verify lipid_class field contains_substring at least one of: 'PC', 'PE', 'PS', 'PG', 'PA', 'PI', 'LPC', 'LPE', 'SM', 'Cer', 'DAG', 'TAG', 'CE' (or equivalent LIPID MAPS nomenclature) — multiple defensible class schemes exist
- Verify row_count_equals is greater than 10 (minimum viable library size for CCS bias assessment across multiple lipid classes)

## Expert Review

- Review CCS values for physical plausibility: confirm they fall within expected range for singly or doubly charged lipid ions under nitrogen drift gas (typical range ~200–600 Ų for phospholipids, ~300–800 Ų for triacylglycerols); requires domain knowledge of ion mobility physics
- Review lipid class coverage: confirm library includes sufficient diversity of lipid classes (phospholipids, glycerolipids, sphingolipids, etc.) to support the stated use case of 'internal standardization across multiple lipid classes'
- Cross-check library entries against abstract claim that DTCCSN2 library is 'newly established': verify entries are not simple duplicates of existing public CCS databases (e.g., LipidBlast, Lipidomics Workbench); inspect metadata or publication date if available
- Validate row consistency: confirm all rows have non-null CCS_value, lipid_class, and isotope_label fields; flag any missing or malformed entries
