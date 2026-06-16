# Evidence Snippets

## ev_001

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[intro] What is the multi-stage Docker build process that produces the airdpro:cli image from a Ubuntu 22.04 base with Wine environment?: 'AirdPro is a GUI client for conversion from vendor files to Aird files. AirdPro is written in C# and is based on pwiz_bindings_cli.dll from the ProteoWizard project.'

## ev_002

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[intro] The document describes that AirdPro is built using Docker with Wine to run the C#-based application in Linux containers, leveraging .NET Framework 4.8 and pwiz_bindings_cli.dll from ProteoWizard, but the specific multi-stage Dockerfile build steps and image size metrics are not detailed in the provided text.: 'AirdPro is written in C# and is based on pwiz_bindings_cli.dll from the ProteoWizard project.'

## ev_003

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[methods] Build-docker.sh script and Dockerfile multi-stage configuration from AirdPro project root directory: 'Build all images (first build may take longer)
./build-docker.sh'

## ev_004

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[methods] System with Docker Engine version 20.10 or later installed and running: 'Docker Desktop for Mac (version 20.10+)'

## ev_005

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[methods] airdpro:cli Docker image, verified to exist in local Docker image registry with reported size metric in the range 6–7 GB: 'CLI Version (For batch processing tasks)
Size: ~6-7GB'

## ev_006

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[methods] Build log output confirming successful multi-stage build completion with no fatal errors: 'Build process explanation:
- Download Ubuntu base image
- Install Wine and dependencies
- Initialize Wine environment
- Install .NET Framework 4.8
- Compile AirdPro application'

## ev_007

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[methods] Docker Desktop for Mac: 'Docker Desktop for Mac (version 20.10+)'

## ev_008

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[methods] Wine: 'Wine to run Windows applications in Linux containers'

## ev_009

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[methods] .NET Framework 4.8: '.NET Framework 4.8 installed and run through Wine'

## ev_010

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[methods] Docker Compose: 'Docker Compose configuration'

## ev_011

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[discussion] No changelog documenting Docker build process, versioning, or layer structure changes: '_No changelog found._'
