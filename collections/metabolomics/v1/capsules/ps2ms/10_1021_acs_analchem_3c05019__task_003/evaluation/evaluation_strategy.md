# Evaluation Strategy

## Direct Checks

- verify that jhhung/PS2MS repository is accessible and contains trained model artifacts or weights
- verify that evaluation dataset files exist in the repository with documented NPS analogue structures
- verify that prediction score outputs (confidence/probability values) can be extracted from the model for test compounds
- verify that structural diversity metadata or SMILES/InChI strings are present for evaluation set compounds
- script_runs: load deposited model, execute inference on evaluation set, and generate per-compound confidence score table with no errors

## Expert Review

- classify test compounds as structurally novel or diverse relative to training set; assess whether groupings align with chemical intuition
- interpret confidence score distributions across structural classes; assess whether low-confidence predictions correlate plausibly with greater structural novelty or synthetic complexity
- evaluate whether score variation patterns are consistent with expected model behavior for out-of-distribution or chemically unfamiliar compounds
