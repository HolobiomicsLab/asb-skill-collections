---
name: oracle-mode-structural-constraint-integration
description: Use when when you have loaded both a known compound and its modified analog with MS/MS spectra, initially generated baseline modification probability scores, and then obtained or confirmed the structure of the modified compound.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3802
  edam_topics:
  - http://edamontology.org/topic_0121
  - http://edamontology.org/topic_3520
  tools:
  - ModiFinder
  - Python
  - RDKit
  - matplotlib
  - Pillow
  - MAGMaAnnotationEngine
  - CosineAlignmentEngine
derived_from:
- doi: 10.1021/jasms.4c00061
  title: ModiFinder
evidence_spans:
- mf = ModiFinder(known_compound, modified_compound, mz_tolerance=0.01, ppm_tolerance=40)
- mf = ModiFinder(known_compound, modified_compound, helpers=helpers_array, **args)
- ModiFinder requires Python 3.9 or above.
- ModiFinder requires Python 3.9 or above
- 'rdkit: http://www.rdkit.org/'
- ModiFinder includes powerful visualization tools built on RDKit and matplotlib for creating publication-quality figures.
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
  zenodo_doi: TODO-zenodo
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# oracle-mode-structural-constraint-integration

## Summary

A refinement workflow in ModiFinder that uses the known structure of a modified compound to propagate structural constraints through peak-to-fragment mappings, improving annotation accuracy and modification site localization confidence. This oracle-mode approach re-annotates spectra after setting a compound's structure as known, yielding updated probability scores that reflect structural guidance.

## When to use

When you have loaded both a known compound and its modified analog with MS/MS spectra, initially generated baseline modification probability scores, and then obtained or confirmed the structure of the modified compound. Apply this skill when you want to refine peak annotations by leveraging the now-available structural information to constrain which fragments are chemically plausible given the known modification sites.

## When NOT to use

- The modified compound's structure is unknown or unavailable; use baseline ModiFinder instead.
- You have no baseline probability scores to refine; first generate initial probabilities without oracle mode.
- The MS/MS spectra for both compounds have not been loaded and normalized; initialize and validate spectra first.

## Inputs

- ModiFinder instance with baseline probabilities already computed
- Modified compound Compound object with is_known flag ready to be set to True
- Annotation engine (e.g., MAGMaAnnotationEngine or CosineAlignmentEngine)
- Known SMILES string for the modified compound

## Outputs

- Re-annotated ModiFinder network with structural constraints propagated
- Updated modification probability scores reflecting oracle-refined annotations
- Prediction visualization comparing baseline and refined probabilities
- Improved site localization confidence metrics

## How to apply

After creating Compound objects for both the unmodified reference (with known SMILES) and the modified analog (initially without structure), instantiate a ModiFinder instance with specified tolerances (mz_tolerance=0.01, ppm_tolerance=40, ratio_to_base_peak=0.01, normalize_peaks=True) and generate baseline modification probabilities using the default CosineAlignmentEngine and MAGMaAnnotationEngine. Once the modified compound's structure becomes available, set its is_known flag to True to signal that structural constraints can now be applied. Call re_annotate() on the ModiFinder network, passing the annotation engine, to propagate structural constraints through existing peak-to-fragment mappings. Then call generate_probabilities() on the updated network to recompute modification probability scores incorporating the oracle-refined annotations. Finally, compare the refined probabilities against the baseline using draw_prediction() to visualize the improvement in site localization confidence.

## Related tools

- **ModiFinder** (Core framework providing re_annotate() and generate_probabilities() methods for oracle-mode refinement; manages Compound objects and annotation engines) — https://github.com/Wang-Bioinformatics-Lab/ModiFinder_base
- **MAGMaAnnotationEngine** (Annotation engine used to propagate structural constraints and refine fragment-to-peak mappings during re-annotation)
- **CosineAlignmentEngine** (Spectral alignment engine for baseline and refined modification probability scoring)
- **RDKit** (Underlying chemistry library for structure parsing, modification site analysis, and fragment constraint validation) — http://www.rdkit.org/
- **matplotlib** (Visualization of baseline vs. refined prediction probabilities and site localization confidence improvements) — http://matplotlib.org/

## Examples

```
siteLocator = ModiFinder(main_compound, mod_compound); siteLocator.generate_probabilities(); mod_compound.is_known = True; siteLocator.re_annotate(annotation_engine); siteLocator.generate_probabilities(); siteLocator.draw_prediction()
```

## Evaluation signals

- Modification probability scores increase or shift toward correct sites after re_annotate() compared to baseline
- Peak-to-fragment mappings in the network respect chemical plausibility given the known modified structure
- Visualization from draw_prediction() shows tighter confidence intervals or higher probability mass at the true modification site(s)
- No structural constraint violations (e.g., fragments that would require breaking bonds in the known modified structure are deprioritized)
- The re_annotate() method completes without throwing structural incompatibility errors, confirming the known SMILES is valid

## Limitations

- Effectiveness depends on the accuracy and completeness of the provided SMILES string for the modified compound; incorrect or tautomeric ambiguity in structure will propagate incorrect constraints.
- Oracle-mode refinement assumes the baseline ModiFinder network has already correctly matched most peaks; severe misalignment in the baseline may not be corrected by structure alone.
- Requires both compounds to have comparable MS/MS data quality and precursor mass accuracy; tolerance parameters (mz_tolerance, ppm_tolerance) must be set appropriately for the instrument and sample.
- The method is designed for localization of structural modifications; it may not improve confidence when the modification affects ionization properties or fragmentation patterns unpredictably.

## Evidence

- [other] Set the is_known flag on the modified compound to True to signal that its structure is now available for annotation refinement.: "Set the is_known flag on the modified compound to True to signal that its structure is now available for annotation refinement."
- [other] Call the re_annotate() method on the ModiFinder network using the annotation engine to propagate structural constraints through peak-to-fragment mappings.: "Call the re_annotate() method on the ModiFinder network using the annotation engine to propagate structural constraints through peak-to-fragment mappings."
- [other] Re-generate modification probability scores using generate_probabilities() on the updated network to incorporate oracle-refined annotations.: "Re-generate modification probability scores using generate_probabilities() on the updated network to incorporate oracle-refined annotations."
- [other] Draw the prediction visualization using draw_prediction() on the refined probabilities, comparing against the baseline to demonstrate improvement in site localization confidence.: "Draw the prediction visualization using draw_prediction() on the refined probabilities, comparing against the baseline to demonstrate improvement in site localization confidence."
- [other] ModiFinder provides spectrum utilities (Create consensus spectra, refine spectra, handle adducts) and molecule utilities (Calculate edit distances, find modification sites, analyze transitions) that work seamlessly with the core functionality to process MS data.: "ModiFinder provides spectrum utilities (Create consensus spectra, refine spectra, handle adducts) and molecule utilities (Calculate edit distances, find modification sites, analyze transitions) that"
