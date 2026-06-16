# Evaluation Strategy

## Direct Checks

- verify file exists: pbmc10k_multiome dataset accessible via snapatac2.datasets.pbmc10k_multiome
- script_runs: SnapATAC2 pipeline execution script completes without errors (fragment import → tile matrix → spectral embedding → leiden clustering → macs3 peak calling)
- file_exists: output AnnData object (.h5ad) or equivalent structured artifact generated after full pipeline
- field_present: cluster assignments present in output object (e.g., .obs['leiden'] or equivalent clustering annotation column)
- file_format_is: output object in HDF5-backed AnnData format or native SnapATAC2 format
- output_matches_reference: UMAP layout coordinates byte-for-byte or robust to random seed variation — clarify whether tutorial provides fixed reference embeddings or multiple valid outcomes
- value_in_range: cluster count (number of distinct leiden clusters) falls within expected range documented in tutorial (if range is specified)
- contains_substring: peak calling output (BED or equivalent) contains expected genomic coordinates and peak statistics fields

## Expert Review

- biological plausibility of cluster assignments: do recovered clusters correspond to expected cell types (e.g., T cells, B cells, monocytes, etc.) as described in tutorial or original pbmc10k_multiome analysis?
- quality of spectral embedding and UMAP visualization: do clusters show expected separation and structure consistent with tutorial figures or reference publication?
- peak calling quality: are called peaks consistent with known open chromatin regions and do they show expected enrichment patterns (e.g., TSS proximity, motif content)?
- parameter sensitivity: does pipeline produce substantially different cluster assignments or peak calls under reasonable parameter variations (e.g., n_components, resolution, min_peak_size)? — note if reproducibility is brittle or robust
