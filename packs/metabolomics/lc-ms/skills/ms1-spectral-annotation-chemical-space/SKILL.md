---
name: ms1-spectral-annotation-chemical-space
description: Use when you have (1) a peaklist from untargeted LC/HRMS analysis with m/z and intensity values (typically output from IDSL.IPA or similar peak-picking tools), (2) a need to assign molecular formulas to detected peaks, and (3) only MS1 spectral data available (MS/MS is not required).
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3632
  edam_topics:
  - http://edamontology.org/topic_3172
  - http://edamontology.org/topic_0121
  tools:
  - IDSL.UFA
  - IDSL.IPA
  - R
  techniques:
  - LC-MS
derived_from:
- doi: 10.1021/acs.analchem.2c00563
  title: IDSL.UFA
evidence_spans:
- '**United Formula Annotation (UFA)** by the [**Integrated Data Science Laboratory for Metabolomics and Exposomics (IDSL.ME)**](https://www.idsl.me/) is a light-weight R package'
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
  zenodo_doi: TODO-zenodo
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# MS1 Spectral Annotation with Isotopic Profile Matching Against Prioritized Chemical Space

## Summary

Annotate untargeted LC/HRMS peaklists with molecular formulas by matching observed MS1 isotopic patterns against theoretically predicted profiles from a prioritized chemical space database. This approach requires only MS1 data and is particularly valuable for exposomics and metabolomics studies where compounds originate from diverse formula sources beyond common metabolite databases.

## When to use

Apply this skill when you have (1) a peaklist from untargeted LC/HRMS analysis with m/z and intensity values (typically output from IDSL.IPA or similar peak-picking tools), (2) a need to assign molecular formulas to detected peaks, and (3) only MS1 spectral data available (MS/MS is not required). It is especially suitable for population-scale studies (n > 500) and when you need to annotate compounds from broad chemical spaces including non-metabolite compounds.

## When NOT to use

- MS/MS (MS2) spectral data is available and structural (not just molecular formula) annotation is the primary goal — consider using tools that exploit fragmentation patterns for higher specificity.
- The input peaklist is already fully annotated with chemical identities — molecular formula assignment adds no new information.
- Chemical space is highly constrained and known in advance (e.g., a targeted panel of ~50 metabolites) — simpler exact-mass database matching may be more appropriate than isotopic profile matching.
- MS1 resolution is insufficient to resolve isotopic fine structure (e.g., low-resolution or time-of-flight instruments with m/z error > 10 ppm) — isotopic profile matching relies on accurate m/z spacing and relative intensities.

## Inputs

- IDSL.IPA-formatted peaklist with m/z, retention time, and intensity values
- High-resolution MS1 spectral data (mzXML, mzML, or netCDF format)
- Isotopic Profile DataBase (IPDB) in Rdata format for the target chemical space and ionization mode
- UFA parameter spreadsheet with configured PARAM0004 (IPDB address), PARAM0009 (MS1 data location), PARAM0011 (peaklists directory), and PARAM0012 (peak_alignment directory)

## Outputs

- Annotated peaklist table with original m/z, intensity, assigned molecular formula, and isotopic matching score for each peak
- Batch untargeted isotopic profile match figures showing observed vs. theoretical patterns
- Aggregated molecular formula assignments aligned across the peak table to capture formula consensus and recurring ion patterns

## How to apply

First, process your raw MS data (mzXML, mzML, or netCDF format) through IDSL.IPA to extract chromatographic peak information (m/z and retention time). Next, download or generate a pre-calculated Isotopic Profile DataBase (IPDB) corresponding to your ionization mode (positive or negative) and chemical space (e.g., RefMetDB for metabolites). Load the IDSL.IPA peaklist into IDSL.UFA and configure parameters including the IPDB address and MS1 data location. For each detected peak, IDSL.UFA calculates the theoretical isotopic distribution for candidate molecular formulas in the prioritized chemical space and ranks candidates by isotopic profile similarity (matching observed m/z, intensity ratios, and spacing to predictions). Assign the top-ranked formula to each peak, then aggregate results across the aligned peak table to handle recurring adducts and fragment ions. The isotopic matching score and candidate ranking enable prioritization of likely correct assignments.

## Related tools

- **IDSL.UFA** (Primary tool that performs isotopic profile matching and molecular formula annotation of peaklists using a prioritized chemical space) — https://github.com/idslme/IDSL.UFA
- **IDSL.IPA** (Upstream peak-picking and peaklist generation tool that produces the m/z-RT chromatographic information required as input to IDSL.UFA) — https://github.com/idslme/IDSL.IPA
- **R** (Programming language and runtime environment for executing IDSL.UFA and IDSL.IPA workflows)

## Examples

```
library(IDSL.UFA)
UFA_workflow("path/to/UFA_parameters.xlsx")
```

## Evaluation signals

- Annotated peaklist contains a molecular formula assignment and isotopic matching score for each input peak; no missing values in the formula column for peaks above the SNR threshold.
- Isotopic matching scores are in a reasonable range (typically 0–1 or 0–100% depending on scoring scheme); scores near 1.0 or 100% indicate close agreement between observed and theoretical isotopic patterns.
- Batch isotopic profile match figures show visual alignment between observed and predicted isotopic envelopes for representative peaks, confirming that m/z spacing and relative intensities are accurately matched.
- Aggregated formula table shows expected clustering of formulas across aligned peaks, with recurring ion masses (e.g., adducts, in-source fragments) assigned consistent formulas after aggregation.
- Formula assignments respect known chemical constraints (e.g., integer counts of C, H, N, O, S; valence rules; no implausible elemental ratios) and match reference databases when available.

## Limitations

- Isotopic profile matching depends critically on MS1 mass accuracy and resolution; errors > 5–10 ppm or insufficient isotopic fine structure can lead to incorrect or ambiguous formula assignments.
- The method is restricted to the prioritized chemical space encoded in the IPDB; compounds not represented in that space cannot be annotated, even if they are present in the sample.
- Multiple molecular formulas may produce nearly identical isotopic patterns (e.g., isotopologues or isobars); the method ranks candidates but cannot always resolve ambiguity without MS/MS or other orthogonal data.
- No changelog is available for IDSL.UFA, limiting transparency regarding bug fixes, performance improvements, or changes in scoring algorithms across versions.
- Parallel processing in Windows and Linux is supported, but performance and cross-platform consistency have not been independently validated in all environments.

## Evidence

- [readme] annotate peaklists from the IDSL.IPA package with molecular formula of a prioritized chemical space using an isotopic profile matching approach. The IDSL.UFA pipeline only requires MS1: "annotate peaklists from the IDSL.IPA package with molecular formula of a prioritized chemical space using an isotopic profile matching approach. The IDSL.UFA pipeline only requires MS1"
- [readme] molecular formulas are fundamental property of chemical compounds and represent their elemental compositions. Assigning molecular formulas to peaks in data generated using untargeted LC/HRMS can help in gaining biological insights from metabolomics and exposomics datasets.: "Assigning molecular formulas to peaks in data generated using untargeted LC/HRMS can help in gaining biological insights from metabolomics and exposomics datasets."
- [readme] Because of the naturally occuring isotope atoms for each element, MS1 spectral data have more than one mass to charge ratio (m/z) values observed for an ionized species. The isotopic pattern for a chemical structure can be accurately predicted using a set of combinatorial rules that uses atomic mass tables: "The isotopic pattern for a chemical structure can be accurately predicted using a set of combinatorial rules that uses atomic mass tables"
- [readme] Generating comprehensive in-silico theoretical libraries (known as IPDB) using natural isotopic distribution profiles: "Generating comprehensive in-silico theoretical libraries (known as IPDB) using natural isotopic distribution profiles"
- [readme] Aggregating annotated molecular formulas on the aligned peak table. This is a very unique feature that is only presented by IDSL.UFA.: "Aggregating annotated molecular formulas on the aligned peak table. This is a very unique feature that is only presented by IDSL.UFA."
- [readme] Analyzing population size untargeted studies (n > 500): "Analyzing population size untargeted studies (n > 500)"
- [readme] there is still unmet needs to improve the workflow for larger studies and various sources of molecular formula. This is important for exposomics studies where we do expect to see many more compounds from formula sources other than common metabolite databases.: "exposomics studies where we do expect to see many more compounds from formula sources other than common metabolite databases."
