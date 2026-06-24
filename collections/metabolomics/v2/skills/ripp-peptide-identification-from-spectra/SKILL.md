---
name: ripp-peptide-identification-from-spectra
description: Use when you have LC-MS/MS spectra (MGF, mzXML, mzML, or mzData format)
  and either raw genome nucleotide sequences or antiSMASH/BOA genome mining tool output,
  and you need to identify which RiPPs are present in your sample.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3631
  edam_topics:
  - http://edamontology.org/topic_0121
  - http://edamontology.org/topic_3172
  - http://edamontology.org/topic_0080
  tools:
  - NPDtools 2.5.0
  - MetaMiner
  - antiSMASH
  - Dereplicator
  - BOA
  - ProteoWizard
  techniques:
  - LC-MS
  license_tier: open
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

# ripp-peptide-identification-from-spectra

## Summary

Identify ribosomally synthesized and post-translationally modified peptides (RiPPs) by matching tandem mass spectrometry data against a RiPP structure database constructed from genomic biosynthetic gene clusters. This skill integrates metabolomic (LC-MS/MS) and genomic data to enable discovery of novel RiPPs and their variants.

## When to use

You have LC-MS/MS spectra (MGF, mzXML, mzML, or mzData format) and either raw genome nucleotide sequences or antiSMASH/BOA genome mining tool output, and you need to identify which RiPPs are present in your sample. Use this when seeking to discover novel RiPPs or confirm the presence of known RiPP peptides in your metabolomic data.

## When NOT to use

- Input spectra are not centroided or are in unsupported formats without ProteoWizard conversion capability.
- No genome sequence or genome mining tool output is available — MetaMiner requires genomic data for BGC and precursor peptide identification.
- You seek to identify non-RiPP natural products; use Dereplicator+ or VarQuest for broader PNP/metabolite identification instead.

## Inputs

- LC-MS/MS spectra directory (centroided, in MGF, mzXML, mzML, or mzData format)
- Genome nucleotide sequences (FASTA format preferred, or antiSMASH .final.gbk/.gbk file)
- MS/MS spectra files (e.g., AmfS.mgf)

## Outputs

- significant_matches.tsv file containing RiPP identifications and match scores
- RiPP structure database (constructed intermediate)
- Spectral network graphs (if matplotlib and networkx installed, else plain text format)

## How to apply

Prepare genome sequences (FASTA format or antiSMASH .final.gbk/.gbk output, though FASTA is more reliable for format-dependent detection). Feed these alongside centroided LC-MS/MS spectra into MetaMiner, which will: (i) identify putative biosynthetic gene clusters and corresponding precursor peptides from the genome input, (ii) construct a putative RiPP structure database with post-translational modification variants, and (iii) match the tandem mass spectra against this database using Dereplicator to score candidate matches. Parse the output significant_matches.tsv file and verify presence of expected RiPP peptide sequences or modified forms. If using antiSMASH output as genome input, be aware of format-dependent detection differences and consider validating with FASTA input if results are unexpectedly negative.

## Related tools

- **MetaMiner** (Primary metabologenomic pipeline that identifies BGCs from genome input, constructs RiPP structure databases, and matches tandem mass spectra against the database using Dereplicator) — https://github.com/mohimanilab/MetaMiner
- **Dereplicator** (Core scoring engine within MetaMiner that matches tandem mass spectra against the constructed post-translationally modified RiPPs structure database) — https://github.com/ablab/npdtools
- **antiSMASH** (Genome mining tool whose .final.gbk or .gbk output can be used as sequence input to MetaMiner for BGC identification (though format-dependent detection differences exist compared to FASTA input))
- **BOA** (Alternative genome mining tool whose .annotated.txt output can be used as sequence input to MetaMiner for BGC and precursor peptide identification) — https://github.com/idoerg/BOA
- **ProteoWizard** (Provides msconvert utility used by MetaMiner to convert spectra in formats other than MGF (mzXML, mzML, mzData) to the native MGF format)

## Examples

```
python metaminer.py test_data/metaminer/msms/ -s test_data/metaminer/fasta/ -o metaminer_outdir
```

## Evaluation signals

- Output significant_matches.tsv contains expected RiPP peptide sequence(s) or known modified forms with non-zero match scores
- FASTA input and antiSMASH .gbk input produce consistent detections (or document input-format-dependent detection differences, as observed with AmfS)
- Match scores in significant_matches.tsv exceed background noise thresholds documented in MetaMiner output
- Spectral network visualization shows connected clusters of related RiPP spectra (if matplotlib/networkx available)
- No missing or malformed sequence entries in the constructed RiPP structure database (verify precursor peptides extracted from each BGC)

## Limitations

- MetaMiner fails to detect RiPPs when using antiSMASH .gbk output as input but succeeds with FASTA sequences (format-dependent detection differences documented in task_002). Practitioners should validate unexpected negative results with FASTA-format genome input.
- Detection depends on quality of genome assembly and completeness of BGC prediction; fragmented or incomplete assemblies may fail to identify RiPPs present in the sample.
- Post-translational modification prediction is limited to variants in the constructed RiPP structure database; novel or unanticipated PTM patterns may not be detected.
- Requires centroided spectra; non-centroided spectra will produce incorrect matches. If spectra are in unsupported formats, ProteoWizard msconvert conversion is necessary but may fail if not properly installed.
- Performance scales with number of spectra and BGCs; large datasets or complex genomes may require parallel processing via joblib Python library.

## Evidence

- [readme] MetaMiner is a metabologenomic pipeline which integrates metabolomic (tandem mass spectra) and genomic data to identify novel RiPPs: "MetaMiner is a metabologenomic pipeline which integrates metabolomic (tandem mass spectra) and genomic data to identify novel RiPPs"
- [readme] Starting from the genome assemblies, MetaMiner (i) identifies putative BGCs and the corresponding precursor peptides, (ii) constructs putative RiPP structure databases, (iii) matches tandem mass spectra against the constructed post-translationally modified RiPPs structure database using Dereplicator: "identifies putative BGCs and the corresponding precursor peptides, (ii) constructs putative RiPP structure databases, (iii) matches tandem mass spectra against the constructed post-translationally"
- [readme] MetaMiner uses either raw nucleotide sequences or specific genome mining tools' output: raw nucleotide sequences `.fasta` format or *antiSMASH*'s `.final.gbk` or `.gbk` file: "MetaMiner uses either raw nucleotide sequences or specific genome mining tools' output: raw nucleotide sequences `.fasta` format or *antiSMASH*'s `.final.gbk` or `.gbk` file"
- [readme] While `MetaMiner` successfully detect AmfS using the `contigs.fasta` file, it fails with antiSMASH result as input: "While `MetaMiner` successfully detect AmfS using the `contigs.fasta` file, it fails with antiSMASH result as input"
- [readme] Spectra files must be centroided and be in an open spectrum format (**MGF**, **mzXML**, **mzML** or **mzData**). NPDtools natively supports MGF: "Spectra files must be centroided and be in an open spectrum format (**MGF**, **mzXML**, **mzML** or **mzData**)"
- [other] Parse the generated significant_matches.tsv output file and verify absence of AmfS peptide (TGSQVSLLVCEYSSLSVVLCTP or modified form): "Parse the generated significant_matches.tsv output file and verify absence of AmfS peptide (TGSQVSLLVCEYSSLSVVLCTP or modified form)"
