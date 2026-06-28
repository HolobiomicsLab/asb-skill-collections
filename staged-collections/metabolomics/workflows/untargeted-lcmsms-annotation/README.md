# untargeted-lcmsms-annotation-workflow — STAGING

**Status:** STAGING ONLY — promote via `release_gate.py` after human review.
**Kind:** composite-workflow (P1 canonical set).
**Bound by:** perspicacite-semantic (text-embedding-3-large retrieval + EDAM-aware primary selection).

## Stages

1. **preprocess** — raw mzML -> aligned feature table + MS2 exports (GNPS-FBMN mgf + SIRIUS mgf)  →  `peak-detection-and-mass-alignment`, `mass-spectrometry-feature-detection-validation`, `lcms-peak-detection-and-alignment`, `spectral-feature-table-generation`, `cross-sample-feature-alignment`
2. **qc_filter** (optional) — (optional) remove blank / background / low-quality features before annotation  →  `blank-sample-feature-filtering`, `feature-table-blank-intensity-detection`, `background-ion-contaminant-removal`, `feature-table-quality-control`, `background-ion-blank-comparison`
3. **network** — MS2 spectra -> molecular family graph (modified cosine; GNPS-style components)  →  `molecular-networking-construction`, `molecular-family-graph-construction`, `spectral-similarity-network-generation`, `spectral-library-molecular-networking`, `gnps-molecular-network-integration`, `graph-based-metabolite-similarity-assessment`
4. **library_match** — MS2 spectra -> spectral library annotations (cosine match to reference libraries)  →  `spectral-library-matching-annotation`, `spectral-library-matching`, `spectral-library-matching-with-cosine-similarity`, `mass-spectrometry-library-ranking`, `spectral-library-annotation-matching`
5. **sirius** — MS2 spectra -> formula + structure + class (SIRIUS / CSI:FingerID / CANOPUS)  →  `sirius-spectral-request-construction`, `web-service-api-integration`, `spectrum-query-formatting`, `spectral-fingerprint-web-service-query`, `molecular-fingerprint-parsing`
6. **taxonomy_propagate** (optional) — (optional) taxonomy-aware re-weighting / propagation of annotations  →  `taxonomic-weighting-in-annotation`, `metabolite-annotation-taxonomic-integration`, `metabolite-annotation-scoring`, `metabolite-annotation-network-architecture`
7. **fusion** — consolidate networking + library + SIRIUS (+ taxonomy) into one master table  →  `feature-metadata-annotation`, `feature-network-construction-from-mass-spectrometry`, `sample-centric-metabolite-annotation`, `feature-table-consensus-aggregation`, `unannotated-feature-characterization`, `feature-table-integration-and-normalization`

`derived_from_workflows` in the frontmatter is the eval-ablation set (SPEC §8).
