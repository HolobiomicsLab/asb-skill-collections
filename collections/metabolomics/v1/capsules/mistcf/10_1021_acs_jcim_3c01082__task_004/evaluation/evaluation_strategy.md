# Evaluation Strategy

## Direct Checks

- Verify file exists: the MIST-CF repository (samgoldman97/mist-cf) contains a sinusoidal formula embedding implementation or module
- Verify script runs: a computational agent can load the embedding layer from the MIST-CF codebase and execute it on a test set of chemical formulas without errors
- Verify output_matches_reference: embedding vectors produced by the agent's implementation have the same dimensionality as reported in SCARF or MIST-CF documentation
- Verify value_in_range: all numerical values in the output embedding vectors fall within a defensible range (e.g. [-1, 1] for sinusoidal embeddings), robust to parameter choices
- Verify row_count_equals: the number of output embedding vectors equals the number of input chemical formulas

## Expert Review

- Confirm that the sinusoidal embedding formula and hyperparameters (e.g., frequency scaling, periodicity, dimension) match the SCARF paper specification and are correctly transcribed into the implementation
- Assess reproducibility: expert inspection of whether computed embeddings exhibit expected periodicity and symmetry properties characteristic of sinusoidal encodings
