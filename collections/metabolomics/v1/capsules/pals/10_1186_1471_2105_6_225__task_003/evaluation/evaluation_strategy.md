# Evaluation Strategy

## Direct Checks

- Verify that PALS repository (github:glasgowcompbio/PALS) contains documented implementation of PLAGE decomposition method
- Verify file_exists: locate example or test data in PALS repository using GNPS Molecular Families format
- Verify file_exists: locate example or test data in PALS repository using MS2LDA Mass2Motifs format
- Script_runs: execute PALS decomposition on GNPS Molecular Families input and confirm output artifact is produced
- Script_runs: execute PALS decomposition on MS2LDA Mass2Motifs input and confirm output artifact is produced
- Verify output_matches_reference: compare decomposition scores/loadings from both non-pathway metabolite sets against any published reference results or supplementary tables reporting PLAGE application to these data types

## Expert Review

- Confirm that reported decomposition results for Molecular Families and Mass2Motifs demonstrate statistically and biologically meaningful variance decomposition consistent with the PLAGE method's theoretical properties
- Assess whether the generalization to fragmentation-spectrum-derived groupings (GNPS and MS2LDA) is substantively different from pathway-based analysis and whether results validate the claim of generalization
- Evaluate robustness claims: verify that PLAGE scores on these non-pathway metabolite sets show comparable or superior noise tolerance relative to ORA/GSEA baselines if such comparisons are reported
