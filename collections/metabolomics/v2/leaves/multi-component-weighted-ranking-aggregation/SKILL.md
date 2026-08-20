---
name: multi-component-weighted-ranking-aggregation
description: Use when you have completed LC–MS/MS feature detection and annotation
  (via MZmine2/3 and GNPS/SIRIUS/CANOPUS), have compiled a taxonomically annotated
  metadata table, and need to rank extracts by their likelihood of containing novel
  chemistry.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3927
  edam_topics:
  - http://edamontology.org/topic_0121
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_0625
  tools:
  - MZmine2
  - MZmine3
  - timaR
  - CANOPUS
  - MEMO
  - GNPS
  - SIRIUS
  - Lotus Database
  - Inventa
  techniques:
  - LC-MS
  license_tier: open
  provenance_tier: literature
derived_from:
- doi: 10.3389/fmolb.2022.1028334
  title: Inventa
- doi: 10.1038/s41467-021-23953-9
  title: ''
evidence_spans:
- MZmine output format using only the 'Peak area', 'row m/z' and 'row retention time'
  columns. -Inventa takes input directly from MZmine2
- Inventa takes input directly from MZmine2 or MZmine 3
- -Inventa takes input directly from MZmine2 or [MZmine 3](http://mzmine.github.io/),
  is possible to use other processing sofwares
- 'tima_results_filename: timaR reponderated output format. - for performing in silico
  annotations and taxonomically informed reponderation.'
- 'tima_results_filename: timaR reponderated output format'
- 'Class Component (CC): a score considering the presence of predicted known chemical
  classes new to the species'
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_inventa_cq
    doi: 10.3389/fmolb.2022.1028334
    title: Inventa
  dedup_kept_from: coll_inventa_cq
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.3389/fmolb.2022.1028334
  all_source_dois:
  - 10.3389/fmolb.2022.1028334
  - 10.1038/s41467-021-23953-9
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# multi-component-weighted-ranking-aggregation

## Summary

Combines four independent discovery-potential scores (Feature, Literature, Class, and Similarity components) into a single Priority Rank using user-defined weights to identify structurally novel natural product extracts. This skill prioritizes samples for follow-up chemistry based on their combination of annotation sparsity, taxonomic novelty, unreported chemistry classes, and spectral uniqueness.

## When to use

Apply this skill when you have completed LC–MS/MS feature detection and annotation (via MZmine2/3 and GNPS/SIRIUS/CANOPUS), have compiled a taxonomically annotated metadata table, and need to rank extracts by their likelihood of containing novel chemistry. Use this especially when pursuing high-throughput discovery workflows where computational prioritization must replace manual curation.

## When NOT to use

- Input is a single extract or fewer than 3 samples—the Similarity Component requires comparative context and outlier detection algorithms perform poorly on tiny cohorts.
- Feature annotations are already exhaustively assigned or metadata is taxonomically sparse or unvalidated—the Literature Component depends on clean species/genus names (e.g., from Open Tree of Life) and FC relies on annotation sparsity as a signal.
- MS2 spectral data are missing or uniform across all samples—the Similarity Component and Class Component both depend on discriminative MS2 information and chemical class variability.

## Inputs

- MZmine2/MZmine3 feature quantification table (Peak area, row m/z, row retention time columns)
- GNPS metadata table (GNPS format with mandatory ATTRIBUTE_Species and ATTRIBUTE_Organe columns)
- GNPS molecular networking job ID
- timaR reponderated annotation results (optional)
- SIRIUS compound_identification.tsv (optional)
- CANOPUS npc_summary.tsv output
- MEMO vectorized dissimilarity matrix (optional)
- Lotus Database entries for taxonomic reference

## Outputs

- TSV table with per-sample scores for Feature Component, Literature Component, Class Component, Similarity Component, and final Priority Rank
- Ranked list of extracts by Priority Rank for downstream screening

## How to apply

First, compute each of the four components independently: (1) Feature Component (FC) as the ratio of specific non-annotated features (≥90% specificity threshold) to total features per sample; (2) Literature Component (LC) from 1.0 minus fractions of reported compounds at species/genus/family levels using thresholds max_comp_reported_sp=20, max_comp_reported_g=50, max_comp_reported_f=500; (3) Class Component (CC) by detecting unreported CANOPUS chemical classes in each extract compared to Lotus Database entries for the species and genus, with min_class_confidence=0.8 and min_recurrence=5; (4) Similarity Component (SC) using MEMO dissimilarity matrix and machine-learning-based outlier detection to assign binary scores (1 for outliers, 0 otherwise) based on MS2 spectral peaks and neutral losses. Then compute Priority Rank as PR = (w1×FC) + (w2×LC) + (w3×CC) + (w4×SC) with user-defined modulating weights (default w1=w2=w3=w4=1). The rationale is that each component measures novelty along a different axis (annotation rarity, taxonomic documentation, chemistry class novelty, and spectral dissimilarity), and their weighted sum balances these complementary signals.

## Related tools

- **MZmine2** (Provides feature detection and quantification table (Peak area, m/z, retention time) as primary input to component calculation)
- **MZmine3** (Alternative to MZmine2 for feature detection and quantification; Inventa accepts both formats directly)
- **GNPS** (Provides molecular networking and spectral library matching results; used to obtain GNPS job ID and metadata format)
- **SIRIUS** (Generates compound identification and confidence scores (ZodiacScore, ConfidenceScore) filtered by min_ZodiacScore=0.9 for annotation cleaning in FC)
- **CANOPUS** (Detects chemical classes (NPClassifyre ontology) used to compute Class Component by comparing unreported classes at species/genus level) — https://github.com/kaibioinfo/canopus_treemap
- **timaR** (Performs taxonomically informed annotation reponderation; optional input to annotate features for FC filtering by ppm_error=5, shared_peaks=10, cosine=0.7)
- **MEMO** (Generates vectorized dissimilarity matrix based on MS2 peaks and neutral losses; input to machine-learning outlier detection for Similarity Component) — https://github.com/mandelbrot-project/memo
- **Lotus Database** (Provides reference compound lists at species, genus, and family levels for Literature Component calculation and Class Component comparison)
- **Inventa** (Core implementation that orchestrates all four component calculations, weighting, and Priority Rank aggregation) — https://github.com/luigiquiros/inventa

## Examples

```
# Set parameters in Inventa notebook: w1=1; w2=1; w3=1; w4=1; min_specificity=90; max_comp_reported_sp=20; min_class_confidence=0.8; ppm_error=5; cosine=0.7. Then run the configured notebook to output a TSV table with per-sample FC, LC, CC, SC, and final Priority Rank.
```

## Evaluation signals

- Each sample has all four component scores (FC, LC, CC, SC) computed and present in output table with no null ranks.
- Priority Rank equals the sum of weighted components: verify PR = (w1×FC) + (w2×LC) + (w3×CC) + (w4×SC) for each row.
- Component values fall within expected ranges: FC ∈ [0, 1] (ratio), LC ∈ [0, 1] (1-sum of fractions), CC ∈ [0, 1] (0.5 per novel class level), SC ∈ [0, 1] (binary outlier score).
- When annotation counts are increased (fewer filtered-out SIRIUS/ISDB entries), FC decreases; when compounds reported for a taxon increase, LC decreases.
- Samples flagged as MS2 spectral outliers by MEMO machine learning algorithms receive SC=1; non-outliers receive SC=0.

## Limitations

- Literature Component accuracy depends on completeness and curation quality of Lotus Database and user-supplied taxonomic names; uncleaned or misidentified species names will inflate LC scores artificially.
- Feature Component specificity threshold (90%) is a fixed cutoff; features with borderline specificity (85–90%) may be misclassified, and this threshold may not transfer across different extract cohorts or organisms.
- Class Component requires CANOPUS predictions with min_class_confidence=0.8, which may be stringent for some chemical classes and may miss weak signals from structurally ambiguous compounds; comparison depends on accurate species/genus annotation in CANOPUS outputs and Lotus Database.
- Similarity Component performs outlier detection via machine learning on MEMO dissimilarity matrix; results may be unstable with very small cohorts (<3 samples) and depend on the quality of MS2 spectral data and absence of batch effects (e.g., different LC methods, ionization modes).
- No changelog exists for Inventa versions; reproducibility may require version pinning and complete documentation of all parameter choices (w1, w2, w3, w4, thresholds).

## Evidence

- [methods] The Priority Score (PS) is the addition of the four components. A modulating factor (wn) gives each component a relative weight according to the user's preferences.: "The Priority Score (PS) is the addition of the four components. A modulating factor (wn) gives each component a relative weight according to the user's preferences."
- [methods] The Feature Component (FC) is a ratio of the number of specific non-annotated features over the total number of features of each extract.: "The Feature Component (FC) is a ratio of the number of specific non-annotated features over the total number of features of each extract."
- [methods] The Literature Component (LC) is a score based on the number of compounds reported in the literature for the taxon of a given extract. It is independent of the spectral data.: "The Literature Component (LC) is a score based on the number of compounds reported in the literature for the taxon of a given extract. It is independent of the spectral data."
- [methods] The Class Component (CC) indicates if an unreported CANOPUS chemical class is detected in a given extract compared to those reported in the species and the genus.: "The Class Component (CC) indicates if an unreported CANOPUS chemical class is detected in a given extract compared to those reported in the species and the genus."
- [methods] The Similarity Component (SC) is a complementary score that compares extracts based on their general MS2 spectral information independently from the feature alignment used in FC, using the MEMO: "The Similarity Component (SC) is a complementary score that compares extracts based on their general MS2 spectral information independently from the feature alignment used in FC, using the MEMO"
- [other] Compute Priority Rank (PR) as sum of all four components (FC + LC + CC + SC), applying user-defined modulating weights (w1=1 for FC, w2=1 for LC, w3=1 for SC, w4=1 for CC).: "Compute Priority Rank (PR) as sum of all four components (FC + LC + CC + SC), applying user-defined modulating weights (w1=1 for FC, w2=1 for LC, w3=1 for SC, w4=1 for CC)."
- [readme] The rank comes from the addition of four individual components: "The rank comes from the addition of four individual components"
- [readme] Inventa calculates multiple scores that estimate the structural novelty potential of the natural extracts. It has the potential to accelerate the discovery of new natural products.: "Inventa calculates multiple scores that estimate the structural novelty potential of the natural extracts. It has the potential to accelerate the discovery of new natural products."
