# Evidence Snippets

## ev_001

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[results] What are the required method signatures and implementations needed to create a complete MsBackendTest class that extends MsBackend and provides full read-write access to mass spectrometry spectral data?: 'To create a new backend a class extending the virtual `MsBackend` needs to be implemented. In the example below we create thus a simple class with a `data.frame` to contain general spectral'

## ev_002

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[results] MsBackendTest requires implementation of 9 required accessor methods (spectraData, spectraVariables, backendInitialize, peaksData, extractByIndex, backendMerge, intensity, mz, spectraNames) plus 7 data replacement methods ($<-, spectraData<-, intensity<-, mz<-, peaksData<-, selectSpectraVariables, dataStorage<-, spectraNames<-) with specific signatures. The class uses three slots: spectraVars (data.frame), mz (NumericList), and intensity (NumericList), where each row in spectraVars represents one spectrum and corresponding elements in mz/intensity lists contain peak data.: 'The 3 slots `spectraVars`, `mz` and `intensity` will be used to store our MS data, each row in `spectraVars` being data for one spectrum with the columns being the different *spectra variables* (i.e.'

## ev_003

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[intro] MsBackend virtual class API specification and documentation: 'The `MsBackend` virtual class defines the API that new *backend* classes need to implement in order to be used with the `Spectra` object.'

## ev_004

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[intro] R source file containing complete MsBackendTest class implementation with all required methods: 'To create a new backend a class extending the virtual `MsBackend` needs to be implemented.'

## ev_005

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[intro] Spectra: 'The *Spectra* package defines an efficient infrastructure for storing and handling mass spectrometry spectra'

## ev_006

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[intro] S4Vectors: 'return the **full** spectra data within a backend as a `DataFrame` object (defined in the `r Biocpkg("S4Vectors")`'

## ev_007

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[intro] R: 'library(Spectra)
library(IRanges)'

## ev_008

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[discussion] No changelog document available to verify version history or API changes to MsBackendTest class: '_No changelog found._'

## ev_009

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[discussion] Specific implementation details of MsBackendTest class methods are not provided in the discussion section: '_No changelog found._'
