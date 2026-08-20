# ms-imaging-spatial-metabolomics-workflow — STAGING

**Status:** STAGING ONLY — promote via `release_gate.py` after human review.
**Kind:** composite-workflow (P1 canonical set).
**Bound by:** perspicacite-semantic (text-embedding-3-large retrieval + EDAM-aware primary selection).

## Stages

1. **preprocess_imaging** — load imzML, peak pick, align m/z across pixels  →  `mass-spectrometry-imaging-data-import`, `mass-spectrometry-peak-detection-and-alignment`, `spatial-pixel-coordinate-alignment`, `spectral-peak-alignment-across-pixels`, `imzml-metadata-parsing`
2. **spatial_annotation** — annotate ion images to metabolites with FDR control  →  `maldi-imaging-mass-spectrometry-data-interpretation`, `spatial-metabolomics-feature-annotation`, `imaging-mass-spectrometry-ion-identification`, `mass-spectral-feature-annotation`, `m-z-metabolite-annotation-mapping`, `metabolite-annotation-at-scale`
3. **segmentation** — spatial segmentation / clustering into regions  →  `spatial-segmentation-shrunken-centroids`, `spatial-spectral-array-processing`, `cardinal-object-structure-understanding`
4. **region_statistics** — compare metabolite intensities across spatial regions  →  `bioinformatic-object-conversion`, `spatial-coordinate-mapping-msi`, `spot-level-intensity-aggregation`

`derived_from_workflows` in the frontmatter is the eval-ablation set (SPEC §8).
