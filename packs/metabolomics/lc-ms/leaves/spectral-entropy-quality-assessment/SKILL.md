---
name: spectral-entropy-quality-assessment
description: Use when after feature detection and alignment in untargeted MS data
  processing, when you need to filter or rank candidate metabolite annotations by
  spectral quality before committing to xenobiotic metabolite assignments. Use when
  combining fragmentation similarity scores (e.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3632
  edam_topics:
  - http://edamontology.org/topic_3172
  - http://edamontology.org/topic_0091
  - http://edamontology.org/topic_3407
  tools:
  - tidyverse
  - CluMSID
  - CluMSIDdata
  - grid
  - OrgMassSpecR
  - pheatmap
  - reshape2
  - MSMSsim
  - msentropy
  - readxl
  techniques:
  - LC-MS
  license_tier: restricted
  provenance_tier: literature
derived_from:
- doi: 10.1021/acs.est.5c08558
  title: CMDN
evidence_spans:
- tidyverse
- CluMSID
- CluMSIDdata
- grid
- OrgMassSpecR
- pheatmap
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_cmdn_cq
    doi: 10.1021/acs.est.5c08558
    title: CMDN
  dedup_kept_from: coll_cmdn_cq
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1021/acs.est.5c08558
  all_source_dois:
  - 10.1021/acs.est.5c08558
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# spectral-entropy-quality-assessment

> **License: restricted** — no clear open-source license detected for the underlying tool; verify licensing before commercial use or redistribution. <!-- asb-license-banner -->
## Summary

Calculate spectral entropy from MS/MS fragmentation patterns to assess the complexity and confidence of spectral annotations in untargeted metabolomics. High entropy indicates well-resolved, information-rich spectra suitable for reliable metabolite identification; low entropy may signal noise, poor fragmentation, or ambiguous annotations.

## When to use

After feature detection and alignment in untargeted MS data processing, when you need to filter or rank candidate metabolite annotations by spectral quality before committing to xenobiotic metabolite assignments. Use when combining fragmentation similarity scores (e.g., from MSMSsim) with confidence metrics to discriminate true metabolite signals from instrumental or chemical noise.

## When NOT to use

- Input spectra are already manually curated or have undergone aggressive noise filtering that removes informative low-intensity peaks; entropy will not discriminate signal.
- Xenobiotic metabolites of interest are known to fragment minimally or produce dominant single peaks; entropy-based filtering may incorrectly deprioritize authentic metabolites.
- Feature table already contains orthogonal confidence metrics (e.g., isotope pattern fit, adduct consistency); entropy may introduce redundant filtering and remove borderline-but-valid identifications.

## Inputs

- Aligned MS/MS feature table (output from CluMSID feature detection)
- Raw MS/MS spectra in netCDF, mzXML, or mzML format
- Feature-to-spectrum mapping (m/z, retention time, cluster ID)

## Outputs

- Spectral entropy scores per feature (numeric vector, range 0–1 or 0–log(n))
- Entropy-ranked feature annotation confidence table
- QC report flagging low-entropy or ambiguous spectra

## How to apply

Apply the msentropy R package to compute spectral entropy values for each aligned feature's MS/MS spectrum. Entropy is calculated from the distribution of peak intensities in the fragmentation pattern, where higher entropy reflects greater peak diversity and lower entropy reflects dominant single peaks or noise-like patterns. Integrate entropy scores as a confidence filter: features with entropy below a project-defined threshold (not specified in the source, but typically empirically optimized per instrument and metabolite class) may be deprioritized or flagged for manual review. Use entropy alongside MSMSsim cosine similarity and exact mass accuracy to form a composite annotation confidence score; this tri-partite ranking supports automated annotation propagation and reduces false-positive metabolite calls in xenobiotic metabolite discovery.

## Related tools

- **msentropy** (Computes spectral entropy from MS/MS fragmentation patterns to quantify spectral complexity and confidence)
- **MSMSsim** (Calculates fragmentation pattern similarity scores that are integrated with entropy for composite annotation ranking)
- **CluMSID** (Performs feature detection and alignment upstream of entropy calculation; entropy scores are used to refine cluster-based annotation propagation)
- **OrgMassSpecR** (Provides exact mass calculation for candidate metabolites; combined with entropy and similarity scores for final annotation confidence)

## Evaluation signals

- Entropy scores are numeric, bounded (typically 0–1 or 0–log(n_peaks)), and vary across features; constant or all-zero entropy suggests calculation failure.
- Features with high entropy (>0.7, typical threshold) show multiple peaks of comparable intensity in their MS/MS spectra; low-entropy features show dominant single peaks or noise-like distributions.
- Entropy-ranked annotations correlate with manual curation or orthogonal validation (e.g., literature-matched reference spectra, external database hits); high-entropy matches have higher validation rate.
- Entropy-filtered feature table is smaller and more homogeneous than unfiltered; retained features show lower false-discovery rate in downstream pathway or toxicity prediction tasks.
- Entropy values can be visually inspected in annotated heatmaps or scatter plots (entropy vs. similarity score, entropy vs. m/z) to identify outliers or systematic bias.

## Limitations

- Entropy is sensitive to spectral preprocessing (noise removal, peak intensity normalization); inconsistent preprocessing pipelines across instruments or labs will yield non-comparable entropy values.
- No universal entropy threshold is provided in the CMDN framework; users must empirically optimize cutoffs for their specific metabolite class, instrument, and ionization method.
- Entropy alone cannot distinguish genuine low-abundance fragments from noise; it must be combined with other metrics (similarity, mass accuracy, isotope pattern) to avoid misclassification.
- Metabolites with intrinsically simple fragmentation patterns (few dominant losses) will have low entropy despite being authentic; entropy-based filtering may inadvertently bias discovery toward high-fragmentation metabolites.

## Evidence

- [other] Calculate spectral entropy using msentropy to assess fragment complexity and confidence: "Calculate spectral entropy using msentropy to assess fragment complexity and confidence."
- [readme] CMDN is a top-down untargeted metabolomics-based MS data processing framework to enable high-throughput and automated annotation of reaction-derived xenobiotic metabolites: "Compound metabolite discovery network (CMDN) is an "top-down" untargeted metabolomics-based MS data processing framework to enable high-throughput and automated annotation of reaction-derived"
- [other] Apply MSMSsim to compute fragmentation pattern similarity scores between unknown features and reference spectra: "Apply MSMSsim to compute fragmentation pattern similarity scores between unknown features and reference spectra."
- [other] Annotate metabolites by matching aligned features to xenobiotic reaction databases using OrgMassSpecR for exact mass calculation and CluMSID for cluster-based annotation propagation: "Annotate metabolites by matching aligned features to xenobiotic reaction databases using OrgMassSpecR for exact mass calculation and CluMSID for cluster-based annotation propagation."
