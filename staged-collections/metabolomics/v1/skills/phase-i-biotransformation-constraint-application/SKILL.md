---
name: phase-i-biotransformation-constraint-application
description: Use when filtering putative metabolite features in LC-HRMS metabolomics by enforcing biochemical mass-shift constraints for phase-I oxidative transformations (reduction, oxidation, hydrolysis, dehydration) to discriminate true phase-I metabolites from phase-II conjugation artifacts.
when_to_use_negative:
- Input features are already restricted to known phase-I metabolites (e.g., pre-curated reference standards).
- The parent pesticide ionization state is ambiguous or multiple adducts ([M+H]+, [M+Na]+, etc.) are present without mode-specific labeling.
- The study explicitly includes phase-II metabolites (glucuronides, sulfates) as targets; in this case, increase the upper mass-defect cutoff or apply a separate phase-II constraint (e.g., +176 u for glucuronidation).
edam_operation: http://edamontology.org/operation_3695
edam_topics:
- http://edamontology.org/topic_0153
- http://edamontology.org/topic_3172
tools:
- name: incubatoR
  role: R workflow that implements mass-difference filtering in metabolites.R script as step 3, calculating and removing features with m/z > +50 u relative to parent pesticide
  repo: https://github.com/chufz/incubatoR
- name: XCMS
  role: Feature detection and alignment prior to mass-difference filtering; provides m/z and retention-time coordinates
- name: CAMERA
  role: Isotope and adduct annotation; used to componentize features before mass-difference filtering to reduce false positives
- name: R v3.6.1
  role: Scripting environment for implementing mass-difference calculations and filtering logic
provenance:
  source_task_ids:
  - task_003
  source_papers:
  - doi: 10.1021/acs.analchem.1c00972
    title: Improving the Screening Analysis of Pesticide Metabolites in Human Biomonitoring by Combining High-Throughput <i>In Vitro</i> Incubation and Automated LC–HRMS Data Processing
schema_version: 0.2.0
metadata:
  merge_audit:
    n_source_runs: 2
    source_files:
    - outputs/pesticide_full_2026-05-10_v2/skills/phase-i-biotransformation-constraint-application/SKILL.md
    - outputs/pesticide_full_2026-05-10_v2/skills/phase-i-biotransformation-constraint-application/skill.md
    merged_at: '2026-05-25T06:57:01.622286+00:00'
    merge_kind: slug_match_union
  iri: https://w3id.org/holobiomicslab/asb-skill/phase-i-biotransformation-constraint-application@sha256:75f94f4c8dffc210e6d6d6d2c0485093cbd39c3a79bcd1ad7caf8a5503c56717
derived_from:
- doi: 10.1021/acs.analchem.1c00972
---

# Phase-I-biotransformation-constraint-application

## Summary

This skill applies biochemical constraints to filter putative metabolite features in LC–HRMS data by removing signals with mass shifts inconsistent with phase-I oxidative transformations (reduction, oxidation, hydrolysis, dehydration). It distinguishes true phase-I metabolites from artifacts of phase-II conjugation or instrumental noise by enforcing strict bounds on mass difference relative to the parent pesticide m/z.

## When to use

Apply this skill after abundance-filtering and blank-subtraction have reduced the feature table, but before molecular formula assignment. Specifically, when you have a list of detected features (each with m/z, retention time, and fold-change metrics) and a known parent pesticide [M+H]+ or [M−H]− ion, and you wish to exclude features whose structure would require phase-II conjugation (e.g., glucuronidation, sulfation) or are otherwise implausible as direct phase-I products.

## When NOT to use

- Input features are already restricted to known phase-I metabolites (e.g., pre-curated reference standards).
- The parent pesticide ionization state is ambiguous or multiple adducts ([M+H]+, [M+Na]+, etc.) are present without mode-specific labeling.
- The study explicitly includes phase-II metabolites (glucuronides, sulfates) as targets; in this case, increase the upper mass-defect cutoff or apply a separate phase-II constraint (e.g., +176 u for glucuronidation).

## Inputs

- Feature table (m/z, retention time, fold-change, replicates) after abundance filtering (fold-change > 4, detected in ≥2 of 3 replicates) and blank subtraction
- Parent pesticide m/z (e.g., [M+H]+ in ESI+ mode)
- Ionization mode (ESI+ or ESI−) for each sample set

## Outputs

- Filtered feature table containing only features with Δm/z ≤ +50 u relative to parent pesticide
- List of removed features and their mass differences (for diagnostic inspection)
- Diagnostic plots showing m/z and mass-defect distribution before and after filtering

## How to apply

First, compute the nominal mass difference (Δm/z) between each feature's m/z and the parent pesticide's [M+H]+ or [M−H]− ion m/z in the same ionization mode. Remove all features with Δm/z > +50 u, as these correspond to addition of more than three oxygen atoms and are more likely to arise from phase-II conjugation (e.g., glucuronidation, +176 u) rather than phase-I oxidation, reduction, or hydrolysis. Optionally, also apply a lower mass-defect threshold (e.g., −100 mmu) to exclude features with implausibly low mass (e.g., large fragments or instrumental artifacts). Document the number of features retained before and after this filter, and inspect EICs and MS/MS spectra of borderline features manually to validate the filter cutoff. The rationale is that phase-I metabolism is catalyzed by cytochrome P450 and related enzymes and operates primarily through addition or removal of oxygen, hydrogen, or small functional groups; additions exceeding +50 u signal subsequent conjugation or non-enzymatic reactions.

## Related tools

- **incubatoR** (R workflow that implements mass-difference filtering in metabolites.R script as step 3, calculating and removing features with m/z > +50 u relative to parent pesticide) — https://github.com/chufz/incubatoR
- **XCMS** (Feature detection and alignment prior to mass-difference filtering; provides m/z and retention-time coordinates)
- **CAMERA** (Isotope and adduct annotation; used to componentize features before mass-difference filtering to reduce false positives)
- **R v3.6.1** (Scripting environment for implementing mass-difference calculations and filtering logic)

## Evaluation signals

- Feature retention count: verify that ~60% or fewer features remain after combined blank subtraction and mass-difference filtering, consistent with the article's observation that blank/isotope/adduct removal reduces peaks by ~60%.
- Mass-difference distribution histogram: confirm that no features with Δm/z > +50 u are present in the output; plot m/z difference vs. intensity to identify any borderline features near the +50 u threshold.
- Comparison to literature and BioTransformer predictions: verify that ≥60% of retained features correspond to known phase-I metabolites (oxidation, hydroxylation, dehydrogenation) reported in EFSA dossiers or predicted by rule-based phase-I models; absence of obvious phase-II signatures (e.g., glucuronidated ions at [M+176]+) in the filtered list.
- EIC and MS/MS quality: spot-check 5–10 retained features to confirm that their extracted-ion chromatograms are clean (no baseline noise) and MS/MS spectra show fragmentation consistent with phase-I products (e.g., loss of H₂O, CO, or functional groups, not mass additions > +16 u).
- Replicate consistency: verify that retained features are detected consistently across ≥2 of 3 replicates (already enforced by upstream abundance filter) and show fold-change > 4 relative to blanks and reference standard.

## Limitations

- Mass-difference threshold (+50 u) is empirical and generic; it may be overly strict for phase-I metabolites involving sequential hydroxylations (+16 u each) or overly permissive for conjugations just below the cutoff (e.g., sulfation, +80 u in some cases).
- The filter assumes phase-I is the primary pathway of interest; if phase-II metabolites (glucuronides, sulfates) are biomarkers of exposure, they will be discarded and must be detected via separate workflows (e.g., incubation with glucuronidase/sulfatase, or prior deconjugation).
- Some in vitro metabolites may not be detected at all due to low ionization efficiency, sample loss during extraction, or incomplete enzymatic turnover (e.g., only 3 of 12 registered mammalian metabolites of metazachlor were observed in the assay); mass-difference filtering cannot recover these.
- The article notes that BioTransformer does not predict all phase-I reactions (e.g., reduction, consecutive hydroxylations, weak bond cleavage); hence, some true phase-I metabolites may remain after filtering if they have unusual structural rearrangements.
- Ionization-mode cross-talk: if ESI+ and ESI− data are mixed without proper sample-set labeling, the parent m/z and thus the mass-difference calculation may be incorrect; always verify that samples are segregated by polarity.

## Evidence

- [methods] abundance-filter-fold-change: "We used a generic cutoff value of >4 for the fold change and kept only the features that were detected in at least two of three replicates"
- [methods] mass-difference-threshold-and-rationale: "all features with a mass difference higher than +50 u to the parent compound, corresponding to an addition of three O atoms, were also not further evaluated"
- [discussion] phase-I-vs-conjugation-distinction: "Features with an m/z value >+50 mu to the parent pesticide were removed since they are more likely to occur from conjugation"
- [readme] workflow-step-filtering-order: "Filtering of non-metabolic features by several cut-off values and plotting for manual evaluation by `Rscripts/metabolites.R`"
- [discussion] in-vitro-incubation-metabolite-coverage: "A comparison with the literature data and metabolization prediction showed that the S9 incubation does not cover all potential or existing metabolites."
- [discussion] incomplete-metabolite-detection-example: "For metazachlor, 12 mammalian metabolites are described in the registration dossier, but we only observed three in the incubation experiment."
