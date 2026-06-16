# Evaluation Strategy

## Direct Checks

- verify file exists at github:glasgowcompbio__vimms (repository accessible)
- verify Beer1pos mzML dataset is retrievable from glasgowcompbio/vimms-data repository
- verify ViMMS package can be imported and TopNController class is accessible
- verify simulated mzML output file is generated with valid mzML format
- verify simulated mzML contains MS1 and MS2 scans in byte-for-byte valid XML structure
- verify comparison metrics (fragmentation coverage, peak matching) can be computed from both real and simulated mzML files using reported parameters (MS1 tolerance 1 ppm, MS2 tolerance 0.05 ppm, minimum 3 matching peaks)
- verify output comparison table or figure matches structure and numerical range of reported Beer Top-N demo result

## Expert Review

- assess whether simulated acquisition strategy (TopNController with N parameter) faithfully reproduces the selectivity and timing patterns of real Beer1pos instrument run
- assess whether comparison metrics (fragmentation coverage percentage, number of matched compounds) are consistent with metabolomics best practices and the paper's reported values
- assess biological plausibility: verify that matched metabolites and fragmentation patterns are chemically and biologically consistent with beer composition
