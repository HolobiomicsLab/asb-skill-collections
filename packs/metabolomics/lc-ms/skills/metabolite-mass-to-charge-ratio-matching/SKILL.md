---
name: metabolite-mass-to-charge-ratio-matching
description: Use when you have a negative-mode or positive-mode LC-MS feature table with observed m/z values and peak intensities, and you need to identify which metabolites (by KEGG ID) are likely represented.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3632
  edam_topics:
  - http://edamontology.org/topic_0121
  - http://edamontology.org/topic_3172
  tools:
  - mWISE
  - R
  - CAMERA
  - cliqueMS
  - FELLA
  - igraph
  - KEGG database
  techniques:
  - LC-MS
derived_from:
- doi: 10.1021/acs.analchem.1c00238
  title: mWISE
evidence_spans:
- mWISE (metabolomics Wise Inference of Speck Entities) is an R package that provides tools for context-based annotation of untargeted LC-MS data.
- mWISE (metabolomics Wise Inference of Speck Entities) is an R package
- The default table of adducts and fragments is built using information from CAMERA R package
- The default table of adducts and fragments is built using information from CAMERA R package, H. Tong et al., and cliqueMS.
- information from CAMERA R package, H. Tong et al., and cliqueMS.
- we will now use the sample graph provided by FELLA R package
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_mwise_cq
    doi: 10.1021/acs.analchem.1c00238
    title: mWISE
  dedup_kept_from: coll_mwise_cq
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1021/acs.analchem.1c00238
  all_source_dois:
  - 10.1021/acs.analchem.1c00238
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# metabolite-mass-to-charge-ratio-matching

## Summary

Matches observed mass-to-charge ratio (m/z) values from untargeted LC-MS feature tables to KEGG metabolite database entries, accounting for adducts and in-source fragments. This is the first stage of the mWISE annotation workflow and produces candidate KEGG identifiers ranked by mass accuracy.

## When to use

You have a negative-mode or positive-mode LC-MS feature table with observed m/z values and peak intensities, and you need to identify which metabolites (by KEGG ID) are likely represented. Use this skill when your input has not yet been matched to a metabolite database and you want to generate a ranked list of candidate KEGG compounds for each observed feature.

## When NOT to use

- Input is already a KEGG-annotated feature table with metabolite IDs assigned—matching has been completed.
- You have only a single m/z value without intensity or frequency context; clustering and prioritization steps require intensity and co-elution patterns.
- The experimental ionization method (adducts and fragments) are completely unknown and cannot be reasonably inferred from the LC-MS method—accuracy will be low without appropriate adduct selection.

## Inputs

- LC-MS feature table (negative-mode or positive-mode) with m/z and intensity columns
- KEGG database (data frame with KEGG identifiers and their exact masses)
- Adducts and in-source fragments table (user-selected subset or mWISE default)

## Outputs

- Ranked list of candidate KEGG compounds per observed m/z feature
- Mass accuracy scores or mass differences for each candidate match

## How to apply

Load the mWISE package and the Trypanosoma sample dataset (or your own LC-MS feature table). Prepare a table of adducts and in-source fragments—mWISE provides defaults built from CAMERA, cliqueMS, and domain expertise, but you should select a subset of adducts that matches your experimental ionization conditions (e.g., [M-H]−, [M+Na]−, [M+Cl]− for negative mode) to improve accuracy. Call the mWISE.annotation wrapper function (or its underlying mass-to-charge ratio matching component) with the feature table and KEGG database (e.g., KeggDB or sample.keggDB). The function performs pairwise mass difference calculations between observed m/z and each KEGG compound mass, accounting for the selected adducts and fragments, to produce candidate matches. The results are candidate KEGG identifiers and their mass accuracy scores; these are then fed to downstream clustering and filtering stages.

## Related tools

- **mWISE** (Orchestrates mass-to-charge ratio matching to KEGG database; provides the mWISE.annotation wrapper function and default adduct/fragment tables.) — https://dev.b2s.club/b2slab/mWISE
- **KEGG database** (Reference metabolite database with exact masses; queried to find matches for observed m/z values.)
- **CAMERA** (Provides default adducts and fragments table used to build mWISE's reference ionization list.)
- **cliqueMS** (Contributes to the default adducts and fragments table in mWISE.)
- **R** (Execution environment for mWISE functions and workflows.)

## Examples

```
data("sample.dataset"); data("sample.keggDB"); result <- mWISE.annotation(sample.dataset$features, sample.keggDB, adducts = c("[M-H]-", "[M+Na]-"))
```

## Evaluation signals

- All observed m/z features receive at least one candidate KEGG match (no unmapped features unless intentionally filtered by mass tolerance).
- Mass accuracy of top-ranked candidates falls within the expected range for the instrument (typically < 5 ppm for high-resolution LC-MS).
- Candidate lists for features known a priori (e.g., from spiked standards) include the correct metabolite KEGG ID in the top-3 ranks.
- Comparing top-3 performance metrics (precision, recall, F1-score) computed by performanceEvaluation against df.Ref benchmark reference peaks shows expected annotation quality.
- When subset adducts are used instead of all defaults, mass accuracy improves and false-positive candidates decrease.

## Limitations

- Mass-to-charge ratio matching alone cannot distinguish isomeric metabolites with identical exact masses; downstream clustering and network diffusion are required for disambiguation.
- Accuracy depends heavily on selection of appropriate adducts and in-source fragments for the specific LC-MS method; misspecified ionization conditions lead to incorrect or missing candidates.
- The KEGG database has incomplete coverage of certain metabolite classes (e.g., some lipids, modifications); candidates outside KEGG space will not be matched.
- In-source fragments and multiply charged species can complicate matching; recovery of completely removed peaks by recoveringPeaks function is necessary to mitigate loss.

## Evidence

- [intro] matching mass-to-charge ratio values to KEGG database, ii) clustering and filtering the potential KEGG candidates, and iii) building a final prioritized list using diffusion in networks: "matching mass-to-charge ratio values to KEGG database with adducts and in-source fragments"
- [intro] The default table of adducts and fragments is built using information from CAMERA R package, H. Tong et al., and cliqueMS.: "The default table of adducts and fragments is built using information from CAMERA R package"
- [intro] A subset of the adducts or fragments available in mWISE can be selected for the matching stage. This is strongly recommended, since the expertise of the users with the experimental settings of their: "A subset of the adducts or fragments available in mWISE can be selected for the matching stage"
- [other] Execute mWISE.annotation wrapper function on the negative-mode feature table, which internally performs mass-to-charge ratio matching to KEGG database with adducts and in-source fragments.: "Execute mWISE.annotation wrapper function on the negative-mode feature table, which internally performs mass-to-charge ratio matching to KEGG database with adducts and in-source fragments"
