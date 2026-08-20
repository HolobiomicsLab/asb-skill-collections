---
name: spectrum-preprocessing-binning-normalization
description: Use when when preparing raw MS/MS spectra for input to a Siamese neural
  network trained to predict structural similarity scores (Tanimoto).
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3215
  edam_topics:
  - http://edamontology.org/topic_0121
  - http://edamontology.org/topic_3520
  tools:
  - MS2DeepScore
  - RDKit
  - Python
  - matchms
  techniques:
  - LC-MS
  - ion-mobility-MS
  license_tier: open
derived_from:
- doi: 10.1186/s13321-021-00558-4
  title: MS2DeepScore
evidence_spans:
- MS2DeepScore to predict structural similarity scores for spe
- we used the MS2DeepScore base network (Fig. 1) to compute the 200-dimensional spectral
  embeddings for all 3601 spectra in the test set
- we used Tanimoto scores on RDKit [23] Daylight fingerprints (2048 bits) to compute
  structural similarities
- Our MS2DeepScore Python library offers two types of data generators
- Our MS2DeepScore Python library
- Metadata was cleaned and checked using matchms [18] version 0.8.2, which included
  cleaning compound names
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_ms2deepscore
    doi: 10.1186/s13321-021-00558-4
    title: MS2DeepScore
  dedup_kept_from: coll_ms2deepscore
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1186/s13321-021-00558-4
  all_source_dois:
  - 10.1186/s13321-021-00558-4
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# spectrum-preprocessing-binning-normalization

## Summary

Preprocesses tandem mass spectra by removing low-intensity peaks, applying intensity transformations, and binning peak data into fixed m/z intervals to prepare inputs for deep learning similarity prediction. This standardization ensures consistent feature representation across spectra of varying quality and intensity distributions.

## When to use

When preparing raw MS/MS spectra for input to a Siamese neural network trained to predict structural similarity scores (Tanimoto). Apply this skill before computing spectral embeddings or training a deep learning model on spectrum pairs, particularly when spectra have variable peak counts, intensity ranges, or quality levels that could bias learning.

## When NOT to use

- Input spectra are already in pre-binned or normalized vector form (e.g., from a prior preprocessing step).
- The analysis requires preservation of the original peak intensities or m/z values for downstream interpretation (e.g., fragment assignment or peak annotation).
- Spectra come from instruments or methods where the 10–1000 m/z range does not cover the relevant chemical space (e.g., intact protein MS, ion mobility experiments).

## Inputs

- Raw MS/MS spectrum data (peaks with m/z and intensity values)
- Spectrum metadata (e.g., maximum peak intensity per spectrum)

## Outputs

- Preprocessed spectrum vectors (10,000-dimensional binned intensity arrays)
- Optionally: filtered peak lists before binning

## How to apply

Remove peaks with intensities below 0.1% of the maximum peak intensity in each spectrum, then retain only the 1,000 highest-intensity peaks to reduce noise and excessive dimensionality. Apply square-root transformation to peak intensities to reduce bias toward the highest peaks and improve feature balance. Finally, bin the transformed peaks into 10,000 equally-sized m/z intervals spanning 10–1000 m/z. This produces a fixed-length feature vector per spectrum suitable for neural network input. The square-root transformation is critical because it prevents the model from over-weighting dominant peaks; the binning converts variable-length peak lists into dense, comparable vectors.

## Related tools

- **matchms** (Spectrum data cleaning, metadata extraction, and filtering pipeline; applies intensity thresholds and peak count limits) — https://github.com/matchms/matchms
- **RDKit** (Generates molecular fingerprints (Daylight, 2048 bits) from chemical structures to compute ground-truth Tanimoto scores for training labels)
- **MS2DeepScore** (Siamese network that receives preprocessed binned spectra as input and outputs structural similarity predictions) — https://github.com/matchms/ms2deepscore

## Examples

```
from matchms.Pipeline import Pipeline, create_workflow
from matchms.filtering.default_pipelines import DEFAULT_FILTERS
from ms2deepscore import MS2DeepScore
from ms2deepscore.models import load_model

model = load_model('ms2deepscore_model.pt')
pipeline = Pipeline(create_workflow(query_filters=DEFAULT_FILTERS, score_computations=[[MS2DeepScore, {'model': model}]]))
report = pipeline.run('spectra.mgf')
preprocessed_spectra = pipeline.spectra_queries
```

## Evaluation signals

- Output vectors have shape (n_spectra, 10000) with no missing values after binning.
- Peak intensity values are in the range [0, sqrt(max_original_intensity)] after square-root transformation.
- All spectra with more than 1,000 peaks are correctly truncated; those with fewer peaks retain their non-zero bins.
- Peaks below 0.1% of maximum intensity are removed; verify by checking that minimum non-zero intensity > 0.001 × max_intensity.
- RMSE on held-out test set matches reported values (~0.15 without uncertainty filtering, ~0.10 with IQR < 0.025) when preprocessed spectra are fed to the trained model.

## Limitations

- The fixed 10–1000 m/z binning range may lose information from spectra with significant peaks outside this range (e.g., high-mass fragments, small molecular ions).
- Square-root transformation reduces but does not eliminate bias toward high-intensity peaks; very weak peaks may be further suppressed and lose discriminative power.
- Binning into 10,000 fixed intervals can blur fine m/z distinctions near the detection limit; spectra with very sparse peaks may have insufficient feature density.
- The 0.1% intensity threshold and 1,000-peak limit are fixed hyperparameters; data with atypical noise profiles or peak distributions may require empirical re-tuning.
- No explicit handling of instrument artifacts, isotope peaks, or adducts; preprocessing assumes prior removal of such features or tolerance to their presence.

## Evidence

- [methods] The spectra underwent basic filtering to remove excessive amounts of peaks, by removing peaks with intensities < 0.1% of the maximum peak intensity and limiting the maximum number of peaks to the 1000 highest intensity peaks: "removing peaks with intensities < 0.1% of the maximum peak intensity and limiting the maximum number of peaks to the 1000 highest intensity peaks"
- [methods] Peak intensities were square root transformed to avoid a too strong focus on the highest intensity peaks only: "Peak intensities were square root transformed to avoid a too strong focus on the highest intensity peaks only"
- [methods] Spectrum peaks were binned in 10,000 equally-sized bins ranging from 10 to 1000 m/z: "Spectrum peaks were binned in 10,000 equally-sized bins ranging from 10 to 1000 m/z"
- [other] Prepare test spectra by applying the same preprocessing: remove peaks with intensity < 0.1% of maximum, keep top 1,000 peaks, apply square-root transformation to intensities, and bin into 10,000 equally-sized bins (10–1000 m/z).: "remove peaks with intensity < 0.1% of maximum, keep top 1,000 peaks, apply square-root transformation to intensities, and bin into 10,000 equally-sized bins"
- [methods] Metadata was cleaned and checked using matchms [18] version 0.8.2, which included cleaning compound names, extracting adduct information from the given metadata, moving metadata to consistent fields: "Metadata was cleaned and checked using matchms [18] version 0.8.2, which included cleaning compound names, extracting adduct information"
