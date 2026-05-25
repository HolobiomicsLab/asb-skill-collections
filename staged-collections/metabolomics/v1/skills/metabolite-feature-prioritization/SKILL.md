---
name: metabolite-feature-prioritization
description: Use when prioritizing pesticide metabolite features detected in LC–HRMS data by applying sequential statistical and chemical filters such as abundance fold-change, mass defect, mass difference, and blank subtraction to eliminate artifacts and non-metabolic peaks.
when_to_use_negative:
- Input is already a confirmed molecular structure or validated spectral library; this skill operates on unidentified features requiring prioritization.
- Studying conjugation metabolites or Phase II transformations where mass differences >+50 u are expected and legitimate (e.g., glucuronide, sulfate adducts).
- Working with direct biomonitoring samples without parallel in vitro incubation controls; blank and replicate structure are fundamental to the approach.
edam_operation: http://edamontology.org/operation_3695
edam_topics:
- http://edamontology.org/topic_0091
- http://edamontology.org/topic_3172
- http://edamontology.org/topic_3407
tools:
- name: XCMS
  role: Feature detection, alignment, and retention time correction upstream of prioritization
- name: CAMERA
  role: Componentization of isotope and adduct peaks prior to filtering
- name: incubatoR
  role: Integrated R workflow implementing all prioritization filters (abundance, mass defect, mass difference, blank subtraction) in sequence
  repo: https://github.com/chufz/incubatoR
- name: R
  role: Statistical comparison and filtering step execution (v3.6.1 in this implementation)
- name: ProteoWizard
  role: Upstream raw mass spectrum conversion to mzML and centroiding (v3.0.18265)
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
    - outputs/pesticide_full_2026-05-10_v2/skills/metabolite-feature-prioritization/SKILL.md
    - outputs/pesticide_full_2026-05-10_v2/skills/metabolite-feature-prioritization/skill.md
    merged_at: '2026-05-25T06:57:01.596612+00:00'
    merge_kind: slug_match_union
  iri: https://w3id.org/holobiomicslab/asb-skill/metabolite-feature-prioritization@sha256:7a4ccd30d9896b92987934ffe9031671672254b32d14182e056bf749d249307f
derived_from:
- doi: 10.1021/acs.analchem.1c00972
---

# metabolite-feature-prioritization

## Summary

Prioritize pesticide metabolite features detected in LC–HRMS data by applying sequential statistical and chemical filters (abundance fold-change, mass defect, mass difference, blank subtraction) to eliminate artifacts and non-metabolic peaks, reducing feature complexity while retaining true Phase I transformation products.

## When to use

Apply this skill after LC–HRMS feature detection and componentization (XCMS/CAMERA) when you have abundance-normalized peak tables for xenobiotic compounds incubated in vitro and need to identify which detected features are genuine metabolites rather than instrument artifacts, conjugation products, standard impurities, or isotope/adduct peaks.

## When NOT to use

- Input is already a confirmed molecular structure or validated spectral library; this skill operates on unidentified features requiring prioritization.
- Studying conjugation metabolites or Phase II transformations where mass differences >+50 u are expected and legitimate (e.g., glucuronide, sulfate adducts).
- Working with direct biomonitoring samples without parallel in vitro incubation controls; blank and replicate structure are fundamental to the approach.

## Inputs

- abundance-normalized LC–HRMS feature table (XCMS/CAMERA output as .tsv or .rds)
- parent pesticide m/z value ([M+H]+ or [M−H]− ion)
- retention time windows for parent compound
- replicate group labels (incubated vs. control samples)
- blank injection/sample preparation spectra

## Outputs

- prioritized metabolite feature table (mass@retention time identifiers)
- visualization plots: fold-change distribution, mass defect scatter, feature m/z vs. RT
- filtered feature list (.txt) with peak IDs for EIC extraction and MS/MS analysis

## How to apply

Begin with abundance-filtered features (fold-change >4, detected in ≥2 of 3 replicates). Remove features with mass defect shift <−100 or >+50 mmu relative to the parent compound to eliminate instrumental noise and isotope artifacts. Subtract blank intensities and remove features with higher mean intensity in blanks than samples. Remove standard impurities by comparing incubated sample peaks to reference standard peaks at the same concentration. Apply the critical mass-difference filter: remove all features with m/z >+50 u above the parent pesticide's [M+H]+ or [M−H]− ion, as these exceed Phase I oxidation/reduction/cleavage products and likely represent conjugation artifacts (addition of >3 oxygen atoms). Output the retained feature table for downstream molecular formula assignment and spectral library generation.

## Related tools

- **XCMS** (Feature detection, alignment, and retention time correction upstream of prioritization)
- **CAMERA** (Componentization of isotope and adduct peaks prior to filtering)
- **incubatoR** (Integrated R workflow implementing all prioritization filters (abundance, mass defect, mass difference, blank subtraction) in sequence) — https://github.com/chufz/incubatoR
- **R** (Statistical comparison and filtering step execution (v3.6.1 in this implementation))
- **ProteoWizard** (Upstream raw mass spectrum conversion to mzML and centroiding (v3.0.18265))

## Evaluation signals

- Feature count reduction from ~60% loss after blank/isotope/adduct removal to final prioritized list; confirm that non-metabolite noise has been substantially eliminated while metabolites are retained.
- Comparison of retained features against literature-reported metabolites and BioTransformer predictions: approximately two-thirds of in vitro-detected metabolites should overlap with known or predicted transformations.
- Validation of mass difference filter: confirm that all features with Δm/z >+50 u relative to parent [M+H]+ or [M−H]− have been removed; spot-check remaining features are consistent with Phase I reactions (oxidation, reduction, bond cleavage).
- Blank intensity check: verify that features removed due to blank subtraction had mean blank intensity ≥ mean sample intensity, confirming correct filtering logic.
- Visual inspection of MDF (mass defect filter) and Feature (m/z vs. RT) scatter plots: remaining features should cluster near expected mass defect range (−100 to +50 mmu) and show distinct RT separation from parent compound.

## Limitations

- Mass difference filter (+50 u cutoff) will exclude legitimate Phase II conjugation products (e.g., glucuronide, sulfate adducts with Δm/z >+50 u), limiting detection to Phase I metabolites only.
- In vitro S9 liver microsome incubation does not reproduce all human metabolic pathways; some reduction reactions, consecutive hydroxylations, and weak bond breaking may not be captured, leading to false negatives.
- Low ionization efficiencies or hydrophilic compound losses during sample extraction/cleanup can result in false negatives for true metabolites that are formed but undetected.
- Replicate structure requirement (≥2 of 3 replicates detected) limits applicability to study designs with at least three independent incubation replicates per compound.
- Generic fold-change cutoff (>4) and mass defect thresholds may require compound-specific optimization; variable filtering strictness is recommended in the workflow but not automated.

## Evidence

- [methods] abundance filter: "We used a generic cutoff value of >4 for the fold change and kept only the features that were detected in at least two of three replicates"
- [methods] mass difference filtering rationale: "all features with a mass difference higher than +50 u to the parent compound, corresponding to an addition of three O atoms, were also not further evaluated."
- [methods] mass defect filtering: "a threshold of −100 mmu for the lower and +50 mmu for the upper mass defect cutoff level"
- [methods] blank subtraction and isotope/adduct removal: "The application of a blank subtraction combined with isotope/adduct peak removal steps reduced the number of peaks by about 60% in both ESI+ and ESI−."
- [readme] incubatoR filtering workflow overview: "Main task is to identify metabolic transformation products in a LC-HRMS2 dataset of in-parallel incubated xenobiotic compounds by applying statistical tools as well as mass defect filtering"
- [methods] standard impurity removal: "To remove impurities stemming from the used pesticide standards in the metabolite data, mean group intensities after incubation were compared to the intensities measured in the pure pesticide standard"
- [methods] metabolite detection outcomes: "By applying the data processing workflow, we could assign in total 91 unambiguous molecular formulas to a number of 82 prioritized features in ESI+ and 39 in ESI− for the 22 pesticides."
- [discussion] incomplete metabolite coverage: "S9 incubation does not cover all potential or existing metabolites"
