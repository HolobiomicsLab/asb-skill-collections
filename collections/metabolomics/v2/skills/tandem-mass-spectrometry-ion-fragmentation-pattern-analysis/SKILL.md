---
name: tandem-mass-spectrometry-ion-fragmentation-pattern-analysis
description: Use when after MS1 feature extraction and prescreening quality control
  have completed on mzML files, and you need to inspect the MS2 fragmentation patterns
  of candidate compounds to verify their identity or assess whether extracted features
  are genuine metabolites rather than noise or artifacts.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3632
  edam_topics:
  - http://edamontology.org/topic_0121
  - http://edamontology.org/topic_3520
  tools:
  - shinyscreen
  - R
  - devtools
  - Docker
  techniques:
  - LC-MS
  license_tier: open
derived_from:
- doi: 10.1186/s13321-025-01044-x
  title: Shinyscreen
evidence_spans:
- Shinyscreen is a Shiny application for visualizing and analyzing high resolution
  mass spectrometry data.
- Shinyscreen can be installed in R via `devtools`
- docker run -p 3838:3838 \ -v C:/your/path/project:/home/ssuser/projects
- docker pull registry.gitlab.com/uniluxembourg/lcsb/eci/shinyscreen:master
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_shinyscreen_cq
    doi: 10.1186/s13321-025-01044-x
    title: Shinyscreen
  dedup_kept_from: coll_shinyscreen_cq
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1186/s13321-025-01044-x
  all_source_dois:
  - 10.1186/s13321-025-01044-x
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# tandem-mass-spectrometry-ion-fragmentation-pattern-analysis

## Summary

Extract and visualize MS2 fragmentation spectra and ion chromatograms for detected compounds to confirm metabolite identity and assess data quality. This skill enables inspection of tandem mass spectrometry patterns within a high-resolution metabolomics workflow, bridging feature extraction with compound annotation.

## When to use

After MS1 feature extraction and prescreening quality control have completed on mzML files, and you need to inspect the MS2 fragmentation patterns of candidate compounds to verify their identity or assess whether extracted features are genuine metabolites rather than noise or artifacts.

## When NOT to use

- Input contains only MS1 data (no MS2 spectra acquired); fragmentation patterns cannot be visualized or analyzed.
- Prescreening quality control has flagged a compound as a contaminant or artifact; fragmentation inspection will not recover a failed QC check.
- The mzML files were processed with MS/MS disabled or with very restrictive inclusion lists that excluded the m/z of interest; MS2 data will be absent.

## Inputs

- prescreened feature table from Shinyscreen (CSV with compound metadata, adduct assignment, quality scores)
- extracted mzML data (MS1 and MS2 spectra indexed by retention time and m/z)
- compound list with expected m/z values and ionization modes (e.g., AAs_CmpdList.csv)

## Outputs

- MS2 fragmentation spectrum plot (m/z vs. intensity)
- extracted ion chromatogram (EIC) showing retention time profile
- MS2 peak profile visualization
- visual confirmation/rejection decision for each compound candidate

## How to apply

In the Shinyscreen Results Explorer tab, click on a row corresponding to a compound of interest. This opens three visualization panels: the extracted ion chromatogram (EIC), the MS2 peak profile, and the MS2 spectrum. Compare the observed fragmentation pattern (m/z of fragment ions and their relative intensities) against known reference patterns for the compound or compound class (e.g., for amino acids, expect characteristic loss of water or carboxyl groups). Examine the retention time alignment between the EIC and MS2 peaks to ensure they co-elute, indicating a genuine molecular feature rather than a chromatographic artifact. Use the Plot Controls to adjust retention time and intensity ranges if needed to refine visibility of weak or overlapping peaks.

## Related tools

- **shinyscreen** (Interactive Shiny application that hosts the Results Explorer tab for MS2 spectrum and EIC visualization and retrieves fragmentation data from extracted features) — https://gitlab.com/uniluxembourg/lcsb/eci/shinyscreen
- **R** (Runtime environment for executing Shinyscreen and rendering visualizations)

## Evaluation signals

- MS2 spectrum plot displays one or more fragment ion peaks (m/z > 0, intensity > 0) that co-elute with the EIC retention time window.
- EIC peak shape is unimodal or has a single dominant lobe, indicating a discrete molecular feature rather than baseline noise or co-eluting isomers.
- Fragmentation pattern matches expected neutral losses or characteristic ions for the compound class (e.g., loss of 18 m/z for H₂O from protonated amino acids).
- MS2 peak intensity is significantly above the detection threshold relative to local background in the intensity-adjusted Plot Controls view.
- Retention time alignment: EIC and MS2 peak maxima occur within <0.2 min of each other (typical chromatographic resolution).

## Limitations

- Shinyscreen displays MS2 spectra only if they were acquired during data collection; low-resolution or MS1-only methods will yield no fragmentation data.
- Visual inspection is subjective; automated spectral matching (library matching, in silico fragmentation prediction) is not performed within this step and must be performed separately.
- Co-eluting isomers or compounds with very similar m/z values may produce ambiguous MS2 spectra if not baseline-resolved chromatographically.
- Retention time shifts between sample runs or columns can lead to misalignment between expected and observed EIC windows; manual retention time adjustment in Plot Controls may be necessary.

## Evidence

- [methods] View compound details: click on compound row in table to open EIC, MS2 peak and MS2 spectrum: "simply click on the corresponding row in the table. This will open up the extracted ion chromatogram (EIC), MS2 peak and MS2 spectrum"
- [methods] Results Explorer provides visualization and filtering of prescreened compounds: "proceed to the **Results Explorer** tab to visualize your results and export them"
- [methods] Plot Controls allows dynamic adjustment of display ranges for refined inspection: "Plot Controls panel allows users to refine the display by adjusting the retention time and intensity ranges."
- [methods] Prescreen step performs quality control checks on extracted features before visualization: "Then click the **Prescreen** button to run quality control checks."
- [methods] Shinyscreen processes high-resolution mass spectrometry data for analysis and visualization: "Shinyscreen is a Shiny application for visualizing and analyzing high resolution mass spectrometry data."
