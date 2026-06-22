---
name: acquisition-mode-enumeration-and-validation
description: Use when adopting a mass spectrometry-based analysis tool (e.
license: CC-BY-4.0
metadata:
  edam_topics:
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_0121
  tools:
  - Q-Exactive orbitrap
  - LipidMatch
  - Q-Exactive orbitrap UHPLC-HRMS/MS
  - Agilent Q-TOF UHPLC-HRMS/MS
  - Bruker Q-TOF UHPLC-HRMS/MS
  - SCIEX Q-TOF UHPLC-HRMS/MS
  - MZmine
derived_from:
- doi: 10.1186/s12859-017-1744-3
  title: lipidmatch
evidence_spans:
- tested and validated using Q-Exactive orbitrap UHPLC-HRMS/MS data
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_lipidmatch
    doi: 10.1186/s12859-017-1744-3
    title: lipidmatch
  dedup_kept_from: coll_lipidmatch
schema_version: 0.2.0
---

# acquisition-mode-enumeration-and-validation

## Summary

Systematically enumerate and document the complete matrix of instrument platforms, vendors, and acquisition modes for which a lipidomics software tool (LipidMatch) has been validated, including explicit negative cases. This skill produces a validated compatibility matrix that guides instrument selection and mode configuration for downstream analyses.

## When to use

Apply this skill when adopting a mass spectrometry-based analysis tool (e.g., LipidMatch) and you need to confirm whether your instrument platform, vendor, and acquisition mode combination (targeted, data-dependent top-N, all ion fragmentation, direct infusion, or imaging) are explicitly supported, or when building documentation or decision trees for laboratory deployment that must account for unsupported platforms.

## When NOT to use

- When the tool's documentation does not publicly disclose validated platforms or modes — in this case, contact developers or conduct empirical validation rather than assume coverage
- When your instrument platform is not mentioned in the validated matrix and you lack resources for custom validation — relying on an undocumented platform introduces unquantified failure risk

## Inputs

- GitHub repository URL or local clone of the tool
- Tool README and documentation files
- Supplementary materials and validation study references

## Outputs

- Validated instrument/vendor/mode compatibility matrix (CSV or tabular format)
- Enumeration of supported acquisition modes (targeted, ddMS2-topN, AIF, direct infusion, imaging, etc.)
- Enumeration of supported instrument vendors and models
- Explicit list of unsupported platforms and modes

## How to apply

Clone or download the tool repository and systematically scan the README, documentation, and supplementary materials for explicit statements naming validated instrument platforms (vendor and model), validated acquisition modes (e.g., targeted, ddMS2-topN, AIF, direct infusion, imaging), and any platforms or modes explicitly marked as unsupported. Extract confirmed validated combinations from the repository and any cited validation studies. Construct a tabular CSV matrix with columns for instrument vendor, instrument model, acquisition mode, validation status (supported/unsupported), and supporting reference (evidence location in documentation). Cross-check the matrix against all named platforms and modes mentioned in the source material to ensure completeness. Document negative cases (e.g., Waters instruments) as explicitly unsupported to prevent false assumptions about scope.

## Related tools

- **LipidMatch** (Target tool for which compatibility matrix is constructed; performs lipid identification via matching experimental and simulated fragment m/z values) — https://github.com/GarrettLab-UF/LipidMatch
- **Q-Exactive orbitrap UHPLC-HRMS/MS** (Validated instrument platform with targeted, ddMS2-topN, and AIF acquisition modes)
- **Agilent Q-TOF UHPLC-HRMS/MS** (Validated instrument platform for direct infusion and imaging experiments)
- **Bruker Q-TOF UHPLC-HRMS/MS** (Validated instrument platform for direct infusion and imaging experiments)
- **SCIEX Q-TOF UHPLC-HRMS/MS** (Validated instrument platform for direct infusion and imaging experiments)
- **MZmine** (Compatible peak picking software used upstream of LipidMatch in modular workflow)

## Evaluation signals

- Completeness check: All instrument vendors and models explicitly named in the documentation appear in the final matrix with assigned validation status
- Mode coverage check: All acquisition mode types mentioned (targeted, ddMS2-topN, AIF, direct infusion, imaging) are documented for each supported instrument platform
- Negative case verification: Explicitly unsupported platforms (e.g., Waters) are listed and cross-referenced to the source statement ('does not currently support Waters files')
- Reference traceability: Each matrix row includes a citation or section reference pointing to the exact location in README or documentation supporting that combination's status
- Schema consistency: Matrix columns (vendor, model, mode, status, reference) are populated uniformly across all rows with no missing or ambiguous entries

## Limitations

- The documented matrix reflects validation status at the time of publication; newer instruments or acquisition modes released after publication are not covered and would require empirical testing
- LipidMatch validation for Q-Exactive orbitrap is explicitly documented for targeted, ddMS2-topN, and AIF modes, but other acquisition modes (if they exist on this platform) are not addressed
- Waters platform is explicitly unsupported ('does not currently support Waters files'), but the README does not enumerate which Waters models or file formats are affected, limiting precision of the negative case
- The enumeration reflects software support only; successful use also depends on data quality, sample preparation, and peak-picking accuracy from upstream tools (MZmine, XCMS, MS-DIAL, Compound Discoverer)

## Evidence

- [readme] LipidMatch has been tested and validated using Q-Exactive orbitrap UHPLC-HRMS/MS data obtained from multiple sample types using targeted, data-dependent top-N (ddMS2-topN), and all ion fragmentation (AIF) approaches: "LipidMatch has been tested and validated using Q-Exactive orbitrap UHPLC-HRMS/MS data obtained from multiple sample types using targeted, data-dependent top-N (ddMS2-topN), and all ion fragmentation"
- [readme] LipidMatch has also been applied for the annotation of direct infusion and imaging experiments with Agilent, Bruker and SCIEX Q-TOF platforms: "LipidMatch has also been applied for the annotation of direct infusion and imaging experiments"
- [readme] The software does not currently support Waters files: "The software does not currently support Waters files"
- [readme] LipidMatch is modular, allowing it to fit in various workflows and can be used with various peak picking software: "LipidMatch can be used with various peak picking software (for example MZmine, XCMS, MS-DIAL, and Compound Discoverer)"
