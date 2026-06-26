---
name: adduct-and-fragment-neutral-mass-calculation
description: Use when you have an LC-MS peak-intensity matrix with observed m/z values
  (from negative or positive mode ionization) and need to map each peak to candidate
  neutral masses in KEGG. Use this skill when you have a curated Cpd.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3632
  edam_topics:
  - http://edamontology.org/topic_0091
  - http://edamontology.org/topic_3520
  tools:
  - mWISE
  - R
  - CAMERA
  - cliqueMS
  - KEGG database
  techniques:
  - LC-MS
  license_tier: restricted
  provenance_tier: literature
derived_from:
- doi: 10.1021/acs.analchem.1c00238
  title: mWISE
evidence_spans:
- mWISE (metabolomics Wise Inference of Speck Entities) is an R package that provides
  tools for context-based annotation of untargeted LC-MS data.
- mWISE (metabolomics Wise Inference of Speck Entities) is an R package
- The default table of adducts and fragments is built using information from CAMERA
  R package
- The default table of adducts and fragments is built using information from CAMERA
  R package, H. Tong et al., and cliqueMS.
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
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# adduct-and-fragment-neutral-mass-calculation

> **License: restricted** — no clear open-source license detected for the underlying tool; verify licensing before commercial use or redistribution. <!-- asb-license-banner -->
## Summary

Calculate neutral mass candidates from observed LC-MS peak m/z values by applying precomputed adduct and in-source fragment transformations from a reference table. This is the foundational step in mWISE's matching stage that enables annotation of peaks against the KEGG database.

## When to use

You have an LC-MS peak-intensity matrix with observed m/z values (from negative or positive mode ionization) and need to map each peak to candidate neutral masses in KEGG. Use this skill when you have a curated Cpd.Add reference table (built from CAMERA, cliqueMS, and literature sources) and want to systematically explore all plausible neutral mass interpretations before KEGG compound matching.

## When NOT to use

- Your peaks are already assigned to KEGG compounds or metabolite identities; this skill is for candidate generation, not refinement.
- You lack a polarity specification (negative or positive mode) or the ionization mode is unknown or mixed.
- You have no curated adduct/fragment reference table and cannot construct or download one from CAMERA, cliqueMS, or literature sources.

## Inputs

- Peak.List: peak-intensity matrix (rows = peaks, columns include m/z values)
- Cpd.Add table: reference table of KEGG compounds with precomputed adducts and fragments (mass deltas, ionization modes)
- polarity: ionization mode setting (negative or positive)

## Outputs

- Peak.Cpd candidate table: matrix where each row is a detected peak and columns contain matched KEGG identifiers with scoring metrics
- Peak.List: original peak-intensity matrix (preserved in output list)

## How to apply

Load the Peak.List (peak-intensity matrix with m/z column) and the Cpd.Add table containing adducts and fragments with their mass deltas and ionization modes. For each observed m/z, apply the inverse transformation of each applicable adduct/fragment (e.g., subtract the adduct mass delta or add back the fragment mass loss) to recover candidate neutral masses. Filter adducts/fragments by polarity setting (negative or positive mode) to avoid incorrect candidates. The matchingStage function in mWISE automates this process: it tests all possible neutral mass candidates derived from the Cpd.Add adducts and fragments for each observed peak, then returns an annotated Peak.Cpd table mapping each peak to KEGG identifiers with associated scoring metrics.

## Related tools

- **mWISE** (Implements matchingStage function that orchestrates neutral mass calculation and KEGG candidate matching) — https://dev.b2s.club/b2slab/mWISE
- **CAMERA** (Source of default adduct and fragment definitions used to build the Cpd.Add reference table)
- **cliqueMS** (Contributes adduct and fragment information to the Cpd.Add reference table)
- **R** (Execution environment for mWISE and the matchingStage function)
- **KEGG database** (Source of compound identifiers and exact masses matched against calculated neutral mass candidates)

## Examples

```
data(sample.dataset); data(Cpd.Add); result <- matchingStage(Peak.List = sample.dataset$Peak.List, Cpd.Add = Cpd.Add, polarity = 'negative')
```

## Evaluation signals

- The output Peak.Cpd table has one row per input peak and includes valid KEGG identifiers in matched candidate columns.
- No negative or null neutral masses are produced; all calculated masses are physically plausible (typically 50–2000 Da for small metabolites).
- Adduct/fragment filtering by polarity is correct: negative-mode peaks are matched only against adducts/fragments appropriate for negative ionization, and vice versa.
- A spot-check of 3–5 peaks confirms that at least one calculated neutral mass per peak falls within expected mass tolerance (typically ±5 ppm) of a known KEGG compound.
- The Peak.Cpd output is a matrix or data frame with consistent schema (peak identifiers, KEGG IDs, scores) matching the mWISE Peak.Cpd specification.

## Limitations

- Accuracy depends on completeness and correctness of the Cpd.Add table; missing or incorrectly parameterized adducts/fragments will produce incomplete or incorrect candidates.
- Multiple neutral masses from a single observed m/z may be equally plausible within mass tolerance, leading to ambiguous candidate lists; downstream filtering (clustering, network diffusion) is required to prioritize.
- In-source fragmentation patterns are heuristic and may not capture all adduct/fragment possibilities for complex matrices or unusual ionization conditions.
- No integration of retention time, isotope patterns, or spectral similarity at this stage; those signals are used only in later mWISE stages (diffusion prioritization).

## Evidence

- [intro] matching mass-to-charge ratio values to KEGG database using adducts and in-source fragments: "matching mass-to-charge ratio values to KEGG database using adducts and in-source fragments"
- [intro] The matchingStage function accepts a Peak.List (peak-intensity matrix), a Cpd.Add table of KEGG compounds with adducts/fragments, and a polarity setting, and returns a list containing the original Peak.List and an annotated Peak.Cpd table mapping peaks to KEGG candidate compounds.: "The matchingStage function accepts a Peak.List (peak-intensity matrix), a Cpd.Add table of KEGG compounds with adducts/fragments, and a polarity setting, and returns a list containing the original"
- [intro] the matchingStage function from mWISE to match each observed m/z value against the KEGG database by testing all possible neutral mass candidates derived from the Cpd.Add adducts and fragments.: "the matchingStage function from mWISE to match each observed m/z value against the KEGG database by testing all possible neutral mass candidates derived from the Cpd.Add adducts and fragments."
- [intro] The default table of adducts and fragments is built using information from CAMERA R package: "The default table of adducts and fragments is built using information from CAMERA R package"
- [intro] mWISE (metabolomics Wise Inference of Speck Entities) is an R package that provides tools for context-based annotation of untargeted LC-MS data.: "mWISE (metabolomics Wise Inference of Speck Entities) is an R package that provides tools for context-based annotation of untargeted LC-MS data."
