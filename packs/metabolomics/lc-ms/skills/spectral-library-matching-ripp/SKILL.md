---
name: spectral-library-matching-ripp
description: Use when you have tandem mass spectrometry data (LC-MS/MS in MGF, mzXML, mzML, or mzData format) and genomic data from a target organism, and you want to identify RiPPs by matching experimental spectra against a database of predicted post-translationally modified RiPP structures derived from.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3767
  edam_topics:
  - http://edamontology.org/topic_0121
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_0593
  tools:
  - NPDtools 2.5.0
  - MetaMiner
  - Dereplicator
  - ProteoWizard
  - NPDtools
  - joblib
  - antiSMASH
  techniques:
  - LC-MS
derived_from:
- doi: 10.1038/s41467-018-06082-8
  title: dereplicator
evidence_spans:
- The latest version is available in the Natural Product Discovery toolkit (NPDtools) at https://github.com/ablab/npdtools
- MetaMiner is a metabologenomic pipeline which integrates metabolomic (tandem mass spectra) and genomic data to identify novel RiPPs
- MetaMiner is a metabologenomic pipeline which integrates metabolomic (tandem mass spectra) and genomic data to identify novel Ribosmally synthesized and Post-translationally modified Peptides (RiPPs)
- matches tandem mass spectra against the constructed post-translationally modified RiPPs structure database using Dereplicator
- MetaMiner natively supports MGF, mzXML, mzData and uses msconvert utility from the ProteoWizard package to convert spectra in other formats to MGF
- uses msconvert utility from the ProteoWizard package to convert spectra in other formats to MGF
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
  zenodo_doi: TODO-zenodo
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# Spectral Library Matching for RiPPs

## Summary

Match tandem mass spectra against a post-translationally modified ribosomally synthesized and post-translationally modified peptide (RiPP) structure database to identify known and novel RiPP compounds. This skill integrates genomic predictions of precursor peptides with mass spectrometry data to dereplicat and confirm RiPP identities.

## When to use

Use this skill when you have tandem mass spectrometry data (LC-MS/MS in MGF, mzXML, mzML, or mzData format) and genomic data from a target organism, and you want to identify RiPPs by matching experimental spectra against a database of predicted post-translationally modified RiPP structures derived from biosynthetic gene clusters. Particularly valuable when antiSMASH or manual BGC annotation has identified putative RiPP gene clusters and you need to confirm their expression and structure via mass spectrometry.

## When NOT to use

- Input spectra are not centroided; they must be centroided before matching.
- Genomic data is unavailable or poorly assembled; MetaMiner requires contigs or scaffolds to predict precursor peptides.
- You are screening for non-peptidic metabolites; use Dereplicator+ or VarQuest instead, which support broader chemical classes.

## Inputs

- Centroided LC-MS/MS spectra (MGF, mzXML, mzML, or mzData format)
- Genomic nucleotide sequences in FASTA format or antiSMASH .final.gbk/.gbk output
- Specification of RiPP class to search (e.g., lantibiotic, thiopeptide)

## Outputs

- Tab-separated significant_matches.tsv file with columns: FragmentSeq (core peptide), ModifiedSeq (with PTM annotations and mass shifts), matching score, spectral metadata
- RiPP compound identifications with assigned fragmentation patterns and post-translational modifications

## How to apply

First, prepare centroided LC-MS/MS files in MGF format (converting if needed via ProteoWizard's msconvert utility). Second, construct a putative RiPP structure database from genomic input by running MetaMiner on raw nucleotide sequences (.fasta format) or antiSMASH output (.final.gbk or .gbk files), specifying the appropriate RiPP class (e.g., lantibiotic, thiopeptide). Third, match experimental spectra against the constructed database using Dereplicator, which scores fragment ion matches and reports significant identifications in a tab-separated output file (significant_matches.tsv). Finally, parse results by filtering on FragmentSeq and ModifiedSeq columns to verify presence of expected post-translational modifications (PTM mass shifts such as T-18 for dehydrobutyrine, S-18 for dehydroalanine) and core peptide sequences. Note: raw nucleotide sequences (.fasta) reliably detect RiPPs; antiSMASH-formatted output may fail depending on gene cluster annotation completeness.

## Related tools

- **MetaMiner** (Metabologenomic pipeline that integrates genomic data with mass spectra; identifies putative BGCs, constructs post-translationally modified RiPP structure databases, and performs spectral matching via Dereplicator) — https://github.com/ablab/npdtools
- **Dereplicator** (Core database search engine that matches tandem mass spectra against RiPP structure databases and reports significant identifications with scoring) — https://github.com/ablab/npdtools
- **ProteoWizard** (Converts spectra in non-native formats (e.g., raw instrument data) to MGF via msconvert utility)
- **antiSMASH** (Optional source for genome mining output; MetaMiner accepts antiSMASH .final.gbk or .gbk files as alternative to raw FASTA, though raw nucleotide sequences are more reliable)
- **NPDtools 2.5.0** (Toolkit container providing MetaMiner, Dereplicator, and associated binaries (rippquest_ms, dereplicate) for RiPP discovery workflow) — https://github.com/ablab/npdtools/releases

## Examples

```
python metaminer.py test_data/metaminer/msms/ -s test_data/metaminer/fasta/ -c lantibiotic -o metaminer_outdir
```

## Evaluation signals

- Presence of matched compound identifications in significant_matches.tsv with non-null scores and matching spectral evidence
- FragmentSeq column matches expected core peptide sequence from literature or BGC prediction (e.g., AmfS: TGSQVSLLVCEYSSLSVVLCTP)
- ModifiedSeq shows expected post-translational modifications with correct mass shifts (e.g., T-18 and S-18 for dehydrobutyrine/dehydroalanine in lantibiotics)
- Spectral network expansion (if enabled) shows coherent clustering of related RiPP identifications with cosine similarity propagation
- Verification that raw .fasta input succeeds while antiSMASH .final.gbk input for the same organism/sample fails or produces subset results, confirming input format sensitivity

## Limitations

- MetaMiner fails to detect RiPPs when input is antiSMASH-formatted .final.gbk or .gbk output for some organisms; raw nucleotide sequences (.fasta) are required for reliable detection.
- Spectral matching requires high-quality, centroided spectra; uncentroided or low-resolution data will reduce sensitivity.
- Post-translational modification database is limited to known PTM types; novel or unusual modifications may not be detected or scored correctly.
- Parallel processing requires joblib Python library; without it, processing defaults to single-threaded execution and may be slow for large spectral datasets.
- Spectral networking visualization (matplotlib, networkx) is optional; if libraries are not installed, propagation is generated in plain text format only.

## Evidence

- [other] MetaMiner successfully detects AmfS using contigs.fasta genome files, though it fails when using antiSMASH results as input, indicating that raw nucleotide sequence format supports lantibiotic discovery.: "While `MetaMiner` successfully detect AmfS using the `contigs.fasta` file, it fails with antiSMASH result as input"
- [readme] MetaMiner integrates metabolomic and genomic data to identify RiPPs through a four-step pipeline: BGC identification, RiPP structure database construction, spectral matching, and spectral networking.: "MetaMiner (i) identifies putative BGCs and the corresponding precursor peptides, (ii) constructs putative RiPP structure databases, (iii) matches tandem mass spectra against the constructed"
- [readme] Spectra must be centroided and in open formats; MGF is natively supported, other formats require msconvert from ProteoWizard.: "Spectra files must be centroided and be in an open spectrum format (**MGF**, **mzXML**, **mzML** or **mzData**). NPDtools natively supports MGF"
- [other] Post-translational modifications are identified by mass shift patterns in the ModifiedSeq output column.: "verifying presence of AmfS by FragmentSeq column matching 'TGSQVSLLVCEYSSLSVVLCTP' and ModifiedSeq showing dehydrobutyrine/dehydroalanine modifications (T-18 and S-18 mass shifts)"
- [readme] MetaMiner accepts either raw nucleotide sequences or output from genome mining tools like antiSMASH.: "MetaMiner uses either raw nucleotide sequences or specific genome mining tools' output: raw nucleotide sequences `.fasta` format or *antiSMASH*'s `.final.gbk` or `.gbk` file"
