# SciTask Card: Reconstruct the molecular network export step that produces a GraphML network artifact from a trained motifset

- Task ID: `task_005`
- Schema version: `0.18.0`
- Created at: `2026-06-15T21:44:19.295434+00:00`
- Source package: `/Users/nothiasl/git/AgenticScienceBuilder/outputs/asbb_pilot/coll_ms2lda/synthesized_package`
- Domain: `mass-spectrometry / metabolomics`
- Subtask categories: `data-processing`, `visualization`
- GitHub: `vdhooftcompmet/MS2LDA`
- Input from: `task_002`
- Quality: Score 2/5 — Coherent: false, placeholder, 6 grounding failures

## Classification

- Task kind: `component_reconstruction`
- Article type: `software-tool`
- Primary domain: `metabolomics`
- Subdomains: `computational-metabolomics`, `untargeted-metabolomics`, `natural-products`
- Techniques: `clustering`, `dimensionality-reduction`, `machine-learning`, `molecular-networking`, `spectral-library-matching`, `tandem-ms`

## Research Question
How does MS2LDA construct a network graph that encodes spectral similarity relationships and motif membership annotations for post-processing visualization and export?

## Connected Finding
MS2LDA provides a postprocessing pipeline that reads discovered motifs and LDA model outputs to generate a network representation (network.graphml) where nodes represent spectra annotated with their motif memberships and edges encode spectral similarity relationships, enabling integrated workflow visualization and export.

## Task Description
Construct a molecular network in GraphML format (network.graphml) encoding Mass2Motifs as nodes with spectral similarity edges and motif-membership attributes, reading from an inferred motifset JSON file and the trained LDA model.

## Inputs
- Inferred motifset in JSON format (motifset.json or motifset_optimized.json) containing Mass2Motif definitions with fragment and neutral-loss probabilities
- Trained LDA model (optional, ms2lda.bin) for accessing motif loadings and spectral assignments

## Expected Outputs
- GraphML-formatted network file (network.graphml) with Mass2Motif nodes, similarity-weighted edges, and motif metadata attributes

## Expected Output File

- `network.graphml`

## Landmark Outputs

- `motif_pseudospectra.csv`
- `motif_similarity_matrix.csv`
- `network_nodes.csv`
- `network_edges.csv`

## Tools
- MS2LDA
- Python

## Skills
- mass2motif-network-construction
- spectral-similarity-computation
- graph-serialization-graphml
- motif-metadata-annotation
- json-parsing-motifset-extraction

## Workflow Description
1. Load the inferred motifset from motifset.json or motifset_optimized.json, extracting Mass2Motif definitions (fragment and neutral-loss compositions). 2. Retrieve or reconstruct pseudo-spectra representations from each motif's probability-weighted fragments and losses. 3. Compute pairwise spectral similarity (e.g., cosine similarity) between all Mass2Motif pseudo-spectra. 4. Build a directed or undirected graph where each Mass2Motif is a node, with weighted edges between motifs exceeding a similarity threshold. 5. Annotate nodes with motif metadata (ID, fragment/loss composition, spectra count loading on motif) and edges with similarity scores. 6. Serialize the network to GraphML format and write to network.graphml.

## Available Artifacts
| Path | Role | Indexable |
|---|---|---|
| `figures/CompMetabolomics_logo.jpg` | figure | False |
| `figures/MS2LDA_LOGO_black.jpg` | figure | False |
| `figures/MS2LDA_LOGO_white.jpg` | figure | False |
| `figures/MS2LDA_Workflow.jpg` | figure | False |
| `figures/WUR_RGB_standard_2021.png` | figure | False |
| `figures/WUR_logo.jpg` | figure | False |
| `figures/pnas.jpg` | figure | False |
| `paper.md` | main_article | True |

## Missing Information
- The changelog section contains only a header 'Added' with no documented changes, features, or implementation details for the postprocessing network construction step.
- No information is provided about the expected structure, schema, or content of ARTIFACT-MOTIFSET input or ARTIFACT-LDA-MODEL input required for the postprocessing step.
- No details are given regarding spectral similarity computation method, thresholding strategy, or parameters that govern edge construction in the network graph.
- No specification is provided for the node attribute schema encoding motif-membership or edge attribute schema encoding spectral similarity in the GraphML output.

## Domain Knowledge
- Mass2Motifs are recurring fragmentation patterns represented as probability distributions over fragment and neutral-loss m/z values; nodes in the network encode these motif identities and their fragment compositions.
- Spectral similarity in tandem mass spectrometry networks is typically computed using cosine similarity on pseudo-spectra intensity vectors derived from motif fragment and loss probabilities.
- GraphML is an XML-based graph format supporting node and edge attributes; nodes and edges must have unique identifiers and metadata labels for visualization in network viewers (e.g., Cytoscape).
- Motif-membership attributes (e.g., document count, average loading) reflect how many spectra are significantly assigned to each motif and are essential for downstream interpretation and filtering.

## Uncertainty Notes
- This card was generated by the LLM-assisted pipeline and needs scientific expert review.
- Each TracedClaim's evidence_span has been substring-checked against its source section; see logs/llm_calls.jsonl and capsules/<task_id>/quality_report.json for groundedness results.
- Synthesis grounding: the following tools/outputs were NOT found in the source paper and are inferred — verify before use: GraphML-formatted network file (network.graphml) with Mass2Motif nodes, similarity-weighted edges, and motif metadata attributes.

## Evidence Snippets
- `ev_001` from `agent2_synthesis` (agent2_traced): [intro] How does MS2LDA construct a network graph that encodes spectral similarity relationships and motif membership annotations for post-processing visualization and export?: 'offering users an integrated workflow with improved usability, detailed visualizations, and a searchable motif database (MotifDB)'
- `ev_002` from `agent2_synthesis` (agent2_traced): [intro] MS2LDA provides a postprocessing pipeline that reads discovered motifs and LDA model outputs to generate a network representation (network.graphml) where nodes represent spectra annotated with their motif memberships and edges encode spectral similarity relationships, enabling integrated workflow visualization and export.: 'MS2LDA is an advanced tool designed for unsupervised substructure discovery in mass spectrometry data, utilizing topic modeling and providing automated annotation of discovered motifs'
- `ev_003` from `agent2_synthesis` (agent2_traced): [other] Inferred motifset in JSON format (motifset.json or motifset_optimized.json) containing Mass2Motif definitions with fragment and neutral-loss probabilities: 'motifset.json           # Discovered Mass2Motifs in JSON format
├─ motifset_optimized.json # Optimized Mass2Motifs in JSON format'
- `ev_004` from `agent2_synthesis` (agent2_traced): [other] Trained LDA model (optional, ms2lda.bin) for accessing motif loadings and spectral assignments: '├─ ms2lda.bin              # Binary dump of the trained LDA model'
- `ev_005` from `agent2_synthesis` (agent2_traced): [other] GraphML-formatted network file (network.graphml) with Mass2Motif nodes, similarity-weighted edges, and motif metadata attributes: '├─ network.graphml         # Molecular network export (GraphML)'
- `ev_006` from `agent2_synthesis` (agent2_traced): [other] MS2LDA: 'invoke the main script `ms2lda_runfull.py` with your arguments'
- `ev_007` from `agent2_synthesis` (agent2_traced): [other] Python: 'Configure the Python environment (set PYTHONPATH, activate conda, etc.)'
- `ev_008` from `agent2_synthesis` (agent2_traced): [discussion] The changelog section contains only a header 'Added' with no documented changes, features, or implementation details for the postprocessing network construction step.: '## [Unreleased]

### Added'
- `ev_009` from `agent2_synthesis` (agent2_traced): [discussion] No information is provided about the expected structure, schema, or content of ARTIFACT-MOTIFSET input or ARTIFACT-LDA-MODEL input required for the postprocessing step.: '[UNTRUSTED_DOCUMENT] section provides only metadata (synthesized date, repository reference) with no technical specifications.'
- `ev_010` from `agent2_synthesis` (agent2_traced): [discussion] No details are given regarding spectral similarity computation method, thresholding strategy, or parameters that govern edge construction in the network graph.: '[UNTRUSTED_DOCUMENT] section contains no method description for network construction.'
- `ev_011` from `agent2_synthesis` (agent2_traced): [discussion] No specification is provided for the node attribute schema encoding motif-membership or edge attribute schema encoding spectral similarity in the GraphML output.: '[UNTRUSTED_DOCUMENT] section contains no attribute specification details.'

## Evaluation Strategy
### Direct Checks
- verify file network.graphml exists in expected outputs or repository
- file_format_is network.graphml: verify XML structure conforms to GraphML schema (http://graphml.graphdrawing.org/)
- field_present: verify 'node' elements exist with 'id' attribute
- field_present: verify 'data' child elements within nodes include motif-membership attributes
- field_present: verify 'edge' elements exist with 'source' and 'target' attributes
- field_present: verify 'data' child elements within edges encode spectral similarity weights or scores
- script_runs: verify the postprocessing script executes without error when provided valid ARTIFACT-MOTIFSET and optional ARTIFACT-LDA-MODEL inputs
- output_matches_reference: node count and edge count are consistent with input motif set cardinality (no canonical answer — depends on spectral similarity threshold and motif clustering parameters)
- verify network.graphml can be parsed by a standard GraphML reader (robust to GraphML schema version, parameter-sensitive to node/edge attribute names)

### Expert Review
- Verify that spectral similarity edge weights are computed using an appropriate metric (e.g., cosine similarity, Euclidean distance) and that the choice of metric is documented
- Verify that motif-membership node attributes correctly encode the assignment of spectra or fragments to discovered motifs from the LDA model
- Verify that the graph structure meaningfully represents the relationships between motifs or spectra based on spectral similarity and shared motif membership
- Assess whether the GraphML serialisation preserves all relevant metadata (motif identifiers, similarity thresholds, LDA model hyperparameters) needed for downstream analysis or visualization

## Review Questions
- Is the research question correctly identified and scoped?
- Does the connected finding have enough supporting evidence?
- Which artifacts are required before this can become an executable benchmark task?
- What direct, visual, textual, or expert-review checks should be used for evaluation?

## Methodology Summary
1. Load motifset JSON and extract Mass2Motif fragment and neutral-loss probability distributions.
2. Construct pseudo-spectra for each motif by converting probabilities to intensity-weighted m/z vectors.
3. Compute pairwise cosine similarity between all motif pseudo-spectra.
4. Filter edges by similarity threshold and populate graph with motif nodes and weighted similarity edges.
5. Annotate nodes with motif metadata (ID, fragment composition, spectra count) and edges with similarity scores.
6. Serialize graph to GraphML format with proper XML structure and attribute declarations.
7. Validation: verify network.graphml is valid XML, contains all motif nodes with unique IDs, edges reflect computed similarity, and file is parseable by standard graph tools (e.g., NetworkX, Cytoscape).

## Workflow Ports

**Inputs:**

- `motifset_json` — Inferred motifset JSON (motifset.json or motifset_optimized.json) ← `task_002/lda_model`
- `lda_model` — Trained LDA model binary (ms2lda.bin)

**Outputs:**

- `network_graphml` — Molecular network in GraphML format (network.graphml)

## Provenance

- **Source kind:** github
- **Synthesized from:** `github:vdhooftcompmet__MS2LDA`
- **Synthesized at:** 2026-06-15T21:52:38+00:00

## Extraction Quality
- Score: 2/5
- Coherent: false
- Placeholder detected: true
- Groundedness failures (6):
  - tools[1]: evidence_span not found in section 'other' (value='Python', span='Configure the Python environment (set PYTHONPATH, activate c')
  - missing_information[1]: evidence_span not found in section 'discussion' (value='No information is provided about the expected structure, sch', span='[UNTRUSTED_DOCUMENT] section provides only metadata (synthes')
  - missing_information[2]: evidence_span not found in section 'discussion' (value='No details are given regarding spectral similarity computati', span='[UNTRUSTED_DOCUMENT] section contains no method description ')
  - missing_information[3]: evidence_span not found in section 'discussion' (value='No specification is provided for the node attribute schema e', span='[UNTRUSTED_DOCUMENT] section contains no attribute specifica')
  - research_question: evidence_span does not address HOW network graphs encode similarity relationships or motif annotations—it only mentions 'visualizations' and 'MotifDB', missing the core technical mechanism
  - finding: evidence_span is generic descriptor of MS2LDA tool, not specific evidence about network.graphml construction, pseudo-spectra, or motif-node encoding
- Notes: This card exhibits severe coherence and grounding failures. The research_question and finding are semantically disconnected from their evidence_spans—the question asks 'how' graph construction works, but the evidence only describes MS2LDA as a visualization tool. The finding makes specific claims about node/edge encoding (motif memberships, spectral similarity) that are not supported by any cited source text. Four of six missing_information entries cite '[UNTRUSTED_DOCUMENT]' instead of actual sections, indicating placeholder or fabricated evidence. The task_objective and workflow_description are well-structured and concrete, but they are not grounded in the research_question or finding—they appear to be independent specifications. The tools field references 'Python' with an evidence_span that does not exist. Critical implementation details (similarity metric choice, threshold strategy, node/edge attribute schema) are relegated to 'missing information' rather than being specified as task parameters. The card conflates MS2LDA as a whole tool with the specific postprocessing component being reconstructed. Quality is low due to lack of grounding, semantic incoherence, and reliance on unverified evidence.

---

*Card produced by **AgenticScienceBuilder (ASB)** — heuristic + LLM-assisted extraction from a research artifact. See the `ro-crate-metadata.json` in this capsule for full provenance.*
