---
name: mass-spectrometry-file-format-parsing
description: Use when you have raw MS/MS spectral data in one or more standard mass spectrometry file formats (.mgf, .msp, or .mzML) and need to convert them into a standardized bag-of-fragments representation for unsupervised topic modeling or substructure discovery workflows.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3632
  edam_topics:
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_0121
  tools:
  - MS2LDA
  - MS2LDA.Preprocessing.load_and_clean
  - Python
  - Conda
  - MS2LDA.Preprocessing.generate_corpus
  - ProteoWizard Library and Tools
  - pwiz
  techniques:
  - LC-MS
  - ion-mobility-MS
derived_from:
- doi: 10.1073/pnas.1608041113
  title: MS2LDA
- doi: 10.1021/acs.jproteome.9b00640
  title: ''
evidence_spans:
- MS2LDA (Mass Spectrometry–Latent Dirichlet Allocation) is a framework
- MS2LDA uses Latent Dirichlet Allocation (LDA) to infer which motifs are most likely to explain the observed fragmentation patterns
- from MS2LDA.Preprocessing import load_and_clean
- Configure the Python environment (set PYTHONPATH, activate conda, etc.)
- These steps assume you have Conda installed
- The ProteoWizard Library and Tools are a set of modular and extensible open-source, cross-platform tools and software libraries
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_eclipse_cq
    doi: 10.1093/bioinformatics/btaf290/8128335
    title: Eclipse
  - build: coll_matchms_cq
    doi: 10.1186/s13321-024-00878-1
    title: matchms
  - build: coll_ms2lda
    doi: 10.1073/pnas.1608041113
    title: MS2LDA
  - build: coll_skyline_small_molecules_cq
    doi: 10.1021/acs.jproteome.9b00640
    title: Skyline (small molecules)
  dedup_kept_from: coll_ms2lda
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1073/pnas.1608041113
  all_source_dois:
  - 10.1073/pnas.1608041113
  - 10.1021/acs.jproteome.9b00640
  zenodo_doi: TODO-zenodo
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# mass-spectrometry-file-format-parsing

## Summary

Parse and normalize tandem mass spectrometry spectra from multiple input file formats (.mgf, .msp, .mzML) into a unified internal representation with extracted fragment ion masses, intensity normalization, and neutral loss calculation. This foundational preprocessing step converts raw spectral data into a structured format suitable for downstream motif discovery and LDA modeling.

## When to use

You have raw MS/MS spectral data in one or more standard mass spectrometry file formats (.mgf, .msp, or .mzML) and need to convert them into a standardized bag-of-fragments representation for unsupervised topic modeling or substructure discovery workflows. Apply this skill at the beginning of any MS2LDA pipeline before noise filtering, corpus generation, or LDA training.

## When NOT to use

- Your spectral data is already in a pre-processed bag-of-fragments or document-term matrix format — skip directly to corpus filtering or LDA training.
- Your input files use non-standard or proprietary formats not listed in the MS2LDA.Preprocessing module documentation (.raw Thermo, .d Bruker, .wiff AB Sciex) — you will need custom format converters before applying this skill.
- You require retention-time-aware alignment or ion mobility dimension preservation that extends beyond single-spectrum parsing — this skill operates on individual MS/MS spectra and does not natively handle LC-IM-MS data integration.

## Inputs

- MS/MS spectral data file in .mgf format (Mascot Generic Format)
- MS/MS spectral data file in .msp format (NIST MS Search format)
- MS/MS spectral data file in .mzML format (mzML XML-based format)
- Precursor m/z and charge state annotations (per spectrum)
- Peak intensity lists (m/z, intensity pairs per spectrum)

## Outputs

- Unified internal spectral representation with parsed fragment ion masses
- Intensity-normalized fragment peak lists (per spectrum)
- Calculated neutral loss m/z values for all fragment pairs
- Preprocessed corpus object compatible with LDA model input (document-term matrix or serialized representation)
- Metadata log documenting format conversion, normalization scheme, and filtering thresholds applied

## How to apply

Load MS/MS spectra from the input file using the MS2LDA.Preprocessing.load_and_clean module, which handles multiple format conversions transparently. Extract fragment ion masses from each spectrum and normalize peak intensities to a common scale (e.g., intensity of the base peak = 100). Calculate neutral loss values for all observed fragment ion pairs by subtracting fragment m/z values from the precursor mass minus common adducts. Document which intensity normalization scheme and neutral loss calculation method were applied, as these choices affect downstream motif inference. The preprocessing module outputs a structured corpus object ready for filtering and LDA training.

## Related tools

- **MS2LDA.Preprocessing.load_and_clean** (Primary module for loading and normalizing raw MS/MS spectra from multiple file formats) — https://github.com/vdhooftcompmet/MS2LDA
- **MS2LDA.Preprocessing.generate_corpus** (Generates the final bag-of-fragments corpus representation by binning fragments and neutral losses into discrete mass tokens) — https://github.com/vdhooftcompmet/MS2LDA
- **Python** (Scripting language required to invoke MS2LDA preprocessing modules and configure the execution environment)
- **Conda** (Environment manager for installing MS2LDA and its dependencies with consistent versions)

## Examples

```
from MS2LDA.Preprocessing import load_and_clean, generate_corpus
spectra = load_and_clean('data/compounds.mgf', ion_mode='positive')
corpus = generate_corpus(spectra, bin_width=0.1)
```

## Evaluation signals

- All input spectra are successfully parsed without format conversion errors or missing precursor m/z / charge annotations.
- Fragment ion intensity distributions are normalized to a consistent scale (e.g., max intensity per spectrum equals 100); verify by inspecting normalized intensity histograms across a sample of spectra.
- Neutral loss m/z values are calculated for all fragment pairs and fall within expected chemical mass ranges (e.g., 18.01 for H₂O, 44.01 for CO₂, typical loss < precursor m/z); spot-check calculated neutral losses against known fragmentation rules.
- The output corpus object is serializable and can be loaded by the LDA training module without schema mismatch errors; validate by attempting to instantiate the LDA model on the generated corpus.
- The preprocessing module log records the input file format, normalization method applied, number of spectra loaded, and any spectra excluded due to missing precursor annotations or other quality filters.

## Limitations

- The MS2LDA.Preprocessing module assumes standard tandem MS/MS formats (.mgf, .msp, .mzML); other vendor-specific formats (Thermo .raw, Bruker .d, AB Sciex .wiff) require external conversion before preprocessing.
- Intensity normalization is applied per-spectrum; if your dataset spans multiple acquisition instruments or methods with systematically different dynamic ranges, cross-file normalization may be required as an additional preprocessing step.
- Neutral loss calculation is deterministic given the precursor mass and fragment m/z values, but the choice of mass binning resolution (e.g., integer vs. decimal m/z bins) during corpus generation affects downstream motif granularity and must be selected before LDA training.
- High noise floors in spectra can inflate the number of spurious fragment ions and neutral losses; filtering by minimum intensity threshold or statistical significance is performed in a separate workflow step (not part of this skill) to remove noise.
- The preprocessing module does not correct for systematic mass calibration errors; spectra should be calibrated to ≤5 ppm accuracy before parsing, otherwise fragment and neutral loss identification may fail.

## Evidence

- [methods] Load MS/MS spectra from input file (.mgf, .msp, or .mzML) using the MS2LDA.Preprocessing.load_and_clean module: "Load MS/MS spectra from input file (.mgf, .msp, or .mzML) using the MS2LDA.Preprocessing.load_and_clean module."
- [methods] Extract fragment ion masses and normalize peak intensities within each spectrum.: "Extract fragment ion masses and normalize peak intensities within each spectrum."
- [methods] Calculate neutral loss values for all observed fragment pairs.: "Calculate neutral loss values for all observed fragment pairs."
- [methods] Generate a bag-of-fragments corpus representation using MS2LDA.Preprocessing.generate_corpus, binning fragments and losses into discrete mass tokens.: "Generate a bag-of-fragments corpus representation using MS2LDA.Preprocessing.generate_corpus, binning fragments and losses into discrete mass tokens."
- [other] The preprocessing module converts MS/MS spectra into a bag-of-fragments format, extracts neutral losses, and filters out noise to prepare data for LDA modeling.: "The preprocessing module converts MS/MS spectra into a bag-of-fragments format, extracts neutral losses, and filters out noise to prepare data for LDA modeling."
- [readme] MS2LDA (Mass Spectrometry–Latent Dirichlet Allocation) is a framework that brings the concept of topic modeling to the world of tandem mass spectrometry: "MS2LDA (Mass Spectrometry–Latent Dirichlet Allocation) is a framework that brings the concept of topic modeling to the world of tandem mass spectrometry"
