# Evaluation Strategy

## Direct Checks

- verify file exists: downloaded hmdb_compounds.p from https://github.com/glasgowcompbio/vimms-data/raw/main/hmdb_compounds.p
- verify file_format_is: output mzML file is valid mzML (XML-based, contains scan elements with m/z and intensity arrays)
- verify script_runs: Python script instantiates FullScanController, IndependentMassSpectrometer with KnownChemical objects, and Environment; calls env.run() without error
- verify file_exists: output mzML file is written to disk by Environment.write_mzML()
- verify contains_substring: output mzML contains MS1 spectrum entries (scan@msLevel='1') with m/z and intensity data
- verify output_matches_reference: mzML structure (scan count, m/z range ~100–1000, spectrum type) is consistent with demo notebook expectations, robust to exact peak intensity variations across reruns

## Expert Review

- confirm that sampled KnownChemical objects from HMDB exhibit expected m/z distribution (100–1000 range) and chemical diversity representative of metabolomics
- confirm that FullScanController generates MS1-only scans (no fragmentation) with appropriate retention time spacing and realistic ion intensities for the simulated sample
- confirm that mzML output is compatible with standard metabolomics workflows (can be opened by OpenMS, mzmine2, or equivalent peak-picking tools without corruption)
