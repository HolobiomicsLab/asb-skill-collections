---
name: ms-ms-spectrum-preprocessing
description: Use when you have raw or semi-processed MS/MS spectral data from bottom-up tandem mass spectrometry experiments (data-dependent acquisition) that you intend to input to de novo peptide sequencing tools like Casanovo.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3432
  edam_topics:
  - http://edamontology.org/topic_0121
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_0769
  tools:
  - Casanovo
  - PyTorch
  - PDV
  - limelight-import-casanovo
  - MIST
  - MIST-CF
  - SIRIUS
  - SCARF
  - spectrum_utils
  - cosine_neutral_loss
  techniques:
  - LC-MS
  - ion-mobility-MS
derived_from:
- doi: 10.1038/s41467-024-49731-x
  title: Casanovo
- doi: 10.1093/bib/bbac542
  title: ''
- doi: 10.1021/acs.jcim.3c01082
  title: ''
- doi: 10.1021/jasms.2c00153
  title: ''
- doi: 10.1016/1044-0305
  title: ''
evidence_spans:
- Casanovo is a state-of-the-art deep learning tool designed for _de novo_ peptide sequencing.
- Casanovo is a state-of-the-art deep learning tool designed for _de novo_ peptide sequencing
- Pytorch is installed automatically when installing Casanovo
- Upgraded minimum Lightning version to 2.6.
- an extension of MIST for annotating MS1 precursor masses from MS/MS data
- MIST-CF ranks chemical formula and adduct assignments for an unknown mass spectrum using an end-to-end energy based modeling approach
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_casanovo_cq
    doi: 10.1038/s41467-024-49731-x
    title: Casanovo
  - build: coll_mistcf
    doi: 10.1021/acs.jcim.3c01082
    title: mistcf
  - build: coll_neutral_loss_similarity_cq
    doi: 10.1021/jasms.2c00153
    title: Neutral-loss similarity
  dedup_kept_from: coll_casanovo_cq
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1038/s41467-024-49731-x
  all_source_dois:
  - 10.1038/s41467-024-49731-x
  - 10.1093/bib/bbac542
  - 10.1021/acs.jcim.3c01082
  - 10.1021/jasms.2c00153
  - 10.1016/1044-0305
  zenodo_doi: TODO-zenodo
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# MS/MS Spectrum Preprocessing

## Summary

Prepare raw tandem mass spectrometry (MS/MS) spectra for de novo peptide sequencing by converting, validating, and standardizing spectral data into formats suitable for neural network-based peptide prediction. This skill ensures data quality and consistency across diverse mass spectrometry instruments and acquisition protocols.

## When to use

You have raw or semi-processed MS/MS spectral data from bottom-up tandem mass spectrometry experiments (data-dependent acquisition) that you intend to input to de novo peptide sequencing tools like Casanovo. Preprocessing is required when spectra are in non-standard formats (mzML, mzXML, raw instrument output), lack proper annotation, or have not been validated for peak quality and mass accuracy before neural network prediction.

## When NOT to use

- Input spectra are already in validated, annotated MGF format and have been quality-checked by the data provider.
- Your workflow requires database-dependent peptide identification rather than de novo sequencing (different preprocessing priorities).
- Spectra are from untargeted or high-resolution proteomics where precursor charge state or m/z assignment is ambiguous or missing.

## Inputs

- Raw or semi-processed MS/MS spectral data (mzML, mzXML, proprietary instrument formats)
- Annotated spectral files (MGF, mzTab, or vendor-specific formats)
- Metadata: precursor m/z, charge state, retention time, scan identifiers

## Outputs

- Annotated MGF files with validated peak lists
- Quality control summary (spectrum count, mass accuracy statistics, peak intensity distributions)
- Flagged or filtered spectra (low-quality or anomalous records)

## How to apply

Convert spectral data to annotated MGF (Mascot Generic Format) files, which Casanovo accepts as input. Ensure spectra are annotated with precursor m/z, charge state, and retention time metadata. Validate peak lists for mass accuracy (typically within instrument tolerance, e.g., 5–20 ppm depending on mass analyzer) and intensity thresholds to remove low-quality or noise-dominated spectra. Remove or flag spectra with insufficient peak counts or anomalous mass distributions. The preprocessing workflow should produce MGF files with consistent formatting suitable for batch processing by transformer-based models, as Casanovo loads pre-trained checkpoints and validation datasets of annotated MS/MS spectra in MGF format to predict peptide sequences.

## Related tools

- **Casanovo** (De novo peptide sequencing engine that accepts preprocessed MGF-format spectral input and predicts amino acid sequences using a transformer neural network) — https://github.com/Noble-Lab/casanovo
- **PDV** (Visualization tool for inspecting and validating preprocessed spectral data and de novo predictions in graphical interface) — https://github.com/wenbostar/PDV
- **PyTorch** (Deep learning framework underlying Casanovo; required for GPU acceleration of spectrum processing and prediction if using neural network-based preprocessing modules)
- **limelight-import-casanovo** (Converter for transforming preprocessed Casanovo results (mzTab) into Limelight XML format for downstream visualization and quality assessment) — https://github.com/yeastrc/limelight-import-casanovo

## Evaluation signals

- MGF files conform to standard format specification: each spectrum has precursor m/z, charge state, retention time, and annotated peaks; no malformed or missing fields.
- Mass accuracy of precursor ions is within instrument tolerance (verify by comparing theoretical m/z to observed; document ppm error distribution).
- Peak intensity distributions are consistent within quality tiers (e.g., median peak counts per spectrum, intensity range); outliers are documented and flagged.
- Spectrum count and metadata completeness match input dataset expectations; no spectra are silently dropped without logging.
- Processed MGF files are successfully ingested by Casanovo without parsing errors and produce non-empty predicted peptide lists (confirming structural validity).

## Limitations

- Preprocessing quality depends critically on the source instrument's calibration and dynamic range; high-resolution instruments (e.g., Orbitrap) may require different tolerance thresholds than lower-resolution analyzers.
- Casanovo is particularly useful for immunopeptidomics, metaproteomics, paleoproteomics, and venomics but may not be optimal for highly complex proteomes with extensive post-translational modifications if preprocessing does not account for neutral loss or fragment ion patterns specific to those modifications.
- MGF format lossy conversion from vendor formats (mzML, mzXML) may discard instrument-specific metadata (e.g., scan-level MS1 profiles, ion mobility information) that could inform preprocessing decisions.
- Preprocessing thresholds (mass accuracy, peak count, intensity cutoffs) are not tuned in the article; practitioners must validate on their own datasets before running large batches.

## Evidence

- [other] Load a pre-trained Casanovo checkpoint and a validation dataset of annotated MS/MS spectra in MGF format.: "Load a pre-trained Casanovo checkpoint and a validation dataset of annotated MS/MS spectra in MGF format."
- [other] Casanovo is powered by a transformer neural network that translates peaks in MS/MS spectra into amino acid sequences.: "Casanovo is powered by a transformer neural network that translates peaks in MS/MS spectra into amino acid sequences."
- [readme] Casanovo can be used to find unexpected peptide sequences in any data-dependent acquisition, bottom-up tandem mass spectrometry dataset.: "Casanovo can be used to find unexpected peptide sequences in any data-dependent acquisition, bottom-up tandem mass spectrometry dataset"
- [other] The data for this benchmark are available as annotated MGF files on MassIVE with dataset identifier MSV000090982: "The data for this benchmark are available as annotated MGF files on MassIVE with dataset identifier MSV000090982"
- [readme] Casanovo is particularly useful for immunopeptidomics, metaproteomics, paleoproteomics, venomics, or any setting in which you are interested in identifying peptides that may not be in your protein database.: "Casanovo is particularly useful for immunopeptidomics, metaproteomics, paleoproteomics, venomics, or any setting in which you are interested in identifying peptides that may not be in your protein"
