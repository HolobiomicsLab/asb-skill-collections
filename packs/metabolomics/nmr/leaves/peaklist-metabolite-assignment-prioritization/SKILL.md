---
name: peaklist-metabolite-assignment-prioritization
description: Use when you have extracted m/z and retention time (m/z-RT) information
  for peaks from untargeted LC/HRMS data (using tools like IDSL.IPA) and need to assign
  molecular formula identities to those peaks.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3631
  edam_topics:
  - http://edamontology.org/topic_0599
  - http://edamontology.org/topic_3172
  tools:
  - IDSL.UFA
  - IDSL.IPA
  - R
  techniques:
  - CE-MS
  - NMR
  license_tier: open
  provenance_tier: literature
derived_from:
- doi: 10.1021/acs.analchem.2c00563
  title: IDSL.UFA
evidence_spans:
- '**United Formula Annotation (UFA)** by the [**Integrated Data Science Laboratory
  for Metabolomics and Exposomics (IDSL.ME)**](https://www.idsl.me/) is a light-weight
  R package'
- annotate peaklists from the IDSL.IPA package with molecular formula
- light-weight R package
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_idsl_ufa_cq
    doi: 10.1021/acs.analchem.2c00563
    title: IDSL.UFA
  dedup_kept_from: coll_idsl_ufa_cq
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1021/acs.analchem.2c00563
  all_source_dois:
  - 10.1021/acs.analchem.2c00563
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# Molecular formula annotation of peaklists using isotopic profile matching

## Summary

Assign molecular formulas to detected peaks in LC/HRMS peaklists by matching observed MS1 isotopic patterns against theoretical isotopic profiles predicted for candidate formulas from a prioritized chemical space. This MS1-only approach enables annotation without requiring MS2 fragmentation data.

## When to use

Use this skill when you have extracted m/z and retention time (m/z-RT) information for peaks from untargeted LC/HRMS data (using tools like IDSL.IPA) and need to assign molecular formula identities to those peaks. Apply it particularly when MS2 spectral data is unavailable or when you are analyzing exposomics or metabolomics samples where formulas from multiple chemical sources (beyond common metabolite databases) are expected.

## When NOT to use

- When MS1 isotopic pattern resolution is insufficient—e.g., low-resolution mass spectrometry data where 13C and 12C peaks are not baseline-resolved.
- When the candidate chemical space is unknown or extremely broad (e.g., all possible organic compounds). The skill relies on a prioritized, curated IPDB; if no appropriate formula database exists for your sample type, annotation accuracy will suffer.
- When peaks have already been assigned molecular formulas via orthogonal methods (e.g., MS2-based spectral matching or NMR). This skill complements but does not replace MS2-based structural annotation.

## Inputs

- peaklist table with m/z, retention time, and intensity values (output from IDSL.IPA or equivalent peak detection tool)
- MS1-level LC/HRMS raw data files (mzXML, mzML, or netCDF format)
- prioritized in-silico isotopic profile database (IPDB) in Rdata format, indexed by molecular formula and ionization mode

## Outputs

- annotated peaklist table with columns: original m/z, intensity, assigned molecular formula, isotopic matching score, and confidence ranking
- batch-level isotopic profile match figures (visualizing observed vs. theoretical patterns)
- aggregated molecular formula assignments aligned across multiple samples in population-scale studies

## How to apply

First, generate or obtain a prioritized in-silico isotopic profile database (IPDB) by computing theoretical isotopic distributions for candidate molecular formulas using IUPAC atomic mass tables and combinatorial rules. For each detected peak with m/z and intensity values, extract its observed MS1 isotopic pattern (the set of m/z-intensity pairs corresponding to different isotopologue masses). Compare this observed pattern against the theoretical isotopic profiles in the IPDB using matching criteria (typically correlation or cosine similarity of relative intensities). Rank candidate formulas by isotopic profile matching score and assign the top-ranked formula to the peak. The workflow prioritizes chemical space—typically curated reference metabolite databases like RefMet—so that higher-confidence formula assignments are favored. Output an annotated peaklist table with original m/z, intensity, assigned molecular formula, and the isotopic matching score to enable downstream validation and filtering.

## Related tools

- **IDSL.UFA** (R package that performs isotopic profile matching and molecular formula ranking against MS1 data; core tool for executing this skill) — https://github.com/idslme/IDSL.UFA
- **IDSL.IPA** (R package that generates peaklists (m/z-RT-intensity) from raw LC/HRMS data; prerequisite input generator for IDSL.UFA workflow) — https://github.com/idslme/IDSL.IPA
- **R** (Computing language and environment for running IDSL.UFA and IDSL.IPA packages)

## Examples

```
library(IDSL.UFA)
UFA_workflow("path/to/UFA_parameters.xlsx")
```

## Evaluation signals

- Assigned molecular formulas have isotopic matching scores above a specified threshold (e.g., cosine similarity > 0.7 or correlation coefficient > 0.8), indicating close agreement between observed and theoretical isotopic patterns.
- Annotation consistency: when the same peak is observed in multiple samples, the assigned molecular formula should be identical or the top-ranked candidate across replicates.
- Mass accuracy: the observed m/z of the monoisotopic peak should match the theoretical m/z of the assigned formula within the instrument's mass tolerance (typically ≤ 5 ppm for Orbitrap instruments).
- Isotopic peak presence: the observed MS1 spectrum should contain intensity peaks at all major predicted 13C, 2H, 15N, 18O, etc. isotopologue m/z values with relative intensities consistent with theoretical predictions.
- Formula chemical validity: assigned formulas should obey electron valence rules (e.g., even-electron ions) and fall within plausible elemental composition ranges for the sample type (e.g., C, H, N, O, S, P limits for metabolites).

## Limitations

- Isotopic pattern matching is most reliable for monoisotopic masses m/z ≥ 150; at lower m/z, natural isotope abundances are smaller and isotopic patterns are sparse, reducing discrimination power between candidate formulas.
- The skill requires high-resolution MS1 data (resolving power R ≥ 60,000 at m/z 400 recommended for Orbitrap instruments) to resolve 12C/13C and other isotopologue peaks; low-resolution data will not support reliable isotopic profile matching.
- Annotation depends critically on the completeness and quality of the prioritized chemical space database (IPDB). Compounds absent from or misrepresented in the database cannot be assigned. For novel or non-metabolite compounds (e.g., environmental contaminants, industrial chemicals), custom IPDBs may be required.
- Isobaric or near-isobaric formulas (formulas with identical or very similar m/z) may not be distinguishable by MS1 isotopic pattern alone; MS2 data or additional chromatographic separation is needed for disambiguation.
- The presence of adducts, in-source fragments, or overlapping peaks in the MS1 spectrum can distort observed isotopic patterns and degrade formula assignment accuracy; peak curation before annotation is recommended.

## Evidence

- [intro] IDSL.UFA enables molecular formula annotation using isotopic profile matching with only MS1 data: "annotate peaklists from the IDSL.IPA package with molecular formula of a prioritized chemical space using an isotopic profile matching approach. The IDSL.UFA pipeline only requires MS1"
- [other] The workflow compares observed MS1 isotopic patterns against predicted patterns for candidate formulas: "For each detected peak, perform isotopic profile matching by comparing the observed MS1 isotopic pattern against predicted patterns for candidate molecular formulas in the chemical space"
- [other] Candidate formulas are ranked by isotopic profile similarity and the top-ranked is assigned: "Rank candidate formulas by isotopic profile similarity and assign the top-ranked formula to each peak"
- [readme] IDSL.UFA generates in-silico theoretical libraries using natural isotopic distribution profiles: "Generating comprehensive *in-silico* theoretical libraries (known as [IPDB](https://github.com/idslme/IDSL.UFA/wiki/Isotopic-Profile-DataBase-(IPDB))) using natural isotopic distribution profiles"
- [readme] Molecular formulas are a fundamental property for gaining biological insights from metabolomics: "***molecular formulas*** are fundamental property of chemical compounds and represent their elemental compositions. Assigning molecular formulas to peaks in data generated using untargeted LC/HRMS"
- [readme] Isotopic patterns are predicted using IUPAC atomic mass tables and combinatorial rules: "The theoretical isotopic profile of carbon-containing compounds can be accurately predicted using a set of combinatorial rules that uses atomic mass tables provided by the [International Union of"
- [readme] The skill supports MS1-only analysis for population-scale studies: "Analyzing population size untargeted studies (n > 500)"
