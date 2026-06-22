---
name: mztab-format-export-and-annotation
description: Use when after Casanovo has generated ranked peptide sequence predictions from MS/MS spectra and you need to persist, share, or integrate the results into a proteomics data management or visualization pipeline.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3765
  edam_topics:
  - http://edamontology.org/topic_0121
  - http://edamontology.org/topic_3520
  tools:
  - Casanovo
  - PyTorch
  - DepthCharge
  - CUDA Toolkit
  - Limelight XML converter (yeastrc/limelight-import-casanovo)
  - PDV (Proteomics Data Viewer)
derived_from:
- doi: 10.1038/s41467-024-49731-x
  title: Casanovo
- doi: 10.1093/bib/bbac542
  title: ''
evidence_spans:
- Casanovo is a state-of-the-art deep learning tool designed for _de novo_ peptide sequencing.
- Casanovo is a state-of-the-art deep learning tool designed for _de novo_ peptide sequencing
- Pytorch is installed automatically when installing Casanovo
- Upgraded minimum Lightning version to 2.6.
- Upgraded minimum DepthCharge version to 0.4.10.
- Install the latest version of the NVIDIA drivers using the official CUDA Toolkit
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_casanovo_cq
    doi: 10.1038/s41467-024-49731-x
    title: Casanovo
  dedup_kept_from: coll_casanovo_cq
schema_version: 0.2.0
---

# mztab-format-export-and-annotation

## Summary

Export de novo peptide sequencing predictions from Casanovo to mzTab format with standardized metadata, modification annotations in ProForma 2.0 notation, and per-residue confidence scores. This skill ensures that predicted peptide sequences, along with their MS/MS spectral metadata and quality metrics, are recorded in a portable, standards-compliant format suitable for downstream analysis and integration with visualization tools.

## When to use

Apply this skill after Casanovo has generated ranked peptide sequence predictions from MS/MS spectra and you need to persist, share, or integrate the results into a proteomics data management or visualization pipeline. Use when predictions must include per-residue amino acid scores, modification annotations, precursor mass tolerance assessment, and scan metadata in a standardized, machine-readable format.

## When NOT to use

- Do not use if predictions are already in a database search result format (e.g., mzIdentML from search engines like MS-GF+) — mzTab export is specifically for de novo predictions without reference database matching.
- Do not apply if you require full spectral annotation or mirror plots comparing experimental vs. predicted fragmentation patterns — mzTab export is a structured metadata format and does not include visual spectrum data.
- Do not use if precursor mass tolerance or peptide length constraints have not yet been defined for your experimental context — export without these filters may include low-confidence, chemically implausible predictions.

## Inputs

- Casanovo beam search decoded predictions (sequence strings with confidence logits)
- Preprocessed MS/MS spectra metadata (precursor m/z, charge state, scan identifiers)
- Spectrum file paths and scan indices (MGF, mzML, or mzXML format)

## Outputs

- mzTab format file (.mztab) containing PSM-level predictions
- Standardized peptide annotations with ProForma 2.0 modification notation
- Per-residue confidence scores and aggregate peptide scores

## How to apply

After beam search decoding generates candidate peptide sequences ranked by score, apply post-hoc filters: reject predictions failing the minimum peptide length threshold (min_peptide_len), penalize or flag predictions outside the precursor mass tolerance window (precursor_mass_tol in ppm or Da), and compute amino acid scores as the product of per-residue confidence logits. Construct the mzTab export by writing each prediction as a row containing: sequence, modifications in ProForma 2.0 notation, per-residue amino acid scores, aggregate peptide score, precursor m/z, charge state, and associated scan metadata (scan ID, filename). The mzTab format ensures compatibility with downstream tools (e.g., Limelight XML conversion, PDV visualization) and enables integration with monoclonal antibody assembly or immunopeptidomics workflows where database-independent peptide identification is required.

## Related tools

- **Casanovo** (Generates beam search decoded peptide sequence predictions with per-residue confidence scores from MS/MS spectra; primary source of predictions exported to mzTab) — https://github.com/Noble-Lab/casanovo
- **Limelight XML converter (yeastrc/limelight-import-casanovo)** (Converts Casanovo mzTab results to Limelight XML for interactive visualization and data management in the Limelight web application) — https://github.com/yeastrc/limelight-import-casanovo
- **PDV (Proteomics Data Viewer)** (Provides graphical user interface for inspecting and annotating Casanovo mzTab predictions, including spectral annotation and mirror plots for de novo sequences) — https://github.com/wenbostar/PDV
- **PyTorch** (Underlying deep learning framework used by Casanovo to generate predictions; installed automatically with Casanovo)

## Evaluation signals

- mzTab file is valid and conforms to the mzTab specification (row structure, column headers, required fields present)
- All exported peptide sequences have length ≥ min_peptide_len threshold; no predictions below this threshold are present in output
- Precursor m/z values in mzTab match input spectra within declared precursor_mass_tol (ppm or Da); out-of-tolerance predictions are flagged or excluded
- Per-residue amino acid scores for each exported sequence are products of per-residue confidence logits; aggregate peptide scores are computed consistently across all rows
- Modifications are notated in ProForma 2.0 format; scan metadata (identifiers, filenames, charge states) are correctly linked to each PSM row

## Limitations

- mzTab export does not include spectral intensity data or peak annotations — full spectrum visualization requires the original MGF, mzML, or mzXML file plus a tool like PDV.
- Precursor mass tolerance filtering is a heuristic post-hoc filter; it does not account for systematic mass calibration errors or non-standard isotope labeling unless explicitly configured in precursor_mass_tol settings.
- ProForma 2.0 notation support is limited to modifications explicitly trained in Casanovo; non-standard or rare post-translational modifications may not be correctly predicted or annotated.
- Per-residue amino acid scores reflect confidence in individual residues but do not account for context-dependent interpretation (e.g., mass degeneracy between I/L, or ambiguous fragmentation patterns).

## Evidence

- [other] Export predictions to mzTab format with standardized metadata: "Export predictions to mzTab format, including sequence, modifications in ProForma 2.0 notation, amino acid scores, peptide score, precursor m/z, charge state, and scan metadata."
- [other] Per-residue confidence scoring via logit products: "assign amino acid scores as the product of per-residue confidence logits"
- [other] Post-hoc filtering on peptide length and precursor mass tolerance: "Apply post-hoc filters: reject predictions failing the minimum peptide length (min_peptide_len), penalize predictions outside precursor mass tolerance (precursor_mass_tol in ppm or Da)"
- [methods] Limelight XML conversion from mzTab for downstream visualization: "A converter for generating Limelight XML from Casanovo results is available, see the converter documentation"
- [methods] PDV support for Casanovo mzTab inspection: "PDV provides a graphical interface for inspecting Casanovo outputs. refer to the PDV documentation"
