---
name: spectral-library-molecular-networking
description: Use when you have deconvolved GC-MS spectra (from overlapping chromatographic peaks) in MGF or mzTab format and want to group chemically related compounds, visualize their similarity relationships, and identify spectral families without prior library matching.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3357
  edam_topics:
  - http://edamontology.org/topic_0121
  - http://edamontology.org/topic_3520
  tools:
  - MSHub
  - GNPS
  techniques:
  - LC-MS
  - GC-MS
derived_from:
- doi: 10.1038/s41587-020-0700-3
  title: mshub
evidence_spans:
- MSHub auto-deconvolution
- Auto-deconvolution and molecular networking of gas chromatography–mass spectrometry data
- GNPS molecular networking
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_mshub
    doi: 10.1038/s41587-020-0700-3
    title: mshub
  dedup_kept_from: coll_mshub
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1038/s41587-020-0700-3
  all_source_dois:
  - 10.1038/s41587-020-0700-3
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# spectral-library-molecular-networking

## Summary

Build and analyze molecular networks from deconvolved GC-MS spectra by clustering them via cosine similarity in GNPS, enabling compound discovery and family annotation in complex mixtures. This skill bridges automated spectral deconvolution with graph-based metabolite relationship discovery.

## When to use

You have deconvolved GC-MS spectra (from overlapping chromatographic peaks) in MGF or mzTab format and want to group chemically related compounds, visualize their similarity relationships, and identify spectral families without prior library matching. Use this when exploring untargeted metabolomics data where compound identity is unknown but structural relationships matter.

## When NOT to use

- Input spectra are already annotated with library matches and you only need confidence scoring.
- You have targeted quantitative data and are not interested in untargeted family discovery.
- Spectra are from liquid chromatography–mass spectrometry (LC-MS); this skill is optimized for GC-MS data where chromatographic peak overlap and co-elution are dominant challenges.

## Inputs

- Deconvolved GC-MS spectra in MGF (Mascot Generic Format) or mzTab format
- GC-MS raw data (NetCDF or vendor format) pre-processed by MSHub auto-deconvolution

## Outputs

- Molecular network graph (nodes = spectra/compounds, edges = cosine similarity scores)
- Network visualization (graphML, .cytoscape, or interactive HTML)
- Spectral cluster assignments and metadata tables

## How to apply

Export deconvolved spectra from MSHub in a GNPS-compatible format (MGF or mzTab). Upload the spectra to GNPS and configure the molecular networking workflow with cosine similarity as the clustering metric and default or published parameters (e.g., parent mass tolerance, minimum matched peaks). The workflow clusters spectra into nodes and draws edges weighted by cosine similarity scores between pairs, constructing a network graph where connected nodes represent chemically similar or related compounds. Compare the resulting network topology (node degree, connected components, hub structures) to published reference networks or biological expectations to validate that the deconvolution and clustering captured meaningful chemical relationships.

## Related tools

- **MSHub** (Performs automated deconvolution of overlapping chromatographic peaks to extract individual compound spectra from GC-MS raw data)
- **GNPS** (Hosts the molecular networking workflow that clusters deconvolved spectra by cosine similarity and constructs the network graph) — https://gnps.ucsd.edu/

## Evaluation signals

- Network contains connected components (clusters) with cosine similarity edges ≥ reported threshold (typically > 0.7 for GC-MS spectra).
- Node count and edge count match expected scale from the deconvolved spectrum dataset (e.g., 100s to 1000s of spectra should yield corresponding nodes).
- Network topology visually reproduces the published reference network in node degree distribution, hub structure, and cluster cohesion.
- Hub nodes (high-degree spectra) correspond to known common metabolites or contamination patterns expected in the sample matrix.
- Isolated nodes (degree 0) are rare; if abundant, re-examine deconvolution or cosine similarity thresholds.

## Limitations

- Cosine similarity clustering does not inherently assign compound identity; annotation requires orthogonal library matching or manual curation.
- Network topology is sensitive to the choice of parent mass tolerance and minimum matched peaks parameters; published parameters should be reported and justified.
- GC-MS data with very high background noise or extensive peak overlap may yield over-fragmented or under-connected networks despite deconvolution.
- Molecular networks are descriptive, not quantitative; they visualize presence and relationship but not abundance or statistical significance.

## Evidence

- [other] Apply MSHub auto-deconvolution algorithm to extract individual compound spectra from overlapping chromatographic peaks.: "Apply MSHub auto-deconvolution algorithm to extract individual compound spectra from overlapping chromatographic peaks."
- [other] Export deconvolved spectra in a format compatible with GNPS (e.g., MGF or mzTab).: "Export deconvolved spectra in a format compatible with GNPS (e.g., MGF or mzTab)."
- [other] Upload deconvolved spectra to GNPS and execute molecular networking workflow with default or reported parameters to cluster spectra by cosine similarity and construct the network graph.: "Upload deconvolved spectra to GNPS and execute molecular networking workflow with default or reported parameters to cluster spectra by cosine similarity and construct the network graph."
- [other] Retrieve and visualize the resulting molecular network (nodes = spectra/compounds, edges = similarity scores) and compare topology to the published network.: "Retrieve and visualize the resulting molecular network (nodes = spectra/compounds, edges = similarity scores) and compare topology to the published network."
- [intro] Auto-deconvolution and molecular networking methods for gas chromatography–mass spectrometry data analysis: "Development of auto-deconvolution and molecular networking methods for gas chromatography–mass spectrometry data analysis"
