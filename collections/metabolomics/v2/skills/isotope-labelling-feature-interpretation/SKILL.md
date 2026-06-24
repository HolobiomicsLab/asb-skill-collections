---
name: isotope-labelling-feature-interpretation
description: Use when after basepeak_finder has identified base peaks from isotope-labelled
  feature clusters with fold-change and intensity thresholds met.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3860
  edam_topics:
  - http://edamontology.org/topic_3172
  - http://edamontology.org/topic_0121
  - http://edamontology.org/topic_3407
  tools:
  - geoRge
  - R
  - XCMS
  techniques:
  - LC-MS
  license_tier: open
derived_from:
- doi: 10.1021/acs.analchem.5b03628
  title: geoRge
evidence_spans:
- library(geoRge)
- hits <- database_query(geoRgeR = s2, adducts = negative, db = db)
- This is an R Markdown document
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_george_cq
    doi: 10.1021/acs.analchem.5b03628
    title: geoRge
  dedup_kept_from: coll_george_cq
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1021/acs.analchem.5b03628
  all_source_dois:
  - 10.1021/acs.analchem.5b03628
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# isotope-labelling-feature-interpretation

## Summary

Reconstruct metabolite annotations from stable isotope-labelled LC/MS features by matching observed m/z values against a reference database using adduct-specific mass shifts and ppm tolerance windows. This skill bridges putative incorporation detection and candidate metabolite identification in untargeted metabolomics workflows.

## When to use

After basepeak_finder has identified base peaks from isotope-labelled feature clusters with fold-change and intensity thresholds met. Use this skill when you have m/z and intensity data from labelled features and need to assign metabolite identities by cross-referencing a compound database accounting for ionization adducts (e.g., negative-mode [M−H]⁻, [M+Cl]⁻). Essential when the analysis goal includes stable isotope incorporation tracking and metabolite annotation.

## When NOT to use

- Input is already a manually curated feature-to-metabolite annotation table; this skill is for *de novo* database matching.
- No reference database is available or the database lacks ionization adduct specifications.
- The basepeak_finder step has not been completed; raw peak picking output is insufficient for this annotation step.

## Inputs

- basepeak_finder output object (s2)
- negative-mode adducts list (text file with ionization forms and mass shifts)
- metabolite reference database (CSV with compound m/z and identities)

## Outputs

- hits table (matched metabolite candidates with m/z, metabolite name, adduct form, match quality metrics)

## How to apply

Execute the database_query function in geoRge with three inputs: (1) basepeak_finder output (s2 object) containing observed m/z values and intensities from putatively labelled features, (2) a list of negative-mode adducts specifying ionization forms and their mass shifts (e.g., adducts_negative.txt), and (3) a metabolite reference database (e.g., ExampleDatabase.csv) with known compound m/z and identities. The function matches observed m/z values against theoretical adduct masses of each database compound within a 6.5 ppm tolerance window. Return hits are ranked by match quality and include m/z, metabolite name, adduct form, and metrics. Inspect the hits table for high-confidence matches; filter by mass accuracy and adduct plausibility to assign candidate annotations to labelled features.

## Related tools

- **geoRge** (Executes database_query function to match observed m/z values against theoretical adduct masses within specified ppm tolerance) — https://github.com/jcapelladesto/geoRge
- **R** (Runtime environment for geoRge library and database_query execution)
- **XCMS** (Upstream peak picking, alignment, and grouping to prepare data for basepeak_finder and database_query) — https://bioconductor.org/packages/release/bioc/html/xcms.html

## Examples

```
hits <- database_query(geoRgeR = s2, adducts = negative, db = db)
```

## Evaluation signals

- Hits table is returned with non-empty rows; each row contains metabolite name, m/z, adduct form, and numeric match quality metrics.
- All matched m/z values fall within ±6.5 ppm of theoretical adduct masses; no hits exceed the tolerance window.
- Adduct forms in hits table are present in the input adducts list; no spurious or unspecified ionization forms appear.
- Number and distribution of hits per feature are reasonable (typically 0–5 high-confidence candidates per observed m/z); extreme numbers (>10) suggest database contamination or parameter miscalibration.
- Hits are sorted or ranked by match quality metric; practitioner can prioritize candidates by mass accuracy and intensity coherence.

## Limitations

- Mass accuracy tolerance (6.5 ppm) is fixed in the geoRge implementation; may not be optimal for all instrument types or mass ranges.
- Database completeness and quality directly determine annotation recall; incomplete or mis-annotated reference databases yield false negatives or false positives.
- Multiple adducts for the same compound can generate multiple hits per feature, requiring manual or algorithmic disambiguation.
- The function does not account for in-source fragmentation, neutral loss, or multiply charged ions; simple [M±adduct]⁻ matching only.
- No changelog is available in the repository; version history and parameter changes are undocumented.

## Evidence

- [methods] database_query function takes basepeak_finder output, adducts, and database as inputs: "Execute database_query function in geoRge with s2, negative adducts, and the database to match observed m/z values"
- [intro] matching operates within 6.5 ppm tolerance window: "match observed m/z values against theoretical adduct masses within the 6.5 ppm tolerance window"
- [methods] return hits table with metabolite identities and match metrics: "Return and save the hits table containing matched metabolite candidates with m/z, metabolite name, adduct form, and match quality metrics"
- [intro] basepeak_finder output structure and role: "s2 <- basepeak_finder(PuIncR = s1, XCMSet = mtbls213, UL.atomM=12.0,L.atomM=13.003355, ppm.s=6.5,Basepeak.minInt=2000)"
- [readme] installation and library invocation: "install_github("jcapelladesto/geoRge")
library(geoRge)"
