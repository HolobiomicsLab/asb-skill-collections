# feature-based-molecular-networking-and-propagation-workflow — STAGING

**Status:** STAGING ONLY — promote via `release_gate.py` after human review.
**Kind:** composite-workflow (P1 canonical set).
**Bound by:** perspicacite-semantic (text-embedding-3-large retrieval + EDAM-aware primary selection).

## Stages

1. **preprocess** — raw mzML -> aligned feature table + MS2 exports (GNPS-FBMN mgf + SIRIUS mgf)  →  `peak-detection-and-mass-alignment`, `cross-sample-feature-alignment`, `lcms-peak-detection-and-alignment`, `spectral-feature-table-generation`, `mass-spectrometry-feature-detection-validation`
2. **network** — MS2 spectra -> molecular family graph (modified cosine; GNPS-style components)  →  `spectral-similarity-network-generation`, `molecular-family-graph-construction`, `metabolomic-spectral-annotation-and-molecular-family-clustering`, `molecular-family-grouping-analysis`, `metabolomic-molecular-family-networking-gnps`
3. **seed_annotate** — MS2 spectra -> seed spectral-library annotations to propagate from  →  `spectral-library-matching-annotation`, `spectral-library-matching`, `spectral-library-molecular-networking`, `mass-spectrometry-library-ranking`
4. **class_annotate** — MS2 spectra -> molecular formula + chemical class (SIRIUS / CANOPUS / NPClassifier)  →  `chemical-ontology-mapping`, `spectral-feature-chemical-assignment`, `consensus-classification-reconciliation`, `structural-annotation-integration`, `chemical-classification-scheme-validation`
5. **propagate** — spread seed annotations + chemical classes across molecular families  →  `graph-based-feature-annotation`, `chemical-class-metadata-integration`, `molecular-network-node-annotation`, `molecular-network-attribute-enrichment`, `molecular-network-annotation-integration`
6. **consolidate** — consolidate network family + seed + class + propagated annotations into one table  →  `feature-metadata-annotation`, `feature-consolidation-across-batches`, `untargeted-metabolomics-dataset-integration`, `lcms-feature-table-construction`, `feature-annotation-consolidation`

`derived_from_workflows` in the frontmatter is the eval-ablation set (SPEC §8).
