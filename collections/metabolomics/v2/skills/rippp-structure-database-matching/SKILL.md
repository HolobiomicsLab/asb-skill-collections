---
name: rippp-structure-database-matching
description: 'Use when you have: (1) tandem MS/MS spectra in MGF, mzXML, mzML, or
  mzData format from LC-MS/MS analysis; (2) a set of predicted RiPP precursor peptides
  derived from genomic biosynthetic gene cluster mining (via antiSMASH, BOA, or raw
  FASTA);'
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3646
  edam_topics:
  - http://edamontology.org/topic_0121
  - http://edamontology.org/topic_3373
  - http://edamontology.org/topic_3520
  tools:
  - MetaMiner
  - NPDtools 2.5.0
  - matplotlib
  - networkx
  - Dereplicator
  - antiSMASH
  - BOA
  - ProteoWizard
  techniques:
  - LC-MS
  license_tier: restricted
derived_from:
- doi: 10.1038/s41467-018-06082-8
  title: dereplicator
evidence_spans:
- MetaMiner is a metabologenomic pipeline which integrates metabolomic (tandem mass
  spectra) and genomic data to identify novel RiPPs
- MetaMiner is a metabologenomic pipeline which integrates metabolomic (tandem mass
  spectra) and genomic data to identify novel Ribosmally synthesized and Post-translationally
  modified Peptides (RiPPs)
- The latest version is available in the Natural Product Discovery toolkit (NPDtools)
  at https://github.com/ablab/npdtools
- For presenting Spectral Network propagation graphs, MetaMiner also requires `matplotlib`
  and `networkx` Python libraries
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

# RiPP Structure Database Matching

> **License: restricted** — no clear open-source license detected for the underlying tool; verify licensing before commercial use or redistribution. <!-- asb-license-banner -->
## Summary

Match tandem mass spectra against a constructed database of post-translationally modified RiPP structures to identify novel ribosomally synthesized and post-translationally modified peptides. This is a core step in the MetaMiner metabologenomic pipeline that bridges genomic predictions with mass spectrometry evidence.

## When to use

Apply this skill when you have: (1) tandem MS/MS spectra in MGF, mzXML, mzML, or mzData format from LC-MS/MS analysis; (2) a set of predicted RiPP precursor peptides derived from genomic biosynthetic gene cluster mining (via antiSMASH, BOA, or raw FASTA); and (3) the goal is to identify which genomically predicted RiPPs are actually expressed and detectable in the sample.

## When NOT to use

- Input spectra are not centroided (profile mode) — preprocessing to centroid is required before matching.
- RiPP precursor sequences are unavailable or not provided — matching requires known or predicted peptide sequences.
- The goal is to identify small-molecule metabolites or non-peptidic natural products — use Dereplicator+ or VarQuest instead for broader chemical structure databases.

## Inputs

- Tandem MS/MS spectra (MGF, mzXML, mzML, or mzData format)
- RiPP precursor peptide sequences (FASTA file)
- Genomic context (antiSMASH .final.gbk/.gbk files or raw contigs.fasta, optional but recommended)

## Outputs

- Dereplicator match results with PSM scores and p-values
- List of identified RiPPs with matched spectra and modification assignments
- Detailed match report showing theoretical vs. observed fragmentation patterns

## How to apply

The matching process uses Dereplicator, which scores PSMs (peptide-spectrum matches) between experimental MS/MS spectra and in silico fragmentation patterns of post-translationally modified RiPP structures constructed from genomic precursor sequences. Run MetaMiner with the `--blind` flag for open modification search if testing novel RiPPs, or without it for modification-restricted search. The workflow reads the RiPP FASTA file (or antiSMASH .final.gbk / .gbk output), generates candidate PTM-modified structures, and scores matches against the input spectra. Evaluate matches using the scoring metrics reported in the output; higher PSM scores and lower p-values indicate stronger matches. The detailed output includes matched spectral peaks, theoretical fragmentation patterns, and per-spectrum match confidence.

## Related tools

- **Dereplicator** (Core scoring and matching engine that performs database search of MS/MS spectra against RiPP structure database) — https://github.com/ablab/npdtools
- **MetaMiner** (Wrapper pipeline that orchestrates RiPP structure database construction from genomic sequences and invokes Dereplicator for matching) — https://github.com/mohimanilab/MetaMiner
- **antiSMASH** (Genome mining tool to identify biosynthetic gene clusters and predict RiPP precursor peptides from genomic DNA)
- **BOA** (Alternative genome mining tool for BGC identification and precursor peptide prediction) — https://github.com/idoerg/BOA
- **ProteoWizard** (Spectrum format conversion utility (msconvert) to convert non-native MS formats to MGF before matching)

## Examples

```
python metaminer.py test_data/metaminer/msms/ -s test_data/metaminer/fasta/ -o metaminer_outdir
```

## Evaluation signals

- PSM p-value < 0.05 (or equivalent significance threshold reported in results) indicates a confident match.
- Matched spectra show substantial overlap between observed and theoretical fragment peaks, with peak intensity ranking preserved.
- Multiple spectra from the same RiPP or related cluster match, increasing confidence in the identification.
- Identified RiPPs correspond to BGCs detected in genomic data, confirming biosynthetic plausibility.
- Output files (match scores, matched fragments, modification assignments) are non-empty and properly formatted.

## Limitations

- Database-dependent: matching relies on accurate RiPP precursor sequence prediction; errors in genomic mining (e.g., antiSMASH missing AmfS) will reduce sensitivity.
- PTM diversity: the tool can only identify RiPPs with PTMs in its modification grammar; novel or unexpected modifications may be missed.
- Spectral quality: low-resolution or noisy spectra reduce match confidence; centroided data is required.
- No changelog available for version 2.5.0, limiting clarity on algorithm changes or bug fixes from prior releases.

## Evidence

- [methods] matches tandem mass spectra against the constructed post-translationally modified RiPPs structure database using Dereplicator: "matches tandem mass spectra against the constructed post-translationally modified RiPPs structure database using Dereplicator"
- [methods] MetaMiner successfully detect AmfS using the contigs.fasta file, it fails with antiSMASH result as input: "While `MetaMiner` successfully detect AmfS using the `contigs.fasta` file, it fails with antiSMASH result as input"
- [methods] MetaMiner natively supports MGF, mzXML, mzData and uses msconvert utility from the ProteoWizard package to convert spectra in other formats to MGF: "MetaMiner natively supports MGF, mzXML, mzData and uses msconvert utility from the ProteoWizard package to convert spectra in other formats to MGF"
- [other] python metaminer.py <spectra_files> -s test_data/metaminer/molnet/example_RiPP.fasta --blind --spec-network test_data/metaminer/molnet/ProteoSAFe-METABOLOMICS-SNETS-V2-unpacked -o metaminer_outdir: "python metaminer.py <spectra_files> -s test_data/metaminer/molnet/example_RiPP.fasta --blind --spec-network test_data/metaminer/molnet/ProteoSAFe-METABOLOMICS-SNETS-V2-unpacked -o metaminer_outdir"
- [readme] Spectra files must be centroided and be in an open spectrum format (MGF, mzXML, mzML or mzData): "Spectra files must be centroided and be in an open spectrum format (**MGF**, **mzXML**, **mzML** or **mzData**)."
