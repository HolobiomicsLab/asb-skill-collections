---
name: mass-spectrum-similarity-scoring
description: Use when when you have a query MS/MS spectrum (m/z and intensity pairs) that you need to match against a library of reference spectra, and you want to identify the -matching library entry while accounting for unmatched peaks that may indicate spectral contamination or chimerism.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3632
  edam_topics:
  - http://edamontology.org/topic_0121
  - http://edamontology.org/topic_3520
  tools:
  - cosine.py
  - entropy.py
  - bhattacharya1.py
  - reverse_search
derived_from:
- doi: 10.1021/acs.analchem.5c02047
  title: Reverse Spectral Search
evidence_spans: []
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_reverse_spectral_search_cq
    doi: 10.1021/acs.analchem.5c02047
    title: Reverse Spectral Search
  dedup_kept_from: coll_reverse_spectral_search_cq
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1021/acs.analchem.5c02047
  all_source_dois:
  - 10.1021/acs.analchem.5c02047
  zenodo_doi: TODO-zenodo
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# mass-spectrum-similarity-scoring

## Summary

Quantify the similarity between query and library MS/MS spectra using penalty-factor-enhanced scoring that balances spectral match sensitivity against quality control. This skill is essential for disambiguating chimeric spectra in metabolite annotation workflows.

## When to use

When you have a query MS/MS spectrum (m/z and intensity pairs) that you need to match against a library of reference spectra, and you want to identify the best-matching library entry while accounting for unmatched peaks that may indicate spectral contamination or chimerism. Apply this skill when standard symmetric spectral search is insufficient and you need to penalize low-quality matches containing unmatched fragment ions.

## When NOT to use

- When the input spectra are already pre-filtered or consensus spectra with chimeric fragments removed by other means—the penalty factor is designed to detect and downweight chimerism, not to handle already-clean spectra.
- When you need symmetric scoring only (query→library and library→query must yield identical scores); the reverse search penalty mechanism is asymmetric by design to favor library-explained peaks.

## Inputs

- Query MS/MS spectrum (m/z-intensity pairs)
- Library MS/MS spectrum (m/z-intensity pairs)
- m/z tolerance threshold (numeric, typically in ppm or Da)
- Penalty factor coefficient (numeric, 0–1 range typical)

## Outputs

- Penalized match score (scalar float)
- List of matched peak pairs (m/z_query, m/z_library, intensity_query, intensity_library)
- Unmatched peaks in query spectrum

## How to apply

Load the query MS/MS spectrum and the library MS/MS spectrum as paired m/z and intensity values. Specify an m/z tolerance threshold (e.g., typical values in the repository code) for peak matching. Identify matched peaks between query and library within the tolerance window. Calculate the base match score using cosine similarity, entropy similarity, or Bhattacharyya angle—all three are implemented in the reverse_search repository. For each unmatched peak in the query spectrum (peaks with no library counterpart within tolerance), apply a penalty factor to the base score. The penalty factor mechanism increases the number of spectral matches identified while maintaining rigorous quality control by downweighting spectra with unexplained fragment ions. Return the final penalized match score as a scalar value; higher scores indicate better-quality matches less likely to be chimeric.

## Related tools

- **cosine.py** (Implements cosine similarity scoring for symmetric and reverse spectral search) — https://github.com/Philipbear/reverse_search/blob/main/reverse_spectral_search/cosine.py
- **entropy.py** (Implements entropy similarity scoring for symmetric and reverse spectral search) — https://github.com/Philipbear/reverse_search/blob/main/reverse_spectral_search/entropy.py
- **bhattacharya1.py** (Implements Bhattacharyya angle similarity scoring for symmetric and reverse spectral search) — https://github.com/Philipbear/reverse_search/blob/main/reverse_spectral_search/bhattacharya1.py
- **reverse_search** (Primary toolset implementing penalty-factor-enhanced reverse spectral search) — https://github.com/Philipbear/reverse_search

## Evaluation signals

- Matched peaks are within the specified m/z tolerance threshold for both query and library m/z values.
- Unmatched peaks identified in the query spectrum have no counterpart in the library within tolerance; verify the list is complete by checking query peaks against library peaks exhaustively.
- Final penalized match score is lower than the base match score (before penalty); the reduction magnitude correlates with the number and intensity of unmatched peaks.
- Spectra with few unmatched peaks receive higher scores than spectra with many unmatched peaks, indicating improved discrimination of chimeric spectra.
- The returned score is a scalar between 0 and 1 (or as normalized by the chosen similarity metric); verify it falls within the expected range for your metric.

## Limitations

- Penalty factor effectiveness depends on correct specification of the m/z tolerance threshold; overly loose thresholds may mask chimerism, while overly tight thresholds may artificially penalize valid matches due to instrument calibration drift.
- The penalty mechanism assumes unmatched peaks are true contaminants; peaks from post-translational modifications, adducts, or loss products not represented in the library will be penalized even if genuine.
- No changelog is available in the repository, limiting reproducibility across versions and making it difficult to track when penalty-factor parameters were modified.

## Evidence

- [readme] Chimeric spectra are ubiquitous in MS/MS data, which compromises the quality and reliability of MS/MS matching-based metabolite annotation: "Chimeric spectra are ubiquitous in MS/MS data, which compromises the quality and reliability of MS/MS matching-based metabolite annotation."
- [readme] enhanced the reverse search by introducing a penalty factor to unmatched peaks, which increases the number of spectral matches while maintaining rigorous quality control: "enhanced the reverse search by introducing a penalty factor to unmatched peaks, which increases the number of spectral matches while maintaining rigorous quality control."
- [other] The reverse spectral search enhancement applies a penalty factor to unmatched peaks in the match scoring calculation, designed to increase spectral matches while maintaining rigorous quality control standards.: "The reverse spectral search enhancement applies a penalty factor to unmatched peaks in the match scoring calculation, designed to increase spectral matches while maintaining rigorous quality control"
- [other] Identify matched peaks between query and library using a specified m/z tolerance threshold. Calculate the base match score from matched peak pairs (e.g., cosine similarity or intensity-weighted sum). Identify unmatched peaks in the query spectrum that have no corresponding library peak within tolerance. Apply a penalty factor to the base match score for each unmatched peak to reduce the final score.: "Identify matched peaks between query and library using a specified m/z tolerance threshold. Calculate the base match score from matched peak pairs (e.g., cosine similarity or intensity-weighted sum)."
