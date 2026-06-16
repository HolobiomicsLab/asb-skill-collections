# Evidence Snippets

## ev_001

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[intro] Does the asari pipeline successfully produce all five canonical output artifacts (preferred_Feature_table.tsv, full_Feature_table.tsv, _mass_grid_mapping.csv, cmap.pickle, and Annotated_empiricalCompounds.json) when executed on a publicly deposited centroided mzML dataset?: 'Trackable and scalable Python program for high-resolution metabolomics data processing.'

## ev_002

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[intro] Asari is designed as a transparent, JSON-centric program with reproducible data structures that enable tracking and backtracking between features and mass tracks (EICs), supporting output artifact generation and traceability.: 'Reproducible, track and backtrack between features and mass tracks (EICs); Transparent, JSON centric data structures, easy to chain other tools'

## ev_003

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[methods] Centroided mzML files from LC-MS metabolomics experiment in publicly accessible repository (e.g., GitHub, Zenodo, MassIVE, MetaboLights, or local directory): 'Input data are centroied mzML files from LC-MS metabolomics.'

## ev_004

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[methods] Optional: custom parameters YAML file specifying ppm tolerance, min_peak_height, and other processing thresholds: 'Users can supply a custom parameter file `xyz.yaml`, via `--parameters xyz.yaml` in command line.'

## ev_005

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[methods] preferred_Feature_table.tsv: recommended feature intensity table with sample columns and feature rows: 'The recommended feature table is `preferred_Feature_table.tsv`.'

## ev_006

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[methods] full_Feature_table.tsv: complete peak table including all features meeting SNR and peakshape thresholds: 'All peaks are kept in `export/full_Feature_table.tsv` if they meet signal (snr) and shape standards'

## ev_007

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[methods] _mass_grid_mapping.csv: m/z alignment results mapping mass tracks across samples: 'MassGrid is exported as a csv file.'

## ev_008

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[methods] cmap.pickle: serialized composite map object for dashboard inspection: 'The composite map is exported as a pickle file, which is used by the visual dashboard.'

## ev_009

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[methods] epd.pickle: serialized empirical compound dictionary for dashboard and downstream analysis: 'The dashboard uses these files under the result folder: 'project.json', 'export/cmap.pickle', 'export/epd.pickle''

## ev_010

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[methods] Annotated_empiricalCompounds.json: pre-annotated empirical compounds with isotope/adduct grouping and database matches: 'Annotation is exported into both JSON and tsv formats.'

## ev_011

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[methods] Python: 'Trackable and scalable Python program for high-resolution LC-MS metabolomics data preprocessing'

## ev_012

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[methods] pymzml: 'The default method uses `pymzml` to parse mzML files.'

## ev_013

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[methods] scipy.signal.find_peaks: 'Asari uses a simple local maxima method (scipy.signal.find_peaks), with prominence control'

## ev_014

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[methods] scipy.signal.detrend: 'detrend (scipy.signal.detrend) is performed on the mass track.'

## ev_015

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[methods] khipu: 'The preannotaion is done via another package khipu (https://github.com/shuzhao-li-lab/khipu)'

## ev_016

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[methods] JMS: 'The empirical compounds are searched against known compound database (default HMDB 4) via another package JMS (https://github.com/shuzhao-li/JMS).'

## ev_017

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[methods] HMDB 4: 'known compound database (default HMDB 4)'

## ev_018

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[discussion] No changelog available to document version history, breaking changes, or artifact schema evolution: '_No changelog found._'
