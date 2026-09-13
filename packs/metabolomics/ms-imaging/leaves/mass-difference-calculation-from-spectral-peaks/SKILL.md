---
name: mass-difference-calculation-from-spectral-peaks
description: Use when you have a list of detected masses (m/z peaks) from MALDI-MS
  imaging data and want to systematically search for adduct relationships. Apply this
  skill when you suspect that observed peaks include not just parent metabolites but
  also their adducts with matrix ions (e.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3632
  edam_topics:
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_0769
  tools:
  - mass2adduct
  - R
  - Cardinal
  techniques:
  - MS-imaging
  license_tier: open
  provenance_tier: literature
derived_from:
- doi: 10.1021/acs.analchem.0c04720
  title: mass2adduct
evidence_spans:
- This package presents tools for counting and identifying possible adducts in MS
  data
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

# mass-difference-calculation-from-spectral-peaks

## Summary

Calculate all pairwise mass differences from MS imaging peak lists to identify potential molecular adducts. This skill detects mass shifts between detected ions that may indicate adduct formation with matrix, salt, or solvent species.

## When to use

You have a list of detected masses (m/z peaks) from MALDI-MS imaging data and want to systematically search for adduct relationships. Apply this skill when you suspect that observed peaks include not just parent metabolites but also their adducts with matrix ions (e.g., DHB-H₂O, [M+Na]⁺) or other cations/anions, and you need to enumerate candidate mass differences before matching against known adduct tables.

## When NOT to use

- Your input is a single, isolated mass value or fewer than 3 peaks — pairwise differences require at least 2 peaks, but meaningful adduct patterns emerge with dozens or more.
- You have already identified and removed all known adducts from your peak list — this skill is designed to discover adduct relationships, not verify pre-filtered data.
- Your data are from non-imaging MS (e.g., bulk LC–MS without spatial distribution) where spatial correlation cannot be used to validate adduct pairs post-hoc.

## Inputs

- msimat object (MSI data matrix with m/z peaks and pixel intensities)
- numeric vector of mass values (m/z peaks)
- MSProcessedImagingExperiment or MSContinuousImagingExperiment (Cardinal v2.2+)

## Outputs

- massdiff object (data.frame with parent masses and pairwise differences)
- histogram (binned mass differences with counts per bin)

## How to apply

Import your peak list as an msimat object (from CSV, Cardinal imaging experiment, or plain numeric vector). Call massdiff() on the peak data to compute all pairwise mass differences; this generates a massdiff object containing parent masses and their differences. Bin the resulting differences into a histogram with user-specified bin width (typically 0.01 Da, adjusted for your instrument's mass accuracy). The bin width should reflect your instrument's known mass precision and measurement uncertainty. Inspect the histogram visually to identify prominent bins, which represent frequently occurring mass differences. These candidates can then be matched to known adduct masses using adductMatch() or ranked by frequency with topAdducts().

## Related tools

- **mass2adduct** (Provides massdiff() function to compute pairwise mass differences and histogram binning; supplies adducts reference dataset for matching) — https://github.com/kbseah/mass2adduct
- **Cardinal** (Supplies MSProcessedImagingExperiment and MSContinuousImagingExperiment objects; requires peakBin() preprocessing before conversion to msimat) — http://cardinalmsi.org/
- **R** (Execution environment for mass2adduct workflows)

## Examples

```
d <- msimat("msi.csv", sep=";"); d.diff <- massdiff(d); d.diff.hist <- hist(d.diff); head(adductMatch(d.diff.hist))
```

## Evaluation signals

- The histogram of binned mass differences shows discrete, interpretable peaks (distinct from background noise); high bin counts at known adduct masses (e.g., 18.01 Da for [M+NH₄]⁺–[M+H]⁺ or 22.99 Da for [M+Na]⁺) indicate adduct formation.
- topAdducts() output lists mass differences with matches to known adducts in the reference table; quantile values for matched adducts should be noticeably higher than for random background bins.
- When followed by corrPairsMSI(), ion pairs with high-count mass differences show statistically significant spatial correlation (p < 0.05 after Bonferroni correction), confirming that putative parent and adduct ions co-localize in the imaging data.
- The number and distribution of detected mass differences scale reasonably with peak count: ~N×(N−1)/2 pairwise comparisons; absence of expected adduct masses suggests incorrect bin width or preprocessing (e.g., missing peakBin() step in Cardinal).
- Bin width is appropriate: no major adduct matches are missed (compare hist bins to known adduct masses within instrument tolerance) and no spurious peaks emerge from over-binning.

## Limitations

- Bin width selection is critical and user-dependent on instrument mass accuracy; too wide a bin merges distinct adducts, too narrow a bin fragments true signal into spurious peaks.
- The method is computationally intensive for very large peak lists (O(N²) pairwise comparisons); corrPairsMSI() with spatial correlation testing may exhaust memory on hundreds or thousands of peaks and requires corrPairsMSIchunks() as a workaround.
- Mass differences alone do not prove adduct identity — spatial correlation testing (corrPairsMSI) is essential to confirm that parent and putative adduct ions truly co-localize in the imaging data; high-frequency mass differences that do not correlate spatially are likely artifacts.
- Requires pre-processed, peak-binned data; raw or incompletely baseline-corrected spectra will produce noisy, unreliable mass differences.
- Built-in adduct reference tables (adducts and adducts2) cover biologically common species but may not include all instrument-specific adducts or analyte-specific modifications; custom adduct tables can be supplied but must match the required three-column data.frame format (name, formula, mass).

## Evidence

- [methods] Take all possible pairs of masses and calculate the mass difference for each pair. These mass differences represent potential molecular adducts.: "Take all possible pairs of masses and calculate the mass difference for each pair. These mass differences represent potential molecular adducts."
- [readme] The calculated mass differences are misleadingly precise, because measurement error and uncertainty are not taken into account. They should be binned into a histogram with a user-specified bin width, that depends on the known mass precision of your instrument.: "The calculated mass differences are misleadingly precise, because measurement error and uncertainty are not taken into account. They should be binned into a histogram with a user-specified bin width,"
- [intro] In mass spectrometry imaging, adducts can form between target molecules (e.g. metabolites) and other substances such as matrix or salt ions.: "In mass spectrometry imaging, adducts can form between target molecules (e.g. metabolites) and other substances such as matrix or salt ions."
- [readme] Output is a massdiff object with three elements: the two parent masses and the difference between them.: "Output is a massdiff object with three elements: the two parent masses and the difference between them."
- [readme] Cardinal MSProcessedImagingExperiment or MSContinuousImagingExperiment objects (requires Cardinal v2.2 and above) can be converted to mass2adduct's msimat format.: "Cardinal MSProcessedImagingExperiment or MSContinuousImagingExperiment objects (requires Cardinal v2.2 and above) can be converted to mass2adduct's msimat format."
