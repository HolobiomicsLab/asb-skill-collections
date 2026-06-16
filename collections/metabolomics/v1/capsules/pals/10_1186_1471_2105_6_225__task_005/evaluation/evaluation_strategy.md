# Evaluation Strategy

## Direct Checks

- verify file exists: input CSV or JSON metabolite set file in repository or test data directory
- verify file_format_is: input metabolite set file conforms to documented CSV or JSON schema (field names, required columns present)
- verify script_runs: PALS pipeline dispatcher accepts uploaded metabolite set file without errors on test input
- verify output_matches_reference: scored results table structure matches the format of PLAGE outputs for shipped set types (columns: metabolite_id, set_id, score, p_value or equivalent), robust to parameter choices in PLAGE algorithm
- verify field_present: output table contains at least score and identifier fields for each metabolite set
- verify contains_substring: Web application UI or API endpoint documentation mentions support for user-uploaded metabolite sets beyond the three shipped types (pathways, Molecular Families, Mass2Motifs)

## Expert Review

- PLAGE scoring results on uploaded metabolite set are statistically sound and consistent with expected behavior on known positive control sets
- Extension maintains robustness to noise and missing peaks (stated PALS advantage) when applied to user-uploaded sets compared to baseline ORA/GSEA
- User-uploaded metabolite set interpretation and scoring are scientifically valid for the metabolomics domain
