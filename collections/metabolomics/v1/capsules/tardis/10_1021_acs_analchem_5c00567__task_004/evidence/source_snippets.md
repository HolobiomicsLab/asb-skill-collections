# Evidence Snippets

## ev_001

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[results] Does the sawtooth artefact appear in extracted ion chromatogram (EIC) output when tardisPeaks() is run on LC-MS data with multiple overlapping m/z scan windows without proper mass_range separation?: 'if your data contains multiple (overlapping) *m/z* scan windows, it is necessary to analyze these separately through the "mass_range" argument. If not, you will notice that peaks will have a sawtooth'

## ev_002

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[results] Peaks display a sawtooth profile when tardisPeaks() processes data with multiple overlapping m/z scan windows without mass_range separation, due to filtering of empty spectra within TARDIS.: 'if your data contains multiple (overlapping) *m/z* scan windows, it is necessary to analyze these separately through the "mass_range" argument. If not, you will notice that peaks will have a sawtooth'

## ev_003

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[methods] Centroided mzML vignette files: 'Input files need to be converted to the .mzML format and have to be centroided'

## ev_004

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[methods] Target list data.frame with compound ID, name, m/z, RT, and polarity: 'compound ID, a unique identifier; A compound Name; Theoretical or measured *m/z*; Expected RT (in minutes); A column that indicates the polarity'

## ev_005

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[results] EIC plots with sawtooth artefact (incorrect mass_range routing): 'The resulting EICs are again saved in the output folder and can be inspected'

## ev_006

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[results] EIC plots with clean peak profiles (correct mass_range routing): 'The resulting EICs are again saved in the output folder and can be inspected'

## ev_007

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[results] Data.frame with AUC metrics for each target across both runs: 'The `results` object is a `list` that contains a `data.frame` with the AUC of each target in each run'

## ev_008

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[intro] Spectra: 'loads MS data as `Spectra` objects so it's easily integrated with other tools'

## ev_009

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[intro] R: 'R package for *TArgeted Raw Data Integration In Spectrometry*'

## ev_010

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[results] knitr: 'knitr::include_graphics'

## ev_011

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[discussion] No changelog or version history provided for the TARDIS package, limiting traceability of changes to tardisPeaks() function signature and mass_range parameter behavior: '_No changelog found._'
