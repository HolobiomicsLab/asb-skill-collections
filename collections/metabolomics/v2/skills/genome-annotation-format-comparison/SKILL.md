---
name: genome-annotation-format-comparison
description: Use when when running metabologenomic RiPP detection pipelines (MetaMiner)
  on the same genomic dataset but with different input sequence formats (e.g., contigs.fasta
  vs. antiSMASH .final.gbk output), or when unexpected null results occur and input
  format choice is a plausible cause.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3227
  edam_topics:
  - http://edamontology.org/topic_0080
  - http://edamontology.org/topic_0621
  - http://edamontology.org/topic_3520
  tools:
  - NPDtools 2.5.0
  - MetaMiner
  - antiSMASH
  - Dereplicator
  - NPDtools
  techniques:
  - LC-MS
  license_tier: restricted
derived_from:
- doi: 10.1038/s41467-018-06082-8
  title: dereplicator
evidence_spans:
- The latest version is available in the Natural Product Discovery toolkit (NPDtools)
  at https://github.com/ablab/npdtools
- MetaMiner is a metabologenomic pipeline which integrates metabolomic (tandem mass
  spectra) and genomic data to identify novel RiPPs
- MetaMiner is a metabologenomic pipeline which integrates metabolomic (tandem mass
  spectra) and genomic data to identify novel Ribosmally synthesized and Post-translationally
  modified Peptides (RiPPs)
- 'MetaMiner uses either raw nucleotide sequences or specific genome mining tools''
  output: raw nucleotide sequences `.fasta` format or *antiSMASH*''s `.final.gbk`
  or `.gbk` file'
- matches tandem mass spectra against the constructed post-translationally modified
  RiPPs structure database using Dereplicator
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_dereplicator
    doi: 10.1038/s41467-018-06082-8
    title: dereplicator
  dedup_kept_from: coll_dereplicator
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1038/s41467-018-06082-8
  all_source_dois:
  - 10.1038/s41467-018-06082-8
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# genome-annotation-format-comparison

> **License: restricted** — no clear open-source license detected for the underlying tool; verify licensing before commercial use or redistribution. <!-- asb-license-banner -->
## Summary

Compare the detection performance of metabologenomic pipelines (e.g. MetaMiner) across different genome annotation input formats (raw FASTA sequences vs. tool-specific outputs like antiSMASH .gbk files) to identify format-dependent detection failures and inform format selection for downstream analysis.

## When to use

When running metabologenomic RiPP detection pipelines (MetaMiner) on the same genomic dataset but with different input sequence formats (e.g., contigs.fasta vs. antiSMASH .final.gbk output), or when unexpected null results occur and input format choice is a plausible cause. Specifically apply this skill when a detection task succeeds with one format but fails with another, suggesting a format-dependent sensitivity issue rather than a data quality problem.

## When NOT to use

- When only one input format is available; this skill requires parallel runs with both formats to meaningfully compare.
- When the metabologenomic pipeline is not MetaMiner or a pipeline with documented format-dependent behavior; comparison may not be informative for tools with format-agnostic parsers.
- When detected differences are attributed to parameter changes (e.g., different BGC detection thresholds or search modes) rather than format alone; isolate format variation by keeping all other parameters constant.

## Inputs

- LC-MS/MS spectra files (MGF format)
- Raw nucleotide sequences (.fasta format)
- Genome annotation files (.final.gbk or .gbk from antiSMASH)
- Expected target RiPP peptide sequence(s) or identifier(s) for validation

## Outputs

- significant_matches.tsv from MetaMiner run with FASTA input
- significant_matches.tsv from MetaMiner run with .gbk input
- Format comparison report documenting presence/absence of target RiPPs in each run
- Empirical recommendation for preferred input format for this dataset class

## How to apply

Execute the metabologenomic pipeline (MetaMiner) twice using identical spectra and BGC detection parameters but with two different genome annotation inputs: (1) raw nucleotide sequences in .fasta format, and (2) tool-specific output (e.g., antiSMASH .final.gbk or .gbk file). Parse both runs' significant_matches.tsv output files and cross-compare for presence/absence of target peptides and their modifications. A discrepancy in detected RiPPs (e.g., AmfS detection in FASTA but failure in .gbk input) indicates format-dependent parsing or precursor peptide extraction differences. Document which format(s) successfully recover the target compound(s) and use this empirical result to inform input format selection for future analyses on similar datasets.

## Related tools

- **MetaMiner** (Metabologenomic pipeline for RiPP detection; executed separately with FASTA and .gbk inputs to benchmark format-dependent detection performance) — https://github.com/mohimanilab/MetaMiner
- **antiSMASH** (Genome mining tool producing .final.gbk output files used as an alternative sequence input format for MetaMiner)
- **Dereplicator** (Spectral matching engine invoked by MetaMiner to match tandem MS data against RiPP structure databases derived from genomic input)
- **NPDtools** (Toolkit containing MetaMiner and supporting utilities for format-aware handling of genome annotation and MS data) — https://github.com/ablab/npdtools

## Examples

```
python metaminer.py test_data/metaminer/msms/ -s test_data/metaminer/fasta/ -o metaminer_fasta_outdir && python metaminer.py test_data/metaminer/msms/ -s test_data/metaminer/antismash/ -o metaminer_gbk_outdir && diff metaminer_fasta_outdir/significant_matches.tsv metaminer_gbk_outdir/significant_matches.tsv
```

## Evaluation signals

- Presence of target RiPP peptide (e.g., AmfS with sequence TGSQVSLLVCEYSSLSVVLCTP or known modified form) in significant_matches.tsv from FASTA input run, with high confidence score.
- Absence of the same target RiPP in significant_matches.tsv from .gbk input run (or presence with substantially lower confidence), indicating format-dependent detection failure.
- Identical run parameters (spectra directory, BGC search mode, output directory structure) documented for both runs to confirm isolation of format as the variable.
- Comparative hit count and peptide diversity: fewer or completely absent detected RiPPs in .gbk-input runs vs. FASTA-input runs, suggesting reduced precursor peptide extraction from GenBank-format annotations.
- Manual verification that precursor peptide sequences are correctly parsed from both input formats by inspecting intermediate MetaMiner logs or by directly querying GenBank file content for expected feature annotations.

## Limitations

- Format-dependent detection differences may be specific to particular annotation tools (e.g., antiSMASH .gbk format) and may not generalize to other genome mining tools or their output formats.
- The .gbk file parser in MetaMiner may have undocumented feature-extraction bugs or incompleteness that are version-dependent; comparison results should be paired with MetaMiner version number.
- Differences in detected RiPP counts between formats could also reflect differences in sequence content (e.g., incomplete or fragmented ORFs in one format) rather than pure parsing differences; validate that both formats represent the same genomic regions.
- LC-MS/MS spectral quality and dynamic range may limit detectability of low-abundance RiPPs regardless of format; use of high-quality, downsampled public datasets (e.g., S. griseus SRR3309439) is recommended for reproducible benchmarking.

## Evidence

- [other] MetaMiner successfully detects AmfS using contigs.fasta input but fails when antiSMASH output is used as input, demonstrating input format-dependent detection differences.: "MetaMiner successfully detects AmfS using contigs.fasta input but fails when antiSMASH output is used as input, demonstrating input format-dependent detection differences."
- [methods] While `MetaMiner` successfully detect AmfS using the `contigs.fasta` file, it fails with antiSMASH result as input: "While `MetaMiner` successfully detect AmfS using the `contigs.fasta` file, it fails with antiSMASH result as input"
- [methods] MetaMiner uses either raw nucleotide sequences or specific genome mining tools' output: raw nucleotide sequences `.fasta` format or *antiSMASH*'s `.final.gbk` or `.gbk` file: "MetaMiner uses either raw nucleotide sequences or specific genome mining tools' output: raw nucleotide sequences `.fasta` format or *antiSMASH*'s `.final.gbk` or `.gbk` file"
- [other] Execute MetaMiner with antiSMASH .gbk file as sequence input and spectra directory, using default lantibiotic search mode: `python metaminer.py test_data/metaminer/msms/ -s test_data/metaminer/antismash/ -o metaminer_outdir`. Parse the generated significant_matches.tsv output file and verify absence of AmfS peptide: "Execute MetaMiner with antiSMASH .gbk file as sequence input and spectra directory, using default lantibiotic search mode: `python metaminer.py test_data/metaminer/msms/ -s"
- [other] Compare results against the baseline FASTA-input run which successfully identifies AmfS to confirm the discrepancy.: "Compare results against the baseline FASTA-input run which successfully identifies AmfS to confirm the discrepancy."
