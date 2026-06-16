# Evidence Snippets

## ev_001

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[results] Does tardisPeaks() in screening mode successfully generate and save extracted ion chromatogram (EIC) plots for all 10 target compounds (5 internal standards + 5 endogenous metabolites) to the diagnostic QC output folder?: 'We can run screening mode using the argument `screening_mode = TRUE` in the tardis_peaks function.'

## ev_002

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[results] tardisPeaks() in screening mode generates EIC plots for all 10 targets that are saved to the output folder and can be inspected, with resulting diagnostic plots for QC runs showing peak detection and integration for each component.: 'The resulting EICs are saved in the output folder and can be inspected'

## ev_003

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[methods] 14 centroided .mzML LC-MS data files (vignette dataset): 'Input files need to be converted to the .mzML format and have to be centroided'

## ev_004

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[methods] Target list data.frame with compound ID, name, m/z, retention time, and polarity: 'compound ID, a unique identifier; A compound Name; Theoretical or measured *m/z*; Expected RT (in minutes); A column that indicates the polarity'

## ev_005

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[results] 10 extracted ion chromatogram (EIC) PNG plots (one per target compound) with peak annotations: 'The resulting EICs are again saved in the output folder and can be inspected'

## ev_006

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[intro] TARDIS: 'R package for *TArgeted Raw Data Integration In Spectrometry*'

## ev_007

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[intro] Spectra: 'loads MS data as `Spectra` objects so it's easily integrated with other tools'

## ev_008

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[intro] xcms: 'It makes use of an established retention time correction algorithm from the `xcms` package'

## ev_009

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[intro] R: 'R package for *TArgeted Raw Data Integration In Spectrometry*'

## ev_010

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[intro] MsExperiment: 'Alternatively, instead of using file paths as input for TARDIS, the user can also use an `MsExperiment` object'

## ev_011

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[results] knitr: 'knitr::include_graphics'

## ev_012

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[discussion] No changelog found: '_No changelog found._'
