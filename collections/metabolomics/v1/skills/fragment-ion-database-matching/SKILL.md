---
name: fragment-ion-database-matching
description: Use when you have centroid-mode LC-MS AIF chromatograms processed through xcms and RAMClustR, a feature table with target m/z and retention time values, and access to fragment libraries (e.g., LipidPos for lipids).
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3282
  edam_topics:
  - http://edamontology.org/topic_0091
  - http://edamontology.org/topic_3375
  - http://edamontology.org/topic_0121
  tools:
  - MetaboAnnotatoR
  - R
  - xcms
  - RamClustR
derived_from:
- doi: 10.1021/acs.analchem.1c03032
  title: metaboannotator
evidence_spans:
- MetaboAnnotatoR is designed to perform metabolite annotation of features from LC-MS All-ion fragmentation (AIF) datasets
- To install this package, start R (version "4.5.0" or higher)
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v1
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_metaboannotator
    doi: 10.1021/acs.analchem.1c03032
    title: metaboannotator
  dedup_kept_from: coll_metaboannotator
schema_version: 0.2.0
---

# fragment-ion-database-matching

## Summary

Match experimental fragment ions from LC-MS All-ion fragmentation (AIF) spectra against curated ion fragment databases to identify and rank candidate metabolite annotations. This skill converts pseudo-MS/MS spectra from xcms and RAMClustR objects into scored metabolite assignments using the MetaboAnnotatoR annotateRC function.

## When to use

You have centroid-mode LC-MS AIF chromatograms processed through xcms and RAMClustR, a feature table with target m/z and retention time values, and access to fragment libraries (e.g., LipidPos for lipids). Use this skill when you need to annotate unidentified features by matching their observed fragment ions against known metabolite fragmentation patterns and obtain ranked candidate annotations with matching scores.

## When NOT to use

- Your input data are profile-mode (non-centroid) LC-MS chromatograms; MetaboAnnotatoR requires centroid-mode data.
- You do not have xcms and RAMClustR processed objects; the skill depends on these pre-processed intermediate objects.
- Your features have already been assigned confident metabolite identities; annotation scoring and ranking is redundant.

## Inputs

- xcms object (peak-picked LC-MS AIF data)
- RAMClustR object (pseudo-MS/MS spectra)
- feature table (CSV format with m/z, retention time, feature identifiers)
- fragment ion library (e.g., LipidPos, MassBank, or user-generated .csv entries)

## Outputs

- ranked candidate metabolite annotations (with matching scores and rank)
- annotation table (CSV or data frame with feature ID, candidate metabolite name, adduct, m/z match, and score)
- visualized spectra with matched fragment ions (optional)
- annotation results directory with ranked candidates per feature

## How to apply

Load the processed xcms object (containing peak-picked data) and RAMClustR object (containing pseudo-MS/MS spectra) alongside your feature table (targetTable.csv format). Configure the fragment library database source (e.g., LipidPos libraries for lipid annotation). Execute the annotateRC function to match fragment ions from your features against the library, applying internal peak-picking thresholds (noise=0.005 default, mpeaksThres=0.1 default) to filter low-intensity and non-marker peaks. The function will score candidate matches using parameters such as mpeaksScore and mzTol (0.01 default), then rank and return all candidate annotations for each feature. Inspect the ranked results to identify high-confidence candidates; visualize matched ions against the experimental spectrum to verify annotation quality.

## Related tools

- **MetaboAnnotatoR** (Core R package implementing annotateRC function for fragment-ion matching and ranked metabolite annotation) — https://github.com/gggraca/MetaboAnnotatoR
- **xcms** (Upstream preprocessing tool to generate peak-picked LC-MS data required as input to fragment matching)
- **RamClustR** (Upstream preprocessing tool to generate pseudo-MS/MS spectra from AIF data required as input to fragment matching)
- **R** (Runtime environment (version 4.5.0 or higher) for executing MetaboAnnotatoR functions)

## Examples

```
library(MetaboAnnotatoR); annotateRC(RC = RC_obj, xset = xcms_obj, targetTable = targetTable.csv, liblist = list(LipidPos_lib), plotSpectra = TRUE, outDir = './annotations_output')
```

## Evaluation signals

- Verify that annotateRC returns a ranked candidate list for each input feature (no NULL or empty results for valid features).
- Confirm that at least one candidate annotation is assigned per feature with a numeric matching score and rank order.
- Check that matched fragment m/z values fall within the specified mzTol tolerance (default ±0.01) of database entries.
- Validate that high-rank annotations (rank 1) correspond to fragment patterns visually consistent with the experimental spectrum.
- Ensure that the output annotation table schema matches the expected format (feature_id, metabolite_name, adduct_notation, score, rank).

## Limitations

- Annotation quality is limited by completeness and accuracy of the fragment library; missing or poorly-characterized metabolites will not be detected.
- The skill relies on pseudo-MS/MS spectra generated by RAMClustR, which may not recapitulate true MS/MS fragmentation patterns if spectral deconvolution is incomplete.
- Default peak-picking thresholds (noise=0.005, mpeaksThres=0.1) may require manual adjustment for different ionization modes or instrumental platforms.
- No changelog or version history is documented, limiting reproducibility and understanding of past or future methodological changes.
- Ranked candidates are statistical matches; even rank-1 annotations must be visually inspected and cross-validated with orthogonal evidence (e.g., retention time, authentic standards).

## Evidence

- [intro] MetaboAnnotatoR is designed to perform metabolite annotation of features from LC-MS All-ion fragmentation (AIF) datasets, using ion fragment databases: "MetaboAnnotatoR is designed to perform metabolite annotation of features from LC-MS All-ion fragmentation (AIF) datasets, using ion fragment databases"
- [readme] It requires raw LC-MS AIF chromatograms acquired/transformed in centroid mode: "It requires raw LC-MS AIF chromatograms acquired/transformed in centroid mode"
- [intro] a processed dataset composed of two objects: RAMClustR (object containing the pseudo-MS/MS spectra) and an XCMS object containing the peak-picked data: "a processed dataset composed of two objects: RAMClustR (object containing the pseudo-MS/MS spectra) and an XCMS object containing the peak-picked data"
- [intro] annotations can be performed using the annotateRC function: "annotations can be performed using the *annotateRC* function"
- [intro] Peak-picking above noise level threshold (default: 0.005) and marker peak threshold (default: 0.1): "noise=0.005 ... mpeaksThres=0.1"
- [intro] Three out of the six features were annotated with to a lipid when annotateRC is applied to six lipidomics features using the LipidPos library: "Three out of the six features were annotated with to a lipid"
- [other] genFragEntry converts an MS/MS spectrum into a library entry by identifying marker peaks above the mpeaksThres threshold (0.1 default) and noise level (0.005 default), attributing occurrence scores to these peaks, with parameters including mpeaksScore=0.9, mzTol=0.01: "genFragEntry converts an MS/MS spectrum into a library entry by identifying marker peaks above the mpeaksThres threshold (0.1 default) and noise level (0.005 default), attributing occurrence scores"
- [intro] It is also possible to inspect if there were other candidate annotations for a given feature and visualise the spectra containing the matched ions to each candidate: "It is also possible to inspect if there were other candidate annotations for a given feature ... It is possible to visualise the spectra containing the matched ions to each candidate"
