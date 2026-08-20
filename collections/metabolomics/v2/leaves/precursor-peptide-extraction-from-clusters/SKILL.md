---
name: precursor-peptide-extraction-from-clusters
description: Use when you have assembled genome FASTA sequences (from SPAdes, metaSPAdes,
  or antiSMASH output) and need to systematically identify precursor peptides corresponding
  to a target RiPP class before constructing the structure database for dereplication.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_0415
  edam_topics:
  - http://edamontology.org/topic_0080
  - http://edamontology.org/topic_0622
  - http://edamontology.org/topic_0749
  tools:
  - MetaMiner
  - NPDtools 2.5.0
  - antiSMASH
  - BOA
  - SPAdes / metaSPAdes
  license_tier: open
  provenance_tier: literature
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

# precursor-peptide-extraction-from-clusters

## Summary

Extract precursor peptide sequences from identified biosynthetic gene clusters (BGCs) in genome assemblies, filtering by RiPP class (lantibiotic, lassopeptide, cyanobactin, etc.). This step bridges genomic mining and structure prediction by producing class-specific precursor sequences that serve as substrates for post-translational modification enumeration.

## When to use

You have assembled genome FASTA sequences (from SPAdes, metaSPAdes, or antiSMASH output) and need to systematically identify precursor peptides corresponding to a target RiPP class before constructing the structure database for dereplication. Use this skill when your goal is to map putative BGCs to their biosynthetic precursors to reduce the downstream search space.

## When NOT to use

- Input is already a curated database of known RiPP precursors—proceed directly to structure enumeration
- Genome assembly is incomplete or highly fragmented (N50 < 50 kb), risking false negatives or truncated precursor extraction
- Target RiPP class is not supported by MetaMiner's BGC identifier module

## Inputs

- Assembled genome sequences in FASTA format
- antiSMASH output (.final.gbk or .gbk file)
- BOA output (.annotated.txt file)
- RiPP class specification (lantibiotic, lassopeptide, cyanobactin, or other)

## Outputs

- Precursor peptide sequences (FASTA or TSV)
- BGC-to-precursor mapping table (TSV)
- Class-annotated precursor list ready for RiPP Structure Database Builder

## How to apply

Load the genome assembly (FASTA, antiSMASH .final.gbk, or BOA .annotated.txt format) into MetaMiner and execute the BGC Identifier module with the --class parameter specifying your target RiPP class. The module scans nucleotide sequences for known BGC signatures and extracts corresponding precursor peptide sequences by parsing annotated regions or homology matches. Validate that extracted precursors match the expected class-specific sequence motifs (e.g., lantibiotic leader peptides). Output the precursor sequences as a structured TSV file mapping precursor ID, sequence, BGC location, and class annotation. These sequences become input to the RiPP Structure Database Builder for enumeration of post-translationally modified variants.

## Related tools

- **MetaMiner** (Executes BGC identification and precursor peptide extraction from genome assemblies; filters results by user-specified RiPP class) — https://github.com/mohimanilab/MetaMiner
- **antiSMASH** (Provides pre-annotated BGC coordinates and gene calls as input to MetaMiner's precursor extraction step)
- **BOA** (Alternative genome mining tool that produces annotated gene predictions (.annotated.txt) consumable by MetaMiner for precursor identification) — https://github.com/idoerg/BOA
- **SPAdes / metaSPAdes** (Assembles raw DNA short reads into contigs/scaffolds that serve as input for BGC and precursor identification)

## Examples

```
python metaminer.py test_data/metaminer/msms/ -s test_data/metaminer/fasta/ -o metaminer_outdir
```

## Evaluation signals

- Extracted precursor sequences contain expected RiPP class-specific motifs (e.g., lantibiotic leader + core regions)
- Number and diversity of extracted precursors is comparable to known BGC counts in the reference genome (if known)
- BGC-to-precursor mapping is one-to-many (one BGC may encode multiple precursors) and all mappings are traceable to genomic coordinates
- Precursor sequences pass length and composition filters appropriate to the target class (e.g., lantibiotic cores typically 20–100 aa)
- No precursors are returned when input genome lacks the target RiPP class (negative control validates specificity)

## Limitations

- antiSMASH output (.final.gbk) may fail to detect some precursor-encoding ORFs that are successfully found in raw contigs.fasta input, as noted for AmfS detection
- Precursor extraction accuracy depends on the quality of the input genome assembly and the availability of training data for the target RiPP class
- MetaMiner's BGC identifier requires nucleotide-level sequence input; it cannot extract precursors from amino acid alignments or protein sequence databases alone
- Class-specific filtering may exclude non-canonical or novel precursor variants that do not match standard motif definitions

## Evidence

- [methods] Starting from the genome assemblies, MetaMiner (i) identifies putative BGCs and the corresponding precursor peptides: "Starting from the genome assemblies, MetaMiner (i) identifies putative BGCs and the corresponding precursor peptides"
- [methods] Execute MetaMiner's BGC identifier module to scan for putative biosynthetic gene clusters and extract precursor peptide sequences matching the target RiPP class (lantibiotic, lassopeptide, cyanobactin, or specified class via --class parameter).: "Execute MetaMiner's BGC identifier module to scan for putative biosynthetic gene clusters and extract precursor peptide sequences matching the target RiPP class (lantibiotic, lassopeptide,"
- [methods] MetaMiner uses either raw nucleotide sequences or specific genome mining tools' output: raw nucleotide sequences `.fasta` format or *antiSMASH*'s `.final.gbk` or `.gbk` file: "MetaMiner uses either raw nucleotide sequences or specific genome mining tools' output: raw nucleotide sequences `.fasta` format or *antiSMASH*'s `.final.gbk` or `.gbk` file"
- [methods] While `MetaMiner` successfully detect AmfS using the `contigs.fasta` file, it fails with antiSMASH result as input: "While `MetaMiner` successfully detect AmfS using the `contigs.fasta` file, it fails with antiSMASH result as input"
- [methods] For each identified precursor peptide, apply the RiPP Structure Database Builder to enumerate putative post-translationally modified variants according to class-specific modification rules.: "For each identified precursor peptide, apply the RiPP Structure Database Builder to enumerate putative post-translationally modified variants according to class-specific modification rules"
