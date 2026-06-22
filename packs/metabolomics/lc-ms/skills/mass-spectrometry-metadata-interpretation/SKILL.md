---
name: mass-spectrometry-metadata-interpretation
description: Use when when integrating LC-MS/MS data from diverse sources (e.g., public repositories like MSV000080102, instrument outputs, or precomputed workflows) into NPDtools pipelines.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3763
  edam_topics:
  - http://edamontology.org/topic_0121
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_0625
  tools:
  - MetaMiner
  - NPDtools 2.5.0
  - matplotlib
  - networkx
  - ProteoWizard msconvert
  - Dereplicator
  - GNPS Spectral Networking / Molecular Networking
  - rawrr
  - RawFileReader
  - MsBackendRawFileReader
  - rawDiag
  - Spectra
  techniques:
  - LC-MS
derived_from:
- doi: 10.1038/s41467-018-06082-8
  title: dereplicator
- doi: 10.1101/2020.10.30.362533
  title: ''
- doi: 10.1021/acs.jproteome.0c00866
  title: ''
evidence_spans:
- MetaMiner is a metabologenomic pipeline which integrates metabolomic (tandem mass spectra) and genomic data to identify novel RiPPs
- MetaMiner is a metabologenomic pipeline which integrates metabolomic (tandem mass spectra) and genomic data to identify novel Ribosmally synthesized and Post-translationally modified Peptides (RiPPs)
- The latest version is available in the Natural Product Discovery toolkit (NPDtools) at https://github.com/ablab/npdtools
- For presenting Spectral Network propagation graphs, MetaMiner also requires `matplotlib` and `networkx` Python libraries
- rawrr::readSpectrum
- Our .NET 8.0 [@dotnet] precompiled wrapper methods are bundled, including the runtime, in the `r BiocStyle::Biocpkg('rawrr')` executable file
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_dereplicator
    doi: 10.1038/s41467-018-06082-8
    title: dereplicator
  - build: coll_rawrr
    doi: 10.1101/2020.10.30.362533
    title: rawrr
  dedup_kept_from: coll_dereplicator
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1038/s41467-018-06082-8
  all_source_dois:
  - 10.1038/s41467-018-06082-8
  - 10.1101/2020.10.30.362533
  - 10.1021/acs.jproteome.0c00866
  zenodo_doi: TODO-zenodo
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# mass-spectrometry-metadata-interpretation

## Summary

Interpret and validate mass spectrometry file formats, centroiding status, and metadata to ensure compatibility with natural product discovery pipelines. This skill bridges raw instrument output and downstream metabologenomic analysis by verifying spectral data readiness and extracting critical acquisition parameters.

## When to use

When integrating LC-MS/MS data from diverse sources (e.g., public repositories like MSV000080102, instrument outputs, or precomputed workflows) into NPDtools pipelines. Apply this skill before running Dereplicator, MetaMiner, or spectral networking stages to confirm that spectra are centroided, in supported formats, and carry necessary metadata for PSM matching and RiPP identification.

## When NOT to use

- Input spectra are already confirmed to be centroided and in a supported open format (MGF, mzXML, mzML, mzData) with verified metadata — skip directly to downstream analysis.
- Spectral data is in a closed, proprietary format with no available converter (msconvert does not support it) — this skill cannot resolve such cases without external vendor tools.
- The analysis goal does not require mass accuracy checks or spectral network propagation (e.g., if running only Dereplicator+ without --spec-network option) — metadata interpretation overhead may be unnecessary.

## Inputs

- LC-MS/MS spectra files in MGF, mzXML, mzML, or mzData format
- Vendor instrument output files (if conversion via msconvert is required)
- Spectral network archive (e.g., ProteoSAFe-METABOLOMICS-SNETS-V2 unpacked directory) containing cluster metadata and interconnectivity information
- Sample metadata or acquisition logs indicating centroiding status and fragmentation method

## Outputs

- Validated, centroided spectra in MGF or native open format ready for MetaMiner or Dereplicator input
- Verification report confirming format compatibility, centroiding status, and presence of critical metadata fields
- Converted spectra files (if msconvert was applied)
- Spectral network metadata index (cluster assignments, inter-cluster edges, PSM propagation annotations)

## How to apply

First, verify that input spectra files are in an open, supported format: MGF (Mascot Generic Format), mzXML, mzML, or mzData. If spectra are in other formats (e.g., proprietary vendor formats), use ProteoWizard's msconvert utility to convert to MGF before proceeding. Second, confirm that spectra are centroided (not profile mode), as NPDtools requires centroided data for accurate mass matching. Third, if using MetaMiner's spectral networking stage (--spec-network option), ensure that the spectral network output directory (e.g., unpacked ProteoSAFe-METABOLOMICS-SNETS-V2 archive) contains expected metadata linking spectra to network clusters. Finally, validate that critical metadata fields (e.g., precursor m/z, fragmentation type, scan properties) are present by spot-checking a sample spectrum or inspecting the file header; missing metadata may cause silent failures in mass matching and propagation scoring.

## Related tools

- **ProteoWizard msconvert** (Convert vendor-specific or unsupported spectrum formats to MGF for NPDtools compatibility) — http://proteowizard.sourceforge.net/tools/msconvert.html
- **MetaMiner** (Primary consumer of validated, centroided spectra; requires proper metadata for RiPP PSM matching and spectral network propagation) — https://github.com/mohimanilab/MetaMiner
- **Dereplicator** (Matches validated tandem mass spectra against post-translationally modified RiPP structure database; depends on centroiding and accurate precursor/fragment metadata) — https://github.com/ablab/npdtools
- **GNPS Spectral Networking / Molecular Networking** (Produces spectral network cluster metadata and inter-spectrum connectivity used by MetaMiner --spec-network option for RiPP propagation and visualization)

## Examples

```
msconvert proprietary_spectrum.raw --mgf --output validated_spectra/ && python metaminer.py validated_spectra/*.mgf -s example_RiPP.fasta --spec-network ProteoSAFe-METABOLOMICS-SNETS-V2-unpacked -o metaminer_outdir
```

## Evaluation signals

- All input spectra files parse without errors in the native NPDtools reader (MGF, mzXML, mzData) or after msconvert conversion to MGF.
- Spot-check: inspect a sample spectrum and confirm presence of centroided m/z-intensity pairs (not continuous profile data) and valid precursor m/z values.
- When using --spec-network, verify that the unpacked spectral network directory contains at least three output files: propagations.pdf, propagations_detailed.txt, and propagations_short.txt, indicating successful cluster metadata parsing.
- Run MetaMiner or Dereplicator on a small subset of validated spectra and confirm that PSM matches are returned; absence of matches despite known RiPPs in the structure database suggests metadata corruption or misconfigured centroiding.
- Cross-check spectral network cluster sizes and inter-cluster edges reported in propagations_detailed.txt against known spectral similarity thresholds (e.g., cosine similarity > 0.7 implied by network construction) to confirm data integrity.

## Limitations

- msconvert support is limited to formats explicitly handled by ProteoWizard; highly proprietary or legacy vendor formats may not convert successfully, requiring manual preprocessing or alternative tools.
- Centroiding status is often not explicitly flagged in file headers; verification requires manual inspection of a sample spectrum or external instrument documentation—automated detection is unreliable.
- Spectral network metadata (propagations files) depend on GNPS preprocessing quality; if the underlying spectral networking stage fails or uses non-standard parameters, propagation annotations may be incomplete or absent.
- Critical metadata fields (e.g., precursor m/z, charge state) may be missing or malformed in publicly deposited datasets due to incomplete instrument configuration logging or submission errors; NPDtools will not warn users of such defects during parsing.

## Evidence

- [readme] Spectra files must be centroided and be in an open spectrum format (**MGF**, **mzXML**, **mzML** or **mzData**).: "Spectra files must be centroided and be in an open spectrum format (**MGF**, **mzXML**, **mzML** or **mzData**)."
- [readme] NPDtools natively supports MGF and mzXML/mzData. We use msconvert utility from the ProteoWizard package to convert spectra in other formats to MGF.: "NPDtools natively supports MGF and mzXML/mzData. We use msconvert utility from the ProteoWizard package to convert spectra in other formats to MGF."
- [methods] Execute MetaMiner with the --spec-network option pointing to the unpacked spectral network directory. Verify that the spec_nets output folder is created within metaminer_outdir containing the three required output files: propagations.pdf, propagations_detailed.txt, and propagations_short.txt.: "Verify that the spec_nets output folder is created within metaminer_outdir containing the three required output files: propagations.pdf, propagations_detailed.txt, and propagations_short.txt."
- [readme] For parallel processing of multiple spectra files, NPDtools also requires joblib Python library. For presenting Spectral Network propagation graphs, MetaMiner requires matplotlib and networkx Python libraries.: "For presenting Spectral Network propagation graphs, MetaMiner requires `matplotlib` and `networkx` Python libraries."
- [readme] The metabologenomic pipelines (currently MetaMiner only) require either raw genome nucleotide sequences or output of specific genome mining tools.: "The metabologenomic pipelines (currently MetaMiner only) require either raw genome nucleotide sequences or output of specific genome mining tools."
