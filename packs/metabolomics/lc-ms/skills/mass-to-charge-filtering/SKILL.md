---
name: mass-to-charge-filtering
description: Use when after generating theoretical B/Y ion spectra or after importing experimental MS/MS scans when your analysis goal requires restricting the ion population to a specific m/z window (e.g., m/z < 2000).
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3695
  edam_topics:
  - http://edamontology.org/topic_0121
  - http://edamontology.org/topic_3520
  tools:
  - Aerith
  - R
  - mzR
  techniques:
  - LC-MS
derived_from:
- doi: 10.1021/acs.analchem.5c03207
  title: Aerith
evidence_spans:
- Aerith is an R package that provides interfaces to read and write mass spectrum scans, calculate the theoretical isotopic peak envelope
- Aerith is an R package that provides interfaces to read and write mass spectrum scans
- Aerith is an R package
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_aerith_cq
    doi: 10.1021/acs.analchem.5c03207
    title: Aerith
  dedup_kept_from: coll_aerith_cq
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1021/acs.analchem.5c03207
  all_source_dois:
  - 10.1021/acs.analchem.5c03207
  zenodo_doi: TODO-zenodo
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# mass-to-charge-filtering

## Summary

Filter theoretical or experimental mass spectrometry peaks by m/z threshold to retain only fragments within a specified mass range. This skill is essential when working with SIP-labeled peptide spectra to remove high m/z noise and focus analysis on biologically relevant ion populations.

## When to use

Apply this skill after generating theoretical B/Y ion spectra or after importing experimental MS/MS scans when your analysis goal requires restricting the ion population to a specific m/z window (e.g., m/z < 2000). Use it when high-mass artifacts or background ions obscure biological signal, or when instrument limitations or method scope restrict the detectable mass range.

## When NOT to use

- Input spectra are already fully processed by downstream tools that expect the full m/z range; filtering may remove required reference peaks.
- Your analysis requires intact high m/z fragments for accurate charge-state or precursor inference; filtering may remove essential information.
- The theoretical ion set is already constrained by your search engine parameters; redundant filtering will not improve specificity.

## Inputs

- AAspectra object (theoretical or experimental) with populated spectra slot containing MZ, intensity, and fragment annotation columns
- numeric m/z threshold value

## Outputs

- filtered AAspectra object or data frame with MZ, intensity, and annotations for peaks within threshold
- TSV file (optional) with filtered ion table

## How to apply

After calling getSipBYionSpectra() or loading experimental spectra into an AAspectra object, access the spectra slot (which contains MZ, intensity, and fragment annotation columns) and subset rows where the MZ column satisfies your threshold condition (e.g., MZ < 2000). Export the filtered table as a TSV or data frame for downstream visualization or scoring. The filtering preserves all annotation metadata (fragment type, isotopic state, charge) so that filtered peaks remain interpretable. Choose your m/z threshold based on instrument capabilities, expected peptide mass, or prior knowledge of background noise distribution.

## Related tools

- **Aerith** (generates theoretical B/Y ion spectra as AAspectra objects and provides the spectra slot structure that filtering operates on) — https://github.com/xyz1396/Aerith
- **R** (environment for subsetting and filtering AAspectra spectra slot using standard data frame operations)
- **mzR** (parses experimental mzML and MGF files into objects that can be filtered by m/z prior to Aerith PSM scoring)

## Examples

```
filtered_spectrum <- subset(your_AAspectra@spectra, MZ < 2000); write.table(filtered_spectrum, file='filtered_ions.tsv', sep='\t', row.names=FALSE)
```

## Evaluation signals

- Verify that all retained peaks have MZ values ≤ threshold; spot-check a random sample of filtered rows against original spectra slot.
- Confirm that fragment annotations (B/Y type, isotopic state) are preserved in the filtered output; no rows should be corrupted or missing metadata.
- Check that the number of retained peaks is reasonable given the input spectrum complexity and threshold stringency (e.g., a threshold of m/z < 2000 on a 25 aa peptide should retain most B/Y ions).
- Compare filtered and unfiltered spectra side-by-side in Aerith's visualization tools to ensure no biologically relevant fragments were unintentionally removed.

## Limitations

- Filtering is a one-way operation; peaks below the threshold are discarded and cannot be recovered without re-running getSipBYionSpectra() or reloading the experimental scan.
- An overly stringent m/z threshold may remove low-mass fragments (e.g., small B ions) that contain isotopic enrichment signature necessary for SIP labeling validation.
- The filter threshold must be set a priori; the method does not automatically detect optimal cutoffs based on signal distribution or noise characteristics.

## Evidence

- [other] Filter the resulting ion table to retain only fragments with m/z < 2000: "Filter the resulting ion table to retain only fragments with m/z < 2000. 4. Export the filtered AAspectra theoretical spectrum table"
- [other] spectra slot contains MZ, intensity, and fragment annotations: "returning an AAspectra object whose spectra slot contains MZ, intensity, and fragment annotations that can be filtered to retain only peaks below a specified mass threshold"
- [intro] calculate the theoretical isotopic peak envelope of peptide precursors and their B Y ions: "calculate the theoretical isotopic peak envelope of peptide precursors and their B Y ions"
