---
name: reaction-pathway-assignment-and-propagation
description: Use when you have detected and clustered unknown MS features from untargeted xenobiotic metabolomics data, computed fragmentation pattern similarity scores between features and reference spectra, and now need to systematically assign individual features to specific biotransformation reactions (e.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3802
  edam_topics:
  - http://edamontology.org/topic_0718
  - http://edamontology.org/topic_3172
  - http://edamontology.org/topic_3520
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
  - Biotransformer 3.0
  - tidyverse, reshape2
  techniques:
  - CE-MS
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

# reaction-pathway-assignment-and-propagation

## Summary

A cluster-based annotation propagation strategy that assigns xenobiotic metabolites to known biotransformation reaction pathways by matching aligned MS features to reaction databases, then propagates those assignments across co-clustered unknown features. This skill enables high-throughput, automated linking of detected metabolites to their parent compound and reaction chemistry without individual spectral matching.

## When to use

You have detected and clustered unknown MS features from untargeted xenobiotic metabolomics data, computed fragmentation pattern similarity scores between features and reference spectra, and now need to systematically assign individual features to specific biotransformation reactions (e.g., Phase I oxidation, Phase II conjugation) and propagate those annotations to co-clustered features that likely represent related metabolites from the same pathway.

## When NOT to use

- Input features are not yet clustered or have not undergone fragmentation pattern similarity scoring — perform CluMSID clustering and MSMSsim matching first.
- Target compounds are endogenous metabolites without known biotransformation pathways — this skill is specific to xenobiotic and drug metabolism where reaction chemistry is well-characterized.
- Reaction database or biotransformer rules are unavailable or incompatible with your parent compound class — the skill depends on accurate reaction mass shifts and enzyme annotations.

## Inputs

- Aligned feature table with m/z, retention time, and intensity values
- Feature clusters (output from CluMSID feature clustering)
- MS/MS fragmentation spectra for unknown features
- Reference MS/MS spectra or fragmentation pattern similarity scores (MSMSsim output)
- Spectral entropy values for detected features (msentropy output)
- Xenobiotic reaction database or biotransformation rules (e.g., Biotransformer 3.0)
- Known parent compound or reference metabolite m/z values

## Outputs

- Annotated feature table with metabolite identities, reaction pathway assignments, and reaction type metadata
- Reaction pathway network or assignment matrix linking features to biotransformation reactions
- Confidence scores or annotations for propagated assignments
- Visualization of annotated feature clusters with reaction pathway labels (via pheatmap/grid)

## How to apply

After feature detection and alignment, use OrgMassSpecR to calculate exact mass differences between unknown features and known xenobiotic parent compounds or metabolite references to identify plausible biotransformation reactions. Cross-reference these mass shifts against a xenobiotic reaction database (e.g., Biotransformer 3.0 outputs) to assign specific reaction types. Use CluMSID's cluster-based annotation propagation to extend reaction assignments from confidently annotated features to other features within the same cluster, leveraging the assumption that co-clustered features share similar fragmentation patterns and therefore likely represent related metabolites. MSMSsim fragmentation similarity scores and msentropy spectral entropy values serve as confidence metrics to weight the propagation: features with high similarity and low entropy uncertainty receive higher confidence in their inherited annotations. Document the reaction pathway metadata (reaction type, mass shift, enzyme class if applicable) in the final feature table alongside metabolite identities.

## Related tools

- **CluMSID** (Performs feature clustering and cluster-based annotation propagation to extend reaction assignments from confidently annotated features to co-clustered unknowns)
- **OrgMassSpecR** (Calculates exact mass differences between features and parent compounds to identify plausible biotransformation mass shifts and match against reaction databases)
- **MSMSsim** (Computes fragmentation pattern similarity scores between unknown features and reference spectra to rank and filter reaction-pathway candidates before propagation)
- **msentropy** (Calculates spectral entropy to assess fragment complexity and provide confidence weighting for propagated annotations)
- **Biotransformer 3.0** (External biotransformation rule engine and xenobiotic reaction database for reference reaction types and mass shifts)
- **pheatmap** (Visualizes annotated feature clusters with reaction pathway metadata as heatmaps)
- **tidyverse, reshape2** (Data reshaping and manipulation to structure reaction assignment outputs and export final annotated feature tables)

## Evaluation signals

- Annotated features have non-null reaction pathway metadata (reaction type, mass shift) linked to a valid xenobiotic biotransformation rule
- Propagated annotations (features inherited from cluster mates) show consistent mass shift patterns relative to parent compound — i.e., features in the same cluster assigned to the same reaction type differ by background noise, not by distinct reaction masses
- Confidence scores or entropy values for propagated features are lower than or equal to those of the source feature — propagation does not artificially inflate confidence
- Cross-validation: high-confidence annotated features (high MSMSsim similarity, low msentropy) anchor the propagation; their downstream metabolites in the same cluster receive lower but systematic confidence penalties
- Final feature table passes schema validation: all rows contain m/z, reaction_type, parent_compound_id, and propagation_source (annotated_de_novo or propagated_from_feature_X)

## Limitations

- Cluster-based propagation assumes all co-clustered features are derived from the same parent via related reactions; false positives occur when clusters contain artifacts or unrelated isobars.
- Reaction database coverage and accuracy depend on Biotransformer version and curated xenobiotic chemistry; rare or novel biotransformations may not be detected.
- Fragmentation pattern similarity (MSMSsim) is an indirect proxy for structural relatedness; features with high similarity may still represent unrelated compounds if reference spectra are incomplete or poorly matched.
- The pipeline requires a priori knowledge of parent compound m/z values or reference metabolite spectra; it does not discover de novo reaction types or handle completely unknown parent structures.

## Evidence

- [intro] Annotate metabolites by matching aligned features to xenobiotic reaction databases using OrgMassSpecR for exact mass calculation and CluMSID for cluster-based annotation propagation.: "Annotate metabolites by matching aligned features to xenobiotic reaction databases using OrgMassSpecR for exact mass calculation and CluMSID for cluster-based annotation propagation"
- [readme] CMDN is a top-down untargeted metabolomics-based MS data processing framework to enable high-throughput and automated annotation of reaction-derived xenobiotic metabolites: "CMDN is an "top-down" untargeted metabolomics-based MS data processing framework to enable high-throughput and automated annotation of reaction-derived xenobiotic metabolites"
- [intro] Apply MSMSsim to compute fragmentation pattern similarity scores between unknown features and reference spectra. Calculate spectral entropy using msentropy to assess fragment complexity and confidence.: "Apply MSMSsim to compute fragmentation pattern similarity scores between unknown features and reference spectra. Calculate spectral entropy using msentropy to assess fragment complexity and confidence"
