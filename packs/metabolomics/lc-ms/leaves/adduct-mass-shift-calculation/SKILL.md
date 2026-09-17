---
name: adduct-mass-shift-calculation
description: Use when when you have a list of observed m/z values from LC/MS feature
  detection and need to identify candidate metabolites by testing whether those m/z
  values correspond to known database compounds in specific ionization forms.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3632
  edam_topics:
  - http://edamontology.org/topic_0091
  - http://edamontology.org/topic_3370
  - http://edamontology.org/topic_3172
  - http://edamontology.org/topic_0769
  tools:
  - geoRge
  - R
  - basepeak_finder
  - XCMS
  - MetaboShiny
  techniques:
  - LC-MS
  license_tier: open
  provenance_tier: literature
derived_from:
- doi: 10.1021/acs.analchem.5b03628
  title: geoRge
- doi: 10.1007/s11306-020-01717-8
  title: ''
evidence_spans:
- library(geoRge)
- hits <- database_query(geoRgeR = s2, adducts = negative, db = db)
- This is an R Markdown document
- Welcome to the info page on MetaboShiny
- Welcome to the info page on MetaboShiny! We are currently on BioRXiv
- Through R
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_george_cq
    doi: 10.1021/acs.analchem.5b03628
    title: geoRge
  - build: coll_metaboshiny_cq
    doi: 10.1007/s11306-020-01717-8
    title: MetaboShiny
  dedup_kept_from: coll_george_cq
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1021/acs.analchem.5b03628
  all_source_dois:
  - 10.1021/acs.analchem.5b03628
  - 10.1007/s11306-020-01717-8
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# adduct-mass-shift-calculation

## Summary

Calculate theoretical m/z values for metabolite ions by applying mass shifts corresponding to different ionization forms (adducts) in negative or positive mode. This skill enables matching of observed mass-to-charge ratios against a database of known compounds by accounting for the systematic mass differences introduced during electrospray ionization.

## When to use

When you have a list of observed m/z values from LC/MS feature detection and need to identify candidate metabolites by testing whether those m/z values correspond to known database compounds in specific ionization forms. Apply this skill if your basepeak_finder output contains putative m/z values that must be matched against a reference metabolite database using a specified adduct list (e.g., negative-mode adducts like [M-H]⁻, [M+Cl]⁻) and a mass accuracy tolerance window (typically 6.5 ppm).

## When NOT to use

- Input is already a confirmed feature table or metabolite annotation table — this skill is for candidate generation, not validation.
- You lack a reference database of metabolites (database_query requires a populated db object); in that case, use alternative untargeted annotation strategies (e.g., MS/MS spectral libraries or network analysis).
- Your observed m/z values are from positive-mode ionization but you only have a negative-mode adducts list — you must use the correct ionization polarity adduct list for your data.

## Inputs

- basepeak_finder output (s2 object): mass-to-charge and intensity data from putatively labelled features
- negative-mode adducts list: text file specifying ionization forms and mass shifts (e.g., [M-H]⁻ = −1.007825 Da)
- metabolite reference database: CSV table with known compound m/z values, neutral masses, and identities

## Outputs

- hits table: matched metabolite candidates with observed m/z, calculated theoretical m/z, metabolite name, adduct form, mass error (ppm), and match quality metrics

## How to apply

Load the negative-mode adducts list (e.g., adducts_negative.txt) that specifies ionization forms and their mass shifts in Daltons. For each observed m/z value from basepeak_finder output and each compound in the reference database, calculate the theoretical m/z by adding the adduct mass shift to the neutral compound mass. Compare each calculated theoretical m/z against the observed m/z within a 6.5 ppm tolerance window (the acceptable mass deviation is computed as: ppm_error = |observed_mz - theoretical_mz| / theoretical_mz × 10⁶). Matches passing the tolerance filter are retained as candidate annotations, with the matched adduct form, metabolite identity, and quality metrics recorded in the hits table. The rationale is that electrospray ionization systematically alters the m/z of neutral compounds by predictable amounts, so enumerating all plausible adduct forms against a reference database dramatically increases annotation specificity compared to mass-only matching.

## Related tools

- **geoRge** (R package that implements the database_query function to match observed m/z values against theoretical adduct masses using the supplied adducts list and database within the specified ppm tolerance) — https://github.com/jcapelladesto/geoRge
- **basepeak_finder** (geoRge function that produces the s2 object containing base peak m/z and intensity data as input to database_query) — https://github.com/jcapelladesto/geoRge
- **XCMS** (Preprocessing package for peak picking, alignment, and grouping that produces the XCMSet object fed upstream to basepeak_finder and the database_query workflow) — https://bioconductor.org/packages/release/bioc/html/xcms.html

## Examples

```
hits <- database_query(geoRgeR = s2, adducts = negative, db = db)
```

## Evaluation signals

- All candidate hits in the output table have mass errors (ppm) ≤ 6.5 ppm; any match exceeding tolerance indicates a calculation or filtering error.
- The adduct mass shifts applied match the values in the loaded adducts list (e.g., if [M-H]⁻ is defined as −1.007825 Da, verify that theoretical_mz = (neutral_mass − 1.007825) / charge for each [M-H]⁻ hit).
- The hits table contains non-null entries only for metabolites whose theoretical m/z (after adduct shift) falls within the tolerance window of an observed m/z; hits with no valid observed counterpart indicate a filtering failure.
- The number of candidate hits is reasonable relative to database size and m/z distribution; an unexpectedly high hit count may indicate a tolerance window that is too wide or a database contamination issue.
- Spot-check: manually calculate theoretical m/z for a known reference compound (e.g., glucose [M-H]⁻ = 179.0557 m/z at 6 ppm) and verify it appears in the hits table with correct metabolite identity and adduct annotation.

## Limitations

- The skill assumes the supplied adducts list is complete and accurate for the ionization mode and matrix used; missing or incorrectly defined adducts will cause true metabolites to be missed.
- Mass accuracy is limited by the 6.5 ppm tolerance: instruments with poorer mass accuracy or databases with poorly validated monoisotopic masses will suffer more false negatives.
- No charge state logic is applied beyond what is encoded in the adducts list; multiply-charged ions (e.g., [M−2H]²⁻) are supported only if explicitly listed in the adducts file.
- The skill does not account for in-source adduct formation, isotope effects, or neutral loss during ionization; it assumes a single, dominant adduct form per compound.
- No changelog is provided in the geoRge repository, limiting visibility into potential bug fixes or parameter changes across versions.

## Evidence

- [other] The database_query function takes basepeak_finder output (geoRgeR), a list of negative adducts, and a database as inputs to produce candidate metabolite annotation hits.: "The database_query function takes basepeak_finder output (geoRgeR), a list of negative adducts, and a database as inputs to produce candidate metabolite annotation hits."
- [other] Execute database_query function in geoRge with s2, negative adducts, and the database to match observed m/z values against theoretical adduct masses within the 6.5 ppm tolerance window.: "Execute database_query function in geoRge with s2, negative adducts, and the database to match observed m/z values against theoretical adduct masses within the 6.5 ppm tolerance window."
- [other] Return and save the hits table containing matched metabolite candidates with m/z, metabolite name, adduct form, and match quality metrics.: "Return and save the hits table containing matched metabolite candidates with m/z, metabolite name, adduct form, and match quality metrics."
- [methods] hits <- database_query(geoRgeR = s2, adducts = negative, db = db): "hits <- database_query(geoRgeR = s2, adducts = negative, db = db)"
- [readme] install.packages("devtools", dependencies=TRUE); library(devtools); install_github("jcapelladesto/geoRge"); library(geoRge): "install.packages("devtools", dependencies=TRUE); library(devtools); install_github("jcapelladesto/geoRge"); library(geoRge)"
