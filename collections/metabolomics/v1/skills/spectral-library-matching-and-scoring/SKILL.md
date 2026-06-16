---
name: spectral-library-matching-and-scoring
description: Use when when you have MS/MS fragment spectra (in .mgf format) acquired from unknown metabolite features and need to annotate them against known compounds.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3631
  edam_topics:
  - http://edamontology.org/topic_0121
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_0625
  tools:
  - R
  - LOTUS
  - ISDB
  - MassBank
  - SIRIUS
  - GNPS-FBMN
  - tima R package
derived_from:
- doi: 10.3389/fpls.2019.01329
  title: tima
- doi: 10.5281/zenodo.3378723
  title: ''
evidence_spans:
- The initial work is available at <https://doi.org/10.3389/fpls.2019.01329>
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v1
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_tima
    doi: 10.3389/fpls.2019.01329
    title: tima
  dedup_kept_from: coll_tima
schema_version: 0.2.0
---

# spectral-library-matching-and-scoring

## Summary

Match experimental MS/MS spectra against reference spectral libraries and score similarity to identify metabolites. This skill integrates multiple spectral databases (LOTUS, ISDB, MassBank, in-house libraries) with customizable scoring algorithms to rank candidate compound matches in the context of taxonomically informed annotation.

## When to use

When you have MS/MS fragment spectra (in .mgf format) acquired from unknown metabolite features and need to annotate them against known compounds. Apply this skill after feature detection and spectra acquisition, particularly when analyzing organisms or sample types with known metabolite compositions that can be leveraged for filtering candidates.

## When NOT to use

- Input spectra lack sufficient quality (very few fragments, low signal-to-noise) to produce reliable matches.
- Library databases do not cover the expected metabolite diversity of your samples (e.g., matching against LOTUS alone when analyzing synthetic compounds or organisms with poorly sampled chemodiversity).
- MS/MS acquisition was not performed or spectra are unavailable; only MSⁿ or low-resolution MS data are available.

## Inputs

- MS/MS spectra file (.mgf format) containing fragment spectra for experimental features
- Feature quantification table with feature ID, m/z, retention time, and sample intensities
- Reference spectral libraries (LOTUS, ISDB, MassBank, or custom .msp files)
- Sample metadata linking samples to organism taxonomy (for filtering library searches)

## Outputs

- Annotated feature table with matched compound identifiers, chemical structures, and match scores
- Ranked candidate list per feature with cosine similarity or other scoring metrics
- Library-matched spectra alignments showing experimental vs. reference fragment patterns

## How to apply

Load your experimental MS/MS spectra (.mgf) and select one or more reference spectral libraries (LOTUS with >650k structure–organism pairs is provided as default; ISDB, MassBank, and custom spectral libraries in .msp format can also be integrated). The tima pipeline performs spectral matching by comparing fragment ion patterns, neutral losses, and precursor m/z values against library entries. Candidate matches are scored based on cosine similarity or other similarity metrics to rank putative identifications. Scoring thresholds and library selection are configurable via the Shiny app interface or YAML parameters. Validate matches by inspecting alignment of experimental and theoretical fragment masses, considering instrumental mass accuracy (typically <5 ppm tolerance for high-resolution MS), and optionally cross-referencing with external annotations from SIRIUS or GNPS-FBMN. Filter results by score cutoff and organism relevance before reporting final annotations.

## Related tools

- **LOTUS** (Provides >650k structure–organism pairs as default spectral and structural reference library for matching and filtering candidates by taxonomy) — https://lotusnprod.github.io/lotus-manuscript/
- **ISDB** (In Silico spectral database for matching experimental spectra against computationally predicted fragment patterns)
- **MassBank** (Community spectral reference library integrated into tima for experimental MS/MS spectrum matching) — https://doi.org/10.5281/zenodo.3378723
- **SIRIUS** (External annotation tool (v5/v6) providing molecular formula and structure predictions that can be integrated alongside spectral library matches)
- **GNPS-FBMN** (External spectral networking results that can be incorporated to contextualize and validate spectral matches)
- **tima R package** (Orchestrates spectral matching workflow, scoring, and library integration via command-line, YAML, or interactive Shiny interface) — https://github.com/taxonomicallyinformedannotation/tima

## Examples

```
tima::run_app()
# Or via CLI after configuration:
# Rscript -e "tima::run_tima(config='params.yaml')"
```

## Evaluation signals

- All experimental features with MS/MS spectra are assigned at least one library match with a non-null similarity score.
- Top-ranked matches have cosine similarity or equivalent scores above a defined threshold (e.g., >0.7 for high confidence).
- Matched fragments in experimental spectra align with theoretical fragment masses within expected m/z tolerance (typically <5 ppm for high-resolution instruments).
- Matched compounds are chemically and taxonomically plausible given the source organism(s) and sample context.
- No score inversions: candidate ranks are monotonically decreasing by similarity score; ties are documented.

## Limitations

- Spectral library matching sensitivity depends on library completeness; rare, novel, or understudied metabolites may lack reference spectra and fail to match.
- Isomeric compounds with identical or near-identical MS/MS fragmentation patterns cannot be resolved by spectral matching alone; additional orthogonal data (e.g., retention time, NMR, chemical derivatization) are required.
- Custom spectral libraries (.msp format) require manual curation and may harbor errors or inconsistent metadata that propagate to false-positive matches.
- High-molecular-weight compounds or those with few characteristic fragments may produce low-scoring matches across multiple candidates, reducing specificity.

## Evidence

- [readme] Spectral library matching integrates LOTUS, ISDB, MassBank, and custom libraries: "**Structure-organism pairs library** - We provide **LOTUS** (>650k pairs) as default ... **Custom spectral libraries** - For in-house compound matching"
- [readme] Input spectra are matched via similarity scoring against reference libraries: "**MS/MS spectra file** (.mgf) - Fragment spectra for each or some features"
- [readme] Scoring and library selection are configurable parameters: "All column names and file paths are customizable through the Shiny app interface or YAML/CLI parameters"
- [readme] SIRIUS and GNPS results can be integrated as external annotations alongside spectral matches: "**External annotations** - SIRIUS (v5/v6), GNPS-FBMN results"
- [other] Workflow applies taxonomically informed filtering to spectral matching: "The workflow is illustrated below. This repository contains everything needed to perform **T**axonomically **I**nformed **M**etabolite **A**nnotation."
