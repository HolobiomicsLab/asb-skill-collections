# Evaluation Strategy

## Direct Checks

- verify that the implementation accepts a binned MS/MS spectrum (210,000-dimensional vector or equivalent sparse representation after 10,000 bin transformation) as input
- verify that the base network produces a 200-dimensional output vector (spectral embedding)
- verify that the implementation applies the three data-augmentation strategies during training: (1) low-intensity peak removal (0–20% of bins), (2) peak intensity jitter (0–40%), (3) new peak addition (0–10 bins with values 0–0.01)
- verify that dense layer weights are trainable and initialized appropriately for the Siamese architecture
- verify that the base network is not shared or modified per-query; it remains fixed throughout inference
- file_exists: verify that a trained model checkpoint or weights file is retrievable from https://zenodo.org/record/4699356
- file_exists: verify that source code for base network implementation is accessible at https://github.com/matchms/ms2deepscore
- script_runs: verify that the base network can be instantiated and forward pass completes in <1 second on a single CPU or GPU for a batch of 32 spectra (parameter-sensitive to hardware; no canonical answer for absolute runtime)
- format_is: verify that output embedding is a floating-point vector of exactly 200 dimensions with values in a reasonable range (e.g., −1 to +1 or 0 to 1; multiple defensible approaches depending on activation function)
- output_matches_reference: verify that when applied to the test set spectra (3601 spectra from zenodo.org/record/4699356), computed embeddings can be used to reconstruct the t-SNE visualization shown in the article's supplementary materials (robust to t-SNE parameter choices, but exact dimensionality 200 is required)

## Expert Review

- assess whether the choice of 200 embedding dimensions is justified and whether this choice aligns with the reported RMSE performance (~0.15) on Tanimoto score prediction
- assess whether the data-augmentation strategies (low-intensity peak removal, jitter, new peak addition) are applied consistently and whether their ranges (0–20%, 0–40%, 0–10 bins) are appropriate for avoiding distribution shift during inference
- assess whether the base network architecture (number and size of dense layers, activation functions, dropout placement) is appropriate for learning structural similarity from spectral data, given no detailed architecture diagram is provided in the discussion section
- assess whether the fixed (non-ensemble) base network achieves the claimed RMSE of ~0.15 when evaluated on the test set, and whether this baseline is consistent with the ensemble results reported in the introduction and abstract
