---
name: mass-spectral-m-z-alignment
description: Use when after you have (1) identified putative labelled features with intensity and m/z measurements from LC/MS data (e.g., via basepeak_finder output in geoRge), (2) defined a list of expected ionization adducts (e.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3627
  edam_topics:
  - http://edamontology.org/topic_0769
  - http://edamontology.org/topic_3172
  tools:
  - geoRge
  - R
  - XCMS
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
  zenodo_doi: TODO-zenodo
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# mass-spectral-m-z-alignment

## Summary

Aligns observed mass-to-charge (m/z) values from LC/MS features against theoretical adduct masses in a reference metabolite database to identify candidate metabolite annotations. This skill enables matching putatively labelled features to known compounds by accounting for ionization form and mass shifts within a specified ppm tolerance window.

## When to use

Apply this skill after you have (1) identified putative labelled features with intensity and m/z measurements from LC/MS data (e.g., via basepeak_finder output in geoRge), (2) defined a list of expected ionization adducts (e.g., negative-mode adducts with their mass shifts), and (3) have access to a reference metabolite database with known compound identities and theoretical m/z values. Use this skill when your research goal is to assign metabolite identities to observed mass features by querying the database within a controlled mass accuracy tolerance (typically 6.5 ppm in stable-isotope labelling studies).

## When NOT to use

- Input basepeak_finder output contains no features above the minimum intensity threshold (Basepeak.minInt); the database_query function will return an empty or near-empty hits table.
- Reference metabolite database is incomplete, outdated, or does not cover the chemical space of your sample; matches will be sparse or absent even if true metabolites are present.
- Mass accuracy tolerance (ppm.s) is set too stringently (e.g., <2 ppm) for the instrument's actual mass resolution; many true metabolites will be missed due to calibration drift or instrument variation.

## Inputs

- basepeak_finder output object (s2 object containing m/z and intensity data for putative features)
- negative-mode adducts list (text file or R list specifying ionization forms and mass shifts)
- metabolite reference database (CSV or data frame with compound identities and theoretical m/z values)

## Outputs

- hits table (data frame with matched metabolite candidates, m/z values, metabolite names, adduct forms, and match quality metrics)

## How to apply

Load the basepeak_finder output (s2 object) containing m/z and intensity data for putatively labelled features. Load the adducts list specifying ionization forms and their mass shifts (e.g., adducts_negative.txt for negative-mode ionization). Load the metabolite reference database (e.g., ExampleDatabase.csv) containing known compound m/z values and identities. Execute the database_query function with the basepeak_finder output, adducts list, and database as inputs, specifying the mass accuracy tolerance (e.g., 6.5 ppm). The function matches each observed m/z against theoretical adduct masses by subtracting or adding mass shifts for each adduct form and checking whether the match falls within the tolerance window. Return the hits table containing matched metabolite candidates annotated with m/z, metabolite name, adduct form, and match quality metrics (e.g., mass error in ppm).

## Related tools

- **geoRge** (Executes database_query function to match observed m/z values against theoretical adduct masses and return metabolite annotation hits.) — https://github.com/jcapelladesto/geoRge
- **R** (Runtime environment for executing geoRge functions and managing data structures (s2 object, adducts list, database data frame).)
- **XCMS** (Upstream preprocessing tool for peak picking, alignment, and grouping that generates the feature data used by basepeak_finder and downstream database_query.) — https://bioconductor.org/packages/release/bioc/html/xcms.html

## Examples

```
hits <- database_query(geoRgeR = s2, adducts = negative, db = db)
```

## Evaluation signals

- hits table is non-empty and contains rows with non-null metabolite names, m/z values, and adduct assignments.
- Mass error (difference between observed and theoretical m/z) for all hits is within the specified tolerance window (e.g., ≤6.5 ppm).
- Each hit's adduct form is a valid member of the supplied adducts list, confirming the mass shift calculation is consistent.
- Number of hits and their m/z distribution are biologically plausible for the sample type and labelling experiment (e.g., enriched features cluster around expected mass shifts).
- Metabolite names in the hits table are resolvable in the reference database and match the theoretical m/z values after adduct mass adjustment.

## Limitations

- Database_query sensitivity depends on the completeness and accuracy of the reference metabolite database; metabolites absent from the database will not be annotated.
- Mass accuracy tolerance (ppm.s) must be calibrated to the specific LC/MS instrument; a poorly chosen tolerance can lead to false positives (too lenient) or false negatives (too stringent).
- The function assumes each observed m/z maps to a single metabolite-adduct pair; isobaric metabolites or overlapping adduct masses can produce ambiguous or multiple assignments.
- No changelog is documented for geoRge, limiting visibility into version-specific behavior or bug fixes that may affect reproducibility.

## Evidence

- [methods] database_query function use and workflow: "hits <- database_query(geoRgeR = s2, adducts = negative, db = db)"
- [intro] basepeak_finder output structure and parameters: "basepeak_finder function to identify base peaks with specified mass accuracy and intensity thresholds"
- [intro] mass accuracy tolerance application: "match observed m/z values against theoretical adduct masses within the 6.5 ppm tolerance window"
- [other] database_query function inputs and outputs: "The database_query function takes basepeak_finder output (geoRgeR), a list of negative adducts, and a database as inputs to produce candidate metabolite annotation hits."
- [other] hits table output contents: "Return and save the hits table containing matched metabolite candidates with m/z, metabolite name, adduct form, and match quality metrics."
