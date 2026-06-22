---
name: metabolomic-heatmap-visualization
description: Use when after completing feature annotation and reaction assignment in an untargeted metabolomics workflow, specifically when you have a feature-by-sample intensity matrix aligned with metabolite identities and want to communicate cluster structure, reaction pathway groupings, and feature.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_0571
  edam_topics:
  - http://edamontology.org/topic_0121
  - http://edamontology.org/topic_3172
  tools:
  - tidyverse
  - CluMSID
  - CluMSIDdata
  - grid
  - OrgMassSpecR
  - pheatmap
  - reshape2
  - MSMSsim
  - msentropy
  - readxl
  techniques:
  - tandem-MS
derived_from:
- doi: 10.1021/acs.est.5c08558
  title: CMDN
evidence_spans:
- tidyverse
- CluMSID
- CluMSIDdata
- grid
- OrgMassSpecR
- pheatmap
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_cmdn_cq
    doi: 10.1021/acs.est.5c08558
    title: CMDN
  dedup_kept_from: coll_cmdn_cq
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1021/acs.est.5c08558
  all_source_dois:
  - 10.1021/acs.est.5c08558
  zenodo_doi: TODO-zenodo
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# metabolomic-heatmap-visualization

## Summary

Visualization of annotated metabolomic feature clusters and their reaction pathway assignments using hierarchical heatmaps. This skill transforms aligned MS features and xenobiotic metabolite annotations into publication-ready cluster dendrograms that reveal co-fragmentation patterns and reaction relationships.

## When to use

Apply this skill after completing feature annotation and reaction assignment in an untargeted metabolomics workflow, specifically when you have a feature-by-sample intensity matrix aligned with metabolite identities and want to communicate cluster structure, reaction pathway groupings, and feature co-occurrence patterns to stakeholders or in manuscripts.

## When NOT to use

- Feature annotation and reaction assignment have not yet been completed — visualization will be uninformative without metabolite identity and pathway metadata.
- Input is a single unannotated feature (no clustering structure to visualize).
- Sample size or feature count is so large (>10,000 features) that heatmap labels and dendrograms become illegible; consider aggregation by reaction pathway or sub-setting by statistical significance instead.

## Inputs

- aligned feature intensity matrix (rows: features, columns: samples)
- feature annotation table with metabolite identities and reaction pathway assignments
- sample metadata (grouping, treatment, or timepoint information)
- cluster assignments from CluMSID analysis

## Outputs

- hierarchical heatmap (PNG or PDF) with feature dendrograms and reaction pathway annotations
- publication-ready multi-panel figure with grid-based layout
- annotated feature cluster visualization showing xenobiotic reaction relationships

## How to apply

After CluMSID-based feature clustering and OrgMassSpecR annotation propagation produce aligned features with reaction metadata, reshape the feature intensity matrix using reshape2 to long format, preserving metabolite identity and reaction pathway annotations as row and column metadata. Pass the reshaped matrix and metadata to pheatmap with grid layout configuration to render a clustered heatmap with hierarchical dendrograms on both axes. Use color scaling to represent normalized feature intensities, and annotate row clusters with reaction pathway labels and column clusters with sample groupings. The pheatmap output is then integrated with grid graphics to compose multi-panel layouts for publication, where dendrograms reveal co-fragmented feature groups and color annotations highlight xenobiotic reaction clusters.

## Related tools

- **pheatmap** (renders hierarchical clustered heatmap with dendrograms and metadata annotations for feature intensity matrices)
- **reshape2** (transforms feature intensity matrix from wide to long format and restructures metadata for pheatmap consumption)
- **grid** (composes multi-panel publication layouts combining pheatmap outputs with pathway annotations and sample groupings)
- **CluMSID** (upstream clustering and feature alignment that produces the cluster assignments visualized in the heatmap)
- **OrgMassSpecR** (upstream tool providing exact mass annotation that annotates heatmap rows with metabolite identities and reaction labels)

## Examples

```
# After reshape2::melt of feature matrix, pheatmap(feature_matrix_long, annotation_row = metabolite_annotations, annotation_colors = reaction_colors, main = 'Xenobiotic Metabolite Clusters') followed by grid::grid.arrange() to compose with pathway legends
```

## Evaluation signals

- Heatmap dendrograms on both axes are present and interpretable; feature clusters with similar fragmentation/metabolite identity group together visually.
- Row and column annotations are correctly mapped: reaction pathways label feature clusters, and sample groupings or treatment labels appear on columns without missing or transposed assignments.
- Color gradient (intensity scale) is monotonic and spans the dynamic range of normalized feature intensities; no saturated or clipped regions.
- Grid layout composes multiple heatmap panels without overlapping legends, labels, or dendrograms; text is legible at publication resolution (≥300 dpi).
- Feature count and sample count match input dimensions; no rows or columns are dropped during reshape or pheatmap rendering.

## Limitations

- Heatmap legibility degrades with >1000 features or >100 samples; practitioners must aggregate (e.g., by reaction pathway or statistical significance) or create sub-set heatmaps.
- pheatmap clustering distance metric and linkage method (default: Euclidean + complete linkage) may not reflect xenobiotic reaction chemistry; user must validate that visual cluster structure aligns with known metabolic transformations.
- Metadata annotation in pheatmap relies on exact row/column name matching; mismatches between feature IDs in intensity matrix and annotation table result in silent failure (missing or misaligned colors).
- Grid-based multi-panel composition requires manual tuning of layout parameters (margins, spacing, font sizes) for different figure sizes and panel counts; no automated responsive layout.
- Color palettes (default viridis) may not meet color-blind accessibility standards; user must select and specify palettes explicitly (e.g., via pheatmap color arguments).

## Evidence

- [intro] Visualize annotated feature clusters and reaction assignments using pheatmap and grid: "Visualize annotated feature clusters and reaction assignments using pheatmap and grid, reshaping output with reshape2."
- [readme] CMDN is a top-down untargeted metabolomics MS data processing framework for high-throughput annotation of reaction-derived xenobiotic metabolites: "Compound metabolite discovery network (CMDN) is an "top-down" untargeted metabolomics-based MS data processing framework to enable high-throughput and automated annotation of reaction-derived"
- [intro] CluMSID performs feature detection and alignment with clustering: "Perform feature detection and alignment using CluMSID with default clustering parameters."
- [intro] OrgMassSpecR and CluMSID enable metabolite annotation by matching to xenobiotic databases: "Annotate metabolites by matching aligned features to xenobiotic reaction databases using OrgMassSpecR for exact mass calculation and CluMSID for cluster-based annotation propagation."
