# Evidence Snippets

## ev_001

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[intro] What are the documented compressed size ranges for each of the four AirdPro Docker image variants (cli, dev, linux, windows)?: 'AirdPro is a GUI client for conversion from vendor files to Aird files'

## ev_002

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[intro] The provided section text does not contain documented compressed size metrics or ranges for any Docker image variants (cli, dev, linux, windows).: '_No examples found._'

## ev_003

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[methods] AirdPro project repository with Dockerfile and multi-stage build configuration: 'Dockerfile uses an optimized build strategy: 1. **Build Stage**: Compile application using .NET Framework SDK 2. **macOS Runtime**: Based on Ubuntu 22.04, pre-configured with Wine and .NET Framework'

## ev_004

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[methods] Docker system with Docker Engine version 20.10 or higher installed and running: 'Docker Desktop for Mac (version 20.10+)'

## ev_005

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[methods] Documented image size metrics from the methods section (cli ~6–7 GB, dev ~9–11 GB, linux ~8–10 GB, windows ~4–5 GB): 'Image Variants: 1. Windows Native (`airdpro:windows`): Size: ~4-5GB. 2. Linux/macOS Wine (`airdpro:linux`, `airdpro:macos`): Size: ~8-10GB. 3. CLI Version (`airdpro:cli`): Size: ~6-7GB. 4.'

## ev_006

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[methods] Structured verification report (JSON or CSV) listing each image variant, its measured compressed size in GB, documented target range, and pass/fail verification status: 'Image Variants: 1. Windows Native (`airdpro:windows`): Size: ~4-5GB. 2. Linux/macOS Wine (`airdpro:linux`, `airdpro:macos`): Size: ~8-10GB. 3. CLI Version (`airdpro:cli`): Size: ~6-7GB. 4.'

## ev_007

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[methods] Docker (docker build, docker inspect, docker system df): 'Build all images (first build may take longer)'

## ev_008

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[methods] Dockerfile (multi-stage build with --target flag): 'Dockerfile uses an optimized build strategy'

## ev_009

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[discussion] No changelog found.: '_No changelog found._'
