---
name: spectral-annotation-and-overlay-visualization
description: Use when after correlation testing has validated putative parent–adduct ion pairs (e.g., via corrPairsMSI() on a massdiff object annotated with adductMatch results), use this skill to annotate and visualize the mass spectrum plot to confirm that identified pairs exhibit expected overlap—e.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3441
  edam_topics:
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_3172
  tools:
  - mass2adduct
  - R
  techniques:
  - MS-imaging
derived_from:
- doi: 10.1021/acs.analchem.0c04720
  title: mass2adduct
evidence_spans:
- This package presents tools for counting and identifying possible adducts in MS data
- library(mass2adduct)
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_mass2adduct
    doi: 10.1021/acs.analchem.0c04720
    title: mass2adduct
  dedup_kept_from: coll_mass2adduct
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1021/acs.analchem.0c04720
  all_source_dois:
  - 10.1021/acs.analchem.0c04720
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# Spectral Annotation and Overlay Visualization

## Summary

Annotate mass spectra with identified parent ions and adduct ions, then visualize them as overlaid scatter plots using contrasting colors and symbols to reveal spatial and spectral relationships. This skill enables discrimination of adduct-parent ion pairs in MALDI-MSI data through simultaneous visual inspection of their co-occurrence patterns.

## When to use

After correlation testing has validated putative parent–adduct ion pairs (e.g., via corrPairsMSI() on a massdiff object annotated with adductMatch results), use this skill to annotate and visualize the mass spectrum plot to confirm that identified pairs exhibit expected overlap—e.g., red points (adduct ions) spatially co-localized with blue points (parent ions) in the imaging data.

## When NOT to use

- Massdiff object has not been correlation-tested; overlays would show spurious associations without spatial validation.
- Adduct type of interest has no statistically significant ion pairs after corrPairsMSI() filtering; visualization would be uninformative.
- Input msimat object is not in mass2adduct format or lacks pixel-level intensity data; pointsAdducts() requires full imaging coordinate information.

## Inputs

- msimat object (preprocessed MSI data matrix with mass and intensity columns)
- massdiff object annotated with adductMatch() results and filtered by corrPairsMSI() p-values

## Outputs

- Annotated mass spectrum plot with overlaid scatter points (red for adducts, blue for parent ions)
- Visual confirmation of parent–adduct ion pair co-localization

## How to apply

Begin with a preprocessed msimat object and a massdiff object that has been (1) annotated with adductMatch() to identify known adduct types and (2) filtered by corrPairsMSI() correlation testing to retain only statistically significant ion pairs. Subset the annotated massdiff object to a single adduct type (e.g., subset(d.diff.annot.cor, matches=='Na adduct')). Invoke pointsAdducts() twice: first with which='adduct', signif=TRUE, pch=20, cex=0.5, col='red' to overlay adduct ion peaks as red filled circles, then with which='parent', signif=TRUE, pch=1, cex=0.5, col='blue' to overlay parent ion peaks as blue circle outlines. The resulting annotated mass spectrum plot should show red and blue point clusters that overlap, indicating ions serving dual roles (adduct and parent) or spatially correlated pairs. Success is indicated by recognizable overlap patterns consistent with the biological hypothesis that parent and adduct ions co-localize in imaging pixels.

## Related tools

- **mass2adduct** (R package providing pointsAdducts() function for annotation and overlay visualization, and msimat/massdiff object classes) — https://github.com/kbseah/mass2adduct
- **R** (Runtime environment for executing pointsAdducts() visualization commands)

## Examples

```
pointsAdducts(d, subset(d.diff.annot.cor, matches=='Na adduct'), which='adduct', signif=TRUE, pch=20, cex=0.5, col='red'); pointsAdducts(d, subset(d.diff.annot.cor, matches=='Na adduct'), which='parent', signif=TRUE, pch=1, cex=0.5, col='blue')
```

## Evaluation signals

- Red and blue point clusters appear at overlapping spatial coordinates on the mass spectrum plot, indicating parent–adduct ion co-localization.
- The proportion of overlapping red–blue point pairs matches the expected frequency of adduct-parent relationships based on biological sample composition.
- Subset filtering (e.g., matches=='Na adduct') reduces the massdiff object to only the target adduct type; pointsAdducts() renders only those pairs.
- Circle outlines (parent ions, pch=1) and filled circles (adduct ions, pch=20) are visually distinct and correctly colored (red vs. blue).
- No spurious isolated points appear far from overlapping clusters, confirming prior corrPairsMSI() significance filtering removed uncorrelated pairs.

## Limitations

- pointsAdducts() is effective only when the msimat object retains full pixel-level spatial information; pre-aggregated or low-resolution spectral matrices will obscure spatial overlap patterns.
- Visualization quality depends on prior correlation testing with appropriate p-value thresholds (default Bonferroni-corrected p < 0.05); looser cutoffs may introduce false-positive overlays.
- Overlapping red and blue points do not confirm chemical causality; they indicate spatial co-localization only. Further validation (e.g., MS/MS fragmentation, metabolite identity) is required to confirm adduct formation.
- For very large ion pair datasets, overlaid scatter plots become visually congested; filtering to top-ranked adduct types (via topAdducts()) may improve clarity.

## Evidence

- [other] The pointsAdducts() function generates a scatter plot that highlights adduct ions in red and parent ions in contrasting colors, enabling visual identification of the red/blue overlap pattern between sodium adducts and their corresponding parent ions.: "The pointsAdducts() function generates a scatter plot that highlights adduct ions in red and parent ions in contrasting colors, enabling visual identification of the red/blue overlap pattern between"
- [other] Invoke pointsAdducts() with which='adduct', signif=TRUE, pch=20, cex=0.5, col='red' to overlay adduct ion peaks in red. Invoke pointsAdducts() again with which='parent', signif=TRUE, pch=1, cex=0.5, col='blue' to overlay parent ion peaks as blue circle outlines.: "Invoke pointsAdducts() with which='adduct', signif=TRUE, pch=20, cex=0.5, col='red' to overlay adduct ion peaks in red. Invoke pointsAdducts() again with which='parent', signif=TRUE, pch=1, cex=0.5,"
- [readme] Test for spatial correlations between mass peaks in MS imaging data (imported with the msimat function). For example, we wish to see if what we believe to be pairs of parent- and derivative-ion masses tend to occur together.: "Test for spatial correlations between mass peaks in MS imaging data (imported with the msimat function). For example, we wish to see if what we believe to be pairs of parent- and derivative-ion"
- [other] You can annotate the original mass spectrum using a massdiff object, to mark peaks corresponding to parent ions and adduct ions in different colors.: "You can annotate the original mass spectrum using a massdiff object, to mark peaks corresponding to parent ions and adduct ions in different colors."
