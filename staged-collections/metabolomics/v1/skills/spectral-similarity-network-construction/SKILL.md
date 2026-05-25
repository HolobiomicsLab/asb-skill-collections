---
name: spectral-similarity-network-construction
description: Use when metabolomics technique involves LC-MS or GC-MS to construct feature-based molecular networks by computing cosine similarity scores between MS/MS fragmentation spectra and visualizing them as spectral similarity networks.
when_to_use_negative:
- Input is already a pre-curated list of known metabolites with confirmed structures — direct targeted analysis is more efficient.
- MS/MS spectra lack sufficient fragmentation (e.g., only precursor ion observed) — spectral similarity scoring requires informative product ion peaks.
- Sample complexity is very low (e.g., single purified compound) — network visualization adds no interpretive value.
edam_operation: http://edamontology.org/operation_0315
edam_topics:
- http://edamontology.org/topic_0121
- http://edamontology.org/topic_3520
tools:
- name: GNPS
  role: Hosts feature-based molecular networking (FBMN) workflow and computes cosine similarity scoring between all MS/MS spectra; provides access to public MS/MS reference library for spectral node annotation
- name: LC-MS/MS
  role: Generates raw MS/MS fragmentation spectra used as input for spectral similarity calculations
- name: MassQL
  role: Post-hoc spectral filtering to annotate subsets of molecular network nodes by neutral loss or fragment ion patterns (e.g., pentosylation/hexosylation signatures)
provenance:
  source_task_ids:
  - task_001
  source_papers:
  - doi: 10.1073/pnas
    title: Proceedings of the National Academy of Sciences
schema_version: 0.2.0
derived_from:
- doi: 10.1073/pnas
metadata:
  iri: https://w3id.org/holobiomicslab/asb-skill/spectral-similarity-network-construction@sha256:d31f4718adb1b0d1fb3b44cd285e235197dd90c59e88643335745dac11bf311e
---

# spectral-similarity-network-construction

## Summary

Construct feature-based molecular networks by computing cosine similarity scores between MS/MS fragmentation spectra and visualizing them as spectral similarity networks. This skill enables rapid, untargeted annotation of metabolite clusters and detection of related compounds in complex fungal biotransformation LC-MS/MS datasets.

## When to use

Apply this skill when you have feature-extracted LC-MS/MS data (aligned peaks and MS/MS spectra) from complex biological samples and need to discover metabolite clusters, relate structurally similar compounds, or annotate unknown spectral nodes against reference libraries. Particularly valuable when investigating enzymatic biotransformation of multiple compounds across multiple fungal species, where direct structure elucidation is infeasible and spectral similarity can guide prioritization.

## When NOT to use

- Input is already a pre-curated list of known metabolites with confirmed structures — direct targeted analysis is more efficient.
- MS/MS spectra lack sufficient fragmentation (e.g., only precursor ion observed) — spectral similarity scoring requires informative product ion peaks.
- Sample complexity is very low (e.g., single purified compound) — network visualization adds no interpretive value.

## Inputs

- Feature-extracted LC-MS/MS data (mzML or NetCDF format with aligned peaks and MS/MS spectra)
- Sample metadata (fungal species, treatment condition, time point)
- MS/MS peak detection threshold (recommended: amplitude > 10,000 to cutoff noise)

## Outputs

- Spectral similarity network (nodes = spectral features, edges = cosine similarity ≥ threshold)
- Network edge list with cosine similarity scores
- Annotated spectral nodes linked to GNPS MS/MS reference library hits
- Clustered metabolite groups for downstream structural or enzymatic analysis

## How to apply

Upload your feature-extracted LC-MS/MS dataset to GNPS and initiate the feature-based molecular networking (FBMN) workflow with default parameters for MS/MS peak detection and alignment. Configure FBMN to generate a spectral similarity network using cosine similarity scoring (default threshold typically 0.7 or site-dependent). The workflow automatically computes pairwise cosine similarity between all MS/MS spectra, filters edges by the similarity threshold, and produces a network graph where nodes represent spectral features and edges represent cosine similarity relationships. Retrieve the resulting molecular network nodes and edges upon job completion. Cross-reference the spectral nodes against the GNPS public MS/MS reference library to structurally annotate clusters. Clusters of high-similarity nodes often correspond to isobaric metabolites, regioisomers, or congeners differing by small chemical modifications (e.g., hydroxylation, glycosylation).

## Related tools

- **GNPS** (Hosts feature-based molecular networking (FBMN) workflow and computes cosine similarity scoring between all MS/MS spectra; provides access to public MS/MS reference library for spectral node annotation)
- **LC-MS/MS** (Generates raw MS/MS fragmentation spectra used as input for spectral similarity calculations)
- **MassQL** (Post-hoc spectral filtering to annotate subsets of molecular network nodes by neutral loss or fragment ion patterns (e.g., pentosylation/hexosylation signatures))

## Evaluation signals

- Network connectivity and clustering: spectral nodes with identical precursor m/z should appear in the same connected component if fragmentation patterns are sufficiently similar; absence suggests poor MS/MS quality or low cosine similarity threshold.
- Cross-validation against known structures: seven xylosylated metabolites (2a–2g) from NMR characterization should all appear in a single or closely related cluster in the molecular network, confirming cosine similarity correctly groups regioisomers and congeners.
- Reference library coverage: the percentage of spectral nodes with GNPS library annotations should be non-negligible (>30% in typical untargeted fungal metabolomics); low coverage indicates sparse reference data for the organism or chemical class.
- Edge weight distribution: cosine similarity scores should follow a right-skewed distribution with a peak near the threshold and a long tail toward 1.0; bimodal distributions may indicate subpopulations of spectral quality or chemical class.
- Repeatability: identical sample run on the same platform should yield the same network topology and edge scores within a tolerance (e.g., cosine similarity difference < 0.05).

## Limitations

- Cosine similarity is blind to absolute chemical differences: regioisomers with very similar MS/MS fragmentation patterns (e.g., 2,3-xylosylated vs. 2,4-xylosylated baicalein) may be indistinguishable without complementary analytical methods (NMR, HRMS, or MS3).
- Network inference is highly sensitive to MS/MS spectral quality and peak detection threshold; noisy or weakly ionizing metabolites produce unreliable similarity scores and poor clustering.
- Reference library coverage bias: spectral nodes for non-model organisms (e.g., wood-decaying fungi) often lack direct library hits; annotation relies on presumed similarity to known compounds, which can lead to false positives or missed structural variants.
- Computational scalability: feature-based molecular networking is memory-intensive for very large datasets (>10,000 unique precursor ions); GNPS job runtime can exceed 24 hours for complex samples.
- Cosine similarity threshold is user-defined and dataset-dependent; no universal consensus threshold exists. The authors did not explicitly state a threshold value, relying on GNPS defaults, which may vary.

## Evidence

- [other] Upload dataset to GNPS and initiate the feature-based molecular networking (FBMN) workflow with default parameters for MS/MS peak detection and alignment.: "Upload dataset to GNPS and initiate the feature-based molecular networking (FBMN) workflow with default parameters for MS/MS peak detection and alignment."
- [other] Configure FBMN to generate a spectral similarity network and cosine similarity scoring.: "Configure FBMN to generate a spectral similarity network and cosine similarity scoring."
- [results] Many spectral nodes could be structurally annotated due to high coverage of the GNPS MS/MS reference library: "Many spectral nodes could be structurally annotated due to high coverage of the GNPS MS/MS reference library"
- [discussion] with peak detection set at over 10,000 amplitudes to cutoff noise level: "with peak detection set at over 10,000 amplitudes to cutoff noise level"
- [results] An example of the molecular network- and MassQL-based enzymatic reactivity annotation: "An example of the molecular network- and MassQL-based enzymatic reactivity annotation"
