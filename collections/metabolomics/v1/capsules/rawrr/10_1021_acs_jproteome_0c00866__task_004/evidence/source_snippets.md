# Evidence Snippets

## ev_001

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[results] Does the parallel reaction monitoring (PRM) acquisition in the example raw file maintain consistent scan spacing across all cycles targeting the LGGNEQVTR++ precursor ion?: 'When subsetting it for our scan type of interest it becomes clear that the example data was recorded using parallel reaction monitoring (PRM) since the parent ion 487.2567 was isolated in'

## ev_002

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[results] The delta between consecutive PRM scans targeting LGGNEQVTR++ (487.2567) is consistently 22 scans, representing one complete PRM cycle.: 'The delta between consecutive scans is always 22 scans (one PRM cycle) and the `depedencyType` of the MS2 scans is `NA` (since it was triggered by an inclusion list).'

## ev_003

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[methods] 20181113_010_autoQC01.raw file from MassIVE dataset MSV000086542: 'The example file `20181113_010_autoQC01.raw` used throughout this manuscript contains Fourier-transformed Orbitrap spectra (FTMS) recorded on a Thermo Fisher Scientific Q Exactive HF'

## ev_004

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[results] Filtered scan index data frame (CSV or R object) containing only PRM scans with columns: scan, scanType, rtmin, rtmax, and computed delta (inter-scan interval): 'rawrr::readIndex(rawfile = rawfile) |> subset(scanType == ...)'

## ev_005

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[results] Summary statistics report documenting total PRM scan count, delta distribution (mean, min, max), and boolean pass/fail for 22-scan-cycle consistency: 'rawrr::readIndex(rawfile = rawfile) |> subset(scanType == ...)'

## ev_006

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[methods] rawrr: 'rawrr::readIndex(rawfile = rawfile)'

## ev_007

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[methods] RawFileReader: 'Specifically, `R` functions requesting access to data stored in binary raw files (reader family functions listed in Table 1) invoke compiled `C#` wrapper methods using a system call'

## ev_008

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[discussion] The specific scan filter string or column value that uniquely identifies PRM scan events within the readIndex output is not stated.: 'Filter scans by type 'FTMS + c NSI Full ms2 487.2567@hcd27.00 [100.0000-1015.0000]''

## ev_009

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[discussion] The expected cycle length of 22 scans for PRM experiments on this instrument or in this dataset is not explicitly documented in the provided text.: 'No direct statement in provided text; sub-task scope cites '22 scans (one full cycle)' as a target but this is not verified against any reported figure or table in the section text.'
