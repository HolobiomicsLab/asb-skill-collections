---
name: untargeted-lcmsms-annotation-workflow
description: Use when you have raw untargeted LC-MS/MS data (mzML / an mzmine or
  GNPS-FBMN export) and want a full annotated feature table — preprocessing,
  molecular networking, spectral library matching, SIRIUS formula/structure/class,
  taxonomy-informed propagation (optional), and a fused master table with provenance.
license: CC-BY-4.0
metadata:
  kind: composite-workflow
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  techniques: [LC-MS]
  stage_count: 6
  member_skills:
    - peak-detection-and-mass-alignment
    - lc-ms-data-preprocessing
    - feature-detection-in-chromatographic-ms-data
    - lcms-peak-detection-and-alignment
    - xcms-data-import-preprocessing
    - spectral-similarity-network-generation
    - molecular-networking-construction
    - feature-based-molecular-network-interpretation
    - molecular-networking-parameter-configuration
    - spectral-library-matching
    - spectral-library-matching-annotation
    - mass-spectrometry-library-ranking
    - identity-search-spectrum-annotation
    - spectral-library-annotation-matching
    - sirius-spectral-request-construction
    - web-service-api-integration
    - sirius-zodiac-score-filtering
    - spectral-fingerprint-web-service-query
    - de-novo-structure-candidate-ranking
    - metabolite-annotation-taxonomic-integration
    - taxonomic-weighting-in-annotation
    - metabolite-annotation-scoring
    - spectral-library-matching-with-taxonomy
    - ranked-candidate-prioritization
    - mass-spectrometry-feature-deduplication
    - feature-network-construction-from-mass-spectrometry
    - feature-metadata-annotation
    - feature-table-annotation-table-construction
  member_tools:
    - MZmine2
    - Optimus
    - OpenMS
    - NeatMS
    - Python
    - NumPy
    - pandas
    - pyOpenMS
    - MSConvert
    - PFΔScreen
    - ISFrag
    - R
    - XCMS
    - CAMERA
    - MSnbase
    - Spectra
    - MsExperiment
    - BiocParallel
    - GNPS
    - Cytoscape
    - ENPKG
    - MZmine
    - ENPKG MN/ISDB/Taxo module
    - MEMO
    - Jupyter Notebook
    - MZmine3
    - GNPS FBMN
    - Google Colab
    - microbeMASST
    - metadataMASST
    - plantMASST
    - tissueMASST
    - microbiomeMASST
    - foodMASST
    - GNPS_MASST
    - GNPS libraries
    - Fast Search API
    - MASSBANK
    - DrugBANK
    - meRgeION2
    - RChemMass
    - MS2Compound
    - CFM-id
    - mssearchr
    - NIST API
    - MSThunder
    - Windows
    - Anaconda
    - Git
    - MSBERT
    - PyTorch
    - matchms
    - Spec2Vec
    - masscube
    - nplinker
    - pytest
    - CSI:FingerID
    - SIRIUS
    - CANOPUS
    - MSNovelist
    - INVENTA
    - ClassyFire
    - tima (Taxonomically Informed Metabolite Annotation)
    - LOTUS
    - Docker
    - MolNotator
    - PyYAML
    - networkx
    - treelib
    - mass2chem
    - metDataModel
    - asari
    - khipu
    - msFeaST
    - jupyter-notebook
    - msFeaST Dashboard bundle
    - MS-Dial
    - GetFeatistics
    - patRoon
  edam_operations:
    - operation_3215
    - operation_3214
    - operation_3645
    - operation_3631
    - operation_3860
    - operation_3801
    - operation_3434
    - operation_0491
    - operation_3767
    - operation_3432
    - operation_3441
    - operation_3632
  derived_from_workflows:
    - coll_ms2deepscore
    - coll_ramclust_cq
    - coll_xcms_cq
    - coll_inventa_cq
    - coll_nmr2struct
    - spec2vec_grounded
    - spec2vec_pkg_oalarge
    - coll_bioactivity_based_molecular_networking_cq
    - coll_concise_cq
    - coll_redu_cq
    - coll_deepmsprofiler_cq
    - coll_cardinal_cq
    - coll_dures_cq
    - coll_fbmn_stats_cq
    - coll_idsl_ipa_cq
    - coll_metabodirect
    - coll_multiomicsintegrator_cq
    - coll_peakqc_cq
    - coll_tardis
    - coll_vimms
    - coll_lipidin_cq
    - coll_molnetenhancer
    - coll_ms2rescore_immunopeptidome_rescoring_cq
    - coll_npclassscore_cq
    - coll_rapidmass_cq
    - coll_tardis_cq
    - coll_esp_cq
    - coll_graphormer_rt_cq
    - coll_lipidmatch_cq
    - coll_corems
  bound_by: perspicacite-semantic
schema_version: 0.3.0
attribution:
  generator: AgenticScienceBuilder
  date: "2026-06-28"
  method: v2-semantic-binding-perspicacite-text-embedding-3-large-llm-judge
---

## Summary

End-to-end untargeted LC-MS/MS annotation pipeline: raw mzML data files enter
and a fully annotated, fused master feature table exits. Six ordered stages cover
peak detection and mass alignment, molecular networking, spectral library matching,
SIRIUS formula/structure/class prediction, optional taxonomy-informed propagation,
and cross-tool annotation fusion. The pipeline is grounded in the ASB metabolomics
v2 collection (5,865 leaf skills / 568 papers) and is gradable by the
`asb solve-workflow` rubric.

Stage-to-leaf bindings in this v2 artifact were selected by **semantic retrieval**
(Perspicacité, text-embedding-3-large + LLM judge) rather than keyword/index
matching. The v1 (index-bound) artifact is archived at
`../_archive/untargeted-lcmsms-annotation.v1-index` for A/B comparison.

## When to use

- You have raw mzML files (or an mzml/mzXML batch) from an untargeted LC-MS/MS
  experiment and want a complete annotated feature table.
- You are starting from an existing MZmine project output, a GNPS-FBMN job result,
  or a SIRIUS mgf export and want to continue from mid-pipeline.
- You want molecular-family-level annotations with network context (GNPS/matchms
  molecular networking) combined with in silico structure/class prediction (SIRIUS
  CSI:FingerID + CANOPUS) and optional taxonomic reweighting (TIMA/LOTUS).
- You need provenance-aware fusion of multiple annotation sources into a single
  Cytoscape-ready master feature table.

## When NOT to use

- GC-MS data: the preprocess and network stages here target LC-MS/MS; use a
  dedicated GC-MS workflow or the GNPS GC deconvolution workflow directly.
- Targeted quantitation: the pipeline is discovery-mode; targeted MRM/PRM
  workflows are out of scope.
- NMR-only datasets: no MS2 spectra means networking and SIRIUS stages cannot run.
- Single-spectrum identification only: if you have one spectrum and want a quick
  library hit, use the `spectral-library-matching` or `identity-search-spectrum-annotation`
  leaf skills directly.

## Stages

### Stage 1 — preprocess

**Goal:** Convert raw mzML files to an aligned feature table and export MS2 spectra
(GNPS-FBMN mgf + SIRIUS mgf) for downstream stages.

**EDAM operation:** `operation_3215` (peak picking / mass spectrometry data processing)

**Inputs:** Raw mzML files (one per sample)

**Outputs:**
- `feature_table.csv` — aligned feature table (m/z, RT, per-sample intensities)
- `spectra_gnps.mgf` — MS2 export formatted for GNPS-FBMN
- `spectra_sirius.mgf` — MS2 export formatted for SIRIUS

**Primary leaf skill:** `peak-detection-and-mass-alignment`
- Tools: MZmine2, Optimus, OpenMS
- Grounding kb_slugs: `asb-paper-10-1021-acs-jnatprod-7b00737`
- DOIs: `10.1021/acs.jnatprod.7b00737`

**Candidate leaf skills:**
- `lc-ms-data-preprocessing` — NeatMS-based peak quality filtering and matrix
  construction from mzmine-formatted CSV + mzML pairs (Tools: NeatMS, Python,
  NumPy, pandas;
  kb_slugs: `asb-paper-10-1021-acs-analchem-1c02220`;
  DOIs: `10.1021/acs.analchem.1c02220`)
- `feature-detection-in-chromatographic-ms-data` — OpenMS/pyOpenMS centroided
  DDA feature delineation across m/z and RT dimensions (Tools: pyOpenMS, OpenMS,
  Python, MSConvert, PFΔScreen;
  kb_slugs: `asb-paper-10-1007-s00216-023-05070-2`;
  DOIs: `10.1007/s00216-023-05070-2`)
- `lcms-peak-detection-and-alignment` — XCMS/ISFrag multi-sample DDA/DIA/fullscan
  feature extraction with CAMERA adduct grouping (Tools: ISFrag, R, XCMS, CAMERA;
  kb_slugs: `asb-paper-10-1021-acs-analchem-1c01644`;
  DOIs: `10.1021/acs.analchem.1c01644`)
- `xcms-data-import-preprocessing` — XCMS peak detection + m/z bias correction
  from raw mzML/NetCDF/mzXML data (Tools: xcms, MSnbase, Spectra, MsExperiment,
  BiocParallel;
  kb_slugs: `asb-paper-10-1021-ac051437y`;
  DOIs: `10.1021/ac051437y`)

**Verification:** Feature table must have >0 rows; both mgf files must be non-empty
and contain `BEGIN IONS` entries; PEPMASS fields must be present in SIRIUS mgf.

---

### Stage 2 — network

**Goal:** Compute MS/MS spectral similarity scores and construct a molecular family
graph (all-pairs modified cosine; GNPS-style components) as a graphml file.
This stage builds the SIMILARITY GRAPH — it is distinct from library_match, which
queries REFERENCE LIBRARIES for compound identifications.

**EDAM operation:** `operation_3214` (spectral analysis) / `operation_3645`
(molecular networking)

**Inputs:** `spectra_gnps.mgf` (from preprocess)

**Outputs:**
- `network.graphml` — molecular network graph with cosine-similarity edges
- `components.tsv` — component/cluster membership per feature

**Primary leaf skill:** `spectral-similarity-network-generation`
- Tools: MZmine2, Optimus, GNPS, Cytoscape
- Grounding kb_slugs: `asb-paper-10-1021-acs-jnatprod-7b00737`
- DOIs: `10.1021/acs.jnatprod.7b00737`

**Candidate leaf skills:**
- `molecular-networking-construction` — ENPKG-based molecular network construction
  from LC-MS/MS DDA data with MEMO memorization (Tools: ENPKG, MZmine,
  ENPKG MN/ISDB/Taxo module, MEMO;
  kb_slugs: `asb-paper-10-1021-acscentsci-3c00800`;
  DOIs: `10.1021/acscentsci.3c00800`)
- `feature-based-molecular-network-interpretation` — GNPS FBMN network
  interpretation and visualization in R/Jupyter (Tools: R, Jupyter Notebook,
  MZmine3, GNPS FBMN, Google Colab;
  kb_slugs: `asb-paper-10-1038-s41596-024-01046-3`;
  DOIs: `10.1038/s41596-024-01046-3`)
- `molecular-networking-parameter-configuration` — Pre-GNPS parameter setup and
  MGF/feature-table preparation for network submission (Tools: MZmine2, GNPS,
  Optimus, Cytoscape;
  kb_slugs: `asb-paper-10-1021-acs-jnatprod-7b00737`;
  DOIs: `10.1021/acs.jnatprod.7b00737`)

**Verification:** network.graphml must be parseable XML; at least one edge with
cosine score >= 0.7 should exist for typical complex extracts; components.tsv must
have a header and one row per feature.

---

### Stage 3 — library_match

**Goal:** Annotate features by spectral similarity against reference libraries
(GNPS, MassBank, MASST, in-house); produce MSI level 2 hits with cosine scores
and precursor m/z deltas. This stage queries REFERENCE LIBRARIES — it is distinct
from network, which builds the pairwise similarity graph.

**EDAM operation:** `operation_3631` (spectral matching) / `operation_3215`

**Inputs:** `spectra_gnps.mgf` (from preprocess)

**Outputs:**
- `library_matches.tsv` — per-feature spectral library hits with cosine scores,
  precursor m/z delta, MSI level annotations

**Primary leaf skill:** `spectral-library-matching`
- Tools: microbeMASST, metadataMASST, plantMASST, tissueMASST, microbiomeMASST,
  foodMASST, GNPS_MASST, GNPS libraries, Fast Search API, MZmine, MASSBANK,
  DrugBANK, meRgeION2, GNPS, RChemMass, MS2Compound, CFM-id, mssearchr, R,
  NIST API
- Grounding kb_slugs: `asb-paper-10-1038-s41538-022-00137-3`,
  `asb-paper-10-1021-acs-analchem-2c04343`, `asb-paper-10-1089-omi-2021-0051`
- DOIs: `10.1038/s41538-022-00137-3`, `10.1021/acs.analchem.2c04343`,
  `10.1089/omi.2021.0051`

**Candidate leaf skills:**
- `spectral-library-matching-annotation` — UPLC-HRMS MS2 spectral matching against
  known reference spectra via MSThunder (Tools: MSThunder, Windows, GNPS, MSConvert;
  kb_slugs: `asb-paper-10-1016-j-enceco-2025-07-022`;
  DOIs: `10.1016/j.enceco.2025.07.022`)
- `mass-spectrometry-library-ranking` — MSBERT transformer-based library search
  and result ranking (Tools: Python, Anaconda, Git, MSBERT, PyTorch, matchms,
  Spec2Vec;
  kb_slugs: `asb-paper-10-1021-acs-analchem-4c02426`;
  DOIs: `10.1021/acs.analchem.4c02426`)
- `identity-search-spectrum-annotation` — masscube identity search for definitive
  molecular identity assignment from curated spectral library (Tools: masscube,
  Python;
  kb_slugs: `asb-paper-10-1038-s41467-025-60640-5`;
  DOIs: `10.1038/s41467-025-60640-5`)
- `spectral-library-annotation-matching` — nplinker GNPS archive spectral matching
  and annotation enrichment (Tools: nplinker, Python, pytest, GNPS;
  kb_slugs: `asb-paper-10-1186-s40168-022-01444-3`;
  DOIs: `10.1186/s40168-022-01444-3`)

**Verification:** library_matches.tsv must have a non-empty header; cosine column
must be numeric in [0, 1]; precursor m/z delta column must be present.

---

### Stage 4 — sirius

**Goal:** Run SIRIUS 6 (formula assignment, CSI:FingerID structure prediction,
CANOPUS compound-class assignment) on MS2 spectra.

**EDAM operation:** `operation_3860` (molecular formula identification) /
`operation_3801` (structure prediction)

**Inputs:** `spectra_sirius.mgf` (from preprocess)

**Outputs:**
- `sirius_results/compound_identification.tsv` — per-feature formula + structure +
  confidence scores
- `sirius_results/canopus_summary.tsv` — compound-class predictions (ClassyFire)

**Primary leaf skill:** `sirius-spectral-request-construction`
- Tools: CSI:FingerID, SIRIUS, CANOPUS
- Grounding kb_slugs: `asb-paper-10-1038-s41587-021-01045-9`
- DOIs: `10.1038/s41587-021-01045-9`

**Candidate leaf skills:**
- `web-service-api-integration` — Submits parsed mass spectra to SIRIUS web
  service endpoints and retrieves molecular fingerprint predictions, de-novo
  candidates, or compound-class predictions (Tools: CSI:FingerID, MSNovelist,
  SIRIUS, CANOPUS;
  kb_slugs: `asb-paper-10-1038-s41587-021-01045-9`;
  DOIs: `10.1038/s41587-021-01045-9`)
- `sirius-zodiac-score-filtering` — Filters compound_identification.tsv by Zodiac
  and Cosmic confidence scores to eliminate low-confidence SIRIUS annotations
  (Tools: SIRIUS, INVENTA, CANOPUS;
  kb_slugs: `asb-paper-10-3389-fmolb-2022-1028334`,
  `asb-paper-10-1038-s41467-021-23953-9`;
  DOIs: `10.3389/fmolb.2022.1028334`, `10.1038/s41467-021-23953-9`)
- `spectral-fingerprint-web-service-query` — Queries CANOPUS web service for
  systematic structural classification with compound-class confidence estimates
  (Tools: CANOPUS, SIRIUS, CSI:FingerID, ClassyFire;
  kb_slugs: `asb-paper-10-1038-s41587-021-01045-9`;
  DOIs: `10.1038/s41587-021-01045-9`)
- `de-novo-structure-candidate-ranking` — De-novo structure generation and ranking
  via MSNovelist for unknowns absent from spectral libraries (Tools: MSNovelist,
  SIRIUS, CSI:FingerID, CANOPUS;
  kb_slugs: `asb-paper-10-1038-s41587-021-01045-9`;
  DOIs: `10.1038/s41587-021-01045-9`)

**Verification:** compound_identification.tsv must contain InChIKey and ConfidenceScore
columns; canopus_summary.tsv must contain NPC#pathway and ClassyFire#superclass columns.

---

### Stage 5 — taxonomy_propagate  [OPTIONAL]

**Goal:** Reweight and propagate annotations using organism/taxon context (TIMA +
LOTUS) to reduce false positives and propagate high-confidence hits to unannotated
features.

**EDAM operation:** (no canonical EDAM; biological context reweighting)

**Inputs:**
- `library_matches.tsv` (from library_match)
- `sirius_results/compound_identification.tsv` (from sirius)
- Organism taxonomy metadata (sample manifest with taxon names or NCBI/GBIF IDs)

**Outputs:**
- `tima_reweighted.tsv` — reweighted candidate rank list with TIMA scores

**Primary leaf skill:** `metabolite-annotation-taxonomic-integration`
- Tools: R, tima (R package), LOTUS, SIRIUS v5/v6, GNPS, Spectra (R package)
- Grounding kb_slugs: `asb-paper-10-3389-fpls-2019-01329`
- DOIs: `10.3389/fpls.2019.01329`

**Candidate leaf skills:**
- `taxonomic-weighting-in-annotation` — Applies organism/taxon-derived TIMA weights
  to candidate rank lists with Docker deployment (Tools: R, Docker,
  tima (Taxonomically Informed Metabolite Annotation), LOTUS, SIRIUS, GNPS-FBMN;
  kb_slugs: `asb-paper-10-3389-fpls-2019-01329`;
  DOIs: `10.3389/fpls.2019.01329`)
- `metabolite-annotation-scoring` — Full TIMA scoring pipeline integrating MS/MS
  spectral similarity, chemical consistency, and taxonomic plausibility (Tools: R,
  Docker, tima (Taxonomically Informed Metabolite Annotation), LOTUS, SIRIUS,
  GNPS-FBMN;
  kb_slugs: `asb-paper-10-3389-fpls-2019-01329`, `asb-paper-10-1038-nbt-3597`,
  `asb-paper-10-1038-s41592-019-0344-8`;
  DOIs: `10.3389/fpls.2019.01329`, `10.1038/nbt.3597`,
  `10.1038/s41592-019-0344-8`)
- `spectral-library-matching-with-taxonomy` — Ranks annotations by both spectral
  similarity AND biochemical likelihood given organism taxonomy (Tools: R, Docker,
  tima (Taxonomically Informed Metabolite Annotation), LOTUS (Natural Products
  Database), SIRIUS (v5/v6), GNPS-FBMN;
  kb_slugs: `asb-paper-10-3389-fpls-2019-01329`;
  DOIs: `10.3389/fpls.2019.01329`)
- `ranked-candidate-prioritization` — Final reranking of candidate lists using
  TIMA + biological metadata; outputs ranked table (Tools: R, Docker, tima, LOTUS,
  SIRIUS v5/v6, GNPS-FBMN;
  kb_slugs: `asb-paper-10-3389-fpls-2019-01329`;
  DOIs: `10.3389/fpls.2019.01329`)

**Verification (when run):** tima_reweighted.tsv must have a score column; scores
must be numeric and bounded [0, 1]; feature count must match the input feature table.

---

### Stage 6 — fusion

**Goal:** Fuse all per-tool annotations into one master feature table via InChIKey
deduplication and adduct/isotope grouping; export Cytoscape-ready format.

**EDAM operation:** `operation_3434` (format conversion / data integration)

**Inputs:**
- `feature_table.csv` (from preprocess)
- `network.graphml` + `components.tsv` (from network)
- `library_matches.tsv` (from library_match)
- `sirius_results/compound_identification.tsv` + `canopus_summary.tsv` (from sirius)
- `tima_reweighted.tsv` (from taxonomy_propagate, if run)

**Outputs:**
- `master_feature_table.tsv` — one row per feature, all annotation columns joined
- `master_feature_table_cytoscape.graphml` — Cytoscape-compatible export

**Primary leaf skill:** `mass-spectrometry-feature-deduplication`
- Tools: MolNotator, PyYAML, Python
- Grounding kb_slugs: `asb-paper-10-1101-2021-12-21-473622v1`
- DOIs: `10.1101/2021.12.21.473622v1`

**Candidate leaf skills:**
- `feature-network-construction-from-mass-spectrometry` — networkx/asari/khipu
  network construction from LC-MS feature tables with isotope and adduct annotation
  (Tools: networkx, treelib, mass2chem, metDataModel, Python 3, asari, khipu;
  kb_slugs: `asb-paper-10-1021-acs-analchem-2c05810`;
  DOIs: `10.1021/acs.analchem.2c05810`)
- `feature-metadata-annotation` — msFeaST dashboard combining quantification,
  sample metadata, and spectral annotations into a unified queryable artifact
  (Tools: msFeaST, jupyter-notebook, msFeaST Dashboard bundle;
  kb_slugs: `asb-paper-10-1093-bioinformatics-btae584`;
  DOIs: `10.1093/bioinformatics/btae584`)
- `feature-table-annotation-table-construction` — patRoon/GetFeatistics joining of
  XCMS/MS-Dial feature tables with reference compound databases (Tools: R, XCMS,
  MS-Dial, GetFeatistics, patRoon;
  kb_slugs: `asb-paper-10-1515-jib-2025-0047`;
  DOIs: `10.1515/jib-2025-0047`)

**Verification:** master_feature_table.tsv must have one row per input feature;
columns from each upstream stage must be present (network_component, cosine_score,
sirius_formula, etc.); no duplicate feature_id values; Cytoscape graphml must be
parseable.

---

## Grounding

Run `/ground` per stage to verify against source papers via Perspicacité (server
on :8002, KB prefix `asb-paper-*`):

```
/ground stage=preprocess     kb=asb-paper-10-1021-acs-jnatprod-7b00737
/ground stage=network        kb=asb-paper-10-1038-s41596-024-01046-3
/ground stage=library_match  kb=asb-paper-10-1038-s41538-022-00137-3
/ground stage=sirius         kb=asb-paper-10-1038-s41587-021-01045-9
/ground stage=taxonomy_propagate kb=asb-paper-10-3389-fpls-2019-01329  # optional
/ground stage=fusion         kb=asb-paper-10-1021-acs-analchem-2c05810
```

When no Perspicacité server is available, ground against the DOIs listed per stage
using the local `skills_index.json` embedding search (offline fallback, P4).

## Verification contract

The `asb solve-workflow` rubric grades this workflow on eight dimensions:

| Rubric dimension        | Binding | Notes |
|-------------------------|---------|-------|
| STEP_ORDERING           | binding | preprocess → network → library_match → sirius → (taxonomy_propagate) → fusion |
| TOOL_SELECTION          | binding | MZmine/OpenMS for preprocess; GNPS/matchms for network; GNPS/MASSBANK for library_match; SIRIUS 6 for sirius |
| INTERMEDIATE_FIDELITY   | binding | feature_table, mgf×2, network.graphml, library_matches, compound_identification, tima_reweighted |
| END_TO_END_OUTPUT       | binding | master_feature_table.tsv must exist and be non-empty |
| SCIENTIFIC_VALIDITY     | binding | annotations must carry MSI level metadata; provenance columns must trace to source |
| CLAIM_VALIDATION        | informational | cross-check annotation counts vs reported literature benchmarks |
| REPRODUCTION            | informational | mgf → SIRIUS → compound_identification round-trip checksum |
| PARAMETER_SENSITIVITY   | informational | cosine threshold 0.7; SIRIUS confidence filter cosmicScore >= 0.5 |

## Provenance

- **schema_version:** 0.3.0
- **kind:** composite-workflow (P0 pilot)
- **bound_by:** perspicacite-semantic (embedding retrieval text-embedding-3-large + LLM judge)
- **v1 archived:** `../_archive/untargeted-lcmsms-annotation.v1-index` (index-bound)
- **derived_from_workflows:** see `metadata.derived_from_workflows` — these benchmark
  items are ablated by the eval harness when this super-skill is installed
  (SPEC §8 integrity contract).
- **authored:** 2026-06-28
- **generator:** AgenticScienceBuilder v2-semantic-binding
- **collection:** metabolomics v2 (5,865 skills / 909 tools / 568 papers)
