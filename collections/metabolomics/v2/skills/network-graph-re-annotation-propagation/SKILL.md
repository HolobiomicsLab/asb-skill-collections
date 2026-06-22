---
name: network-graph-re-annotation-propagation
description: Use when when you have completed an initial ModiFinder analysis on a compound pair (known compound + modified analog with unknown structure), and you subsequently acquire or determine the structure of the modified compound.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3803
  edam_topics:
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_0121
  tools:
  - ModiFinder
  - Python
  - RDKit
  - matplotlib
  - Pillow
  - CosineAlignmentEngine
  - MAGMaAnnotationEngine
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
---

# Network Graph Re-annotation Propagation

## Summary

Propagate structural constraints through a peak-to-fragment mapping network to refine MS/MS annotations when a previously unknown compound's structure becomes known. This technique leverages graph-based inference to improve modification site localization confidence by redistributing annotation probabilities across aligned fragments.

## When to use

When you have completed an initial ModiFinder analysis on a compound pair (known compound + modified analog with unknown structure), and you subsequently acquire or determine the structure of the modified compound. Use this skill to re-annotate the network graph using the newly available structural information, thereby propagating refinement constraints through fragment alignments to increase confidence in modification site predictions.

## When NOT to use

- The modified compound's structure is still unknown or unvalidated; use initial baseline scoring instead.
- Peak-to-fragment mappings are already saturated or degenerate (e.g., all peaks map to the same fragment); re-annotation will not improve disambiguation.
- The known compound's structure is incorrect or poorly annotated; structural constraints will propagate errors.

## Inputs

- ModiFinder network object with initial baseline annotations
- Compound object with is_known flag set to True and populated structure (SMILES or molecular graph)
- Annotation engine instance (CosineAlignmentEngine or MAGMaAnnotationEngine)

## Outputs

- Updated ModiFinder network with refined peak-to-fragment mappings
- Re-computed modification probability scores incorporating structural constraints
- Visualization comparison (baseline vs. refined probabilities)

## How to apply

After establishing baseline modification probability scores using CosineAlignmentEngine and MAGMaAnnotationEngine, set the is_known flag on the modified compound to True to signal structure availability. Call the re_annotate() method on the ModiFinder network, passing the annotation engine to activate structural constraint propagation through peak-to-fragment mappings. Re-generate modification probabilities using generate_probabilities() on the updated network to incorporate the oracle-refined annotations. Compare the refined probabilities against baseline scores to quantify improvements in site localization confidence. The propagation works by constraining fragment-to-structure mappings bidirectionally: fragments that align to known structural positions reinforce or suppress neighboring peak assignments, and vice versa, converging on a consistent annotation state.

## Related tools

- **ModiFinder** (Core framework providing network structure, re_annotate() method, and probability generation pipeline) — https://github.com/Wang-Bioinformatics-Lab/ModiFinder_base
- **CosineAlignmentEngine** (Alignment engine used to compute initial and refined peak-fragment cosine similarity scores) — https://github.com/Wang-Bioinformatics-Lab/ModiFinder_base
- **MAGMaAnnotationEngine** (Annotation engine that maps fragment peaks to molecular substructures for constraint propagation) — https://github.com/Wang-Bioinformatics-Lab/ModiFinder_base
- **RDKit** (Enables molecular graph construction and structural constraint representation) — http://www.rdkit.org/
- **matplotlib** (Visualization of refined probability predictions and comparison with baseline) — http://matplotlib.org/

## Examples

```
siteLocator = ModiFinder(main_compound, mod_compound); mod_compound.is_known = True; siteLocator.re_annotate(annotation_engine); refined_probs = siteLocator.generate_probabilities(); siteLocator.draw_prediction(refined_probs)
```

## Evaluation signals

- Modification probability scores for correct sites increase (higher confidence) relative to baseline after re_annotate() call.
- Incorrect or ambiguous site probabilities decrease, narrowing the peak-to-site localization to a single dominant annotation.
- Peak-to-fragment mappings in the network are internally consistent: no fragment is simultaneously assigned incompatible site positions.
- Visualization output (draw_prediction()) shows collapsed or resolved ambiguities compared to baseline figure; confidence intervals narrow or branching hypotheses merge.
- Re-annotation converges in finite iterations without oscillation or divergence in probability updates across the network graph.

## Limitations

- Re-annotation assumes the newly determined structure is correct; incorrect structural input will reinforce or create false annotations.
- Propagation effectiveness depends on density and quality of the initial peak-to-fragment mapping network; sparse or low-confidence alignments limit constraint flow.
- The method is sensitive to tolerance parameters (mz_tolerance, ppm_tolerance, ratio_to_base_peak) set during Compound object creation; poorly chosen values may prevent fragments from aligning and block propagation.
- Cyclical or degenerate fragment alignments (e.g., multiple fragments mapping to the same modification site, or structural isomers) can create competing constraints that do not fully resolve.

## Evidence

- [other] Set the is_known flag on the modified compound to True to signal that its structure is now available for annotation refinement.: "Set the is_known flag on the modified compound to True to signal that its structure is now available for annotation refinement."
- [other] Call the re_annotate() method on the ModiFinder network using the annotation engine to propagate structural constraints through peak-to-fragment mappings.: "Call the re_annotate() method on the ModiFinder network using the annotation engine to propagate structural constraints through peak-to-fragment mappings."
- [other] Re-generate modification probability scores using generate_probabilities() on the updated network to incorporate oracle-refined annotations.: "Re-generate modification probability scores using generate_probabilities() on the updated network to incorporate oracle-refined annotations."
- [other] ModiFinder provides spectrum utilities (Create consensus spectra, refine spectra, handle adducts) and molecule utilities (Calculate edit distances, find modification sites, analyze transitions) that work seamlessly with the core functionality to process MS data.: "ModiFinder provides spectrum utilities and molecule utilities that work seamlessly with the core functionality to process MS data."
- [other] Create an initial ModiFinder instance and generate baseline modification probability scores using the default CosineAlignmentEngine and MAGMaAnnotationEngine.: "Create an initial ModiFinder instance and generate baseline modification probability scores using the default CosineAlignmentEngine and MAGMaAnnotationEngine."
