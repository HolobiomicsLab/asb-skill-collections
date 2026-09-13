---
name: mass-spectrometry-annotation-engine-customization
description: Use when when you have baseline MS/MS peak annotations from a known compound
  but need to refine them using newly available structural information (e.
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
  provenance_tier: literature
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

# mass-spectrometry-annotation-engine-customization

> **License: restricted** — no clear open-source license detected for the underlying tool; verify licensing before commercial use or redistribution. <!-- asb-license-banner -->
## Summary

Customize and refine MS/MS peak annotations by swapping or chaining annotation engines (e.g., CosineAlignmentEngine, MAGMaAnnotationEngine) and propagating structural constraints through peak-to-fragment mappings to improve modification site localization confidence. This skill is essential when baseline annotations are insufficient or when oracle (known structure) information becomes available mid-workflow.

## When to use

When you have baseline MS/MS peak annotations from a known compound but need to refine them using newly available structural information (e.g., after confirming the structure of a modified analog via orthogonal methods), or when you want to compare annotation quality across different annotation engines to select the best performer for your tolerance and normalization settings (mz_tolerance=0.01, ppm_tolerance=40, ratio_to_base_peak=0.01, normalize_peaks=True).

## When NOT to use

- The modified compound structure is not experimentally confirmed or remains unknown; oracle-mode refinement requires is_known=True and will not improve predictions without structural ground truth.
- Input spectra have not been normalized or filtered according to your method's requirements (normalize_peaks=True, ratio_to_base_peak threshold); annotation engines are sensitive to peak intensity distributions.
- You are working with a novel compound class where no reference library spectra or known analogs exist; annotation engines trained on or validated against GNPS or similar libraries may not generalize reliably.

## Inputs

- Compound object (known reference) with spectrum (mz/intensity pairs), precursor_mz, precursor_charge, adduct, and SMILES
- Compound object (modified analog) with spectrum, precursor_mz, precursor_charge, adduct, and optional SMILES
- ModiFinder network instance with baseline probability scores
- Annotation engine instance (CosineAlignmentEngine, MAGMaAnnotationEngine, or custom subclass)

## Outputs

- Updated ModiFinder network with refined peak-to-fragment mappings
- Refined modification probability scores (Dict or array keyed by atomic position)
- Comparison visualization (matplotlib Figure) showing baseline vs. oracle-refined predictions
- Improved site localization confidence metrics

## How to apply

Create an initial ModiFinder network using the default CosineAlignmentEngine and MAGMaAnnotationEngine to establish baseline modification probability scores. Load both the known compound and its modified analog as Compound objects with explicit tolerance parameters and set the is_known flag to True on the modified compound once its structure is confirmed. Call the re_annotate() method on the ModiFinder network using your chosen annotation engine to propagate structural constraints through the peak-to-fragment mappings; this refines peak assignments by leveraging the now-known structure. Re-generate modification probability scores using generate_probabilities() on the updated network and visualize the refined probabilities using draw_prediction() to compare against the baseline. Use this comparison to verify that site localization confidence has improved, particularly in regions where the modification is likely.

## Related tools

- **ModiFinder** (Core engine for site localization; houses the re_annotate() method, generate_probabilities() function, and draw_prediction() visualization utility; instantiated with Compound objects and annotation engines.) — https://github.com/Wang-Bioinformatics-Lab/ModiFinder_base
- **CosineAlignmentEngine** (Default spectrum alignment annotation engine; used to compute initial peak-to-fragment assignments via spectral similarity; can be swapped for alternative engines.) — https://github.com/Wang-Bioinformatics-Lab/ModiFinder_base
- **MAGMaAnnotationEngine** (Structure-aware annotation engine that refines peak assignments using molecular fragmentation rules; integrates with ModiFinder's re_annotate() to propagate structural constraints.) — https://github.com/Wang-Bioinformatics-Lab/ModiFinder_base
- **RDKit** (Provides molecule manipulation, edit distance calculations, modification site analysis, and structure visualization; underlying toolkit for fragment enumeration and bond/atom analysis.) — http://www.rdkit.org/
- **matplotlib** (Plotting library used by draw_prediction() to render baseline vs. refined probability comparisons and publication-quality spectrum/molecule visualizations.) — http://matplotlib.org/
- **Python** (Language runtime required (3.9+) for ModiFinder and all annotation engine customization workflows.)

## Examples

```
from modifinder import ModiFinder, Compound, CosineAlignmentEngine, MAGMaAnnotationEngine
main = Compound(spectrum=peaks1, precursor_mz=400.0, precursor_charge=1, adduct='[M+H]+', smiles='C1=CC=C(C=C1)O')
mod = Compound(spectrum=peaks2, precursor_mz=416.0, precursor_charge=1, adduct='[M+H]+', smiles=None)
finder = ModiFinder(main, mod, mz_tolerance=0.01, ppm_tolerance=40, normalize_peaks=True)
probs_baseline = finder.generate_probabilities()
mod.is_known = True
finder.re_annotate(MAGMaAnnotationEngine())
probs_refined = finder.generate_probabilities()
fig = finder.draw_prediction(probs_refined)
```

## Evaluation signals

- After re_annotate() and generate_probabilities(), modification probability scores at the true modification site(s) should increase relative to the baseline, with highest confidence at the correct atomic position(s).
- Peak-to-fragment mappings returned by get_result() should show improved overlap between known and modified compound spectra in regions corresponding to intact structural scaffolds, while unmatched peaks cluster near the modification site.
- draw_prediction() comparison visualization must display annotated fragments and their confidence bars; oracle-refined predictions should show fewer ambiguous peak assignments and narrower confidence intervals.
- Network re_annotate() call completes without errors and the is_known flag on the modified Compound remains True throughout the workflow; otherwise, structural constraints are not propagated.
- Tolerance parameters (mz_tolerance=0.01, ppm_tolerance=40) are respected during annotation refinement; peak matching should not occur for m/z differences exceeding these bounds.

## Limitations

- Annotation engine customization depends critically on the quality and completeness of the known compound's structural annotation; incomplete or incorrect fragment mappings propagate error through re_annotate().
- MAGMaAnnotationEngine and similar structure-aware engines require valid SMILES strings and may fail or produce low-confidence predictions for poorly resolved spectra, complex polycyclic compounds, or modifications affecting core fragmentation patterns.
- Re-annotation is computationally expensive for large spectral networks or high-dimensional fragment spaces; practical runtime scales with the number of candidate fragment assignments and tolerance window width.
- Oracle-mode refinement (is_known=True) only improves predictions when the confirmed structure is substantially similar to the unknown compound (e.g., a known modification rather than a novel scaffold); distant structural relatives may not constrain peak assignments effectively.

## Evidence

- [other] Set the is_known flag on the modified compound to True to signal that its structure is now available for annotation refinement.: "Set the is_known flag on the modified compound to True to signal that its structure is now available for annotation refinement."
- [other] Call the re_annotate() method on the ModiFinder network using the annotation engine to propagate structural constraints through peak-to-fragment mappings.: "Call the re_annotate() method on the ModiFinder network using the annotation engine to propagate structural constraints through peak-to-fragment mappings."
- [other] Re-generate modification probability scores using generate_probabilities() on the updated network to incorporate oracle-refined annotations.: "Re-generate modification probability scores using generate_probabilities() on the updated network to incorporate oracle-refined annotations."
- [other] Draw the prediction visualization using draw_prediction() on the refined probabilities, comparing against the baseline to demonstrate improvement in site localization confidence.: "Draw the prediction visualization using draw_prediction() on the refined probabilities, comparing against the baseline to demonstrate improvement in site localization confidence."
- [other] Create an initial ModiFinder instance and generate baseline modification probability scores using the default CosineAlignmentEngine and MAGMaAnnotationEngine.: "Create an initial ModiFinder instance and generate baseline modification probability scores using the default CosineAlignmentEngine and MAGMaAnnotationEngine."
- [readme] ModiFinder includes several useful utility functions for mass spectrometry data analysis and visualization: "ModiFinder includes several useful utility functions for mass spectrometry data analysis and visualization"
