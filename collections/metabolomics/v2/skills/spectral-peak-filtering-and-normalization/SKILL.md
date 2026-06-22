---
name: spectral-peak-filtering-and-normalization
description: Use when working with raw or minimally processed MS/MS spectra from repositories like GNPS that contain variable peak intensities, noise, and formatting inconsistencies that would interfere with downstream deep learning models trained on normalized spectral representations.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3695
  edam_topics:
  - http://edamontology.org/topic_0121
  - http://edamontology.org/topic_3370
  tools:
  - matchms
  - pubchempy
  - RDKit
  - Python
derived_from:
- doi: 10.1186/s13321-021-00558-4
  title: MS2DeepScore
evidence_spans:
- Metadata was cleaned and checked using matchms [18] version 0.8.2, which included cleaning compound names, extracting adduct information from the given metadata, moving metadata to consistent fields
- For each pair of molecular fingerprints Tanimoto scores were calculated, indicating the structural similarity of that pair. (as implemented in matchms [18])
- We then ran an automated search against PubChem [42] using pubchempy [43] for spectra which still missed InChI or SMILES annotations.
- Unless noted otherwise, we used Tanimoto scores on RDKit [23] Daylight fingerprints (2048 bits) to compute structural similarities.
- Unless noted otherwise, we used Tanimoto scores on RDKit [23] Daylight fingerprints (2048 bits) to compute structural similarities
- Our MS2DeepScore Python library offers two types of data generators, one which iterates over all unique InChIKeys (DataGeneratorAllInchikeys) and one which iterates over all spectra and was used for
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_matchms_2_cq
    doi: 10.1186/s13321-024-00878-1
    title: matchms
  - build: coll_ms2deepscore_cq
    doi: 10.1186/s13321-021-00558-4
    title: MS2DeepScore
  dedup_kept_from: coll_ms2deepscore_cq
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1186/s13321-021-00558-4
  all_source_dois:
  - 10.1186/s13321-021-00558-4
  zenodo_doi: TODO-zenodo
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# spectral-peak-filtering-and-normalization

## Summary

Preprocessing pipeline that removes low-intensity peaks, normalizes peak intensities via square-root transformation, and bins peaks into fixed m/z ranges to prepare raw MS/MS spectra for machine learning. This standardization ensures consistent input representation across spectra of varying quality and intensity distributions.

## When to use

Apply this skill when working with raw or minimally processed MS/MS spectra from repositories like GNPS that contain variable peak intensities, noise, and formatting inconsistencies that would interfere with downstream deep learning models trained on normalized spectral representations. Specifically useful when the goal is to train or apply neural networks that expect fixed-dimension spectral vectors rather than variable-length peak lists.

## When NOT to use

- Input spectra are already binned or feature-engineered into fixed vectors — reapplying binning will lose information or double-bin the data.
- Analysis requires preservation of exact peak positions (e.g., high-resolution accurate mass workflows or isotope pattern analysis) — binning to 10,000 bins (0.1 m/z resolution) is too coarse.
- Downstream model explicitly uses raw peak intensities as training data — the square-root transformation may not be compatible with models trained on untransformed intensity distributions.

## Inputs

- raw MS/MS spectra (mzML, mgf, msp, or json format)
- peak lists with m/z and intensity pairs
- mass range bounds (default 10–1000 m/z)

## Outputs

- binned spectral vectors (10,000-element arrays, one per spectrum)
- filtered and normalized peak intensity values
- metadata indicating number of peaks retained and bins populated

## How to apply

Remove peaks with intensities below 0.1% of the maximum peak intensity within each spectrum, then cap the spectrum to its 1000 highest-intensity peaks to reduce noise and computational burden. Apply a square-root transformation to all remaining peak intensities to reduce the dominance of very high peaks and normalize the intensity scale. Finally, bin the transformed peaks into 10,000 equally-sized bins spanning 10–1000 m/z (0.1 m/z per bin), selecting the maximum intensity when multiple peaks fall into the same bin. This produces a fixed-length vector representation suitable for Siamese neural network training. The square-root transformation is critical because it avoids overfitting to the highest intensity peaks, which often dominate MS/MS spectra but may not be diagnostically informative for structural similarity prediction.

## Related tools

- **matchms** (Metadata cleaning and standardization prior to peak filtering; handles compound name normalization, adduct extraction, and InChI/SMILES conversion) — https://github.com/matchms/matchms
- **RDKit** (Molecular fingerprint generation from chemical structure annotations to compute ground-truth structural similarity labels for training data validation)
- **Python** (Implementation language for peak filtering, intensity transformation, and binning operations)

## Examples

```
from matchms.importing_utils import load_documents; from matchms import Spectrum; spectra = load_documents('spectra.mgf'); filtered_spectra = [s for s in spectra if len(s.peaks) >= 5]; binned = [[max([p[1] for p in s.peaks if 10 <= (p[0]//0.1)*0.1 < 1000 and (p[0]//0.1)*0.1 == b*0.1], default=0)**0.5 for b in range(10000)] for s in filtered_spectra]
```

## Evaluation signals

- Verify that all output spectral vectors have exactly 10,000 bins with no missing dimensions.
- Confirm that no peak intensities exceed 1.0 (the maximum after square-root transformation of normalized intensities); spot-check a sample of transformed values.
- Check that the number of non-zero bins per spectrum is consistent with expected diversity (most spectra should have 50–500 populated bins; very sparse spectra (<10 bins) or fully populated spectra (>9900 bins) may indicate pipeline errors).
- Validate that peak filtering removed ≥90% of the original low-intensity noise by comparing median peak count before and after filtering (raw spectra typically have 100–500 peaks; after filtering and binning, 50–500 should remain).
- Ensure that 9,948 of 10,000 bins contain at least one spectrum's peak intensity in the training set, confirming the binning is not over-sparse.

## Limitations

- Fixed 10,000-bin architecture (0.1 m/z per bin) may lose information in high-resolution accurate mass spectra or miss fine isotope patterns relevant to structure elucidation.
- Square-root transformation assumes intensity follows a scale-dependent noise model; if peak intensity noise is additive (not multiplicative), this transformation may be suboptimal.
- Discarding the top 1000 peaks and removing intensities <0.1% of max may remove diagnostic low-intensity fragments in spectra where weak but structurally informative peaks are present.
- The pipeline does not account for systematic instrumental variations (e.g., different ionization methods, collision energies, instrument types) and treats all spectra uniformly; cross-ionization or cross-instrument predictions may suffer.
- Peak binning with maximum-intensity selection discards information about peak multiplicity within bins; if two isobars of different intensities occupy the same bin, only the higher is retained.

## Evidence

- [methods] by removing peaks with intensities < 0.1% of the maximum peak intensity and limiting the maximum number of peaks to the 1000 highest intensity peaks: "by removing peaks with intensities < 0.1% of the maximum peak intensity and limiting the maximum number of peaks to the 1000 highest intensity peaks"
- [methods] Peak intensities were square root transformed to avoid a too strong focus on the highest intensity peaks only: "Peak intensities were square root transformed to avoid a too strong focus on the highest intensity peaks only"
- [methods] Spectrum peaks were binned in 10,000 equally-sized bins ranging from 10 to 1000 m/z: "Spectrum peaks were binned in 10,000 equally-sized bins ranging from 10 to 1000 m/z"
- [other] Filter spectra to retain only those in positive ionization mode with valid 14-character InChIKey and SMILES/InChI annotation, containing ≥5 peaks in the 10.0–1000.0 Da mass range: "Filter spectra to retain only those in positive ionization mode with valid 14-character InChIKey and SMILES/InChI annotation, containing ≥5 peaks in the 10.0–1000.0 Da mass range"
- [other] Remove bins not represented in training data (9948 of 10,000 bins retained) and output cleaned spectral vectors and metadata: "Remove bins not represented in training data (9948 of 10,000 bins retained) and output cleaned spectral vectors and metadata"
