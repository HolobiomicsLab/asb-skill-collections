# Evidence Snippets

## ev_001

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[methods] Can mass2adduct's massdiff() and adductMatch() pipeline successfully process MSI data converted from Cardinal's MSProcessedImagingExperiment or MSContinuousImagingExperiment objects using the cardinal2msimat() function?: 'If you are using Cardinal to process your MSI data, data objects in the `MSProcessedImagingExperiment` or `MSContinuousImagingExperiment` formats can be converted to mass2adduct's `msimat` format'

## ev_002

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[methods] The mass2adduct package provides cardinal2msimat() for converting Cardinal MSI data objects to the msimat format compatible with the massdiff() and adductMatch() pipeline.: 'If you are using Cardinal to process your MSI data, data objects in the `MSProcessedImagingExperiment` or `MSContinuousImagingExperiment` formats can be converted to mass2adduct's `msimat` format'

## ev_003

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[other] Cardinal MSProcessedImagingExperiment or MSContinuousImagingExperiment object (in-memory R object or saved .rds file): 'If you are using Cardinal to process your MSI data, data objects in the `MSProcessedImagingExperiment` or `MSContinuousImagingExperiment` formats can be converted to mass2adduct's `msimat` format'

## ev_004

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[other] Reference adduct dataset (built-in: adducts or adducts2; or user-supplied data.frame with columns: name, formula, mass): 'There are two built-in data sets `adducts` and `adducts2` (shorter), which list biologically-relevant chemical species that might occur in biological samples.'

## ev_005

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[other] Annotated massdiff object (data.frame with columns A, B, diff, and matches) containing ion pairs matched to known adducts: 'We can match massdiffs to specific adduct types using the same function `adductMatch` that we applied to the histogram above. This adds an additional column to the `massdiff` object called `matches`,'

## ev_006

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[other] Cardinal: 'If you are using Cardinal to process your MSI data, data objects in the `MSProcessedImagingExperiment` or `MSContinuousImagingExperiment` formats can be converted to mass2adduct's `msimat` format'

## ev_007

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[intro] mass2adduct: 'This package presents tools for counting and identifying possible adducts in MS data, and accompanies Janda et al. (in prep.).'

## ev_008

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[other] R: 'library(mass2adduct)'

## ev_009

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[discussion] No changelog found: '_No changelog found._'

## ev_010

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[discussion] No version information or release date for mass2adduct package provided in article or repository metadata: 'Synthesized at: 2026-06-15T13:12:45+00:00'

## ev_011

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[methods] No documentation of cardinal2msimat() function signature, parameter defaults, or error handling behavior in the provided text: 'If you are using Cardinal to process your MSI data, data objects in the `MSProcessedImagingExperiment` or `MSContinuousImagingExperiment` formats can be converted to mass2adduct's `msimat` format'
