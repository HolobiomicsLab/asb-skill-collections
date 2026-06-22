---
name: spectral-library-matching-gnps
description: Use when you have MS2 product-ion spectra in open formats (.mzML or .mzXML) from public mass spectrometry datasets (e.g., from MassIVE with a valid accession) and need to identify chemical compounds by comparing fragmentation patterns against the GNPS reference spectral library.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3631
  edam_topics:
  - http://edamontology.org/topic_3172
  - http://edamontology.org/topic_0121
  tools:
  - GNPS
  - MassIVE
  - ReDU
  - Emperor
  techniques:
  - CE-MS
  - NMR
derived_from:
- doi: 10.1038/s41592-020-0916-7
  title: ReDU
- doi: 10.1186/2047-217x-2-16
  title: ''
evidence_spans:
- a free GNPS account is required to analyze data
- free GNPS account is required to analyze data
- ReDU only interacts with MassIVE
- data uploaded to MassIVE as a public dataset
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_redu_cq
    doi: 10.1038/s41592-020-0916-7
    title: ReDU
  dedup_kept_from: coll_redu_cq
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1038/s41592-020-0916-7
  all_source_dois:
  - 10.1038/s41592-020-0916-7
  - 10.1186/2047-217x-2-16
  zenodo_doi: TODO-zenodo
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# spectral-library-matching-gnps

## Summary

Spectral library matching in GNPS compares MS2 product-ion spectra against a public reference fragmentation library to generate chemical annotations with cosine similarity scores. This skill is essential for converting raw tandem mass spectrometry data into a binary detection matrix (files × chemicals) suitable for downstream ecological or chemical discovery analysis.

## When to use

Apply this skill when you have MS2 product-ion spectra in open formats (.mzML or .mzXML) from public mass spectrometry datasets (e.g., from MassIVE with a valid accession) and need to identify chemical compounds by comparing fragmentation patterns against the GNPS reference spectral library. Use it as the annotation step prior to constructing detection matrices or performing metabolite co-occurrence analysis across multiple samples or files.

## When NOT to use

- Input spectra are already in proprietary binary formats (e.g., .raw, .d) without prior conversion to .mzML or .mzXML—file format conversion must precede this skill.
- Data is private or restricted-access; GNPS spectral library matching requires public or openly shareable data uploaded to MassIVE.
- You require MS1-level feature detection or untargeted metabolomics quantification rather than spectral annotation—this skill provides presence/absence annotations, not quantitative abundance values.

## Inputs

- MS2 product-ion spectra in open format (.mzML or .mzXML)
- Valid MassIVE accession identifier for public dataset
- GNPS account credentials

## Outputs

- Spectral library matching results table (chemical annotations, m/z, cosine similarity scores)
- Binary detection matrix (rows=files, columns=chemicals, values=0/1)
- Tab-separated detection matrix file (.tsv)

## How to apply

First, ensure MS2 spectra are in open format (.mzML or .mzXML) and uploaded to a public MassIVE repository with a MassIVE accession ID. Launch the GNPS spectral library matching workflow via the GNPS web interface (https://gnps.ucsd.edu/) with default parameters, submitting the spectra against the GNPS reference spectral library. Upon workflow completion, retrieve the tabulated spectral library matching results containing matched chemical annotations, m/z values, and cosine similarity scores. Parse the output table to construct a binary detection matrix where rows represent files, columns represent chemical identities, and cell values indicate detection (1) or absence (0) of each chemical per file. Export this matrix as a tab-separated (.tsv) file for integration into visualization or statistical workflows (e.g., Emperor PCA, chemical enrichment analysis). Note that the same chemical may yield multiple GNPS annotations due to slight MS2 spectral variations (m/z or abundance differences).

## Related tools

- **GNPS** (Performs spectral library matching by comparing MS2 product-ion spectra against reference fragmentation patterns in the public GNPS spectral library) — https://gnps.ucsd.edu/ProteoSAFe/static/gnps-splash.jsp
- **MassIVE** (Public mass spectrometry data repository; stores and provides access to MS2 spectra datasets required for GNPS spectral library matching) — https://massive.ucsd.edu/ProteoSAFe/static/massive.jsp
- **ReDU** (User interface and bridge connecting MassIVE data to GNPS workflows; facilitates batch spectral library search and sample information curation for co-analysis of public MS2 data) — https://github.com/mwang87/ReDU-MS2-GNPS
- **Emperor** (Visualization and exploratory analysis tool for plotting GNPS annotation results (e.g., PCA score plots) and exploring chemical detection patterns across files) — https://github.com/biocore/emperor

## Evaluation signals

- Verify that the spectral library matching results table contains non-empty rows for each submitted file with matched chemical names, m/z values, and cosine similarity scores.
- Check that the binary detection matrix has consistent dimensions (number of files × number of unique chemical annotations) and contains only 0 or 1 values.
- Confirm that the number of files in the detection matrix matches the number of MS2 files submitted to GNPS and the count reported in the MassIVE File Selector.
- Validate that cosine similarity scores for matched compounds fall within expected range (typically 0.7–1.0 for high-confidence library matches; threshold varies by analysis goal).
- Cross-check that chemicals appearing multiple times in the GNPS output (due to slight MS2 spectral variation) are correctly deduplicated or flagged in downstream analysis, ensuring count of unique chemical annotations is reasonable and interpretable.

## Limitations

- GNPS annotations via spectral library matching are classified as level 2 (putative annotation based on spectral library similarity) or level 3 (putatively characterized compound class) per the 2007 metabolomics standard initiative—not confirmed structure identifications. Chemical validation via orthogonal methods (e.g., NMR, standards) is required for higher confidence.
- The same chemical can yield multiple GNPS annotations due to minor MS2 spectral variations in m/z or abundance, potentially inflating the count of unique chemicals in the detection matrix and complicating interpretation of chemical diversity.
- GNPS spectral library matching is limited to compounds present in the reference spectral library; novel or rare compounds not in the library will not be annotated, leading to false negatives in the detection matrix.
- Workflow assumes data is already in open-source format (.mzML or .mzXML); proprietary instrument formats require prior conversion, which may introduce artifacts or data loss depending on conversion tool and parameters.

## Evidence

- [other] GNPS library search compares MS2 product-ion spectra against reference fragmentation patterns in its public spectral library, producing tabulated chemical annotations with file detection information—a matrix where cells indicate whether each chemical was detected (1) or not detected (0) in each file.: "GNPS library search compares MS2 product-ion spectra against reference fragmentation patterns in its public spectral library, producing tabulated chemical annotations with file detection"
- [other] Retrieve MS2 spectra in open format (.mzML or .mzXML) from a public MassIVE dataset with a valid MassIVE accession. Launch the GNPS spectral library matching workflow via the GNPS interface with default parameters, submitting the MS2 spectra against the GNPS reference spectral library.: "Retrieve MS2 spectra in open format (.mzML or .mzXML) from a public MassIVE dataset with a valid MassIVE accession. Launch the GNPS spectral library matching workflow via the GNPS interface with"
- [other] Parse the GNPS output to construct a binary detection matrix (rows = files, columns = chemical identities, values = 1 for detected, 0 for not detected) and export as a tab-separated table.: "Parse the GNPS output to construct a binary detection matrix (rows = files, columns = chemical identities, values = 1 for detected, 0 for not detected) and export as a tab-separated table."
- [methods] Chemical annotation is performed in GNPS by comparing MS2 spectra against reference fragmentation patterns in its public spectral library: "Chemical annotation is performed in [GNPS](https://gnps.ucsd.edu/ProteoSAFe/static/gnps-splash.jsp) by comparing MS2 spectra"
- [methods] GNPS annotations via spectral reference matching are considered level 2 (putative annotation based on spectral library similarity) or level 3 (putatively characterized compound class based on: "GNPS annotations via spectral reference matching are considered level 2 (putative annotation based on spectral library similarity) or level 3 (putatively characterized compound class based on"
- [methods] The same chemical can have multiple GNPS annotations. Slight variation in the MS2 spectra (*m/z* or abundance) cause the pattern to match different reference MS2 spectra for the same chemical: "The same chemical can have multiple GNPS annotations. Slight variation in the MS2 spectra (*m/z* or abundance) cause the pattern to match different reference MS2 spectra for the same chemical"
- [readme] ReDU is a launchpad for co- or re-analysis of public data via the Global Natural Products Social Molecular Networking Platform (GNPS). Our aim is to empower researchers to put their data in the context of public data as well as explore questions using public data at the repository scale.: "ReDU is a launchpad for co- or re-analysis of public data via the Global Natural Products Social Molecular Networking Platform [(GNPS)](https://gnps.ucsd.edu/ProteoSAFe/static/gnps-splash.jsp). Our"
- [readme] One of the key steps in ReDU is the updating of the database to include the latest identifications for files within ReDU. These are the following steps: Download batch template for GNPS, Run Batch Workflow for Spectral Library Search, Get the set of tasks as tsv and save: "One of the key steps in ReDU is the updating of the database to include the latest identifications for files within ReDU. These are the following steps: Download batch template for GNPS at"
