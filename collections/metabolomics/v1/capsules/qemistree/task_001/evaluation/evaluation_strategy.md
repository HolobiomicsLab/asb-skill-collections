# Evaluation Strategy

## Direct Checks

- verify q2-qemistree plugin is installable from github:biocore__q2-qemistree
- verify q2-qemistree accepts LC-MS/MS feature data in QIIME 2 artifact format (e.g., FeatureTable[Frequency])
- verify q2-qemistree produces a tree artifact output (Phylogeny[Rooted] or equivalent format)
- script_runs: q2-qemistree command executes without error on valid input feature table and molecular networking data
- verify output tree file exists and is in valid Newick or compatible phylogenetic format
- verify tree contains nodes corresponding to input LC-MS/MS features — row_count_equals or node count matches feature count (robust to tree representation choices)

## Expert Review

- assess whether tree topology reflects expected chemical relatedness among metabolomic features (requires domain knowledge of mass-spectrometry feature clustering)
- evaluate whether branching patterns are biologically/chemically interpretable for untargeted metabolomic comparison
- review whether feature tree enables meaningful downstream statistical or visual analysis as intended by tool design
