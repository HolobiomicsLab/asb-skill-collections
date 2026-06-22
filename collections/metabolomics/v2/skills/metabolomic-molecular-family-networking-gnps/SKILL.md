---
name: metabolomic-molecular-family-networking-gnps
description: Use when when you have untargeted LC-MS/MS spectral data from microbial or environmental samples and aim to group related metabolites into molecular families for natural product discovery, especially when integrating with genomic biosynthetic gene cluster (BGC) annotations to link chemistry to.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3767
  edam_topics:
  - http://edamontology.org/topic_0154
  - http://edamontology.org/topic_3172
  tools:
  - nplinker
  - Python
  - conda
  - pip
  - GNPS
  - BigScape
  - NPLinker
  - AntiSMASH
derived_from:
- doi: 10.1186/s40168-022-01444-3
  title: NPClassScore
evidence_spans:
- It provides the tools [`GNPSDownloader`][nplinker.metabolomics.gnps.GNPSDownloader] and [`GNPSExtractor`][nplinker.metabolomics.gnps.GNPSExtractor]
- '[![github repo badge](https://img.shields.io/badge/github-nplinker-000.svg?color=blue)](https://github.com/NPLinker/nplinker)'
- Python version ≥3.11
- conda create -n npl-3.11 python=3.11
- pip install nplinker
- NPLinker requires GNPS molecular networking data as input. It currently accepts data from both GNPS1 (https://gnps.ucsd.edu) and GNPS2 (https://gnps2.org) workflows.
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_npclassscore_cq
    doi: 10.1186/s40168-022-01444-3
    title: NPClassScore
  dedup_kept_from: coll_npclassscore_cq
schema_version: 0.2.0
---

# metabolomic-molecular-family-networking-gnps

## Summary

Construct and analyze molecular family networks from untargeted metabolomic data using GNPS molecular networking to group spectrally similar compounds and enable downstream natural product discovery through genomic integration.

## When to use

When you have untargeted LC-MS/MS spectral data from microbial or environmental samples and aim to group related metabolites into molecular families for natural product discovery, especially when integrating with genomic biosynthetic gene cluster (BGC) annotations to link chemistry to genomic potential.

## When NOT to use

- Data are already organized into curated chemical databases (e.g., MIBiG, COCONUT) rather than raw spectral networks—use direct lookup instead.
- Spectral data lack sufficient mass accuracy or fragmentation diversity to form meaningful clusters (e.g., low-resolution MS1 only or very few fragments per spectrum).
- No genomic data (BGCs) are available or integration with genomic context is not the research goal.

## Inputs

- GNPS spectral molecular family annotations (family ID, member spectra, family mass, annotations from GNPS workflow output)
- LC-MS/MS spectra in GNPS-compatible format (e.g., MGF, mzML indexed by GNPS)
- GNPS molecular networking metadata (graph structure, spectral similarity scores, cosine similarity thresholds)

## Outputs

- Molecular family objects with member spectra, annotations, and computed family-level features
- Linkage graph connecting molecular families to genomic entities (BGCs, strains) with scoring metrics
- Serialized link tuples (source, target, link type, score) suitable for downstream natural product prioritization

## How to apply

Download or generate GNPS molecular networking data (spectral similarity networks derived from GNPS workflows at https://gnps.ucsd.edu or https://gnps2.org), which groups spectra into molecular families (MFs) by shared fragment ion patterns and precursor mass relationships. Structure the GNPS output in a `gnps` subdirectory with molecular family annotations and spectral metadata. Load the GNPS data using NPLinker's `npl.load_data()` method after configuring the root directory and input mode (local or remote). Access the loaded molecular family objects via `npl.mfs` to retrieve family membership, member spectra, annotations, and computed family mass values. Integrate these MFs with AntiSMASH-predicted BGCs (in an `antismash` subdirectory) to enable linkage scoring—e.g., using metcalf scoring via `npl.get_links()` to compute association scores between molecular families and BGCs. The rationale is that co-occurrence of spectral similarity (indicating chemical relatedness) and genomic proximity (indicating biosynthetic potential) strengthens confidence in natural product-BGC associations.

## Related tools

- **NPLinker** (Framework for loading GNPS molecular networking data, integrating with BGC annotations, and computing metcalf-scored linkages between molecular families and biosynthetic entities.) — https://github.com/NPLinker/nplinker
- **GNPS** (Public spectral molecular networking platform that generates family networks and annotations from untargeted LC-MS/MS data.) — https://gnps.ucsd.edu
- **AntiSMASH** (Genomic biosynthetic gene cluster prediction and annotation tool; output (BGC models) integrated with GNPS MFs for natural product linkage.)
- **BigScape** (Optional automated BGC clustering and network generation; NPLinker can invoke BigScape if BGC networks are required for enhanced linkage analysis.)

## Examples

```
npl.load_data(); links = npl.get_links(npl.gcfs[:3], 'metcalf'); link_tuples = [(l.source, l.target, l.score) for l in links.links]
```

## Evaluation signals

- Molecular family objects are successfully instantiated with non-empty member spectra lists, valid family masses, and annotation counts matching GNPS output inventory.
- LinkGraph serialization produces scored tuples with consistent source (MF) and target (BGC/strain) entity counts and score ranges (e.g., metcalf scores in expected bounds, no NaN/Inf).
- Integration with AntiSMASH BGC data results in linkable family-to-BGC pairs where genomic proximity (e.g., BGC co-location on contigs) correlates with high linkage scores.
- No orphaned molecular families (families with zero linked BGCs if expected from prior biological knowledge) or spurious zero-distance links between unrelated entities.
- Downstream filtering or prioritization (e.g., selecting links above a metcalf score threshold) yields chemically and genomically coherent subsets amenable to experimental validation.

## Limitations

- GNPS molecular family assignment depends on spectral similarity thresholds and fragmentation patterns; poorly fragmented or noisy spectra may fail to cluster or assign to wrong families.
- Linkage scoring (e.g., metcalf) relies on heuristics for BGC-to-MF association; biological validation is required as predicted links may not reflect true biochemical relationships.
- GNPS1 and GNPS2 workflows may produce heterogeneous output formats; data must be carefully prepared and validated before loading to avoid parsing failures.
- The article contains only changelog entries and dependency bumps, with no discussion section addressing reproducibility limitations, methodological caveats, or failure modes.

## Evidence

- [readme] NPLinker is a python framework for data mining microbial natural products by integrating genomics and metabolomics data.: "NPLinker is a python framework for data mining microbial natural products by integrating genomics and metabolomics data."
- [other] Instantiate NPLinker with the configuration file path and call npl.load_data() to load GNPS spectra, molecular families, annotations, and AntiSMASH BGC data from the gnps and antismash subdirectories.: "Instantiate NPLinker with the configuration file path and call npl.load_data() to load GNPS spectra, molecular families, annotations, and AntiSMASH BGC data from the gnps and antismash subdirectories."
- [other] Call npl.get_links(npl.gcfs[:3], 'metcalf') to compute metcalf-scored links between the first three GCFs and other entities, returning a LinkGraph object.: "Call npl.get_links(npl.gcfs[:3], 'metcalf') to compute metcalf-scored links between the first three GCFs and other entities, returning a LinkGraph object."
- [other] currently accepts data from both GNPS1 (https://gnps.ucsd.edu) and GNPS2 (https://gnps2.org) workflows: "currently accepts data from both GNPS1 (https://gnps.ucsd.edu) and GNPS2 (https://gnps2.org) workflows"
- [other] NPLinker requires GNPS molecular networking data as input: "NPLinker requires GNPS molecular networking data as input"
