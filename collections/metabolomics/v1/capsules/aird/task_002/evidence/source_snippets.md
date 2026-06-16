# Evidence Snippets

## ev_001

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[intro] Does execution of AirdPro CLI against a vendor mass spectrometry raw file via the airdpro:cli Docker image complete Wine initialization and produce a converted Aird output file?: 'AirdPro is a GUI client for conversion from vendor files to Aird files'

## ev_002

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[other] AirdPro converts vendor mass spectrometry files to Aird format; first-run execution requires Wine to initialize and download .NET Framework components, a process documented to take more than 30 minutes.: 'AirdPro is a GUI client for conversion from vendor files to Aird files. Wine needs to initialize and download .NET Framework components, taking more than 30 minutes'

## ev_003

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[methods] airdpro:cli Docker image (pre-built from build step): 'CLI Version (For batch processing tasks)'

## ev_004

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[methods] Sample vendor mass spectrometry raw file (e.g., .raw, .d format): 'File conversion example ./run-cli.sh -i data/input.raw -o data/output.mzML'

## ev_005

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[methods] run-cli.sh execution script from project root: './run-cli.sh -i data/input.raw -o data/output.mzML'

## ev_006

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[intro] Aird format output file produced by AirdPro conversion: 'AirdPro is a GUI client for conversion from vendor files to Aird files'

## ev_007

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[methods] Wine startup time log documenting first-run initialization duration (>30 min): 'Wine needs to initialize and download .NET Framework components'

## ev_008

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[methods] Container execution log showing successful CLI completion without errors: 'Container runtime logs'

## ev_009

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[methods] Docker Desktop for Mac: 'Docker Desktop for Mac (version 20.10+)'

## ev_010

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[methods] Wine: 'Wine to run Windows applications in Linux containers'

## ev_011

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[methods] .NET Framework 4.8: '.NET Framework 4.8 installed and run through Wine'

## ev_012

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[intro] AirdPro V5: 'AirdPro V5 is now available at 2023.7'

## ev_013

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[intro] AirdPro V6: 'AirdPro V6 is now available at 2024.4'

## ev_014

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[intro] ProteoWizard: 'pwiz_bindings_cli.dll from the ProteoWizard project'

## ev_015

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[discussion] No changelog documenting versioning, breaking changes, or runtime behavior differences between AirdPro versions available: '_No changelog found._'

## ev_016

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[methods] Wine initialization and .NET Framework download time documented in methods as >30 minutes, but no quantitative baseline or variance data provided for first-run execution: 'Wine needs to initialize and download .NET Framework components, taking more than 30 minutes'

## ev_017

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[discussion] Sample vendor mass spectrometry raw file location, format, and size not specified in provided section text; required as concrete input for run-cli.sh execution: '[No vendor raw file source provided in section]'
