# Evaluation Strategy

## Direct Checks

- file_exists: verify that PR #78 branch or merged code in iomega/ms2query contains a module or function implementing average InChIKey score computation
- file_exists: verify that PR #78 branch or merged code in iomega/ms2query contains a module or function implementing neighbourhood score computation
- script_runs: execute the scoring module with a synthetic candidate match record (from library-matching step) and verify output_matches_reference by comparing returned score fields against manually computed ground-truth values for both metrics — robust to parameter choices in candidate inputs
- field_present: verify that the output record structure includes a named field or key for 'average inchikey score' (or exact variant used in codebase)
- field_present: verify that the output record structure includes a named field or key for 'neighbourhood score' (or exact variant used in codebase)
- file_format_is: verify that scoring module outputs are serialized in a format compatible with downstream matching workflow (e.g. JSON, CSV, or Python dict) — no canonical answer as multiple formats are defensible

## Expert Review

- Validate that the mathematical definition and aggregation logic for 'average InChIKey score' aligns with the intended semantics (e.g., is it mean, median, or weighted average across candidates; does it handle missing or null scores)
- Validate that the mathematical definition and computation of 'neighbourhood score' aligns with domain expectations (e.g., what constitutes a 'neighbour' in chemical or spectral space, how is proximity measured, what weighting scheme is used)
- Validate that both scores produce outputs within defensible numerical ranges (e.g., 0–1 for similarity scores) and that score scaling/normalization is consistent with library-matching step conventions
