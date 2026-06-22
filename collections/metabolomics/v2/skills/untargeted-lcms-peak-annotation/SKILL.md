---
name: untargeted-lcms-peak-annotation
description: Use when you have a peak-intensity matrix from untargeted LC-MS analysis (raw detected peaks with m/z and intensity values) and need to assign putative metabolite identities.
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
  - KEGG database
derived_from:
- doi: 10.1021/acs.analchem.1c00238
  title: mWISE
evidence_spans:
- mWISE (metabolomics Wise Inference of Speck Entities) is an R package that provides tools for context-based annotation of untargeted LC-MS data.
- mWISE (metabolomics Wise Inference of Speck Entities) is an R package
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
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1021/acs.analchem.1c00238
  all_source_dois:
  - 10.1021/acs.analchem.1c00238
  zenodo_doi: TODO-zenodo
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# untargeted-lcms-peak-annotation

## Summary

Annotate detected LC-MS peaks by matching their mass-to-charge ratios against a KEGG compound database using precomputed adduct and in-source fragment tables. This skill addresses a major bottleneck in untargeted metabolomics by systematically resolving observed m/z values to candidate metabolites.

## When to use

You have a peak-intensity matrix from untargeted LC-MS analysis (raw detected peaks with m/z and intensity values) and need to assign putative metabolite identities. This skill is triggered when you have unambiguous m/z observations and wish to generate a ranked list of KEGG compound candidates before downstream filtering and network-based prioritization.

## When NOT to use

- Your input is already a feature table or consensus spectrum (matching stage assumes raw, unfiltered peak detection output).
- You lack a validated Cpd.Add adduct/fragment reference table and cannot construct one from CAMERA, cliqueMS, or literature sources.
- Your LC-MS data is targeted (known compound list) rather than untargeted; use a smaller targeted adduct table or direct database lookup instead.

## Inputs

- Peak.List: peak-intensity matrix (n_peaks × 2 numeric matrix with m/z and intensity columns)
- Cpd.Add table: KEGG compounds with precomputed adducts and fragments (data.frame with compound IDs, exact masses, adduct masses, fragment masses)
- polarity: character string ('positive' or 'negative') indicating LC-MS ionization mode
- sample.keggDB: optional—KEGG database reference (data frame of KEGG identifiers and exact masses)

## Outputs

- Peak.Cpd table: annotated peak-to-compound candidates matrix (n_peaks rows, columns include peak ID, m/z, KEGG compound IDs, mass error, adduct type, scoring metrics)
- Matched Peak.List: original peak-intensity matrix with annotation metadata attached

## How to apply

Load your peak-intensity matrix (rows=peaks, columns=m/z and intensity) and a precomputed Cpd.Add table of KEGG compounds with adducts and fragments (typically built from CAMERA, cliqueMS, and literature sources). Execute the matchingStage function from mWISE, specifying the polarity mode (positive or negative) of your LC-MS acquisition. For each observed m/z, the function tests all possible neutral mass candidates by subtracting each adduct/fragment mass from the peak m/z, then searches the KEGG database for exact or near-match compounds. Optional: subset the adduct/fragment list to match your experimental settings (e.g., ESI+ adducts only) to improve specificity. The function returns an annotated Peak.Cpd table where each peak is mapped to matching KEGG identifiers with associated scoring metrics (typically mass error in ppm and adduct type).

## Related tools

- **mWISE** (Provides the matchingStage function and integrates matching, clustering, and diffusion prioritization for peak annotation) — https://dev.b2s.club/b2slab/mWISE
- **KEGG database** (Source database of compound identifiers, exact masses, and chemical properties for peak-to-metabolite matching)
- **CAMERA** (Contributes adduct and fragment rules used to build the default Cpd.Add reference table)
- **cliqueMS** (Contributes adduct and fragment annotation rules used in the Cpd.Add reference table)
- **R** (Execution environment for mWISE package and matchingStage function)

## Examples

```
data(sample.dataset); data(Cpd.Add); result <- matchingStage(Peak.List=sample.dataset$peak.list, Cpd.Add=Cpd.Add, polarity='negative')
```

## Evaluation signals

- Mass error (m/z difference between observed peak and matched KEGG compound neutral mass minus adduct mass) should remain within experimental tolerance, typically ≤ 5 ppm for high-resolution instruments.
- Peak.Cpd table row count matches input Peak.List row count (every detected peak receives at least one candidate match or is flagged as unmatched).
- Adduct type assignments are consistent with the specified polarity mode (e.g., [M+H]+ for positive mode, [M−H]− for negative mode).
- Scoring metrics (e.g., mass error rank, adduct frequency) are populated for all matched candidates; null/NA values indicate no valid match for that peak.
- Spot-check: manually verify 5–10 high-intensity peaks that the assigned KEGG IDs and their neutral masses, when recalculated with the reported adduct, recover the observed m/z within stated tolerance.

## Limitations

- Matching relies on exact mass and adduct mass tables; errors in the Cpd.Add reference table or missing adduct definitions will propagate to false-negative or false-positive annotations.
- Mass accuracy of the LC-MS instrument is critical; low-resolution or poorly calibrated spectra will generate many spurious matches outside the mass tolerance window.
- Isomeric compounds with identical m/z cannot be distinguished at the matching stage; downstream filtering and network diffusion stages are needed to prioritize among candidates.
- The skill does not account for in-source fragmentation patterns unique to specific compounds; all fragment masses in Cpd.Add are treated equivalently.
- Peaks from contaminants, instrumental artifacts, or non-metabolite species are not filtered before matching and will consume KEGG candidates.

## Evidence

- [intro] mWISE (metabolomics Wise Inference of Speck Entities) is an R package that provides tools for context-based annotation of untargeted LC-MS data.: "mWISE (metabolomics Wise Inference of Speck Entities) is an R package that provides tools for context-based annotation of untargeted LC-MS data."
- [intro] The matchingStage function accepts a Peak.List, Cpd.Add table, and polarity setting, and returns a list containing the original Peak.List and an annotated Peak.Cpd table.: "The matchingStage function accepts a Peak.List (peak-intensity matrix), a Cpd.Add table of KEGG compounds with adducts/fragments, and a polarity setting, and returns a list containing the original"
- [intro] untargeted LC-MS data annotation is a major bottleneck in computational metabolomics.: "untargeted LC-MS data annotation is a major bottleneck in computational metabolomics"
- [intro] The default table of adducts and fragments is built using information from CAMERA R package, H. Tong et al., and cliqueMS.: "The default table of adducts and fragments is built using information from CAMERA R package, H. Tong et al., and cliqueMS."
- [intro] matching mass-to-charge ratio values to KEGG database by testing all possible neutral mass candidates derived from the Cpd.Add adducts and fragments.: "match each observed m/z value against the KEGG database by testing all possible neutral mass candidates derived from the Cpd.Add adducts and fragments."
- [intro] A subset of the adducts or fragments available in mWISE can be selected for the matching stage. This is strongly recommended, since the expertise of the users with the experimental settings of their analysis is crucial.: "A subset of the adducts or fragments available in mWISE can be selected for the matching stage. This is strongly recommended, since the expertise of the users with the experimental settings"
