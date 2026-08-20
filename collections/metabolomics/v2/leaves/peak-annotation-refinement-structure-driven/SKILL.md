---
name: peak-annotation-refinement-structure-driven
description: Use when you have two related compounds (a known reference and its structural
  analog with unknown modification site), baseline peak annotations from cosine alignment,
  and newly available structural information (SMILES or molecular structure) for the
  modified compound.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3632
  edam_topics:
  - http://edamontology.org/topic_0121
  - http://edamontology.org/topic_3520
  tools:
  - ModiFinder
  - Python
  - RDKit
  - matplotlib
  - Pillow
  - CosineAlignmentEngine
  - MAGMaAnnotationEngine
  techniques:
  - LC-MS
  license_tier: restricted
derived_from:
- doi: 10.1021/jasms.4c00061
  title: ModiFinder
evidence_spans:
- mf = ModiFinder(known_compound, modified_compound, mz_tolerance=0.01, ppm_tolerance=40)
- mf = ModiFinder(known_compound, modified_compound, helpers=helpers_array, **args)
- ModiFinder requires Python 3.9 or above.
- ModiFinder requires Python 3.9 or above
- 'rdkit: http://www.rdkit.org/'
- ModiFinder includes powerful visualization tools built on RDKit and matplotlib for
  creating publication-quality figures.
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_modifinder_cq
    doi: 10.1021/jasms.4c00061
    title: ModiFinder
  dedup_kept_from: coll_modifinder_cq
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1021/jasms.4c00061
  all_source_dois:
  - 10.1021/jasms.4c00061
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# peak-annotation-refinement-structure-driven

> **License: restricted** — no clear open-source license detected for the underlying tool; verify licensing before commercial use or redistribution. <!-- asb-license-banner -->
## Summary

Refine MS/MS peak annotations by propagating structural constraints from a known compound through a ModiFinder network to improve fragment-to-modification mappings. This skill uses oracle-mode annotation when a modified compound's structure becomes available, enabling more confident localization of modification sites via re-annotation and probability score regeneration.

## When to use

You have two related compounds (a known reference and its structural analog with unknown modification site), baseline peak annotations from cosine alignment, and newly available structural information (SMILES or molecular structure) for the modified compound. Apply this skill when annotation confidence is low or site localization is ambiguous, and you need to leverage the new structural constraint to disambiguate fragment-to-modification associations.

## When NOT to use

- The modified compound's structure is not available or cannot be reliably determined — oracle mode requires structural ground truth.
- Baseline annotations already exhibit high confidence (e.g., modification site unambiguous from cosine alignment alone) — refinement adds overhead with minimal benefit.
- The two compounds share no common structural scaffold or the modification is not localized to a single site — structural propagation assumes a tractable mapping between known and modified structures.

## Inputs

- Compound object for known reference (with SMILES, spectrum peaks, precursor_mz, precursor_charge, adduct)
- Compound object for modified analog (initially without SMILES or structure)
- Baseline ModiFinder network with initial modification probability scores
- Structure (SMILES or RDKit molecule object) for the modified compound

## Outputs

- Re-annotated ModiFinder network with oracle-refined peak-to-fragment mappings
- Updated modification probability scores incorporating structural constraints
- Refined site localization confidence estimates per candidate modification site
- Visualization comparing baseline vs. oracle-refined predictions

## How to apply

Load both compounds as Compound objects with matched MS/MS tolerances (mz_tolerance=0.01, ppm_tolerance=40, ratio_to_base_peak=0.01, normalize_peaks=True). Generate baseline modification probability scores using ModiFinder with the default CosineAlignmentEngine and MAGMaAnnotationEngine. Set is_known=True on the modified compound to signal structural availability. Call re_annotate() on the ModiFinder network to propagate structural constraints through peak-to-fragment mappings, then regenerate probabilities via generate_probabilities() to incorporate oracle-refined annotations. The refinement works by allowing the annotation engine to use the now-available structure to resolve ambiguous fragments and improve peak-to-site associations, resulting in higher confidence modification site localization.

## Related tools

- **ModiFinder** (Core engine for peak annotation refinement, network management, and probability score regeneration using structural constraints) — https://github.com/Wang-Bioinformatics-Lab/ModiFinder_base
- **RDKit** (Molecular structure processing and fragment analysis for computing edit distances and analyzing transition maps during refinement) — http://www.rdkit.org/
- **matplotlib** (Visualization of baseline vs. refined prediction comparisons and confidence improvements) — http://matplotlib.org/
- **CosineAlignmentEngine** (Baseline spectral alignment metric for initial peak matching before structural refinement) — https://github.com/Wang-Bioinformatics-Lab/ModiFinder_base
- **MAGMaAnnotationEngine** (Fragment annotation engine that uses structural constraints to map peaks to molecular fragments during re-annotation) — https://github.com/Wang-Bioinformatics-Lab/ModiFinder_base

## Examples

```
siteLocator = ModiFinder(main_compound, mod_compound); baseline_peaks, baseline_frags = siteLocator.get_result(); mod_compound.is_known = True; siteLocator.re_annotate(); refined_probs = siteLocator.generate_probabilities(); siteLocator.draw_prediction()
```

## Evaluation signals

- Modification probability scores increase for the correct site and decrease for incorrect candidates after re-annotation, compared to baseline.
- Peak-to-fragment mappings resolve previously ambiguous associations; fragment identities now align with predicted molecular fragments from the refined structure.
- Site localization confidence (entropy or Bayesian posterior) concentrates on fewer candidate sites with higher individual probabilities than baseline.
- Visual comparison (draw_prediction() output) shows tighter, higher-intensity modification site annotations post-refinement.
- No new peaks or spurious fragment assignments are introduced; re-annotation is conservative and only refines existing mappings.

## Limitations

- Requires accurate structural information (SMILES or molecule object) for the modified compound; incorrect or incomplete structures will propagate errors through annotation refinement.
- Refinement assumes a tractable structural relationship between known and modified compounds; highly divergent scaffolds or multi-site modifications may exceed current fragment propagation capabilities.
- Performance depends on quality of baseline annotations; severe initial misalignments may not be fully corrected by structural constraints alone.
- Computational cost of re-annotation scales with network size and fragment complexity; very large compound libraries may require optimization or batching.

## Evidence

- [other] set the is_known flag on the modified compound to True to signal that its structure is now available for annotation refinement: "Set the is_known flag on the modified compound to True to signal that its structure is now available for annotation refinement."
- [other] Call the re_annotate() method on the ModiFinder network using the annotation engine to propagate structural constraints through peak-to-fragment mappings: "Call the re_annotate() method on the ModiFinder network using the annotation engine to propagate structural constraints through peak-to-fragment mappings."
- [other] Re-generate modification probability scores using generate_probabilities() on the updated network to incorporate oracle-refined annotations: "Re-generate modification probability scores using generate_probabilities() on the updated network to incorporate oracle-refined annotations."
- [other] ModiFinder provides spectrum utilities and molecule utilities that work seamlessly with the core functionality to process MS data: "ModiFinder provides spectrum utilities (Create consensus spectra, refine spectra, handle adducts) and molecule utilities (Calculate edit distances, find modification sites, analyze transitions) that"
- [intro] ModiFinder is a tool for site localization of structural modifications using MS/MS data: "ModiFinder is a tool for site localization of structural modifications using MS/MS data."
- [other] Create an initial ModiFinder instance and generate baseline modification probability scores using the default CosineAlignmentEngine and MAGMaAnnotationEngine: "Create an initial ModiFinder instance and generate baseline modification probability scores using the default CosineAlignmentEngine and MAGMaAnnotationEngine."
- [readme] ModiFinder requires two spectrum objects with specified tolerances (mz_tolerance, ppm_tolerance, ratio_to_base_peak, normalize_peaks parameters): "mz_tolerance=0.01, ppm_tolerance=40, ratio_to_base_peak=0.01, normalize_peaks=True"
