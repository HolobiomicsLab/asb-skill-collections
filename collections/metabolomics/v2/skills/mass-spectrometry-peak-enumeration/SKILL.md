---
name: mass-spectrometry-peak-enumeration
description: Use when you have preprocessed MSI data (peaks already binned and normalized)
  and need to detect adduct formation patterns across the dataset.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3632
  edam_topics:
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_0121
  tools:
  - mass2adduct
  - R
  - Cardinal
  - msimat()
  techniques:
  - MS-imaging
  license_tier: restricted
derived_from:
- doi: 10.1021/acs.analchem.0c04720
  title: mass2adduct
evidence_spans:
- This package presents tools for counting and identifying possible adducts in MS
  data
- We can match massdiffs to specific adduct types using the same function `adductMatch`
- If the data matrix is very large, it may need to be reformatted to be loaded into
  memory during an R session.
- corrPairsMSI(d,d.diff.annot)
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_mass2adduct_cq
    doi: 10.1021/acs.analchem.0c04720
    title: mass2adduct
  dedup_kept_from: coll_mass2adduct_cq
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

# mass-spectrometry-peak-enumeration

> **License: restricted** — no clear open-source license detected for the underlying tool; verify licensing before commercial use or redistribution. <!-- asb-license-banner -->
## Summary

Systematically enumerate all pairwise mass differences from a mass spectrometry imaging (MSI) dataset to identify potential molecular adducts. This skill transforms a raw MSI intensity matrix into a ranked catalog of mass-difference patterns, enabling discovery of salt, matrix, and metabolite adducts that may otherwise remain hidden in complex datasets.

## When to use

Apply this skill when you have preprocessed MSI data (peaks already binned and normalized) and need to detect adduct formation patterns across the dataset. Use it particularly when the 'dark metabolome' — abundant but unidentified peaks — dominates your spectra, or when you suspect matrix or salt ions are forming adducts with target metabolites and obscuring their detection.

## When NOT to use

- Input peaks have not yet been binned or normalized (use Cardinal peakBin() or equivalent preprocessing first).
- You already have a validated adduct annotation table and only need to verify or refine assignments (use spatial correlation testing instead).
- Your instrument mass accuracy is worse than ~50 ppm, making histogram binning unreliable across the full mass range.

## Inputs

- CSV matrix of preprocessed MSI intensities (peaks × pixels)
- MSI data matrix in msimat format (preprocessed, peak-binned)
- Cardinal MSProcessedImagingExperiment or MSContinuousImagingExperiment object (v2.2+)
- numeric vector of mass values (if intensity data not available)

## Outputs

- massdiff object (data.frame with parent mass, adduct mass, and difference columns)
- massdiffhist histogram object (binned mass differences with counts)
- ranked data.frame of top adducts with occurrence counts and reference matches
- diffGetPeaks subset (parent–adduct ion pairs matching a target mass difference)

## How to apply

Load the preprocessed MSI data as a CSV matrix using msimat() with the correct field separator. Compute all possible pairwise mass differences with massdiff(), which returns a data.frame with parent ion masses, adduct ion masses, and their differences. Bin these differences into a histogram using hist() with a bin width appropriate to your instrument's mass accuracy (e.g., 0.01 for 10 ppm precision instruments). Rank the histogram bins by occurrence using topAdducts() to identify the most abundant mass differences. Cross-reference these differences against known chemical adducts using adductMatch() with the built-in adducts reference table. The ranked list reveals which adducts dominate your dataset; high-count mass differences that match known adducts (e.g., DHB-H₂O at 136.016 Da) indicate systematic adduct formation.

## Related tools

- **mass2adduct** (Primary R package providing massdiff(), hist(), adductMatch(), topAdducts(), and diffGetPeaks() functions; also manages the built-in adducts reference datasets.) — https://github.com/kbseah/mass2adduct
- **Cardinal** (Optional input source for MSI data; peak-binned MSProcessedImagingExperiment and MSContinuousImagingExperiment objects can be converted to msimat format via cardinal2msimat().)
- **msimat()** (Data import function that loads CSV-formatted MSI intensity matrices (exported from SCiLS, MSiReader, or other software) into the msimat object class required by massdiff().)
- **R** (Language and execution environment for the mass2adduct package workflow.)

## Examples

```
d <- msimat("msi.csv", sep=";"); d.diff <- massdiff(d); d.diff.hist <- hist(d.diff); topAdducts(d.diff.hist, n=10)
```

## Evaluation signals

- massdiff() output is a valid data.frame with exactly 3 columns (parent mass A, adduct mass B, mass difference) and row count equal to n×(n−1)/2 for n input peaks.
- histogram bin width matches instrument precision (e.g., 0.01 Da bin width for 10 ppm nominal resolution); inspect via plot(d.diff.hist) for a smooth, unimodal distribution.
- topAdducts() returns matches to known adducts (name, formula, mass) where the matched mass difference falls within the histogram bin containing the observed difference.
- High-count bins (top 5–10 adducts) correspond to chemically plausible ions (e.g., Na⁺, K⁺, NH₄⁺, matrix–H₂O losses) rather than random noise.
- Absence of spurious mass differences: compare the observed top differences against unexpected values; if all top hits are <50 counts out of millions of pairs, consider higher instrument noise or poor peak alignment.

## Limitations

- The massdiff() function examines all n×(n−1)/2 pairwise combinations; for datasets with thousands of peaks, memory and runtime scale quadratically. Use the Perl script msimunging.pl to reformat large CSV files to triplet format before import, or use corrPairsMSIchunks() for correlation testing.
- Histogram binning requires choosing an appropriate bin width; if too narrow, adjacent adduct signals fragment; if too wide, distinct adducts merge. Bin width should match your instrument's mass measurement uncertainty, typically 5–50 ppm.
- The built-in adducts reference table (adducts and adducts2 datasets) contains common biologically relevant species but may not include rare or instrument-specific adducts; users must supply custom reference data.frames in the same format (name, formula, mass columns).
- No changelog or version-tracking information is provided in the repository, limiting reproducibility when package updates occur.
- The skill does not inherently account for false positives from random pair coincidences; validation via spatial correlation (corrPairsMSI) or external mass spectrometry standards is recommended before interpreting adduct identities.

## Evidence

- [readme] Take all possible pairs of masses and calculate the mass difference for each pair. These mass differences represent potential molecular adducts.: "Take all possible pairs of masses and calculate the mass difference for each pair. These mass differences represent potential molecular adducts."
- [other] The massdiff function takes all possible pairs of masses from the MSI data matrix and calculates the mass difference for each pair, with these differences representing potential molecular adducts and returned as a data.frame object.: "The massdiff function takes all possible pairs of masses from the MSI data matrix and calculates the mass difference for each pair, with these differences representing potential molecular adducts and"
- [readme] The calculated mass differences are misleadingly precise, because measurement error and uncertainty are not taken into account. They should be binned into a histogram with a user-specified bin width, that depends on the known mass precision of your instrument.: "The calculated mass differences are misleadingly precise, because measurement error and uncertainty are not taken into account. They should be binned into a histogram with a user-specified bin width,"
- [other] topAdducts ranks mass differences by their occurrences, and reports them in descending order, as well as matches to known adducts, if any: "topAdducts ranks mass differences by their occurrences, and reports them in descending order, as well as matches to known adducts, if any"
- [readme] In mass spectrometry imaging, adducts can form between target molecules (e.g. metabolites) and other substances such as matrix or salt ions.: "In mass spectrometry imaging, adducts can form between target molecules (e.g. metabolites) and other substances such as matrix or salt ions."
- [readme] For large data sets, where the tables would not fit into memory, it is possible to break up the problem into "chunks" processed serially. Use the function corrPairsMSIchunks instead of corrPairsMSI.: "For large data sets, where the tables would not fit into memory, it is possible to break up the problem into "chunks" processed serially. Use the function corrPairsMSIchunks instead of corrPairsMSI."
