---
name: gnps-workflow-result-processing
description: Use when when you have run a spectral networking job on GNPS (e.g. ProteoSAFe-METABOLOMICS-SNETS-V2) and need to reuse the network output files locally with MetaMiner or another tool that accepts spectral network input directories.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_0335
  edam_topics:
  - http://edamontology.org/topic_0749
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_3365
  tools:
  - MetaMiner
  - NPDtools 2.5.0
  - GNPS Spectral Networking / Molecular Networking
  - matplotlib
  - networkx
  - ProteoWizard (msconvert)
  techniques:
  - tandem-MS
derived_from:
- doi: 10.1038/s41467-018-06082-8
  title: dereplicator
evidence_spans:
- MetaMiner is a metabologenomic pipeline which integrates metabolomic (tandem mass spectra) and genomic data to identify novel RiPPs
- MetaMiner is a metabologenomic pipeline which integrates metabolomic (tandem mass spectra) and genomic data to identify novel Ribosmally synthesized and Post-translationally modified Peptides (RiPPs)
- The latest version is available in the Natural Product Discovery toolkit (NPDtools) at https://github.com/ablab/npdtools
- Spectral network can be easily run through GNPS. Detailed instructions can be found in the [GNPS documentation]
- For presenting Spectral Network propagation graphs, MetaMiner also requires `matplotlib` and `networkx` Python libraries
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

# GNPS workflow result processing

## Summary

Extract and validate output files from GNPS Spectral Networking / Molecular Networking workflows (e.g. ProteoSAFe-METABOLOMICS-SNETS-V2) to enable downstream metabologenomic analysis. This skill ensures that precomputed spectral network archives are correctly unpacked and integrated into tools like MetaMiner for RiPP identification and visualization.

## When to use

When you have run a spectral networking job on GNPS (e.g. ProteoSAFe-METABOLOMICS-SNETS-V2) and need to reuse the network output files locally with MetaMiner or another tool that accepts spectral network input directories. This is necessary when you want to enlarge your RiPP identifications via spectral networking and visualize the propagation results.

## When NOT to use

- If you have not run a spectral networking job on GNPS yet; instead, submit your spectra to GNPS first or use precomputed networks from public datasets.
- If your spectra are in non-centroided format or an unsupported file format (e.g. raw binary); convert to MGF, mzML, mzXML, or mzData first using msconvert.
- If you do not have a RiPP FASTA file or genome sequence file; MetaMiner requires genomic input to construct the RiPP structure database.

## Inputs

- GNPS ProteoSAFe workflow result archive (e.g. .zip containing spectral network output)
- Spectra files in mzML, mzXML, mzData, or MGF format
- RiPP FASTA file (precursor peptide sequences)
- MetaMiner parameters (--spec-network, --blind flag if appropriate)

## Outputs

- Unpacked spectral network directory with network structure files
- propagations.pdf (graphical propagation report)
- propagations_detailed.txt (detailed propagation clusters and neighbors)
- propagations_short.txt (representative propagation per cluster)
- spec_nets folder within MetaMiner output directory

## How to apply

Download or retrieve the precomputed spectral network output archive from GNPS (e.g. ProteoSAFe-METABOLOMICS-SNETS-V2.zip). Unpack the archive to a local directory, which will contain the spectral network structure files. Pass this unpacked directory to MetaMiner using the --spec-network option alongside your spectra files, RiPP FASTA file, and output directory. MetaMiner will then produce three output files within a spec_nets folder: propagations.pdf (graphical report with one page per connected component of significant PSM), propagations_detailed.txt (detailed text report listing all spectra from same cluster and clusters at distance 1 and 2), and propagations_short.txt (representative per cluster). Verify that all three files are present and non-empty before proceeding to result visualization.

## Related tools

- **MetaMiner** (Accepts unpacked GNPS spectral network directory via --spec-network option; uses network output to enlarge RiPP identifications and produce propagation reports) — https://github.com/mohimanilab/MetaMiner
- **GNPS Spectral Networking / Molecular Networking** (Source of the precomputed spectral network archive; generates the ProteoSAFe-METABOLOMICS-SNETS-V2 output that is unpacked and reused) — https://gnps.ucsd.edu/ProteoSAFe/static/gnps-theoretical.jsp
- **ProteoWizard (msconvert)** (Converts spectra in non-native formats (e.g. mzML) to MGF if needed before GNPS submission or local processing)
- **matplotlib** (Required by MetaMiner to generate propagations.pdf graphical report; if absent, propagation output is plain text only)
- **networkx** (Required by MetaMiner to construct and visualize propagation graphs from spectral network data)

## Examples

```
python metaminer.py test_data/metaminer/msms/ -s test_data/metaminer/molnet/example_RiPP.fasta --blind --spec-network test_data/metaminer/molnet/ProteoSAFe-METABOLOMICS-SNETS-V2-unpacked -o metaminer_outdir
```

## Evaluation signals

- All three output files (propagations.pdf, propagations_detailed.txt, propagations_short.txt) are present in spec_nets folder and are non-empty.
- propagations.pdf contains one or more pages, with one page per connected component of significant PSM (if matplotlib is installed); verify page count matches number of expected network clusters.
- propagations_detailed.txt lists all spectra from same cluster and clusters at distance 1 and 2; spot-check that cluster identifiers are consistent and distances are numeric.
- propagations_short.txt contains one representative per cluster; verify that total number of representatives is less than or equal to total clusters in detailed report.
- MetaMiner execution completes without errors and the --spec-network directory path is logged in the command output.

## Limitations

- Spectral network archive structure and naming are specific to the GNPS ProteoSAFe workflow version used; changes in GNPS output format may require archive unpacking adjustments.
- If matplotlib and networkx are not installed, MetaMiner will generate propagations output in plain text format only, not as PDF graphics.
- The skill assumes the GNPS spectral networking job has already completed successfully; if the job failed or was interrupted, the archive may be incomplete or corrupt.
- Spectral network quality depends on the original mass spectrometry data quality and GNPS job parameters (e.g. parent mass tolerance, cosine similarity threshold); poorly tuned parameters upstream will result in spurious propagations.

## Evidence

- [methods] Execute MetaMiner with the --spec-network option pointing to the unpacked spectral network directory, the example RiPP FASTA file (DATITTVTVTSTSIWASTVSNHC), and the --blind flag for demonstration purposes: python metaminer.py <spectra_files> -s test_data/metaminer/molnet/example_RiPP.fasta --blind --spec-network test_data/metaminer/molnet/ProteoSAFe-METABOLOMICS-SNETS-V2-unpacked -o metaminer_outdir: "Execute MetaMiner with the --spec-network option pointing to the unpacked spectral network directory"
- [methods] Verify that the spec_nets output folder is created within metaminer_outdir containing the three required output files: propagations.pdf (graphical report with one page per connected component of significant PSM), propagations_detailed.txt (detailed text report listing all spectra from same cluster and clusters at distance 1 and 2), and propagations_short.txt (same as detailed but with one representative per cluster).: "spec_nets output folder is created within metaminer_outdir containing the three required output files: propagations.pdf, propagations_detailed.txt, and propagations_short.txt"
- [methods] The MetaMiner pipeline includes a spectral networking stage that enlarges the set of identified RiPPs via spectral networking and allows users to visualize the results after identifying some RiPPs.: "MetaMiner pipeline includes a spectral networking stage that enlarges the set of identified RiPPs via spectral networking"
- [readme] For presenting Spectral Network propagation graphs, MetaMiner requires `matplotlib` and `networkx` Python libraries. If they are not installed, the propagation will be generated in a plain text format only (see `--spec-network` option).: "MetaMiner requires `matplotlib` and `networkx` Python libraries. If they are not installed, the propagation will be generated in a plain text format only"
- [methods] Download the three mzML spectra files (C18p_5uL_NASA_Sample_BB2_01_25958.mzML, C18p_5uL_NASA_Sample_BB3_01_25959.mzML, C18p_5uL_NASA_Sample_BB4_01_25960.mzML) from MSV000080102 or retrieve the precomputed spectral network output files from GNPS and unpack the ProteoSAFe-METABOLOMICS-SNETS-V2 archive.: "retrieve the precomputed spectral network output files from GNPS and unpack the ProteoSAFe-METABOLOMICS-SNETS-V2 archive"
