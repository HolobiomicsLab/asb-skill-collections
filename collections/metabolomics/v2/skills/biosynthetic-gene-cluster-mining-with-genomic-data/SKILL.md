---
name: biosynthetic-gene-cluster-mining-with-genomic-data
description: Use when you have LC-MS/MS spectra (MGF, mzXML, mzML, or mzData format)
  from a bacterial or fungal strain and corresponding genomic sequence data (FASTA,
  antiSMASH .final.gbk, or BOA .annotated.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3454
  edam_topics:
  - http://edamontology.org/topic_0160
  - http://edamontology.org/topic_0654
  - http://edamontology.org/topic_3172
  tools:
  - NPDtools 2.5.0
  - MetaMiner
  - antiSMASH
  - Dereplicator
  - BOA
  - SPAdes / metaSPAdes
  - ProteoWizard (msconvert)
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

# biosynthetic-gene-cluster-mining-with-genomic-data

> **License: restricted** — no clear open-source license detected for the underlying tool; verify licensing before commercial use or redistribution. <!-- asb-license-banner -->
## Summary

MetaMiner integrates tandem mass spectrometry data with genomic sequences to identify ribosomally synthesized and post-translationally modified peptides (RiPPs) by mining biosynthetic gene clusters (BGCs). This skill applies metabologenomics to discover novel natural products by matching MS/MS spectra against putative RiPP structure databases constructed from genome mining.

## When to use

You have LC-MS/MS spectra (MGF, mzXML, mzML, or mzData format) from a bacterial or fungal strain and corresponding genomic sequence data (FASTA, antiSMASH .final.gbk, or BOA .annotated.txt), and you want to identify novel RiPPs or validate known RiPPs by correlating genomic BGC content with observed metabolomic signals.

## When NOT to use

- Input sequences are in antiSMASH .final.gbk format and high sensitivity to minor RiPP detection is required (use FASTA contigs instead).
- Spectra are not centroided or are in proprietary binary format unsupported by ProteoWizard (convert before use).
- You only have MS1-level mass data without tandem MS/MS fragmentation patterns (Dereplicator requires MS/MS spectra).

## Inputs

- LC-MS/MS spectra files (MGF, mzXML, mzML, or mzData format)
- Genomic sequence data: FASTA contigs (.fasta) or antiSMASH output (.final.gbk file) or BOA output (.annotated.txt)
- Raw DNA reads (optional; .fastq or .fastq.gz for assembly)

## Outputs

- significant_matches.tsv (identifications of RiPPs matched to spectra)
- RiPP structure database (constructed from BGC precursor peptides)
- Spectral network graphs (optional; for RiPP variant discovery)

## How to apply

First, assemble raw DNA reads (if available) into contigs using SPAdes or metaSPAdes, generating nucleotide sequences in .fasta format or obtain antiSMASH/BOA genome mining output. For reliable detection, prefer raw FASTA-format contigs over antiSMASH .final.gbk output when possible, as the latter may fail to detect target RiPPs depending on input parsing. Execute MetaMiner in lantibiotic (or other RiPP class) search mode by providing the spectra directory and sequence source to the metaminer.py script. MetaMiner then: (i) identifies putative BGCs and precursor peptides from genomic input, (ii) constructs post-translationally modified RiPP structure databases, and (iii) matches tandem mass spectra against the RiPP database using Dereplicator scoring. Parse the significant_matches.tsv output to identify RiPPs present in both genome and metabolome. Verify hits by confirming the expected peptide sequence (or its modified form) appears in the output and cross-reference with known RiPP sequences.

## Related tools

- **MetaMiner** (Main metabologenomics pipeline that integrates genomic BGC mining with MS/MS-based RiPP identification) — https://github.com/mohimanilab/MetaMiner
- **antiSMASH** (Genome mining tool to detect BGCs and generate .final.gbk sequence input for MetaMiner (though FASTA input is more reliable))
- **BOA** (Alternative genome mining tool producing .annotated.txt output for BGC and precursor peptide identification) — https://github.com/idoerg/BOA
- **Dereplicator** (Core scoring and matching engine within MetaMiner that matches tandem mass spectra against RiPP structure database)
- **SPAdes / metaSPAdes** (Assembles raw DNA short reads (.fastq) into nucleotide contigs for genomic input to MetaMiner)
- **ProteoWizard (msconvert)** (Converts mass spectra in non-native formats to MGF for MetaMiner ingestion)
- **NPDtools** (Toolkit container providing MetaMiner and related natural product discovery pipelines) — https://github.com/ablab/npdtools

## Examples

```
python metaminer.py test_data/metaminer/msms/ -s test_data/metaminer/fasta/ -o metaminer_outdir
```

## Evaluation signals

- Target RiPP peptide sequence (or expected post-translationally modified form) appears in significant_matches.tsv output with assigned score and spectral match details.
- Detected RiPP sequence matches known reference peptide (e.g., AmfS consensus TGSQVSLLVCEYSSLSVVLCTP or variants) without truncation or frameshift artifacts.
- Spectral matches show cosine similarity and fragmentation pattern alignment consistent with database-predicted RiPP structure.
- BGC precursor peptide identified in genome corresponds genomically to biosynthetic genes (e.g., lantibiotic biosynthesis cluster) in antiSMASH or BOA output.
- Reproducibility check: re-running MetaMiner with FASTA-format contigs (rather than antiSMASH .gbk) yields RiPP detection; .gbk input may fail due to format-dependent parsing differences.

## Limitations

- MetaMiner fails to detect some RiPPs when antiSMASH .final.gbk output is used instead of raw FASTA sequence input, indicating input format sensitivity; FASTA is preferred for reliable detection.
- Requires centroided spectra; uncentroided or vendor-specific binary formats must be pre-converted using ProteoWizard msconvert.
- Detection accuracy depends on completeness of genomic assembly and accuracy of BGC prediction by antiSMASH or BOA; fragmented assemblies may miss RiPP-encoding regions.
- Spectral networking for RiPP variant discovery requires matplotlib and networkx Python libraries; without them, output is plain text only.
- Performance for parallel processing requires joblib library; single-threaded fallback is slower.

## Evidence

- [other] MetaMiner successfully detects AmfS using contigs.fasta input but fails when antiSMASH output is used as input, demonstrating input format-dependent detection differences.: "While `MetaMiner` successfully detect AmfS using the `contigs.fasta` file, it fails with antiSMASH result as input"
- [readme] MetaMiner integrates metabolomic and genomic data to identify RiPPs through a four-step workflow: BGC and precursor identification, RiPP database construction, MS/MS matching, and spectral networking.: "MetaMiner (i) identifies putative BGCs and the corresponding precursor peptides (ii) constructs putative RiPP structure databases (iii) matches tandem mass spectra against the constructed"
- [readme] MetaMiner accepts raw nucleotide sequences in FASTA format or genome mining tool outputs including antiSMASH .final.gbk and BOA .annotated.txt files.: "MetaMiner uses either raw nucleotide sequences or specific genome mining tools' output: raw nucleotide sequences `.fasta` format or *antiSMASH*'s `.final.gbk` or `.gbk` file"
- [readme] MetaMiner requires LC-MS/MS data in MGF, mzXML, mzML, or mzData format; other formats are converted using ProteoWizard msconvert utility.: "NPDtools natively supports MGF and mzXML/mzData. We use msconvert utility from the ProteoWizard package to convert spectra in other formats to MGF"
- [readme] DNA short reads are assembled into contigs using SPAdes or metaSPAdes prior to MetaMiner analysis for genomic input.: "For users who have raw DNA short read files (.fastq or .fastq.gz), it is convenient to assemble them into longer nucleotide sequences (contigs or scaffolds) with SPAdes or metaSPAdes"
