# Evaluation Strategy

## Direct Checks

- verify file exists in github:JonZwe__PFAScreen repository containing KMD calculation implementation
- verify KMD module accepts a feature list as input (file or data structure with m/z and intensity fields)
- verify KMD module returns grouped or flagged features with at least one output field indicating homologous series membership or KMD cluster assignment
- script_runs: KMD filter executes without error on a test feature list with ≥10 features spanning m/z 200–1200
- verify output contains KMD values (numeric, robust to rounding within ±0.01 Da)
- verify features are grouped or flagged by KMD values with homologous series labels or cluster identifiers

## Expert Review

- assess whether KMD calculation follows established mass defect formulae for PFAS homolog detection (expert judgment on correctness of Kendrick mass basis and defect computation)
- evaluate whether grouping/flagging threshold for homologous series is chemically defensible and documented
- review whether output interpretation and labeling of PFAS series are consistent with literature conventions for KMD-based PFAS screening
