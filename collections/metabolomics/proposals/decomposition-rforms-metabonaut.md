# RforMassSpectrometry and Metabonaut procedure decomposition

This review used the 7 November 2026 repository and article inventories. Each
procedure was searched against the v2 collection with `search_skills.py -k 5
--json`. A procedure is covered only when a returned leaf description names the
same operation. A related operation, another tool, or a narrower scope is
partial coverage.

## Metabonaut articles

| Source | Procedure a user would request | Verdict | Covering or related leaf |
| --- | --- | --- | --- |
| `install_v0.html` | Install the RforMassSpectrometry package stack and verify the installation. | uncovered | none |
| `a-end-to-end-untargeted-metabolomics.html` | Run an end-to-end untargeted LC-MS workflow with the RforMassSpectrometry stack. | partially covered | `masster` |
| `dataset-investigation.html` | Inspect a newly received LC-MS dataset before choosing preprocessing parameters. | partially covered | `dataset-object-serialization-and-deserialization` |
| `notame_normalization_and_feature_selection.html` | Apply Notame quality control, normalisation and feature selection. | partially covered | `feature-abundance-normalization` |
| `large-scale-analysis.html` | Preprocess a large LC-MS study with xcms without exhausting memory. | partially covered | `xcms-data-import-preprocessing` |
| `creating-using-annotation-resources.html` | Build and use a reusable metabolomics annotation resource. | partially covered | `untargeted-metabolomics-annotation` |
| `SpectriPy-tutorial-metabonaut.html` | Annotate LC-MS/MS data by passing Spectra objects between R and Python with SpectriPy. | partially covered | `mass-spectrometry-package-integration` |
| `advanced_feature_annotation_with_RuSirius.html` | Run advanced feature annotation from R through RuSirius. | partially covered | `feature-annotation-augmentation` |
| `alignment-to-external-dataset.html` | Align new LC-MS features to an existing preprocessed reference dataset. | partially covered | `mass-spectrometry-data-alignment` |
| `generation_of_mzTabM_file.html` | Import and export mzTab-M 2.1 from a SummarizedExperiment. | partially covered | `mztab-format-export-and-annotation` |

## RforMassSpectrometry repositories

Sticker, conference, organisation website, documentation-only and empty-description
repositories were excluded as requested.

| Package | Procedure a user would request | Verdict | Covering or related leaf |
| --- | --- | --- | --- |
| Chromatograms | Store, subset and process chromatograms in R. | partially covered | `baseline-and-noise-level-estimation-from-quartile-statistics` |
| CompoundDb | Create and query a reusable chemical compound database. | partially covered | `exact-mass-lookup-and-aggregation-from-chemical-databases` |
| MetaboAnnotation | Coordinate high-level metabolomics data annotation in R. | partially covered | `metabolite-set-annotation-mapping` |
| MetaboCoreUtils | Apply shared metabolomics calculations and conversions in R. | uncovered | none |
| MsBackendDuckDb | Expose DuckDB-hosted spectra through the Spectra backend API. | covered | `ms-backend-api-implementation` |
| MsBackendHSDS | Read remote HDF5 mass-spectrometry data through HSDS. | partially covered | `file-format-identification-mass-spectrometry` |
| MsBackendHmdb | Import and handle HMDB MS/MS spectra as Spectra objects. | partially covered | `spectra-variable-metadata-handling` |
| MsBackendMassIVE | Retrieve public MassIVE data for local Spectra workflows. | covered | `metabolomics-dataset-handling-massive` |
| MsBackendMassbank | Parse MassBank records into Spectra objects. | partially covered | `backend-merging-and-concatenation` |
| MsBackendMetaboLights | Retrieve MetaboLights spectra through a Spectra backend. | partially covered | `usi-namespace-parsing` |
| MsBackendMetabolomicsWorkbench | Retrieve and cache Metabolomics Workbench spectra. | partially covered | `usi-namespace-parsing` |
| MsBackendMgf | Import MGF spectra through a Spectra backend. | covered | `mass-spectrometry-data-import` |
| MsBackendMongoDb | Store and query Spectra data in MongoDB. | partially covered | `metabolic-network-database-output-and-serialization` |
| MsBackendMsp | Import MSP spectra through a Spectra backend. | covered | `mass-spectrometry-data-import` |
| MsBackendMzPeak | Import HUPO-PSI mzPeak data as Spectra objects. | partially covered | `s4-class-extension-development` |
| MsBackendMzSpecLib | Read and write HUPO-PSI mzSpecLib libraries in R. | partially covered | `file-format-compliance-validation` |
| MsBackendSql | Store and retrieve Spectra data in an SQL database. | covered | `spectra-variable-and-peak-data-storage` |
| MsBackendTimsTof | Read Bruker timsTOF data through opentimsr and Spectra. | partially covered | `msexperiment-backend-configuration` |
| MsBackendWeizMass | Expose WeizMass databases through Spectra. | covered | `spectra-data-representation-backends` |
| MsCoreUtils | Apply shared low-level mass-spectrometry utilities in R. | uncovered | none |
| MsDataHub | Discover and load curated mass-spectrometry datasets from ExperimentHub. | partially covered | `data-normalization-in-mass-spectrometry` |
| MsExperiment | Organise samples, spectra and features in an MsExperiment object. | partially covered | `high-resolution-mass-spectral-data-processing` |
| MsExperimentStash | Save and restore MsExperiment objects in interoperable formats. | uncovered | none |
| MsFeatures | Group and compare mass-spectrometry features. | partially covered | `mass-spectrometry-data-alignment` |
| MsIO | Import, export and convert mass-spectrometry object formats. | covered | `mass-spectrometry-format-conversion` |
| MsQuantitation | Represent and analyse quantitative mass-spectrometry assays. | partially covered | `lipidomics-experiment-object-construction` |
| MsStash | Save and restore mass-spectrometry result objects safely. | uncovered | none |
| PSMatch | Perform peptide-spectrum matching. | covered | `peptide-spectrum-matching` |
| PTMods | Represent and use amino-acid post-translational modifications. | covered | `open-modification-peptide-identification` |
| ProtGenerics | Use common S4 generics across mass-spectrometry packages. | uncovered | none |
| QFeatures | Manage and process quantitative feature assays. | partially covered | `mass-spectrometry-data-alignment` |
| QFeaturesGUI | Explore QFeatures assays through a graphical interface. | uncovered | none |
| RforMassSpectrometry | Install and coordinate the RforMassSpectrometry package ecosystem. | partially covered | `mass-spectrometry-package-integration` |
| RmzTabM | Import and export metabolomics and lipidomics results as mzTab-M. | partially covered | `mztab-format-export-and-annotation` |
| RuSirius | Run SIRIUS annotation from RforMassSpectrometry objects. | partially covered | `feature-annotation-augmentation` |
| Spectra | Create, subset and process Spectra objects. | covered | `spectra-object-instantiation-and-manipulation` |
| SpectraQL | Query Spectra objects with MassQL. | covered | `mass-spectrometry-domain-specific-language-comprehension` |
| SpectraStash | Save and restore Spectra objects in interoperable formats. | partially covered | `spectra-data-representation-backends` |
| SpectraVis | Visualise spectra and their annotations in R. | partially covered | `spectra-data-extraction-and-subsetting` |
| SpectriPy | Apply Python mass-spectrometry algorithms to R Spectra objects. | covered | `mass-spectrometry-package-integration` |
| metaRbolomics-book | Compare and select metabolomics packages across R repositories. | uncovered | none |
| xcmsStash | Save and restore xcms results in interoperable formats. | uncovered | none |

## Summary

The decomposition contains 52 procedures (10 Metabonaut articles, 42
RforMassSpectrometry packages): 12 covered, 31 partially covered and
9 uncovered. Partial coverage is intentionally strict: the listed leaf is a
nearby operation, not evidence that the source procedure itself is taught.

## Candidate skills from uncovered procedures

- Install and verify the RforMassSpectrometry stack, grounded by Metabonaut
  `install_v0.html`.
- Apply MetaboCoreUtils conversions and calculations, grounded by
  `MetaboCoreUtils`.
- Apply MsCoreUtils low-level utilities, grounded by `MsCoreUtils`.
- Store and restore MsExperiment objects interoperably, grounded by
  `MsExperimentStash`.
- Store and restore mass-spectrometry results interoperably, grounded by
  `MsStash`.
- Define and reuse proteomics S4 generics, grounded by `ProtGenerics`.
- Explore quantitative feature assays in a GUI, grounded by `QFeaturesGUI`.
- Compare and select metabolomics R packages, grounded by `metaRbolomics-book`.
- Store and restore xcms results interoperably, grounded by `xcmsStash`.
