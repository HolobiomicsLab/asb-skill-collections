---
name: molecular-networking
description: 'Use when running feature-based molecular networking on LC-MS/MS data:
  orchestrates the canonical pipeline — feature detection/alignment, spectral similarity
  networking, library matching with annotation propagation, and network visualization.'
license: CC-BY-4.0
metadata:
  license_tier: open
  provenance_tier: synthetic
  tools_used:
  - gnps-molecular-networking
  - gnps-spectral-libraries
  - matchms
  - spec2vec
  - cytoscape
  skill_kind: super
  orchestrates:
  - lc-ms-feature-extraction-and-alignment
  - ms-ms-feature-preparation-for-gnps
  - spectral-similarity-network-generation
  - molecular-family-graph-construction
  - spectral-cluster-connectivity-assessment
  - spectral-library-matching
  - spectral-network-propagation-analysis
  - molecular-network-node-annotation
  - interactive-network-visualization-rendering
  - molecular-network-metadata-organization
  synthesized_from:
  - lc-ms-feature-extraction-and-alignment
  - ms-ms-feature-preparation-for-gnps
  - spectral-similarity-network-generation
  - molecular-family-graph-construction
  - spectral-cluster-connectivity-assessment
  - spectral-library-matching
  - spectral-network-propagation-analysis
  - molecular-network-node-annotation
  - interactive-network-visualization-rendering
  - molecular-network-metadata-organization
status: hold
related_skills:
- lc-ms-feature-extraction-and-alignment
- ms-ms-feature-preparation-for-gnps
- spectral-similarity-network-generation
- molecular-family-graph-construction
- spectral-cluster-connectivity-assessment
- spectral-library-matching
- spectral-network-propagation-analysis
- molecular-network-node-annotation
- interactive-network-visualization-rendering
- molecular-network-metadata-organization
---
This super-skill orchestrates the canonical **feature-based molecular networking**
pipeline for LC-MS/MS data. It does not re-implement any stage — it sequences the
sub-skills below in order, names the decision points between them, and points each
stage at the tool(s) it grounds on. Apply a stage's sub-skill for the procedure;
use this skill to keep the end-to-end workflow coherent.

## Stage 1 — Feature detection / alignment → GNPS-ready MS/MS
- `lc-ms-feature-extraction-and-alignment` — detect and align LC-MS features across
  samples (grounds on `ms-dial` / equivalent peak-picking).
- `ms-ms-feature-preparation-for-gnps` — export the aligned feature table + MS/MS to
  the GNPS feature-based molecular networking (FBMN) input format.
- **Decision points:** ionization polarity handling (process modes separately);
  whether to deduplicate/merge isotopologues and adducts before export.

## Stage 2 — Spectral similarity / networking
- `spectral-similarity-network-generation` — score MS/MS spectra pairwise and build
  the similarity edges (grounds on `matchms` / `spec2vec` for the similarity metric;
  `gnps-molecular-networking` for the FBMN job).
- `molecular-family-graph-construction` — assemble the network and partition it into
  molecular families (connected components).
- `spectral-cluster-connectivity-assessment` — sanity-check cluster connectivity
  (component sizes, edge density) before trusting downstream propagation.
- **Decision points:** cosine/entropy similarity **threshold** and minimum matched
  fragment peaks; top-K edges per node; max component size.

## Stage 3 — Annotation / propagation
- `spectral-library-matching` — annotate nodes by matching against reference
  libraries (grounds on `gnps-spectral-libraries`).
- `spectral-network-propagation-analysis` — propagate annotations from library-matched
  nodes to their unannotated network neighbours.
- `molecular-network-node-annotation` — write the consolidated annotations
  (and their confidence level) back onto the network nodes.
- **Decision points:** library match score cutoff; library-vs-analog (open) search;
  **when to stop propagating** (how many hops from a confident match) so annotations
  do not drift across a molecular family.

## Stage 4 — Visualization
- `interactive-network-visualization-rendering` — render the annotated network for
  interactive inspection (grounds on `cytoscape`).
- `molecular-network-metadata-organization` — organize node/edge metadata
  (sample groups, intensities, annotations) so the visualization is interpretable.
- **Decision points:** node colouring (chemical class vs. sample group); which
  metadata layers to surface.

## Grounding
Each stage's sub-skill carries its own source paper(s). To ground a stage against its
source, run the Perspicacité binder on that sub-skill's slug, e.g.
`python scripts/perspicacite_kb_bind.py query --collection collections/metabolomics/v2 --skill spectral-similarity-network-generation --question "..."`.
