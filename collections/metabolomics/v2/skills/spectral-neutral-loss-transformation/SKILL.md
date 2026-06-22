---
name: spectral-neutral-loss-transformation
description: Use when when comparing two or more MSMS spectra and you need to emphasize structural relationships revealed by neutral losses (mass differences between precursor and fragment ions) rather than absolute m/z values.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3632
  edam_topics:
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_0769
  tools:
  - github.com/bittremieux/cosine_neutral_loss
  - spectrum_utils
  - cosine_neutral_loss
derived_from:
- doi: 10.1021/jasms.2c00153
  title: Neutral-loss similarity
- doi: 10.1016/1044-0305
  title: ''
evidence_spans:
- github.com__bittremieux__cosine_neutral_loss
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_neutral_loss_similarity_cq
    doi: 10.1021/jasms.2c00153
    title: Neutral-loss similarity
  dedup_kept_from: coll_neutral_loss_similarity_cq
schema_version: 0.2.0
---

# spectral-neutral-loss-transformation

## Summary

Transform fragment peaks in tandem mass spectra to neutral loss values by subtracting each peak m/z from the precursor m/z, enabling structural comparison of molecules via neutral loss similarity scoring. This transformation is used alongside cosine and modified cosine measures to identify structurally related compounds from mass spectral data.

## When to use

When comparing two or more MSMS spectra and you need to emphasize structural relationships revealed by neutral losses (mass differences between precursor and fragment ions) rather than absolute m/z values. Use this when the goal is to discover structurally related molecules or when fragment ion identity is less certain than neutral loss patterns.

## When NOT to use

- Input spectra contain only precursor ions and no fragment peaks; neutral loss transformation requires at least one fragment peak per spectrum.
- The structural relevance of neutral losses is unknown or irrelevant for your use case; use cosine or modified cosine similarity instead.
- Precursor m/z values are missing, unreliable, or not accurately determined, as neutral loss calculation depends critically on precursor accuracy.

## Inputs

- MSMS spectrum with precursor m/z (float)
- Fragment peak list with m/z and intensity values (list of tuples or array)
- Reference MSMS spectrum with precursor m/z and fragment peaks

## Outputs

- Neutral loss similarity score (float, range 0–1)
- Transformed neutral loss intensity vector (normalized array)
- Neutral loss peak list (m/z values as precursor − fragment m/z)

## How to apply

For each input spectrum, parse the precursor m/z and the m/z and intensity values of all fragment peaks. Transform each fragment peak by computing neutral loss = precursor m/z − fragment peak m/z for all peaks in both query and reference spectra. Normalize the resulting neutral loss intensity vectors (e.g., via L2 normalization). Compute cosine similarity between the two neutral loss intensity vectors to obtain a score in the 0–1 range. A score closer to 1.0 indicates strong structural similarity via common neutral loss patterns.

## Related tools

- **spectrum_utils** (Load and preprocess MSMS spectra from USI identifiers; provides MsmsSpectrum class for parsing precursor m/z and fragment peaks) — https://github.com/bittremieux/spectrum_utils
- **cosine_neutral_loss** (Reference implementation of neutral loss similarity alongside cosine and modified cosine measures for spectrum comparison and mirror plot visualization) — https://github.com/bittremieux/cosine_neutral_loss

## Examples

```
import spectrum_utils.spectrum as sus; spectrum1 = sus.MsmsSpectrum.from_usi("mzspec:GNPS:GNPS-LIBRARY:accession:CCMSLIB00000424840"); spectrum1 = spectrum1.set_mz_range(0, spectrum1.precursor_mz); plot.plot_mirror(spectrum1, spectrum2, score="neutral_loss", filename="neutral_loss.png")
```

## Evaluation signals

- Verify that all neutral loss values are positive and less than or equal to the precursor m/z (invariant: 0 ≤ neutral loss ≤ precursor m/z for all peaks).
- Confirm that the neutral loss intensity vector sums to 1.0 after normalization (L2 norm or unit length check).
- Check that similarity scores for identical or near-identical spectra are close to 1.0, and dissimilar spectra yield scores near 0.0.
- Validate that neutral loss patterns match expected fragment ion losses for known compounds (e.g., loss of water, ammonia, or CO2 from precursor mass).
- Confirm reproducibility: repeated transformations of the same input spectrum yield identical neutral loss vectors and similarity scores.

## Limitations

- Neutral loss similarity assumes that fragment ions are correctly identified; m/z measurement error or calibration drift can distort neutral loss values and reduce discriminative power.
- The method may perform poorly when spectra contain few fragment peaks or when neutral loss patterns are sparse and uninformative for structural discrimination.
- Neutral loss similarity does not account for the absolute intensity distribution of fragments, only their relative intensities; intensity-dependent structural signatures may be missed.
- Isobaric or near-isobaric neutral losses from structurally distinct compounds can lead to false positives if m/z tolerance is too permissive during peak matching.

## Evidence

- [other] Transform fragment peaks to neutral losses by subtracting each peak m/z from the precursor m/z for both spectra.: "Transform fragment peaks to neutral losses by subtracting each peak m/z from the precursor m/z for both spectra."
- [other] Create normalized intensity vectors for neutral loss peaks in each spectrum. Compute cosine similarity between the two neutral loss intensity vectors.: "Create normalized intensity vectors for neutral loss peaks in each spectrum. 4. Compute cosine similarity between the two neutral loss intensity vectors."
- [other] Neutral loss similarity is implemented as a spectrum similarity measure in the repository alongside cosine and modified cosine approaches for comparing mass spectral data.: "Neutral loss similarity is implemented as a spectrum similarity measure in the repository alongside cosine and modified cosine approaches for comparing mass spectral data."
- [readme] Comparison of cosine, modified cosine, and neutral loss based spectral alignment for discovery of structurally related molecules: "Comparison of cosine, modified cosine, and neutral loss based spectral alignment for discovery of structurally related molecules"
- [other] Return the neutral loss similarity score (0–1 range).: "Return the neutral loss similarity score (0–1 range)."
