# Evidence Snippets

## ev_001

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[results] What quantitative metrics and output tables does tardisPeaks() generate when run in peak detection mode (screening_mode=FALSE) on LC-MS data?: 'The `results` object is a `list` that contains a `data.frame` with the AUC of each target in each run and a `tibble` that contains a feature table with the average metrics for each target in the QC'

## ev_002

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[results] tardisPeaks() with screening_mode=FALSE produces multiple output tables including: a data.frame with per-target AUC values across runs, a QC feature table tibble with average metrics, and CSV files containing Max Intensity, SNR, peak_cor, and points over the peak for all targets.: 'Other results include tables with the other metrics (Max. Int., SNR, peak_cor and points over the peak) and are saved into the output folder.'

## ev_003

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[methods] Vignette LC-MS dataset in .mzML centroided format with compound target list specifying compound ID, name, m/z, expected RT (minutes), and polarity: 'Input files need to be converted to the .mzML format and have to be centroided; compound ID, a unique identifier; A compound Name; Theoretical or measured *m/z*; Expected RT (in minutes); A column'

## ev_004

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[results] QC feature table tibble containing average metrics for each target in QC runs: 'a `tibble` that contains a feature table with the average metrics for each target in the QC runs'

## ev_005

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[results] CSV file with AUC values for each target in each run: 'The `results` object is a `list` that contains a `data.frame` with the AUC of each target in each run'

## ev_006

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[results] CSV files with Max Intensity, SNR, peak_cor, and points over peak metrics: 'Other results include tables with the other metrics (Max. Int., SNR, peak_cor and points over the peak)'

## ev_007

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[results] Extracted Ion Chromatograms (EICs) saved in the output folder: 'The resulting EICs are again saved in the output folder and can be inspected'

## ev_008

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[intro] Spectra: 'loads MS data as `Spectra` objects so it's easily integrated with other tools'

## ev_009

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[intro] xcms: 'It makes use of an established retention time correction algorithm from the `xcms` package'

## ev_010

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[intro] R: 'R package for *TArgeted Raw Data Integration In Spectrometry*'

## ev_011

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[results] knitr: 'knitr::include_graphics'

## ev_012

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[results] kableExtra: 'kableExtra::kable'

## ev_013

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[discussion] No changelog documentation available: '_No changelog found._'
