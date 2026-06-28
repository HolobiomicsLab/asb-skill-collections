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
    - data-normalization-in-mass-spectrometry
    - feature-table-export-and-formatting
    - tic-peak-boundary-estimation
    - feature-table-export-and-validation
    - spectral-similarity-scoring-cosine
    - spectral-batch-submission-to-networking-server
    - gc-ms-spectral-similarity-clustering
    - molecular-family-graph-construction
    - cosine-similarity-computation
    - candidate-match-retrieval
    - false-discovery-rate-control-in-spectral-matching
    - cosine-distance-scoring
    - spectral-search-logic-control-flow
    - sirius-spectral-request-construction
    - api-endpoint-communication
    - annotation-table-quality-control
    - sirius-zodiac-score-filtering
    - compound-class-annotation-parsing
    - metabolite-annotation-scoring
    - metabolite-annotation-taxonomic-integration
    - taxonomic-weighting-in-annotation
    - ranked-candidate-prioritization
    - annotation-confidence-scoring
    - inchikey-normalization-and-deduplication
    - metabolite-spectral-data-merging
    - compound-identifier-standardization
    - cytoscape-network-format-export
    - molecular-duplicate-detection-and-deduplication
  member_tools:
    - MZmine2
    - Optimus
    - OpenMS
    - MZmine
    - GNPS
    - Jupyter notebook
    - R
    - Autotuner
    - MSconvert
    - XCMS
    - Python
    - matchms
    - Spec2Vec
    - MS2DeepScore
    - GNPS_GC
    - nplinker
    - pytest
    - cosine_neutral_loss repository
    - spectrum_utils
    - MS2Query
    - MS2Deepscore
    - Random Forest Re-ranker
    - GNPS Library
    - ANN-SoLo
    - SIRIUS
    - CSI:FingerID
    - CANOPUS
    - Inventa
    - INVENTA
    - Docker
    - tima (Taxonomically Informed Metabolite Annotation)
    - LOTUS
    - GNPS-FBMN
    - tima (R package)
    - Spectra (R package)
    - MrnAnnoAlgo3 (MetDNA3)
    - RDKit
    - mspcompiler
    - future
    - future.apply
    - parallel
    - Lib2NIST
    - MS-DIAL
    - PubChem
    - jobs.py
    - prepare_wikidata_lotus_prefect.py
    - drugbank_extraction.py
    - MetaMapR
    - cytoscape.js
    - sanitizing.py
    - smiles.py
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
  bound_by: index
schema_version: 0.3.0
attribution:
  generator: AgenticScienceBuilder
  date: "2026-06-28"
  method: P0-pilot-composite-workflow-authoring
---

## Summary

End-to-end untargeted LC-MS/MS annotation pipeline: raw mzML data files enter
and a fully annotated, fused master feature table exits. Six ordered stages cover
peak detection and mass alignment, molecular networking, spectral library matching,
SIRIUS formula/structure/class prediction, optional taxonomy-informed propagation,
and cross-tool annotation fusion. The pipeline is grounded in the ASB metabolomics
v2 collection (5,865 leaf skills / 568 papers) and is gradable by the
`asb solve-workflow` rubric.

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

- GC-MS data: use `gc-ms-spectral-similarity-clustering` or the GNPS GC workflow
  directly; the preprocess stage here targets LC-MS/MS peak detection.
- Targeted quantitation: the pipeline is discovery-mode; targeted MRM/PRM workflows
  are out of scope.
- NMR-only datasets: no MS2 spectra means networking and SIRIUS stages cannot run.
- Single-spectrum identification only: if you have one spectrum and want a quick
  library hit, use the `spectral-similarity-scoring-cosine` or `candidate-match-retrieval`
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
- `data-normalization-in-mass-spectrometry` — MZmine-specific normalization and
  feature detection for raw mzML/mzXML (Tools: MZmine;
  kb_slugs: `asb-paper-10-1101-2024-05-13-593988v1`;
  DOIs: `10.1101/2024.05.13.593988v1`)
- `feature-table-export-and-formatting` — Post-alignment formatting and export to
  GNPS-FBMN and SIRIUS mgf (Tools: MZmine2, Optimus, OpenMS, GNPS, Jupyter notebook;
  kb_slugs: `asb-paper-10-1021-acs-jnatprod-7b00737`;
  DOIs: `10.1021/acs.jnatprod.7b00737`)
- `tic-peak-boundary-estimation` — TIC peak boundary refinement before feature
  extraction (Tools: R, Autotuner, MSconvert, XCMS, MZmine2;
  kb_slugs: `asb-paper-10-1101-812370`;
  DOIs: `10.1101/812370`)
- `feature-table-export-and-validation` — MZmine batch completion and feature table
  export with validation (Tools: MZmine;
  kb_slugs: `asb-paper-10-1101-2024-05-13-593988v1`;
  DOIs: `10.1101/2024.05.13.593988v1`)

**Verification:** Feature table must have >0 rows; both mgf files must be non-empty
and contain `BEGIN IONS` entries; PEPMASS fields must be present in SIRIUS mgf.

---

### Stage 2 — network

**Goal:** Compute MS/MS spectral similarity scores and construct a molecular family
graph (all-pairs modified cosine; GNPS-style components).

**EDAM operation:** `operation_3214` (spectral analysis) / `operation_3645`
(molecular networking)

**Inputs:** `spectra_gnps.mgf` (from preprocess)

**Outputs:**
- `network.graphml` — molecular network graph
- `components.tsv` — component/cluster membership per feature

**Primary leaf skill:** `spectral-similarity-scoring-cosine`
- Tools: Python, matchms, Spec2Vec, MS2DeepScore
- Grounding kb_slugs: `asb-paper-10-1186-s13321-024-00878-1`
- DOIs: `10.1186/s13321-024-00878-1`

**Candidate leaf skills:**
- `spectral-batch-submission-to-networking-server` — Primary network construction
  via GNPS (deconvolved spectra; ProteoSAFe) (Tools: GNPS_GC;
  kb_slugs: `asb-paper-10-1038-s41587-020-0700-3`;
  DOIs: `10.1038/s41587-020-0700-3`)
- `gc-ms-spectral-similarity-clustering` — Spectral clustering for GC-MS spectra
  via GNPS_GC (Tools: GNPS_GC;
  kb_slugs: `asb-paper-10-1038-s41587-020-0700-3`;
  DOIs: `10.1038/s41587-020-0700-3`)
- `molecular-family-graph-construction` — Post-GNPS network parsing via nplinker
  (Tools: nplinker, Python, pytest, GNPS;
  kb_slugs: `asb-paper-10-1186-s40168-022-01444-3`;
  DOIs: `10.1186/s40168-022-01444-3`)
- `cosine-similarity-computation` — Low-level pairwise cosine scoring (Tools:
  cosine_neutral_loss repository, spectrum_utils;
  kb_slugs: `asb-paper-10-1021-jasms-2c00153`, `asb-paper-10-1016-1044-0305`;
  DOIs: `10.1021/jasms.2c00153`, `10.1016/1044-0305`)

**Verification:** network.graphml must be parseable; at least one edge with cosine
score >= 0.7 should exist for typical complex extracts; components.tsv must have
a header and one row per feature.

---

### Stage 3 — library_match

**Goal:** Annotate features by spectral similarity against reference libraries
(MassBank, GNPS, in-house); produce MSI level 2 hits.

**EDAM operation:** `operation_3631` (spectral matching) / `operation_3215`

**Inputs:** `spectra_gnps.mgf` (from preprocess)

**Outputs:**
- `library_matches.tsv` — per-feature spectral library hits with cosine scores,
  precursor m/z delta, MSI level annotations

**Primary leaf skill:** `spectral-similarity-scoring-cosine`
- Tools: Python, matchms, Spec2Vec, MS2DeepScore
- Grounding kb_slugs: `asb-paper-10-1186-s13321-024-00878-1`
- DOIs: `10.1186/s13321-024-00878-1`

**Candidate leaf skills:**
- `candidate-match-retrieval` — MS2Query dual-pathway library search (Tools:
  MS2Query, MS2Deepscore, Spec2Vec, MZMine;
  kb_slugs: `asb-paper-10-1038-s41467-023-37446-4`;
  DOIs: `10.1038/s41467-023-37446-4`)
- `false-discovery-rate-control-in-spectral-matching` — FDR control via ANN-SoLo
  after library matching (Tools: ANN-SoLo;
  kb_slugs: `asb-paper-10-1021-acs-jproteome-8b00359`;
  DOIs: `10.1021/acs.jproteome.8b00359`)
- `cosine-distance-scoring` — Alternative cosine distance scoring metric (Tools:
  matchms, Python, Spec2Vec, MS2DeepScore;
  kb_slugs: `asb-paper-10-1186-s13321-024-00878-1`;
  DOIs: `10.1186/s13321-024-00878-1`)
- `spectral-search-logic-control-flow` — MS2Query architecture routing (Tools:
  MS2Query, MS2Deepscore, Random Forest Re-ranker, GNPS Library;
  kb_slugs: `asb-paper-10-1038-s41467-023-37446-4`;
  DOIs: `10.1038/s41467-023-37446-4`)

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
- Tools: SIRIUS, CSI:FingerID, CANOPUS
- Grounding kb_slugs: `asb-paper-10-1038-s41587-021-01045-9`
- DOIs: `10.1038/s41587-021-01045-9`

**Candidate leaf skills:**
- `api-endpoint-communication` — Submits fingerprint/spectrum data to SIRIUS web
  service endpoints and retrieves compound-class predictions (Tools: CANOPUS,
  SIRIUS, CSI:FingerID;
  kb_slugs: `asb-paper-10-1038-s41587-021-01045-9`;
  DOIs: `10.1038/s41587-021-01045-9`)
- `annotation-table-quality-control` — Validates SIRIUS output tables by Zodiac/Cosmic
  confidence scores (Tools: SIRIUS, CANOPUS, Inventa, GNPS;
  kb_slugs: `asb-paper-10-3389-fmolb-2022-1028334`,
  `asb-paper-10-1038-s41467-021-23953-9`;
  DOIs: `10.3389/fmolb.2022.1028334`, `10.1038/s41467-021-23953-9`)
- `sirius-zodiac-score-filtering` — Filters by Zodiac and Cosmic confidence scores
  to eliminate low-confidence annotations (Tools: SIRIUS, INVENTA, CANOPUS;
  kb_slugs: `asb-paper-10-3389-fmolb-2022-1028334`,
  `asb-paper-10-1038-s41467-021-23953-9`;
  DOIs: `10.3389/fmolb.2022.1028334`, `10.1038/s41467-021-23953-9`)
- `compound-class-annotation-parsing` — Parses CANOPUS web service responses to
  extract compound-class labels (Tools: CANOPUS, SIRIUS;
  kb_slugs: `asb-paper-10-1038-s41587-021-01045-9`;
  DOIs: `10.1038/s41587-021-01045-9`)

**Verification:** compound_identification.tsv must contain InChIKey and ConfidenceScore
columns; canopus_summary.tsv must contain NPC#pathway and ClassyFire#superclass columns.

---

### Stage 5 — taxonomy_propagate  [OPTIONAL]

**Goal:** Reweight and propagate annotations using organism/taxon context (TIMA +
LOTUS) to reduce false positives and propagate high-confidence hits.

**EDAM operation:** (no canonical EDAM; biological context reweighting)

**Inputs:**
- `library_matches.tsv` (from library_match)
- `sirius_results/compound_identification.tsv` (from sirius)
- Organism taxonomy metadata (sample manifest with taxon names or NCBI/GBIF IDs)

**Outputs:**
- `tima_reweighted.tsv` — reweighted candidate rank list with TIMA scores

**Primary leaf skill:** `metabolite-annotation-scoring`
- Tools: R, Docker, tima (Taxonomically Informed Metabolite Annotation), LOTUS,
  SIRIUS, GNPS-FBMN
- Grounding kb_slugs: `asb-paper-10-3389-fpls-2019-01329`,
  `asb-paper-10-1038-nbt-3597`, `asb-paper-10-1038-s41592-019-0344-8`
- DOIs: `10.3389/fpls.2019.01329`, `10.1038/nbt.3597`, `10.1038/s41592-019-0344-8`

**Candidate leaf skills:**
- `metabolite-annotation-taxonomic-integration` — Pairs MS/MS spectra with organism
  taxonomy for annotation recall improvement (Tools: R, tima (R package), LOTUS,
  SIRIUS v5/v6, GNPS, Spectra (R package);
  kb_slugs: `asb-paper-10-3389-fpls-2019-01329`;
  DOIs: `10.3389/fpls.2019.01329`)
- `taxonomic-weighting-in-annotation` — Applies organism/taxon-derived weights to
  candidate rank lists (Tools: R, Docker, tima (Taxonomically Informed Metabolite
  Annotation), LOTUS, SIRIUS, GNPS-FBMN;
  kb_slugs: `asb-paper-10-3389-fpls-2019-01329`;
  DOIs: `10.3389/fpls.2019.01329`)
- `ranked-candidate-prioritization` — Reranks candidate lists using TIMA + biological
  metadata (Tools: R, Docker, tima, LOTUS, SIRIUS v5/v6, GNPS-FBMN;
  kb_slugs: `asb-paper-10-3389-fpls-2019-01329`;
  DOIs: `10.3389/fpls.2019.01329`)
- `annotation-confidence-scoring` — Post-propagation confidence filtering via MetDNA3
  two-layer network consensus (Tools: MrnAnnoAlgo3 (MetDNA3);
  kb_slugs: `asb-paper-10-1038-s41467-025-63536-6`;
  DOIs: `10.1038/s41467-025-63536-6`)

**Verification (when run):** tima_reweighted.tsv must have a score column; scores
must be numeric and bounded [0, 1]; feature count must match the input feature table.

---

### Stage 6 — fusion

**Goal:** Fuse all per-tool annotations into one master feature table via InChIKey
deduplication; export Cytoscape-ready format.

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

**Primary leaf skill:** `inchikey-normalization-and-deduplication`
- Tools: RDKit, matchms, Python
- Grounding kb_slugs: `asb-paper-10-1186-s13321-021-00558-4`
- DOIs: `10.1186/s13321-021-00558-4`

**Candidate leaf skills:**
- `metabolite-spectral-data-merging` — Merges spectral metadata and annotations
  across multiple source libraries (Tools: mspcompiler, R, future, future.apply,
  parallel, Lib2NIST, MS-DIAL;
  kb_slugs: `asb-paper-10-1021-acs-analchem-2c05389`;
  DOIs: `10.1021/acs.analchem.2c05389`)
- `compound-identifier-standardization` — Standardizes heterogeneous compound
  identifiers across annotation sources (Tools: PubChem, jobs.py,
  prepare_wikidata_lotus_prefect.py, drugbank_extraction.py;
  kb_slugs: `asb-paper-10-1038-s41592-025-02813-0`;
  DOIs: `10.1038/s41592-025-02813-0`)
- `cytoscape-network-format-export` — Exports consolidated master table as
  Cytoscape-compatible network (Tools: MetaMapR, cytoscape.js;
  kb_slugs: `asb-paper-10-1093-bioinformatics-btv194`;
  DOIs: `10.1093/bioinformatics/btv194`)
- `molecular-duplicate-detection-and-deduplication` — Identifies and removes
  duplicate molecular records before final consolidation (Tools: R, Python,
  sanitizing.py, Python 3, smiles.py;
  kb_slugs: `asb-paper-10-7554-elife-70780`, `asb-paper-10-1007-s00044-016-1764-y`;
  DOIs: `10.7554/eLife.70780`, `10.1007/s00044-016-1764-y`)

**Verification:** master_feature_table.tsv must have one row per input feature;
columns from each upstream stage must be present (network_component, cosine_score,
sirius_formula, etc.); no duplicate feature_id values; Cytoscape graphml must be
parseable.

---

## Grounding

Run `/ground` per stage to verify against source papers via Perspicacité (server
on :8002, KB prefix `asb-paper-*`):

```
/ground stage=preprocess    kb=asb-paper-10-1021-acs-jnatprod-7b00737
/ground stage=network       kb=asb-paper-10-1186-s13321-024-00878-1
/ground stage=library_match kb=asb-paper-10-1038-s41467-023-37446-4
/ground stage=sirius        kb=asb-paper-10-1038-s41587-021-01045-9
/ground stage=taxonomy_propagate kb=asb-paper-10-3389-fpls-2019-01329  # optional
/ground stage=fusion        kb=asb-paper-10-1186-s13321-021-00558-4
```

When no Perspicacité server is available, ground against the DOIs listed per stage
using the local `skills_index.json` embedding search (offline fallback, P4).

## Verification contract

The `asb solve-workflow` rubric grades this workflow on eight dimensions:

| Rubric dimension        | Binding | Notes |
|-------------------------|---------|-------|
| STEP_ORDERING           | binding | preprocess → network → library_match → sirius → (taxonomy_propagate) → fusion |
| TOOL_SELECTION          | binding | MZmine/OpenMS for preprocess; matchms for network+library_match; SIRIUS 6 for sirius |
| INTERMEDIATE_FIDELITY   | binding | feature_table, mgf×2, library_matches, compound_identification, tima_reweighted |
| END_TO_END_OUTPUT       | binding | master_feature_table.tsv must exist and be non-empty |
| SCIENTIFIC_VALIDITY     | binding | annotations must carry MSI level metadata; provenance columns must trace to source |
| CLAIM_VALIDATION        | informational | cross-check annotation counts vs reported literature benchmarks |
| REPRODUCTION            | informational | mgf → SIRIUS → compound_identification round-trip checksum |
| PARAMETER_SENSITIVITY   | informational | cosine threshold 0.7; SIRIUS confidence filter cosmicScore >= 0.5 |

## Provenance

- **schema_version:** 0.3.0
- **kind:** composite-workflow (P0 pilot)
- **bound_by:** index (fallback; Perspicacité server unreachable at authoring time)
- **derived_from_workflows:** see `metadata.derived_from_workflows` — these benchmark
  items are ablated by the eval harness when this super-skill is installed
  (SPEC §8 integrity contract).
- **authored:** 2026-06-28
- **generator:** AgenticScienceBuilder P0-pilot-composite-workflow-authoring
- **collection:** metabolomics v2 (5,865 skills / 909 tools / 568 papers)
