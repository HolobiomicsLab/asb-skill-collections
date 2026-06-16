# Evidence Snippets

## ev_001

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[results] What are the sequential data processing steps that the PCPFM pipeline executes to transform raw LC-MS metabolomics data into normalized feature tables ready for statistical analysis?: 'The pipeline can convert Thermo .raw to mzML, process mzML data to feature tables (Asari), perform quality control, data normalization and batch correction, pre-annotation to group features to'

## ev_002

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[results] PCPFM implements a fixed orchestrator pipeline that sequences: (1) experiment assembly from metadata; (2) raw file conversion to mzML; (3) Asari feature extraction producing full and preferred feature tables; (4) blank masking by comparing sample to blank intensities with configurable intensity ratios; (5) sample dropping by metadata field or QAQC results; (6) TIC normalization using common features above a percentile threshold; (7) missing value imputation as multiples of minimum feature values; (8) optional batch correction using pycombat; and (9) empirical compound construction via khipu with configurable mz/rt tolerances and adduct/isotope definitions.: 'pcpfm assemble, pcpfm convert, pcpfm asari, pcpfm blank_masking --blank_intensity_ratio, pcpfm drop_samples, pcpfm normalize --TIC_normalization_percentile, pcpfm impute --interpolation_ratio, pcpfm'

## ev_003

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[methods] CSV metadata file with sample names, file paths, sample type classification, and batch identifiers: 'CSV file for metadata (minimal sample names and file path)'

## ev_004

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[methods] Raw LC-MS data files in Thermo .raw or mzML format: 'Inputs should include a set of raw files (.raw or .mzML)'

## ev_005

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[methods] Processed feature table (TSV/CSV) with normalized, imputed, and filtered metabolomic features ready for statistical analysis: 'Outputs are intended to be immediately usable for downstream analysis'

## ev_006

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[methods] Empirical compound JSON file representing putative metabolites grouped by isotopes and adducts with pre-annotation: 'empirical compounds as a JSON file representing putative metabolites that can be annotated with MS1, MS2, or authentic standards'

## ev_007

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[methods] Experiment state JSON file (experiment.json) tracking all processing steps, intermediate tables, and metadata: 'The experiment object will be used throught the processing and store intermediates'

## ev_008

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[intro] Python: 'Python-Centric Pipeline for Metabolomics'

## ev_009

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[intro] ThermoRawFileParser: 'convert Thermo .raw to mzML (ThermoRawFileParser)'

## ev_010

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[intro] Asari: 'process mzML data to feature tables (Asari)'

## ev_011

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[intro] khipu: 'pre-annotation to group featues to empirical compounds (khipu)'

## ev_012

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[discussion] No changelog or version history is documented: '_No changelog found._'

## ev_013

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[discussion] The provided section text contains no description of the ARCH-PIPELINE fixed architecture, its stages, control flow, or orchestrator implementation: '[UNTRUSTED_DOCUMENT] _No changelog found._ ## References ... [/UNTRUSTED_DOCUMENT]'
