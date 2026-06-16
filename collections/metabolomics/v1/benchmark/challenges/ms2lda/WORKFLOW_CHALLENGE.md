# Workflow Challenge: `coll_ms2lda_workflow`


> MS2LDA is an unsupervised machine learning framework that applies Latent Dirichlet Allocation to tandem mass spectrometry data to discover recurring fragmentation patterns (Mass2Motifs) representing molecular substructures, with integrated preprocessing, LDA modeling, automated annotation via MAG and Spec2Vec, MotifDB integration, and interactive visualization.

**Mode:** `actual`  
**Reproducibility tier:** `type-checked`

## Mission

Reproduce the methodology of the source paper as faithfully as possible using the steps below. Where a step's reproducibility tier is `bypassed`, `manual-only`, or `experimental`, use the cached output declared in its resumption contract; do not attempt to re-execute.

## Tier promise

_Every step has typed I/O ports declared; executable optional. Filesystem presence check + type-port resolution._

## Instructions

Reproduce the 5-step workflow below. Honor each step's IO contract; produce the files listed under 'Final expected outputs'.

## Background

MS2LDA implements a complete workflow for unsupervised substructure discovery in mass spectrometry data. The tool describes a preprocessing mechanism that converts MS/MS spectra into bag-of-fragments format, extracts neutral losses, and filters noise to prepare input for LDA modeling. MS2LDA applies Latent Dirichlet Allocation to infer Mass2Motifs—recurring patterns of fragment ions and neutral losses that describe latent fragmentation behaviors across spectral datasets. The framework incorporates automated annotation of discovered Mass2Motifs through a mechanism that integrates the MAG annotation system with Spec2Vec embeddings, loading pretrained models from a Zenodo repository to generate per-motif annotation records. MS2LDA describes integration with a MassQL-searchable MotifDB that enables motif-to-database comparison and retrieval of known reference motifs. The tool provides a postprocessing pipeline that generates molecular network representations (GraphML format) encoding discovered motifs and their relationships. Results are accessible through both an interactive web application (MS2LDAViz) for real-time exploration and command-line interfaces for scripted analysis workflows, with output including Mass2Motif collections, spectra-motif loadings, visualizations, and network exports.

## Research questions

- How does MS2LDA convert mass spectrometry input files in multiple formats (.mgf, .msp, .mzML) into a bag-of-fragments representation suitable for LDA training?
- How does MS2LDA apply Latent Dirichlet Allocation to a bag-of-fragments corpus to infer Mass2Motifs from mass spectrometry fragmentation patterns?
- How does the Spec2Vec-based annotation lookup process generate per-motif annotation records by loading a trained motifset and the Spec2Vec model?
- How does MS2LDA query a MassQL-searchable MotifDB to retrieve and rank database matches for discovered motifs?
- How does MS2LDA construct a network graph that encodes spectral similarity relationships and motif membership annotations for post-processing visualization and export?

## Methods overview

Load spectral data from input file (mgf, msp, or mzML) using format-specific parsers. Extract fragment ion m/z values and peak intensities; calculate neutral loss values for all fragment–precursor pairs. Apply noise filtering to remove low-intensity fragments and statistically insignificant peaks. Bin fragment and neutral loss masses into discrete mass tokens via mass-binning discretization. Generate bag-of-fragments corpus, encoding each spectrum as a document with token frequencies. Validation: verify corpus dimensionality, token inventory completeness, and that all documents are non-empty; check that at least 80% of input spectra are retained post-filtering. Load preprocessed corpus containing bag-of-fragments representations of preprocessed MS/MS spectra Initialize LDA model with specified topic count (n_motifs), hyperparameters (alpha, beta), and iteration limit (n_iterations) Train LDA inference on corpus, iteratively updating topic-fragment and spectrum-topic distributions Monitor and record convergence metrics (log-likelihood or perplexity) across training iterations Extract learned Mass2Motif distributions (topic-fragment probability maps) from converged model Serialize trained model state to pickle binary (ms2lda.bin) and motifset to JSON schema (motifset.json) Validation: convergence curve shows stable or decreasing objective; motifset contains all n_motifs with non-zero fragment probabilities; model and motifset files are non-empty and deserializable Load pre-trained Spec2Vec model and spectral embeddings from Zenodo deposit. Parse trained motifset JSON file to extract all Mass2Motif records and their fragment/loss compositions. Compute cosine similarity between each motif's embedding and reference spectral embeddings using Spec2Vec. Rank candidate annotations by similarity score and extract top-N matches with associated structural labels. Validation: Output JSON contains all motif identifiers with non-null similarity scores and at least one annotation label per motif; similarity scores fall within [0, 1] range and are ranked in descending order. Load the inferred motifset JSON, extracting Mass2Motif definitions (fragment and neutral-loss compositions). For each motif, formulate a MassQL query targeting its characteristic fragment and neutral-loss pattern. Execute the MassQL query against the MotifDB library using the MassQL4MotifDB integration layer. Rank returned matches by similarity or match score (e.g., cosine similarity on fragment-loss overlap). Serialize ranked results to JSON with per-motif match records (MotifDB ID, name, composition, score). Validation: Confirm JSON output contains a ranked match list for each input motif; verify presence of MotifDB identifiers, match scores, and composition metadata for each returned entry. Load motifset JSON and extract Mass2Motif fragment and neutral-loss probability distributions. Construct pseudo-spectra for each motif by converting probabilities to intensity-weighted m/z vectors. Compute pairwise cosine similarity between all motif pseudo-spectra. Filter edges by similarity threshold and populate graph with motif nodes and weighted similarity edges. Annotate nodes with motif metadata (ID, fragment composition, spectra count) and edges with similarity scores. Serialize graph to GraphML format with proper XML structure and attribute declarations. Validation: verify network.graphml is valid XML, contains all motif nodes with unique IDs, edges reflect computed similarity, and file is parseable by standard graph tools (e.g., NetworkX, Cytoscape).

**Domain:** metabolomics

**Techniques:** clustering, dimensionality-reduction, machine-learning, molecular-networking, spectral-library-matching, tandem-ms

## Claims to address (CLAIM_VALIDATION rubric)
Your output should make each binding claim checkable:
- **(finding)** MS2LDA is an advanced tool designed for unsupervised substructure discovery in mass spectrometry data. _[grounded: SYS-MS2LDA]_
- **(finding)** MS2LDA significantly enhances the capabilities described in the original MS2LDA paper from 2016. _[grounded: SYS-MS2LDA]_
- **(finding)** Mass spectrometry fragmentation patterns hold abundant structural information vital for analytical chemistry, natural product research, and food safety assessments.
- **(finding)** MS2LDA identifies recurring substructures (motifs) across spectral datasets without relying on prior compound identification. _[grounded: SYS-MS2LDA]_
- **(finding)** Mass2Motifs can be added to the online MotifDB by raising an issue following the Mass2Motifs template. _[grounded: COMP-MOTIFDB]_
- **(finding)** MS2LDA expects preprocessed MS/MS data typically in .mgf, .mzML, or .msp formats. _[grounded: SYS-MS2LDA]_
- **(finding)** MS2LDA provides Mass2Motifs, spectra-motif loadings, and optional annotations via MotifDB or MAG as output. _[grounded: SYS-MS2LDA]_
- **(finding)** Downloading the required models and storing a few runs typically requires 15–20 GB of free space.
- **(finding)** MS2LDA applies probabilistic topic modeling to tandem mass spectrometry data for unsupervised discovery of fragmentation patterns. _[grounded: SYS-MS2LDA]_
- **(finding)** MS2LDA identifies recurring patterns of mass fragments and neutral losses called Mass2Motifs across MS/MS datasets. _[grounded: SYS-MS2LDA]_
- **(finding)** MS2LDA uses Latent Dirichlet Allocation (LDA) to infer which motifs are most likely to explain the observed fragmentation patterns. _[grounded: SYS-MS2LDA]_
- **(finding)** MS2LDA preprocessing includes converting MS/MS spectra into a bag-of-fragments format. _[grounded: SYS-MS2LDA]_
- **(finding)** MS2LDA preprocessing includes extracting neutral losses. _[grounded: SYS-MS2LDA]_
- **(finding)** MS2LDA preprocessing includes filtering out noise. _[grounded: SYS-MS2LDA]_
- **(finding)** MS2LDA model training applies LDA to processed spectra to learn Mass2Motifs that describe recurring fragmentation patterns. _[grounded: SYS-MS2LDA]_
- **(finding)** MS2LDA postprocessing includes visualizing motif loadings across spectra and comparing motifs to known entries in MotifDB. _[grounded: SYS-MS2LDA]_
- **(finding)** MS2LDA has been successfully applied to discover novel natural products in fungal extracts, plant metabolomics, and marine organisms. _[grounded: SYS-MS2LDA]_
- **(finding)** MS2LDA has applications in environmental monitoring including pesticide detection, water quality assessment, and soil contamination analysis. _[grounded: SYS-MS2LDA]_
- **(finding)** MS2LDA can be used for clinical metabolomics applications including biomarker discovery, drug metabolism studies, and disease profiling. _[grounded: SYS-MS2LDA]_
- **(finding)** MS2LDA has applications in food science including food authenticity testing, quality control, and flavor profiling. _[grounded: SYS-MS2LDA]_
- **(finding)** MS2LDAViz lets users run analyses and explore results in a browser with live controls and rich visualizations. _[grounded: COMP-MS2LDAVIZ]_
- **(finding)** Before running MS2LDA, users must download the Spec2Vec model, embeddings, and library DB from the Zenodo repository. _[grounded: SYS-MS2LDA]_
- **(finding)** MS2LDAViz includes a Motif Rankings tab that allows users to browse all Mass2Motifs ranked based on different thresholds. _[grounded: COMP-MASSQL]_
- **(finding)** MS2LDAViz includes a Motif Details tab for inspecting selected motifs in depth with suggested structures and annotations. _[grounded: SYS-MS2LDA]_
- **(finding)** MS2LDAViz includes a Spectra Search tab for finding individual spectra by parent mass or fragment/loss values. _[grounded: SYS-MS2LDA]_
- **(finding)** MS2LDAViz includes a View Network tab for exploring an interactive network of optimized motifs. _[grounded: COMP-MS2LDAVIZ]_
- **(finding)** MS2LDAViz includes a Motif Search tab for performing motif-motif searches against reference motifs in MotifDB. _[grounded: SYS-MS2LDA]_
- **(finding)** The `run_analysis.sh` script is provided for Linux/macOS users to simplify MS2LDA execution. _[grounded: SYS-MS2LDA]_
- **(finding)** The `run_analysis.bat` script is provided for Windows users to simplify MS2LDA execution. _[grounded: SYS-MS2LDA]_
- **(finding)** MS2LDA command-line interface accepts --input flag for specifying the path to input spectra file. _[grounded: SYS-MS2LDA]_
- **(finding)** MS2LDA command-line interface accepts --output flag for specifying the directory to store results. _[grounded: SYS-MS2LDA]_
- **(finding)** MS2LDA command-line interface accepts --n_topics flag for specifying the number of Mass2Motifs to infer. _[grounded: SYS-MS2LDA]_
- **(finding)** MS2LDA command-line interface accepts --n_iterations flag for specifying the number of LDA training iterations. _[grounded: SYS-MS2LDA]_
- **(finding)** MS2LDA command-line interface accepts --alpha flag for specifying the LDA alpha hyperparameter. _[grounded: SYS-MS2LDA]_
- **(finding)** MS2LDA command-line interface accepts --beta flag for specifying the LDA beta hyperparameter. _[grounded: SYS-MS2LDA]_
- **(finding)** After a successful MS2LDA run, results include a motif_figures folder with individual motif visualizations as PNG files. _[grounded: SYS-MS2LDA]_
- **(finding)** After a successful MS2LDA run, results include a motifs folder with each inferred Mass2Motif. _[grounded: SYS-MS2LDA]_
- **(finding)** After a successful MS2LDA run, results include a motifset.json file with discovered Mass2Motifs in JSON format. _[grounded: SYS-MS2LDA]_
- **(finding)** After a successful MS2LDA run, results include a convergence_curve.png file showing the training convergence plot. _[grounded: SYS-MS2LDA]_
- **(finding)** After a successful MS2LDA run, results include a network.graphml file for molecular network export. _[grounded: SYS-MS2LDA]_
- **(finding)** After a successful MS2LDA run, results include a ms2lda.bin file which is a binary dump of the trained LDA model. _[grounded: SYS-MS2LDA]_
- **(finding)** After a successful MS2LDA run, results include a ms2lda_viz.json.gz file containing compressed results for the MS2LDAViz web app. _[grounded: SYS-MS2LDA]_
- **(finding)** MS2LDA's functionality is organized into modular steps: Preprocessing, Modeling, Annotation, and Visualization. _[grounded: SYS-MS2LDA]_
- **(finding)** MS2LDA Preprocessing module filters and cleans spectra in positive/negative ion mode. _[grounded: SYS-MS2LDA]_
- **(finding)** MS2LDA Modeling module infers Mass2Motifs via LDA. _[grounded: SYS-MS2LDA]_
- **(finding)** MS2LDA Annotation module assigns substructure meaning. _[grounded: SYS-MS2LDA]_
- **(finding)** MS2LDA Visualization module explores and exports results. _[grounded: SYS-MS2LDA]_
- **(finding)** MS2LDA can be installed using pip, Conda, or Poetry. _[grounded: SYS-MS2LDA]_
- **(finding)** MS2LDA is developed by a team led by Rosina Torres Ortega, Jonas Dietrich, and Joe Wandy, under supervision of Justin J.J. van der Hooft at Wageningen University & Research. _[grounded: SYS-MS2LDA]_
- **(finding)** MS2LDA builds on the original work published by van der Hooft et al. in PNAS 2016. _[grounded: SYS-MS2LDA]_

## Invariants (must not change)
Changing any of these **is** a failure regardless of openness:
- MAG is trained on positive ionization mode data

## Steps

### Step `task_001`
- Title: Reconstruct the MS/MS spectral preprocessing step that converts raw spectra into bag-of-fragments format
- Task kind: `component_reconstruction`
- Task: Implement the preprocessing module to read MS/MS spectra from .mgf, .msp, or .mzML formats and convert them into a bag-of-fragments representation with extracted neutral losses, suitable for LDA training.
- Inputs:
  - MS/MS spectra in .mgf (Mascot Generic Format), .msp (NIST-style), or .mzML format
- Expected outputs:
  - Bag-of-fragments corpus in LDA-compatible format (document-term matrix or serialized Python object)
  - Fragment and neutral loss token inventory with mass-to-token mappings
  - Quality control report documenting noise filtering statistics and retained fragment counts
- Tools: MS2LDA, MS2LDA.Preprocessing.load_and_clean, MS2LDA.Preprocessing.generate_corpus, Python, Conda
- Landmark output files: raw_spectra_loaded.json, fragments_and_losses_extracted.csv, noise_filtered_spectrum_table.csv, token_vocabulary.json, corpus_stats.txt
- Primary expected artifact: `corpus.pkl`

### Step `task_002`
- Depends on: `task_001`
- Title: Reconstruct the LDA model training step that produces a trained MS2LDA model artifact from bag-of-fragments input
- Task kind: `component_reconstruction`
- Task: Train a Latent Dirichlet Allocation (LDA) model on a preprocessed bag-of-fragments corpus to infer Mass2Motifs, then serialize the trained model and discovered motif set to ms2lda.bin and motifset.json respectively.
- Inputs:
  - Preprocessed bag-of-fragments corpus (as a Python corpus object or serialized format compatible with MS2LDA.modeling)
  - Model hyperparameters: number of topics (n_motifs), training iterations (n_iterations), alpha hyperparameter, beta hyperparameter
- Expected outputs:
  - Trained LDA model binary artifact (ms2lda.bin)
  - Discovered Mass2Motifs in JSON format with fragment and neutral-loss probabilities (motifset.json)
  - Training convergence curve visualization (convergence_curve.png)
- Tools: MS2LDA, Latent Dirichlet Allocation (LDA), Python
- Landmark output files: convergence_curve.png, motifset.json
- Primary expected artifact: `ms2lda.bin`

### Step `task_003`
- Depends on: `task_002`
- Title: Reconstruct the MAG automated motif annotation step that maps discovered Mass2Motifs to known substructures via Spec2Vec
- Task kind: `component_reconstruction`
- Task: Load a trained MS2LDA motifset and the Spec2Vec model from Zenodo, then perform per-motif annotation lookup using Spec2Vec similarity scoring to produce annotation records with labels and similarity scores for each Mass2Motif.
- Inputs:
  - Trained motifset JSON file (motifset_optimized.json) from MS2LDA modeling step
  - Pre-trained Spec2Vec model, embeddings, and spectral library database from Zenodo
- Expected outputs:
  - Per-motif annotation records in JSON format with motif identifiers, suggested structure labels, Spec2Vec similarity scores, and confidence metrics
- Tools: Spec2Vec, MAG (Mass2Motif Annotation Guidance), Python, MS2LDA
- Landmark output files: motifset_optimized.json, spec2vec_model.pkl, similarity_scores_per_motif.csv, mag_annotations.json
- Primary expected artifact: `mag_annotations.json`

### Step `task_004`
- Depends on: `task_002`
- Title: Reconstruct the MotifDB motif-matching step that retrieves database hits for discovered motifs using MassQL queries
- Task kind: `component_reconstruction`
- Task: Query the MassQL-searchable MotifDB for database matches against a set of inferred Mass2Motifs and return a ranked list of matching motif records per input motif, serialized in JSON format.
- Inputs:
  - Inferred motifset in JSON format (motifset.json or motifset_optimized.json) from MS2LDA modeling step, containing Mass2Motif definitions with fragment and neutral-loss compositions
  - MotifDB reference database library (downloaded from Zenodo, required for MassQL-based lookups)
- Expected outputs:
  - Ranked MotifDB match records per input motif, returned as JSON with per-motif match lists including MotifDB entry ID, name, fragment composition, neutral-loss composition, and match score
- Tools: MassQL, MotifDB, MS2LDA
- Landmark output files: motifset_loaded.json, massql_queries.json, motifdb_matches.json
- Primary expected artifact: `motifdb_matches.json`

### Step `task_005`
- Depends on: `task_002`
- Title: Reconstruct the molecular network export step that produces a GraphML network artifact from a trained motifset
- Task kind: `component_reconstruction`
- Task: Construct a molecular network in GraphML format (network.graphml) encoding Mass2Motifs as nodes with spectral similarity edges and motif-membership attributes, reading from an inferred motifset JSON file and the trained LDA model.
- Inputs:
  - Inferred motifset in JSON format (motifset.json or motifset_optimized.json) containing Mass2Motif definitions with fragment and neutral-loss probabilities
  - Trained LDA model (optional, ms2lda.bin) for accessing motif loadings and spectral assignments
- Expected outputs:
  - GraphML-formatted network file (network.graphml) with Mass2Motif nodes, similarity-weighted edges, and motif metadata attributes
- Tools: MS2LDA, Python
- Landmark output files: motif_pseudospectra.csv, motif_similarity_matrix.csv, network_nodes.csv, network_edges.csv
- Primary expected artifact: `network.graphml`

## Final expected outputs

- `Per-motif annotation records in JSON format with motif identifiers, suggested structure labels, Spec2Vec similarity scores, and confidence metrics` (type: file, tolerance: hash)
- `Ranked MotifDB match records per input motif, returned as JSON with per-motif match lists including MotifDB entry ID, name, fragment composition, neutral-loss composition, and match score` (type: file, tolerance: hash)
- `GraphML-formatted network file (network.graphml) with Mass2Motif nodes, similarity-weighted edges, and motif metadata attributes` (type: file, tolerance: hash)

## How your attempt will be scored

ASB defines seven rubrics in `workflow_rubric.py` (STEP_ORDERING, INTERMEDIATE_FIDELITY, END_TO_END_OUTPUT, TOOL_SELECTION, EFFICIENCY, CLAIM_VALIDATION, ADVERSARIAL_TRAP_AVOIDANCE). Which of them bind for *this* challenge depends on the tier and openness below.

### Tier evaluation profile

**Evaluator:** automated — filesystem presence + type-port resolution; END_TO_END_OUTPUT with declared per-output tolerance.
**Binding rubrics:** STEP_ORDERING, END_TO_END_OUTPUT (typed/tolerance), TOOL_SELECTION, CLAIM_VALIDATION.

### Openness stance

**Openness: open — validity-first.** The deterministic match-rubrics above are demoted to *informational*. The binding evaluator is **SCIENTIFIC_VALIDITY** (below). Any scientifically sound method that addresses the research question is valid, and novel findings or unexplored aspects can score positively — **different is not wrong**.

## SCIENTIFIC_VALIDITY (binding for open / mixed tasks)
Open/mixed steps are graded at **EvalTier** granularity by the shared card judge (`runner_checks` llm_judge), not by exact match. The judge assigns one of `reproduced` / `replicated` / `re_analyzed` / `consistent` / `improved`; `consistent` and `re_analyzed` earn partial credit per the tier multipliers (0.60 / 0.75), so a scientifically sound but different result is credited rather than failed. Exact-match rubrics (INTERMEDIATE_FIDELITY, END_TO_END_OUTPUT) are **informational** for these tasks. Three axes the judge weighs:

1. **Addresses the research question** — does the attempt answer it?
2. **Defensible method** — sound, and respects the *Invariants* above?
3. **Results validity** — consistent with the claims, or a valid, evidenced extension? New supported claims earn credit, not penalty.

## Workflow characterisation

_Suter et al. 2025 (DOI 10.1016/j.future.2025.107974)._

- **Coupling:** loose

- **Composition modularity:** hierarchical

- **Abstraction level:** intermediate

- **Orchestration planning:** static

- **Data transport:** file

- **Characterisation confidence:** inferred


## Submission

Produce two artifacts in your output directory:

1. The output files at the paths declared under **Final expected outputs**.
2. An `attempt.json` matching the schema below.
3. _(Optional)_ `attempt_metrics.json` with `wall_time_s`, `total_tokens`, `cost_usd` for the EFFICIENCY rubric.

### `attempt.json` schema

```json
{
  "workflow_id": "coll_ms2lda_workflow",
  "agent_order": [
    "task_001",
    "task_002",
    "task_003",
    "task_004",
    "task_005"
  ],
  "intermediate_outputs": {
    "task_001": {
      "<output_name>": "<locator>"
    },
    "task_002": {
      "<output_name>": "<locator>"
    },
    "task_003": {
      "<output_name>": "<locator>"
    },
    "task_004": {
      "<output_name>": "<locator>"
    },
    "task_005": {
      "<output_name>": "<locator>"
    }
  },
  "final_outputs": {
    "Per-motif annotation records in JSON format with motif identifiers, suggested structure labels, Spec2Vec similarity scores, and confidence metrics": "<locator>",
    "Ranked MotifDB match records per input motif, returned as JSON with per-motif match lists including MotifDB entry ID, name, fragment composition, neutral-loss composition, and match score": "<locator>",
    "GraphML-formatted network file (network.graphml) with Mass2Motif nodes, similarity-weighted edges, and motif metadata attributes": "<locator>"
  },
  "chosen_tools": {
    "task_001": "<tool_name>",
    "task_002": "<tool_name>",
    "task_003": "<tool_name>",
    "task_004": "<tool_name>",
    "task_005": "<tool_name>"
  }
}
```

---
_Generated by `asb workflow-challenge` (see ASB docs/superpowers/specs/2026-05-12-workflow-evaluation-and-reviewer-ui-design.md)._
