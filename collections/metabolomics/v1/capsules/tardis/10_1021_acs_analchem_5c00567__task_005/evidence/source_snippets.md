# Evidence Snippets

## ev_001

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[results] Do MsExperiment objects with annotated sampleData$type produce identical screening-mode EIC diagnostic outputs compared to file-path-based invocation of tardisPeaks()?: 'Alternatively, instead of using file paths as input for TARDIS, the user can also use an `MsExperiment` object. Here it is necessary to include at least sample type in the sampleData to distinguish'

## ev_002

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[results] The tardisPeaks() function accepts both file paths and MsExperiment objects as input when screening_mode=TRUE, with the MsExperiment approach requiring sampleData$type to be populated to distinguish QC from sample runs.: 'results <- tardisPeaks(
    lcmsData = ms_data,
    dbData = targets,
    mass_range = NULL,
    polarity = "positive",
    output_directory = "vignette_data/output/screening/",
    batch_positions ='

## ev_003

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[methods] mzML files (centroided) corresponding to LC-MS runs for targeted analysis: 'Input files need to be converted to the .mzML format and have to be centroided'

## ev_004

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[methods] Target list data frame with columns: compound ID, compound name, m/z, expected retention time (minutes), and polarity: 'compound ID, a unique identifier; A compound Name; Theoretical or measured *m/z*; Expected RT (in minutes); A column that indicates the polarity'

## ev_005

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[methods] Sample metadata including type labels (e.g., QC, sample) for each mzML file: 'sampleData$type labels'

## ev_006

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[results] EIC PNG diagnostic figures saved to output folder for visual inspection of target peak detection in screening mode: 'The resulting EICs are again saved in the output folder and can be inspected'

## ev_007

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[methods] Verification report confirming EIC PNG files from MsExperiment-based invocation match file-path-based reference invocation: 'verify that the resulting Diagnostic EIC PNG files match those produced from the file-path-based invocation'

## ev_008

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[intro] Spectra: 'loads MS data as `Spectra` objects so it's easily integrated with other tools'

## ev_009

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[intro] MsExperiment: 'Alternatively, instead of using file paths as input for TARDIS, the user can also use an `MsExperiment` object'

## ev_010

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[intro] TARDIS: 'R package for *TArgeted Raw Data Integration In Spectrometry*'

## ev_011

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[intro] R: 'R package for *TArgeted Raw Data Integration In Spectrometry*'

## ev_012

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[results] knitr: 'knitr::include_graphics'

## ev_013

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[discussion] No changelog documenting version history, breaking changes, or API modifications available: '_No changelog found._'
