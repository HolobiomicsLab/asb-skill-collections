---
name: metabolite-set-annotation-mapping
description: Use when you have a metabolomics peak intensity matrix with feature IDs
  (m/z, retention time, or arbitrary peak identifiers) and need to assign these peaks
  to standardized metabolite databases or spectral groupings (KEGG compounds, ChEBI
  IDs, GNPS Molecular Families, or MS2LDA Mass2Motifs) before.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3280
  edam_topics:
  - http://edamontology.org/topic_0769
  - http://edamontology.org/topic_3172
  - http://edamontology.org/topic_0091
  tools:
  - PALS Viewer
  - GNPS
  - MS2LDA
  - PALS (Pathway Activity Level Scoring)
  - GNPS (Global Natural Products Social Molecular Networking)
  techniques:
  - LC-MS
  license_tier: open
derived_from:
- doi: 10.3390/metabo11020103
  title: pals
evidence_spans:
- To access our interactive Web application PALS Viewer, please visit [https://pals.glasgowcompbio.org/app/]
- Molecular Families from GNPS
- This includes in particular *Molecular Families* from [GNPS](http://gnps.ucsd.edu/)
- Mass2Motifs from MS2LDA
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_pals_cq
    doi: 10.3390/metabo11020103
    title: pals
  dedup_kept_from: coll_pals_cq
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.3390/metabo11020103
  all_source_dois:
  - 10.3390/metabo11020103
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# metabolite-set-annotation-mapping

## Summary

Map individual metabolite features (peaks) to standardized metabolite set identifiers (KEGG, ChEBI, GNPS Molecular Families, MS2LDA Mass2Motifs) to enable downstream pathway or metabolite-group activity scoring. This annotation layer converts low-level mass spectrometry peak data into biologically meaningful metabolite groupings required for set-level analysis.

## When to use

You have a metabolomics peak intensity matrix with feature IDs (m/z, retention time, or arbitrary peak identifiers) and need to assign these peaks to standardized metabolite databases or spectral groupings (KEGG compounds, ChEBI IDs, GNPS Molecular Families, or MS2LDA Mass2Motifs) before performing pathway-level or metabolite-set activity scoring. This is the prerequisite step whenever you intend to run PALS or similar set-level decomposition methods.

## When NOT to use

- Peak intensity matrix already contains pre-aggregated pathway or set-level intensities (input is already set-level, not feature-level).
- No standardized metabolite identifiers available for your peaks (e.g., only m/z values with no database cross-reference); consider de novo motif discovery (MS2LDA) instead.
- Annotation workflow is incompatible with your metabolite database schema (e.g., proprietary or non-standard identifiers not supported by PALS or GNPS/MS2LDA).

## Inputs

- Peak intensity matrix (CSV: peak_id × sample_intensities)
- Peak annotation matrix (CSV: peak_id → metabolite_identifier [KEGG, ChEBI, GNPS_family, MS2LDA_motif])
- Metabolite set definitions (pathways, Molecular Families, or Mass2Motifs from external database)

## Outputs

- Annotated feature-to-metabolite mapping table (peak_id → set_member_id)
- Filtered intensity matrix (only annotated peaks retained)
- Set membership matrix (metabolite_set × sample_intensities, aggregated from constituent peaks)

## How to apply

Prepare two input matrices: (1) an intensity CSV with peak feature IDs as rows and sample intensities as columns, and (2) an annotation CSV mapping each peak ID to one or more metabolite identifiers (KEGG ID, ChEBI ID, or spectral family ID). Handle many-to-many relationships: a single peak may map to multiple compound IDs (due to identification uncertainty), and a single compound may be represented by multiple peaks. Use PALS or compatible tools to ingest both matrices and align peaks to metabolite set definitions (pathway members, Molecular Family members, or Mass2Motif clusters). Validate that annotated peaks are present in both the intensity and annotation matrices; peaks with no annotation will be excluded from downstream set-level analysis.

## Related tools

- **PALS (Pathway Activity Level Scoring)** (Accepts annotated intensity and annotation matrices; performs database queries and alignment of peaks to pathway/set members) — https://github.com/glasgowcompbio/PALS
- **GNPS (Global Natural Products Social Molecular Networking)** (Provides Molecular Family groupings that can be used as alternative metabolite sets for annotation mapping) — http://gnps.ucsd.edu/
- **MS2LDA** (Provides Mass2Motifs spectral groupings as alternative metabolite set definitions for annotation) — http://ms2lda.org/
- **PALS Viewer** (Web interface for loading and validating annotated matrices; prioritizes Molecular Families and Mass2Motifs by activity score) — https://pals.glasgowcompbio.org/app/

## Examples

```
from pals.common import *; int_df = pd.read_csv('intensity.csv', index_col=0); annotation_df = pd.read_csv('annotation.csv', index_col=0); ds = DataSource(int_df, annotation_df, experimental_design, database_name='COMPOUND', min_replace=5000)
```

## Evaluation signals

- Proportion of peaks with successful annotation: annotated peaks / total peaks should be >50% (context-dependent); low annotation rate suggests incomplete database cross-reference or poor peak identification quality.
- Many-to-many mapping statistics: verify that multiplicity (peaks per compound, compounds per peak) is documented and reasonable for your MS platform and annotation confidence.
- Data completeness: all samples in the intensity matrix are represented in the annotation matrix; no peaks with valid intensities are silently dropped.
- Metabolite set coverage: for each metabolite set (pathway, Molecular Family, or Mass2Motif), verify that ≥1 annotated peak is mapped to it; sets with zero members should be flagged or excluded.
- Reproducibility of mapping: re-running the annotation workflow with identical inputs produces identical output; no stochastic tie-breaking or non-deterministic ordering of many-to-many mappings.

## Limitations

- Peak identification uncertainty leads to many-to-many mappings; multiplicity must be retained, not collapsed, to avoid information loss in downstream set-level analysis.
- Annotation completeness depends on the chosen metabolite database (KEGG, ChEBI, GNPS, MS2LDA); rare, novel, or unannotated metabolites will be excluded from set-level analysis.
- PALS and MS2LDA assume metabolite sets are predefined externally; no de novo peak grouping is performed during annotation mapping; if no suitable spectral grouping exists, consider first running MS2LDA to generate Mass2Motifs.
- Database version and ID cross-reference consistency: KEGG IDs, ChEBI IDs, and GNPS Family IDs may drift over time; reproducibility requires explicit versioning or snapshot dating of the annotation tables.

## Evidence

- [readme] In addition, users also provide a list of compound annotations assigned to peak features (peaks that do not have annotations will not be used for pathway analysis).: "users also provide a list of compound annotations assigned to peak features (peaks that do not have annotations will not be used for pathway analysis)"
- [readme] As a result of the uncertainty in peak identification, multiple peak IDs may be mapped to multiple compound IDs and vice versa.: "As a result of the uncertainty in peak identification, multiple peak IDs may be mapped to multiple compound IDs and vice versa"
- [readme] The first column (or DataFrame index) is the peak ID while the second column is the assigned metabolite annotation as either KEGG or ChEBI database IDs.: "The first column (or DataFrame index) is the peak ID while the second column is the assigned metabolite annotation as either KEGG or ChEBI database IDs"
- [intro] the decomposition approach in PALS is amenable to the analysis of any group of metabolite sets, not just pathways: "the decomposition approach in PALS is amenable to the analysis of any group of metabolite sets, not just pathways"
- [readme] metabolite sets obtained from the grouping of metabolites according to their fragmentation spectra can also be analysed. This includes in particular Molecular Families from GNPS, as well as Mass2Motifs from MS2LDA.: "metabolite sets obtained from the grouping of metabolites according to their fragmentation spectra can also be analysed. This includes in particular Molecular Families from GNPS, as well as"
