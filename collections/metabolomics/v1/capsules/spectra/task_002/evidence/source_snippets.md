# Evidence Snippets

## ev_001

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[results] Does the spectraData() method on a MsBackendTest instance correctly return all core spectra variables with NA values when only user-supplied spectra variables are stored in the backend?: 'The `DataFrame` **must** provide values (even if they are `NA`) for **all** requested spectra variables of the backend (**including** the core spectra variables).'

## ev_002

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[results] The spectraData() implementation for MsBackendTest uses fillCoreSpectraVariables() to ensure that all core spectra variables are returned, filling missing ones with NA values even when only user-supplied variables like msLevel and rtime are stored.: 'To ensure that `spectraData()` always returns all required *core* spectra variables (of the correct data type) we can use however the `fillCoreSpectraVariables()` function. This function adds'

## ev_003

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[intro] Spectra package documentation and API specification: 'The `MsBackend` virtual class defines the API that new *backend* classes need to implement'

## ev_004

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[intro] User-supplied spectra variables: msLevel and rtime values: 'slots = c(
             spectraVars = "data.frame",
             mz = "NumericList",
             intensity = "NumericList"
         )'

## ev_005

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[intro] MsBackendTest class definition extending MsBackend with implemented core methods: 'To create a new backend a class extending the virtual `MsBackend` needs to be implemented.'

## ev_006

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[intro] DataFrame returned by spectraData() containing all core spectra variables with NA for missing user-supplied values: 'The `spectraData()` method should return the **full** spectra data within a backend as a `DataFrame` object'

## ev_007

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[intro] Spectra: 'The *Spectra* package defines an efficient infrastructure for storing and handling mass spectrometry spectra'

## ev_008

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[intro] S4Vectors: 'return the **full** spectra data within a backend as a `DataFrame` object (defined in the `r Biocpkg("S4Vectors")`'

## ev_009

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[intro] R: 'library(Spectra)
library(IRanges)'

## ev_010

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[discussion] No changelog documenting changes to spectraData() method behavior or fillCoreSpectraVariables() implementation: '_No changelog found._'
