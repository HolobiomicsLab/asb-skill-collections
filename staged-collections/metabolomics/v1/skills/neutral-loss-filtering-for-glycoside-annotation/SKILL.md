---
name: neutral-loss-filtering-for-glycoside-annotation
description: Filter MS/MS spectra by characteristic neutral losses to rapidly annotate glycosylated metabolites in feature-based molecular networks. This skill uses MassQL queries targeting pentose (132.0423 Da) and hexose (162.0528 Da) neutral losses to identify and cluster glycoside variants in untargeted LC-MS/MS data without reference standards.
when_to_use_negative:
- Input is already a fully structurally annotated feature table with confirmed metabolite identities from NMR or MS/MS library matching; neutral-loss filtering adds no value.
- MS/MS spectra lack sufficient fragmentation depth or signal intensity (peaks below 10,000 amplitude threshold) to reliably detect neutral losses.
- Target metabolites are aglycones or contain no glycosidic bonds; no neutral losses of 132 or 162 Da will occur.
edam_operation: http://edamontology.org/operation_3933
edam_topics:
- http://edamontology.org/topic_0625
- http://edamontology.org/topic_3520
- http://edamontology.org/topic_0121
tools:
- name: GNPS (Global Natural Products Social Molecular Networking)
  role: Host platform for feature-based molecular networking (FBMN) workflow and MassQL query execution; generates spectral similarity networks and cosine similarity scoring
  repo: https://gnps.ucsd.edu
- name: MassQL
  role: Query engine for filtering MS/MS spectra by characteristic neutral loss patterns (132.0423 Da pentose, 162.0528 Da hexose) within GNPS spectral nodes
- name: LC-MS/MS
  role: Acquisition instrument generating raw MS/MS fragmentation spectra; spectra are processed and uploaded to GNPS for FBMN and MassQL filtering
- name: Feature Detection and Alignment (FBMN preprocessing)
  role: Converts raw LC-MS/MS data into aligned feature tables with MS/MS scans; peak detection set at >10,000 amplitude threshold to cutoff noise before FBMN upload
provenance:
  source_task_ids:
  - task_001
  source_papers:
  - doi: 10.1073/pnas
    title: Proceedings of the National Academy of Sciences
schema_version: 0.2.0
metadata:
  iri: https://w3id.org/holobiomicslab/asb-skill/neutral-loss-filtering-for-glycoside-annotation@sha256:16c3e80a9877a37678a4ae7f3a9bc9822d949be83cbc9dacfcc7ac5770605e3b
---

# neutral-loss-filtering-for-glycoside-annotation

## Summary

Filter MS/MS spectra by characteristic neutral losses to rapidly annotate glycosylated metabolites in feature-based molecular networks. This skill uses MassQL queries targeting pentose (132.0423 Da) and hexose (162.0528 Da) neutral losses to identify and cluster glycoside variants in untargeted LC-MS/MS data without reference standards.

## When to use

Apply this skill when you have feature-based molecular network (FBMN) spectral nodes from LC-MS/MS and need to annotate glycosylated metabolites (e.g., O-xylosylated, O-glucosylated, or O-glucuronidated compounds) within complex biotransformation or natural product mixtures. Use it when MS/MS spectra show characteristic neutral loss patterns and you want to group structurally similar glycosides together in the network without requiring pure standards or NMR validation for every variant.

## When NOT to use

- Input is already a fully structurally annotated feature table with confirmed metabolite identities from NMR or MS/MS library matching; neutral-loss filtering adds no value.
- MS/MS spectra lack sufficient fragmentation depth or signal intensity (peaks below 10,000 amplitude threshold) to reliably detect neutral losses.
- Target metabolites are aglycones or contain no glycosidic bonds; no neutral losses of 132 or 162 Da will occur.

## Inputs

- feature-based molecular network spectral nodes (FBMN output from GNPS)
- LC-MS/MS peak detection results with MS/MS fragmentation spectra (aligned with precursor m/z and retention time)
- spectral similarity scores (cosine similarity, default or user-optimized)

## Outputs

- MassQL-filtered spectral node list annotated with neutral loss type (pentose or hexose)
- clusters of isobaric or structural glycoside variants grouped in the molecular network
- annotated metabolite identities (e.g., O-xylosylated or O-glucosylated derivatives) mapped to network nodes

## How to apply

After generating a feature-based molecular network in GNPS with cosine similarity scoring, configure a MassQL query to search for MS/MS spectra exhibiting neutral losses of either 132.0423 Da (pentose, e.g., xylose) or 162.0528 Da (hexose, e.g., glucose or glucuronic acid). Execute the MassQL query within GNPS to filter spectral nodes matching these thresholds. Cross-reference the MassQL-filtered spectral nodes with the molecular network clusters to identify and group metabolites sharing the same glycoside modifications. Validate the annotation by comparing detected nodes against known biotransformation pathways (e.g., comparing 1-supplemented versus 2-supplemented culture broths) or by confirming co-clustering with a reference glycoside in the network. The neutral loss thresholds are empirically chosen and represent the exact mass difference for common plant and fungal glycosylation; adjust thresholds only if you observe systematic misses (e.g., deuterated or unusual isotopologue variants).

## Related tools

- **GNPS (Global Natural Products Social Molecular Networking)** (Host platform for feature-based molecular networking (FBMN) workflow and MassQL query execution; generates spectral similarity networks and cosine similarity scoring) — https://gnps.ucsd.edu
- **MassQL** (Query engine for filtering MS/MS spectra by characteristic neutral loss patterns (132.0423 Da pentose, 162.0528 Da hexose) within GNPS spectral nodes)
- **LC-MS/MS** (Acquisition instrument generating raw MS/MS fragmentation spectra; spectra are processed and uploaded to GNPS for FBMN and MassQL filtering)
- **Feature Detection and Alignment (FBMN preprocessing)** (Converts raw LC-MS/MS data into aligned feature tables with MS/MS scans; peak detection set at >10,000 amplitude threshold to cutoff noise before FBMN upload)

## Evaluation signals

- MassQL-filtered spectral nodes cluster with known glycoside references (e.g., baicalin for hexose or xylose variants) in the molecular network with cosine similarity >0.7 between structurally related glycosides.
- Annotated clusters show expected mass shifts corresponding to pentose (−132.04 Da) or hexose (−162.05 Da) loss relative to their aglycone precursor; mass error <5 ppm.
- Multiple glycoside variants from the same aglycone core (e.g., compounds 2a–2g, all xylosylated baicalein derivatives) are grouped together and absent in non-supplemented control cultures.
- Neutral loss filtering recovers >80% of manually identified or NMR-confirmed glycosides in a validation set; false positive rate (aglycones or non-glycosides matching the query) is <10%.
- Peak detection threshold cutoff (>10,000 amplitude) removes noise-level signals while retaining biological replicates with consistent neutral loss patterns across time-course or multi-species experiments.

## Limitations

- Neutral loss filtering assumes glycosidic bonds fragment cleanly; some glycosides may exhibit alternative fragmentation pathways (e.g., side-chain cleavage) and miss the expected 132 or 162 Da loss, leading to false negatives.
- Ambiguous for distinguishing isomeric glycosides (e.g., O-xylose vs. O-glucose, both hexose or pentose families) without additional MS/MS fragmentation patterns or orthogonal validation (NMR, chemical derivatization, or MS/MS/MS); neutral loss alone does not confirm regioisomerism.
- Performance depends on MS/MS spectral quality and instrument sensitivity; low-abundance metabolites or weak fragmentation may fall below the peak amplitude threshold (>10,000) and be filtered out.
- MassQL query specificity may be compromised if non-glycosidic neutral losses (e.g., from loss of larger neutral moieties) coincidentally equal 132 or 162 Da in the focal metabolite class; manual review of top hits is recommended.
- Requires complete FBMN network and GNPS repository availability; partial or offline spectral libraries may miss cross-reference annotations for structurally related compounds.

## Evidence

- [results] MassQL successfully annotated hexosylation and pentosylation by detecting neutral losses of 162.05 Da and 132.04 Da in MS/MS fragmentation spectra: "MassQL successfully annotated hexosylation and pentosylation by detecting neutral losses of 162.05 Da and 132.04 Da in MS/MS fragmentation spectra, enabling rapid annotation of glycosylated flavonoid"
- [results] MassQL was helpful for the annotation of sugar conjugation, as it rapidly annotated hexosylation and pentosylation of the flavonoids: "MassQL was helpful for the annotation of sugar conjugation, as it rapidly annotated hexosylation and pentosylation of the flavonoids"
- [discussion] MS/MS spectra containing neutral losses of 132.0423 or 162.0528 Da were searched via MassQL: "MS/MS spectra containing neutral losses of 132.0423 or 162.0528 Da were searched via MassQL"
- [discussion] with peak detection set at over 10,000 amplitudes to cutoff noise level: "with peak detection set at over 10,000 amplitudes to cutoff noise level"
- [results] Many spectral nodes could be structurally annotated due to high coverage of the GNPS MS/MS reference library: "Many spectral nodes could be structurally annotated due to high coverage of the GNPS MS/MS reference library"
- [other] Apply MassQL queries within GNPS to filter for MS/MS spectra exhibiting neutral losses of 132.0423 Da (pentosylation) or 162.0528 Da (hexosylation): "Apply MassQL queries within GNPS to filter for MS/MS spectra exhibiting neutral losses of 132.0423 Da (pentosylation) or 162.0528 Da (hexosylation)."
- [other] Cross-reference MassQL-annotated spectral nodes with the molecular network to identify clusters corresponding to pentosylated and hexosylated metabolites: "Cross-reference MassQL-annotated spectral nodes with the molecular network to identify clusters corresponding to pentosylated and hexosylated metabolites."
