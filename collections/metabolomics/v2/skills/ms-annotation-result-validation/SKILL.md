---
name: ms-annotation-result-validation
description: Use when after running annotateRC on LC–MS AIF features with fragment
  libraries (e.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3631
  edam_topics:
  - http://edamontology.org/topic_0121
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_0091
  tools:
  - MetaboAnnotatoR
  - R (version or higher)
  - R
  - xcms
  - RamClustR
  - R (version 4.5.0 or higher)
  techniques:
  - LC-MS
  license_tier: restricted
derived_from:
- doi: 10.1021/acs.analchem.1c03032
  title: metaboannotator
evidence_spans:
- MetaboAnnotatoR is designed to perform metabolite annotation of features from LC-MS
  All-ion fragmentation (AIF) datasets
- start R (version "4.5.0" or higher)
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_metaboannotator_cq
    doi: 10.1021/acs.analchem.1c03032
    title: metaboannotator
  dedup_kept_from: coll_metaboannotator_cq
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1021/acs.analchem.1c03032
  all_source_dois:
  - 10.1021/acs.analchem.1c03032
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# MS annotation result validation

> **License: restricted** — no clear open-source license detected for the underlying tool; verify licensing before commercial use or redistribution. <!-- asb-license-banner -->
## Summary

Verify and inspect ranked candidate metabolite annotations from LC–MS All-ion fragmentation data by extracting top-ranked hits, confirming match quality metrics (annotation score, matched ion count), and visualizing experimental spectra against candidate fragmentation patterns. This ensures annotation reliability before downstream interpretation.

## When to use

After running annotateRC on LC–MS AIF features with fragment libraries (e.g., LipidPos), use this skill to confirm that rank-1 candidates have acceptable annotation scores and sufficient matched ion support, and to resolve ambiguous or low-confidence assignments by inspecting spectral overlays.

## When NOT to use

- Input feature table has not yet been processed with annotateRC or another annotation engine — first run annotation before validation.
- Annotations are from targeted methods (e.g., MRM, SRM) where only a single candidate per feature is expected and no ranking is performed.
- Raw LC–MS data has not been processed through xcms and RamClustR; AIF chromatograms must be in centroid mode and clustered before annotation.

## Inputs

- annotations object with rankedResult data from annotateRC
- xcmsSet object (xset) containing LC–MS AIF chromatograms
- RamClustR RC object
- targetTable.csv feature table with m/z, retention time, and feature identifiers

## Outputs

- rank-1 candidate annotation record (name, score, matched ion count per feature)
- summary annotation report listing all rank-1 hits
- spectral overlay plots (experimental vs. candidate) for validated features
- validated annotation table with confidence metadata

## How to apply

Extract the rankedResult object from the annotations output produced by annotateRC. For each feature of interest, retrieve the rank-1 candidate annotation along with its annotation score and matched ion count. Cross-reference the m/z and retention time from the target feature table to ensure correct feature identification. Use plotResultSpec to overlay the experimental spectrum with the candidate's theoretical fragmentation pattern and visually confirm ion matching. Generate a summary report listing candidate name, score, and supporting evidence; features with low matched ion counts or ambiguous spectral overlays warrant inspection of lower-ranked candidates or manual curation. The decision to accept or reject an annotation should account for the number of matched ions relative to the total ions in the experimental spectrum.

## Related tools

- **MetaboAnnotatoR** (Produces ranked candidate annotations and rankedResult object; enables spectral visualization with plotResultSpec function) — https://github.com/gggraca/MetaboAnnotatoR
- **xcms** (Preprocesses and aligns LC–MS AIF chromatograms into feature tables required as input for annotation)
- **RamClustR** (Clusters co-eluting ions and groups them into spectral features before annotation)
- **R (version 4.5.0 or higher)** (Runtime environment for executing annotateRC and validation workflows)

## Examples

```
annotations <- annotateRC(xset, RC, targetTable, DB='LipidPos'); topHit <- annotations$rankedResult[[1]]$rank1; plotResultSpec(annotations, feature=1, rank=1)
```

## Evaluation signals

- Rank-1 candidate m/z and retention time match the target feature coordinates within instrument tolerance
- Annotation score and matched ion count are above acceptable thresholds (thresholds must be set by analyst based on application; evidence of acceptance should be documented)
- Spectral overlay plot shows clear correspondence between experimental fragment peaks and candidate theoretical fragmentation pattern
- Three or more matched ions are present in the experimental spectrum; low-confidence hits (few matched ions) are flagged for manual review
- Summary report can be generated without errors and all features have a rank-1 annotation or explicit null/ambiguous flag

## Limitations

- Annotation quality depends on completeness and accuracy of the fragment library (LipidPos or other); sparse or incorrect library entries will produce false or low-confidence hits.
- MetaboAnnotatoR requires raw LC–MS AIF chromatograms in centroid mode; profile mode data or data from other acquisition methods are not supported.
- In some R environments, installation of MetaboAnnotatoR may fail due to Rcpp version conflicts or i386 architecture issues (documented workarounds exist in README).
- Overlapping m/z or retention time across features may lead to ambiguous spectral assignments; additional separation or manual curation may be required.
- Rank-1 annotation may not always be the correct annotation; visual inspection and domain knowledge are essential for final validation.

## Evidence

- [intro] MetaboAnnotatoR is designed to perform metabolite annotation of features from LC-MS All-ion fragmentation (AIF) datasets, using ion fragment databases: "MetaboAnnotatoR is designed to perform metabolite annotation of features from LC-MS All-ion fragmentation (AIF) datasets, using ion fragment databases"
- [intro] This information can be accessed from the rankedResult object stored in the annotations: "This information can be accessed from the *rankedResult* object stored in the *annotations*"
- [intro] It is possible to visualise the spectra containing the matched ions to each candidate: "It is possible to visualise the spectra containing the matched ions to each candidate"
- [intro] Three out of the six features were annotated with to a lipid: "Three out of the six features were annotated with to a lipid"
- [readme] It requires raw LC-MS AIF chromatograms acquired/transformed in centroid mode.: "It requires raw LC-MS AIF chromatograms acquired/transformed in centroid mode."
