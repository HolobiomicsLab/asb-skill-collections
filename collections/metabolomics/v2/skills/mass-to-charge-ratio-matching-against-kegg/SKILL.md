---
name: mass-to-charge-ratio-matching-against-kegg
description: Use when you have an LC-MS peak-intensity matrix (rows = peaks with m/z and intensity; columns = samples) and need to assign KEGG compound identifiers to observed peaks.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3755
  edam_topics:
  - http://edamontology.org/topic_0121
  - http://edamontology.org/topic_3172
  - http://edamontology.org/topic_0091
  tools:
  - mWISE
  - R
  - KEGG database
  - CAMERA
  - cliqueMS
derived_from:
- doi: 10.1021/acs.analchem.1c00238
  title: mWISE
evidence_spans:
- mWISE (metabolomics Wise Inference of Speck Entities) is an R package that provides tools for context-based annotation of untargeted LC-MS data.
- mWISE (metabolomics Wise Inference of Speck Entities) is an R package
- matching mass-to-charge ratio values to KEGG database
- The default table of adducts and fragments is built using information from CAMERA R package
- The default table of adducts and fragments is built using information from CAMERA R package, H. Tong et al., and cliqueMS.
- information from CAMERA R package, H. Tong et al., and cliqueMS.
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
---

# mass-to-charge-ratio-matching-against-kegg

## Summary

Match observed m/z values from LC-MS peak-intensity matrices to KEGG database compounds by testing all possible neutral mass candidates derived from a precomputed adduct and in-source fragment table. This is the first critical step in untargeted metabolomics annotation, converting raw peaks into candidate metabolite identifiers.

## When to use

You have an LC-MS peak-intensity matrix (rows = peaks with m/z and intensity; columns = samples) and need to assign KEGG compound identifiers to observed peaks. This skill is essential when untargeted LC-MS data annotation is a bottleneck and you have MS1-only peak data (no fragmentation spectra required for matching). Use this before clustering/filtering or network-based prioritization steps.

## When NOT to use

- Peak list is already annotated with confident metabolite identifiers from targeted methods or manual curation — re-matching would be redundant.
- Input lacks m/z values or polarity metadata — matching requires both to derive neutral mass candidates.
- Cpd.Add table is missing or not built from relevant ionization modes or instrument settings — mismatched adduct assumptions will produce low-quality candidates.

## Inputs

- Peak-intensity matrix (rows = peaks with m/z values; columns = sample intensities)
- Cpd.Add table (adduct and fragment reference table with KEGG compounds)
- Polarity setting (negative or positive ionization mode)
- Optional: subset of adducts/fragments for matching stage

## Outputs

- Peak.Cpd candidate table (annotated matrix with peaks as rows, KEGG identifiers and scoring metrics as columns)
- Peak.List (original peak-intensity matrix, preserved for downstream use)

## How to apply

Load the peak-intensity matrix (e.g., Trypanosoma negative-mode dataset) and a Cpd.Add table containing KEGG compounds with precomputed adducts and fragments (built from CAMERA, cliqueMS, and literature sources). Execute the matchingStage function, which tests each observed m/z against all possible neutral masses derived from the Cpd.Add adducts and fragments, optionally filtering adducts by user expertise or observed frequency threshold (default minimum frequency = 0.1). The function returns the original Peak.List and an annotated Peak.Cpd table where each row is a detected peak and columns contain matched KEGG identifiers with associated scoring metrics. The matching tolerates polarity settings (positive/negative mode) and accounts for multiple adduct/fragment hypotheses per peak.

## Related tools

- **mWISE** (Provides the matchingStage function and Peak.Cpd output structure for m/z-to-KEGG annotation) — https://dev.b2s.club/b2slab/mWISE
- **KEGG database** (Source of compound identifiers and exact masses matched against observed m/z values)
- **CAMERA** (Supplies adduct and fragment reference data for the Cpd.Add table construction)
- **cliqueMS** (Contributes adduct and fragment reference data for the Cpd.Add table)
- **R** (Programming environment for loading data and executing matchingStage function)

## Evaluation signals

- Peak.Cpd table row count equals original peak count; no peaks are dropped or duplicated during matching.
- Each peak is assigned at least one KEGG candidate; peaks with zero candidates indicate matching failure and warrant review of adduct/fragment coverage.
- Scoring metrics (e.g., mass error in ppm or Da) fall within expected tolerance ranges for the instrument (typically < 5 ppm for high-resolution LC-MS).
- Candidate KEGG identifiers are valid (e.g., format C######) and correspond to real compounds in the KEGG database version used.
- Matching results are reproducible across independent runs with identical input Cpd.Add table and polarity settings; randomness should not affect peak-to-candidate assignment.

## Limitations

- Matching relies on accurate m/z values and polarity metadata; systematic measurement error or metadata mismatch will degrade candidate quality.
- Adduct/fragment assumptions encoded in Cpd.Add may not cover instrument-specific in-source fragmentation patterns; users with unusual experimental settings should customize the adduct subset before matching.
- Mass-only matching cannot distinguish isomeric compounds; multiple structurally different KEGG candidates may be returned per peak, requiring downstream filtering or orthogonal data.
- Performance and output quality depend critically on Cpd.Add completeness; missing adducts or out-of-date KEGG identifiers lead to false negatives (unmapped peaks) or stale candidates.

## Evidence

- [intro] The matchingStage function accepts a Peak.List (peak-intensity matrix), a Cpd.Add table of KEGG compounds with adducts/fragments, and a polarity setting, and returns a list containing the original Peak.List and an annotated Peak.Cpd table mapping peaks to KEGG candidate compounds.: "The matchingStage function accepts a Peak.List (peak-intensity matrix), a Cpd.Add table of KEGG compounds with adducts/fragments, and a polarity setting, and returns a list containing the original"
- [intro] The matchingStage function from mWISE matches each observed m/z value against the KEGG database by testing all possible neutral mass candidates derived from the Cpd.Add adducts and fragments.: "Execute the matchingStage function from mWISE to match each observed m/z value against the KEGG database by testing all possible neutral mass candidates derived from the Cpd.Add adducts and fragments."
- [intro] The Cpd.Add table is built from adduct and fragment sources including CAMERA, cliqueMS, and literature.: "The default table of adducts and fragments is built using information from CAMERA R package, H. Tong et al., and cliqueMS."
- [intro] Untargeted LC-MS data annotation is a major bottleneck that mWISE addresses through multiple annotation strategies.: "Several computational strategies have been proposed to overcome untargeted LC-MS data annotation, which is still considered a major bottleneck."
- [intro] A subset of adducts or fragments can be selected before matching to improve accuracy based on user expertise and experimental settings.: "A subset of the adducts or fragments available in mWISE can be selected for the matching stage. This is strongly recommended, since the expertise of the users with the experimental settings of their"
- [intro] Cluster-based filtering uses quasi-molecular adducts with optional minimum observed frequency threshold.: "If not, the quasi-molecular adducts available in mWISE, together with the adducts with an observed frequency higher than 0.1 will be used for filtering."
