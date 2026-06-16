# Evaluation Strategy

## Direct Checks

- verify that champ.filter() function exists in the ChAMP package source code at github:YuanTian1991__ChAMP
- verify that HumanMethylation450 test dataset is loadable from ChAMPdata package (version >= 2.23.1)
- script_runs: execute champ.filter() on HumanMethylation450 test dataset with default parameters and confirm no errors occur
- verify that output is a filtered methylation matrix or object with reduced probe count compared to input
- expert_review required: confirm that probes with detection p-value > 0.01 were removed by comparing probe counts pre- and post-filtering (requires validation against filtering source code or documentation)

## Expert Review

- inspect ChAMP package source code or documentation to confirm that champ.filter() removes probes with detection p-value > 0.01 by default
- inspect ChAMP package source code or documentation to confirm that champ.filter() removes probes with fewer than 3 beads in at least 5% of samples by default
- validate that the reported filtering thresholds (detection p-value > 0.01, bead count < 3 in ≥5% samples) match the actual implementation in default parameters
