# Evaluation Strategy

## Direct Checks

- verify file exists: ms2Lib object for Penicillium nordicum (51 MS/MS spectra) is loadable from github:odisce__mineMS2
- verify file exists: GNPS extracted components dataset with precursor m/z values 370.1283 and 404.0891 for component 8
- script_runs: findPatternsExplainingComponents(pnordicum.ms2Lib, gnps_components, metric=c('recall','precision','size'), top=5) executes without error
- output_matches_reference: pattern P70 achieves F1-score of 1.0 for component 8 (byte-for-byte exact numeric match or robust to floating-point precision ≤ 1e-6)
- value_in_range: all other top-5 patterns have recall=1.0 (exact match)
- value_in_range: all other top-5 patterns (excluding P70) have precision < 1.0 (multiple defensible thresholds for 'lower precision')

## Expert Review

- Assess whether F1-score=1.0 for pattern P70 on component 8 represents a chemically meaningful and reproducible result given the Penicillium nordicum secondary metabolite dataset
- Evaluate whether the differential recall (all 1.0) and precision (P70=1.0, others <1.0) pattern across top-5 patterns is consistent with expected mineMS2 behavior on GNPS-coupled molecular networks
