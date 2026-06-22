---
name: cross-database-structural-homology-matching
description: Use when when you have antiSMASH-predicted BGCs and wish to link them to metabolomic data via structure prediction, but only BGCs with sufficient structural homology to characterized reference clusters will yield reliable predictions.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_0346
  edam_topics:
  - http://edamontology.org/topic_0621
  - http://edamontology.org/topic_0080
  - http://edamontology.org/topic_3372
  tools:
  - antiSMASH
  - BiG-SCAPE
  - NPLinker
  - GNPS
  - MIBiG
  - BLAST
derived_from:
- doi: 10.1101/2024.10.11.617756
  title: NPLinker
- doi: 10.1371/journal.pcbi.1008920
  title: ''
evidence_spans:
- after downloading the strain assemblies and metabolomics data, the genomes were run through antiSMASH v5.0.0 for BGC detection
- genomes were run through antiSMASH v5.0.0 for BGC detection
- and BiG-SCAPE v1.0.0 to cluster the BGCs into GCFs
- BiG-SCAPE v1.0.0 to cluster the BGCs into GCFs
- NPLinker, a software framework to link genomic and metabolomic data
- NPLinker creates objects for spectra, MFs, BGCs and GCFs in the data set
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_nplinker
    doi: 10.1101/2024.10.11.617756
    title: NPLinker
  dedup_kept_from: coll_nplinker
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1101/2024.10.11.617756
  all_source_dois:
  - 10.1101/2024.10.11.617756
  - 10.1371/journal.pcbi.1008920
  zenodo_doi: TODO-zenodo
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# cross-database-structural-homology-matching

## Summary

Match biosynthetic gene clusters (BGCs) to reference database entries (MIBiG) using cumulative BLAST homology scoring to identify those with known or predicted metabolite structures. This filtering step enables downstream molecular fingerprint extraction and structure-guided metabolomic-genomic linking.

## When to use

When you have antiSMASH-predicted BGCs and wish to link them to metabolomic data via structure prediction, but only BGCs with sufficient structural homology to characterized reference clusters will yield reliable predictions. Use this skill to identify which subset of your BGC collection has actionable structural annotations from MIBiG or similar curated repositories.

## When NOT to use

- Your BGCs are already structurally characterized by orthology or biochemical validation; homology filtering adds no new information.
- Your metabolomic dataset has no associated spectra or structure libraries; structural homology alone cannot rank BGC–metabolite links without a second scoring modality.
- You are working with plant or environmental samples with very low sequence identity to MIBiG bacterial clusters; the homology threshold may eliminate all candidate BGCs.

## Inputs

- antiSMASH-predicted BGC protein sequences (or FASTA format)
- MIBiG database (flat file or indexed BLAST database)
- BGC-to-strain mapping (optional but recommended for correlation analysis)

## Outputs

- Filtered BGC set with cumulative BLAST scores ≥ threshold
- BGC-to-MIBiG entry mapping table
- Molecular fingerprints and structures extracted from MIBiG annotations
- Candidate set of structures for spectrum-to-BGC scoring

## How to apply

Run BLAST of your BGC protein sequences against the MIBiG database and accumulate raw BLAST bit scores for each BGC-MIBiG entry pair. Apply a cumulative BLAST score threshold (≥10,000 in the NPLinker study) to identify BGCs with substantial structural homology to at least one MIBiG entry. For each passing BGC, extract the associated metabolite structures and molecular fingerprints from MIBiG annotations; these fingerprints become features for structure-informed scoring (e.g., IOKR) of metabolite-BGC associations. Document the number of BGCs passing the homology filter and how many MIBiG reference structures were retrieved, as this directly determines the size of the candidate set for downstream metabolomic matching.

## Related tools

- **BLAST** (Sequence homology search to identify BGCs with structural homology to MIBiG entries and accumulate cumulative scores)
- **MIBiG** (Reference database of characterized biosynthetic clusters with structural annotations and metabolite predictions)
- **antiSMASH** (BGC prediction and initial annotation prior to homology matching) — https://github.com/sdrogers/nplinker
- **NPLinker** (Framework integrating BGC homology filtering, structure extraction, and metabolomic linking) — https://github.com/NPLinker/nplinker

## Evaluation signals

- Number of BGCs passing the cumulative BLAST score threshold (≥10,000) and percentage of the input BGC set recovered; in the study, 2,242 of 3,316 BGCs (67.6%) passed this filter.
- Validation that all retrieved MIBiG structures have associated molecular fingerprints in the expected format(s) (CDK substructure, PubChem, Klekota-Roth).
- Spot-check that a random sample of high-scoring BGC-MIBiG pairs show plausible product-class consistency (e.g., both flagged as PKS or NRP).
- Downstream enrichment: validated BGC–metabolite links retrieved from the homology-filtered candidate set should show significantly higher enrichment in IOKR or combined scores than links from the full BGC set (p < 0.05).
- Cross-reference: confirm that no manual false negatives occur—i.e., visually inspect a small set of filtered-out BGCs to ensure they do not harbour obvious structural homology that the threshold missed.

## Limitations

- Reliance on MIBiG homology restricts applicability to BGCs with considerable sequence identity to characterized clusters; novel or divergent clusters are excluded. The study acknowledges: 'restricts its use to those BGCs which show considerable homology with MIBiG entries. While still useful in this form, predicting molecular fingerprints directly from BGCs would broaden the…' scope.
- Cumulative BLAST score threshold (≥10,000) is somewhat arbitrary and may vary by organism, gene cluster type, and sequencing depth; no universal threshold is validated across all microbiomes.
- MIBiG database coverage is biased toward well-studied bacterial taxa and secondary metabolite classes (e.g., PKS, NRPS); underrepresented lineages or rare chemistry will have few or no homologs.
- Molecular fingerprints extracted from MIBiG structures depend on the structure being correctly assigned and fully resolved; partial or ambiguous structures will yield uninformative fingerprints.
- The filtered candidate set is fixed at the time of analysis; as MIBiG grows, the set must be regenerated to capture newly annotated homologs.

## Evidence

- [methods] For BGCs with MIBiG structural homology (cumulative BLAST score ≥10,000), extract molecular fingerprints from predicted metabolite structures: "For BGCs with MIBiG structural homology (cumulative BLAST score ≥10,000), extract molecular fingerprints from predicted metabolite structures and score BGC–spectrum links using Input-Output Kernel"
- [results] Out of 3316 BGCs in the data set, 2242 could be assigned structure based on similarity to MIBiG entries, and used as candidate set for the 6246 MS2 spectra in the data set: "Out of 3316 BGCs in the data set, 2242 could be assigned structure based on similarity to MIBiG entries, and used as candidate set for the 6246 MS2 spectra in the data set"
- [discussion] restricts its use to those BGCs which show considerable homology with MIBiG entries. While still useful in this form, predicting molecular fingerprints directly from BGCs would broaden the: "restricts its use to those BGCs which show considerable homology with MIBiG entries. While still useful in this form, predicting molecular fingerprints directly from BGCs would broaden the"
- [discussion] By pairing the MIBiG and GNPS databases, and using the Paired omics Data Platform, we introduced data sets to test the efficiency of the scoring methods: "By pairing the MIBiG and GNPS databases, and using the Paired omics Data Platform, we introduced data sets to test the efficiency of the scoring methods"
- [readme] NPLinker is a python framework for data mining microbial natural products by integrating genomics and metabolomics data.: "NPLinker is a python framework for data mining microbial natural products by integrating genomics and metabolomics data."
