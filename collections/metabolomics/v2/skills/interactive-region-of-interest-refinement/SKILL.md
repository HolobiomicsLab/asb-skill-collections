---
name: interactive-region-of-interest-refinement
description: Use when after loading a LA-ICP-MS image into pew², you need to isolate tissue or sample regions from instrumental background or matrix before calculating elemental concentrations or ratios.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3443
  edam_topics:
  - http://edamontology.org/topic_3520
  tools:
  - pewpew
  - pewlib
  - pew²
derived_from:
- doi: 10.1021/acs.analchem.1c02138
  title: Pew2
- doi: 10.1529/biophysj.103.038422
  title: ''
evidence_spans:
- The built in `Filtering Tool` removes spikes by comparing pixel values to a locally defined threshold
- '|pewpew| is an open-source LA-ICP-MS data import and processing application'
- based on the python library pewlib_
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_pew2_cq
    doi: 10.1021/acs.analchem.1c02138
    title: Pew2
  dedup_kept_from: coll_pew2_cq
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1021/acs.analchem.1c02138
  all_source_dois:
  - 10.1021/acs.analchem.1c02138
  - 10.1529/biophysj.103.038422
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# Interactive Region-of-Interest Refinement

## Summary

Iteratively refine tissue selections in LA-ICP-MS images through threshold-based segmentation dialogs, combining manual selection tools with automated masking methods (Otsu's method, comparison operators) to separate analytically relevant tissue regions from background. Essential for isolating spatially localized elemental signals before quantitative analysis.

## When to use

After loading a LA-ICP-MS image into pew², you need to isolate tissue or sample regions from instrumental background or matrix before calculating elemental concentrations or ratios. Use this skill when raw pixel intensities span a wide dynamic range and automated global thresholding alone does not produce anatomically or chemically sensible boundaries—particularly when tissue morphology varies across the ablation field.

## When NOT to use

- Input image is already well-segmented or classified (e.g., from prior supervised machine-learning step). Use direct masking instead.
- Sample morphology is too complex or heterogeneous for single-threshold methods (e.g., finely interleaved tissue and bone, or multi-phase materials). Consider k-means clustering or manual polygon selection instead.
- Image contains strong instrumental artifacts or saturation that invalidates pixel intensity as a proxy for tissue presence.

## Inputs

- LA-ICP-MS image (loaded in pew² GUI; supported formats: Agilent .b directories, Thermo CSV/LDR, PerkinElmer ELAN .xl, Nu Instruments Vitesse, generic CSV, imzML)
- Optional: pre-existing coarse region selection (for iterative refinement)

## Outputs

- Binary mask image separating tissue from background
- Refined region-of-interest selection (overlay visualization)
- Masked image restricted to selected tissue pixels

## How to apply

Open the Selection Dialog via right-click context menu on the loaded LA-ICP-MS image. Select a thresholding method from the Method combo-box: Otsu's method is recommended for unknown or variable tissue contrast because it automatically finds the optimal threshold by minimizing intra-class variance; alternatively, manually set a threshold value. Choose a Comparison operator (e.g., '>' to select pixels above threshold, '<' to select below) that aligns with the expected signal distribution of your analyte. Optionally check 'Limit thresholding to selected value' to refine within a pre-existing coarse selection, reducing edge artifacts. Apply the threshold to generate a binary mask separating tissue pixels from background. Visualize the resulting selection overlay on the image and iteratively adjust the threshold value or method until the selection boundary aligns visually with tissue morphology and matches your chemical expectations (e.g., excluding bone matrix if analyzing soft tissue, or vice versa).

## Related tools

- **pew²** (GUI container for interactive selection dialog, image visualization, and threshold preview; applies segment, mask, and otsu filters to refine selections in real time) — https://github.com/djdt/pewpew
- **pewlib** (Underlying Python library implementing threshold, segment, mask, otsu, and kmeans filter operations that drive the Selection Dialog backend) — https://github.com/djdt/pewlib

## Examples

```
# In pew² GUI: right-click on loaded LA-ICP-MS image → Selection Dialog → select 'Otsu' from Method combo-box → set Comparison operator to '>' → click Apply → verify selection boundary overlay on tissue region → export masked image via Export Dialog
```

## Evaluation signals

- Selection boundary aligns visually with tissue morphology (e.g., follows epithelial/stromal border, excludes obvious background pixels)
- Resulting masked image contains no NaN or zero pixels in regions of known high analyte signal; background-only regions are fully masked out
- Quantitative outputs (e.g., mean elemental concentration within selection) are consistent with expected range for the tissue type and instrument calibration; outlier pixels have been removed
- Overlay transparency and color contrast allow the selection edge to be clearly distinguished from the underlying image without visual ambiguity
- Iterative refinement converges: successive threshold adjustments produce diminishing changes in selection area and boundary position

## Limitations

- Otsu's method assumes a bimodal (tissue vs. background) intensity distribution; fails or produces arbitrary splits in unimodal or multimodal images (e.g., heterogeneous tissue with multiple mineral phases).
- Single-threshold approaches cannot resolve sub-tissue regional heterogeneity (e.g., varying elemental uptake within tumor vs. stroma). Refinement produces a binary mask; finer compositional stratification requires multi-class methods (k-means) or external anatomical labels.
- Manual threshold choice is operator-dependent; results may not be reproducible across analysts or images from different instruments or ablation campaigns without explicit SOP and reference standards.
- Real-time visualization in the GUI depends on image size and screen resolution; very large LA-ICP-MS maps may render slowly, making iterative adjustment cumbersome.

## Evidence

- [other] The Selection Dialog implements segmentation through filter operations including Otsu's method and threshold-based masking: "The pew² application implements segmentation through filter operations including Otsu's method and threshold-based masking: the 'segment' filter creates a mask image from thresholds, the 'otsu'"
- [other] Workflow steps to open and use Selection Dialog: "Open the Selection Dialog via right-click context menu on the image. Select a thresholding method (e.g., Otsu's method) from the Method combo-box and set the Comparison operator (e.g., '>') to define"
- [other] Optional refinement within pre-existing selections: "Optionally check 'Limit thresholding to selected value' to restrict the thresholding operation to a pre-existing selection."
- [readme] pew² is a GUI for processing LA-ICP-MS data: "Pew² is a GUI for importing and processing line-by-line, spot-wise and ablation-time-aligned LA-ICP-MS data using the python library pewlib"
- [other] Filter operations available in pewlib for segmentation: "Otsu | image | Otsu's method of image; segment | image, threshold | creates a mask image of thresholds; mask | image, mask | selects from image using mask"
