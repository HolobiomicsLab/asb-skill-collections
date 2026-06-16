# Workflow Challenge: `coll_aird_workflow`


> AirdPro is a containerized mass spectrometry data conversion tool that converts vendor files to Aird format using Docker and Wine to enable cross-platform deployment on macOS, Linux, and Windows. The system architecture employs multi-stage Docker builds with .NET Framework 4.8 and ProteoWizard integration, supporting both GUI and CLI modes.

**Mode:** `actual`  
**Reproducibility tier:** `type-checked`

## Mission

Reproduce the methodology of the source paper as faithfully as possible using the steps below. Where a step's reproducibility tier is `bypassed`, `manual-only`, or `experimental`, use the cached output declared in its resumption contract; do not attempt to re-execute.

## Tier promise

_Every step has typed I/O ports declared; executable optional. Filesystem presence check + type-port resolution._

## Instructions

Reproduce the 3-step workflow below. Honor each step's IO contract; produce the files listed under 'Final expected outputs'.

## Background

This documentation describes AirdPro, a GUI and command-line application for converting vendor mass spectrometry files to Aird format, implemented in C# on .NET Framework 4.8 using pwiz_bindings_cli.dll from ProteoWizard. The deployment approach uses Docker containers with Wine to enable execution on non-Windows platforms (macOS and Linux). The system supports multiple image variants: a Windows native version, Linux/macOS Wine-based versions, a lightweight CLI variant, and a development variant. First-run initialization requires Wine to download and configure .NET Framework components, a process documented to require more than 30 minutes. The architecture includes multi-stage Dockerfile builds, systemd service integration for Linux, X11 display forwarding for GUI support on non-Windows systems, and configurable resource allocation (8GB+ RAM recommended). Data persistence is managed through volume mounting of local directories to container paths (/data for input/output, /logs for application logs). The documentation provides platform-specific setup instructions for Ubuntu/Debian, CentOS/RHEL/Fedora, and macOS systems, configuration guidance for X11 and Docker networking, and troubleshooting procedures for common deployment issues including permission errors, display problems, memory constraints, and Wine initialization failures.

## Research questions

- What is the multi-stage Docker build process that produces the airdpro:cli image from a Ubuntu 22.04 base with Wine environment?
- Does execution of AirdPro CLI against a vendor mass spectrometry raw file via the airdpro:cli Docker image complete Wine initialization and produce a converted Aird output file?
- What are the documented compressed size ranges for each of the four AirdPro Docker image variants (cli, dev, linux, windows)?

## Methods overview

Invoke the build-docker.sh script to trigger Docker's multi-stage build pipeline targeting the runtime-cli stage. Download and configure the Ubuntu 22.04 base image, then install Wine and all required Linux dependencies for Windows application support. Initialize the Wine environment and install .NET Framework 4.8 within the Wine prefix so that compiled C# binaries can execute. Compile the AirdPro application using the .NET SDK during the build stage, then copy the CLI executable into the runtime-cli final image. Verification: Query docker images to confirm airdpro:cli exists and report its size; confirm the reported size falls within 6–7 GB range. Prepare Docker container with airdpro:cli image and mount vendor raw file input directory and Aird output directory as volumes. Execute run-cli.sh script with input vendor raw file path, capturing container stderr/stdout to log Wine initialization and framework download activity. Record elapsed time from container start to first Wine prompt or .NET Framework component completion message. Allow CLI conversion process to complete; monitor for successful Aird file generation in output directory. Validation: confirm Aird output file exists with non-zero size, Wine startup time is ≥30 min on first run, and container exit code is 0 with no error messages in execution log. Build all four Docker image variants (cli, dev, linux, windows) using multi-stage Dockerfile with --target flags. Query uncompressed and compressed image sizes using Docker API (`docker inspect`, `docker system df`). Convert byte measurements to gigabytes and benchmark against documented ranges from methods section. Generate structured verification report with image name, measured size, documented range, and pass/fail status. Validation: each image's compressed size must fall within its documented range (±10% tolerance for minor variations in dependencies and build artifacts).

**Domain:** bioinformatics

## Claims to address (CLAIM_VALIDATION rubric)
Your output should make each binding claim checkable:
- **(finding)** AirdPro V5 is available at version 2023.7. _[grounded: airdpro_system]_
- **(finding)** AirdPro V6 is available at version 2024.4. _[grounded: airdpro_system]_
- **(finding)** AirdPro is a GUI client for conversion from vendor files to Aird files. _[grounded: airdpro_system]_
- **(finding)** AirdPro is written in C#. _[grounded: airdpro_system]_
- **(finding)** AirdPro is based on pwiz_bindings_cli.dll from the ProteoWizard project. _[grounded: airdpro_system]_
- **(finding)** AirdPro is opensource under the MulanPSL2 license. _[grounded: airdpro_system]_
- **(finding)** AirdPro is a Windows desktop application based on .NET Framework 4.8. _[grounded: airdpro_system]_
- **(finding)** macOS does not natively support .NET Framework.
- **(finding)** AirdPro can run on macOS through Docker + Wine technology. _[grounded: airdpro_system]_
- **(finding)** The Wine + Docker solution for AirdPro uses Wine to run Windows applications in Linux containers. _[grounded: airdpro_system]_
- **(finding)** macOS 10.15+ (Catalina or later) is required for AirdPro deployment. _[grounded: airdpro_system]_
- **(finding)** Docker Desktop for Mac version 20.10+ is required for AirdPro deployment. _[grounded: airdpro_system]_
- **(finding)** A minimum of 8GB available RAM is required for AirdPro deployment on macOS. _[grounded: airdpro_system]_
- **(finding)** A minimum of 20GB available disk space is required for AirdPro deployment. _[grounded: airdpro_system]_
- **(finding)** XQuartz is required for GUI display support in AirdPro on macOS. _[grounded: airdpro_system]_
- **(finding)** The AirdPro Docker build process downloads an Ubuntu base image. _[grounded: airdpro_system]_
- **(finding)** The AirdPro Docker build process installs .NET Framework 4.8. _[grounded: airdpro_system]_
- **(finding)** Wine initialization and .NET Framework downloads can take more than 30 minutes on first run. _[grounded: comp_wine]_
- **(finding)** 20-30% performance degradation occurs when running AirdPro through Wine. _[grounded: airdpro_system]_
- **(finding)** Wine needs to initialize and download .NET Framework components. _[grounded: comp_wine]_
- **(finding)** AirdPro is a mass spectrometry data analysis tool. _[grounded: airdpro_system]_
- **(finding)** AirdPro supports Windows, Linux, and macOS through containerized deployment. _[grounded: airdpro_system]_
- **(finding)** Docker version 20.10 or later is required for AirdPro deployment. _[grounded: airdpro_system]_
- **(finding)** Docker Compose version 2.0 or later is optional for AirdPro deployment. _[grounded: airdpro_system]_
- **(finding)** Minimum 8GB RAM is required for AirdPro deployment. _[grounded: airdpro_system]_
- **(finding)** At least 20GB free disk space is required for AirdPro deployment. _[grounded: airdpro_system]_
- **(finding)** Multi-core processor with 4+ cores is recommended for AirdPro deployment. _[grounded: airdpro_system]_
- **(finding)** Windows 10/11, macOS 10.15+, or Linux distributions are supported platforms for AirdPro. _[grounded: airdpro_system]_
- **(finding)** Docker Desktop for Windows is required for Windows-based AirdPro deployment. _[grounded: airdpro_system]_
- **(finding)** Docker Desktop for Mac is required for macOS-based AirdPro deployment. _[grounded: airdpro_system]_
- **(finding)** Docker Engine or Docker Desktop is required for Linux-based AirdPro deployment. _[grounded: airdpro_system]_
- **(finding)** Dockerfile uses a multi-stage build strategy with build and runtime stages.
- **(finding)** The macOS runtime for AirdPro is based on Ubuntu 22.04. _[grounded: airdpro_system]_
- **(finding)** Windows Native image variant is approximately 4-5GB in size.
- **(finding)** Linux/macOS Wine image variant is approximately 8-10GB in size. _[grounded: comp_wine]_
- **(finding)** CLI version of AirdPro is approximately 6-7GB in size. _[grounded: airdpro_system]_
- **(finding)** Development version of AirdPro is approximately 9-11GB in size. _[grounded: airdpro_system]_
- **(finding)** Docker Desktop version 20.10 or later is required for Linux deployment. _[grounded: comp_docker_desktop]_
- **(finding)** Debian 10 (Buster) is a supported Linux distribution for AirdPro deployment. _[grounded: airdpro_system]_
- **(finding)** x86_64 (AMD64) architecture is required for Linux-based AirdPro deployment. _[grounded: airdpro_system]_
- **(finding)** Minimum 8GB RAM is required for Linux-based AirdPro deployment. _[grounded: airdpro_system]_
- **(finding)** At least 20GB disk space is required for Linux-based AirdPro deployment. _[grounded: airdpro_system]_
- **(finding)** Wine + Docker solution uses Docker containers to provide isolated Linux runtime environment. _[grounded: comp_wine]_
- **(finding)** Wine serves as a Windows application compatibility layer in the Docker solution. _[grounded: comp_wine]_
- **(finding)** XQuartz is an X11 server for macOS used for GUI display. _[grounded: comp_xquartz]_
- **(finding)** .NET Framework 4.8 is installed and run through Wine in the Docker solution. _[grounded: comp_wine]_
- **(finding)** Current version of AirdPro is 1.0.0 as of December 2024. _[grounded: airdpro_system]_

**Speculative claims (excluded from scoring):**
- **(finding)** Performance may not match native Windows environments when running AirdPro through Wine and Docker. _[grounded: airdpro_system]_
- **(finding)** The first run of AirdPro requires longer initialization time. _[grounded: airdpro_system]_

## Sanctioned method substitutions
Using any of these instead of the source method is **not penalized**:
- Use CLI version for batch processing to reduce resource usage
- Use Linux/macOS Wine version as alternative to Windows native version

## Invariants (must not change)
Changing any of these **is** a failure regardless of openness:
- Wine solution cannot guarantee identical performance and functionality as native Windows environments
- XQuartz is required for GUI display support on macOS
- Stable internet connection required for first run
- Complex network configurations may require additional setup

## Steps

### Step `task_001`
- Title: Reconstruct the Docker multi-stage build pipeline producing the airdpro:cli image
- Task kind: `component_reconstruction`
- Task: Execute the multi-stage Dockerfile build process to produce the airdpro:cli Docker image from Ubuntu 22.04 + Wine base, then verify the image exists and matches the expected ~6–7 GB size metric.
- Inputs:
  - Build-docker.sh script and Dockerfile multi-stage configuration from AirdPro project root directory
  - System with Docker Engine version 20.10 or later installed and running
- Expected outputs:
  - airdpro:cli Docker image, verified to exist in local Docker image registry with reported size metric in the range 6–7 GB
  - Build log output confirming successful multi-stage build completion with no fatal errors
- Tools: AirdPro V5, Docker Desktop for Mac, Wine, .NET Framework 4.8, Docker Compose
- Landmark output files: Dockerfile (source file confirming multi-stage structure), docker build output log (showing Ubuntu download, Wine installation, .NET Framework installation steps)

### Step `task_002`
- Depends on: `task_001`
- Title: Reconstruct the Wine-mediated CLI conversion run and verify first-run initialisation behaviour
- Task kind: `component_reconstruction`
- Task: Execute the AirdPro CLI application within the pre-built airdpro:cli Docker container against a sample vendor mass spectrometry raw file, document the Wine initialization startup time (expected >30 min on first run), and verify successful conversion to an Aird output file.
- Inputs:
  - airdpro:cli Docker image (pre-built from build step)
  - Sample vendor mass spectrometry raw file (e.g., .raw, .d format)
  - run-cli.sh execution script from project root
- Expected outputs:
  - Aird format output file produced by AirdPro conversion
  - Wine startup time log documenting first-run initialization duration (>30 min)
  - Container execution log showing successful CLI completion without errors
- Tools: Docker Desktop for Mac, Wine, .NET Framework 4.8, AirdPro V5, AirdPro V6, ProteoWizard
- Landmark output files: wine_startup_diagnostics.log, cli_execution.log, output.aird
- Primary expected artifact: `output.aird`

### Step `task_003`
- Depends on: `task_001`
- Title: Implement a Docker image size audit across all four airdpro image variants
- Task kind: `component_reconstruction`
- Task: After building all four Docker image variants (airdpro:cli, airdpro:dev, airdpro:linux, airdpro:windows) using the provided Dockerfile, programmatically query each image's compressed size via the Docker API and verify that each falls within its documented metric range (cli ~6–7 GB, dev ~9–11 GB, linux ~8–10 GB, windows ~4–5 GB). Produce a size-verification report.
- Inputs:
  - AirdPro project repository with Dockerfile and multi-stage build configuration
  - Docker system with Docker Engine version 20.10 or higher installed and running
  - Documented image size metrics from the methods section (cli ~6–7 GB, dev ~9–11 GB, linux ~8–10 GB, windows ~4–5 GB)
- Expected outputs:
  - Structured verification report (JSON or CSV) listing each image variant, its measured compressed size in GB, documented target range, and pass/fail verification status
- Tools: AirdPro V5, Docker (docker build, docker inspect, docker system df), Dockerfile (multi-stage build with --target flag)
- Landmark output files: docker_build.log, image_sizes_raw.csv, image_size_verification_report.json
- Primary expected artifact: `image_size_verification_report.json`

## Final expected outputs

- `Aird format output file produced by AirdPro conversion` (type: file, tolerance: hash)
- `Wine startup time log documenting first-run initialization duration (>30 min)` (type: file, tolerance: hash)
- `Container execution log showing successful CLI completion without errors` (type: file, tolerance: hash)
- `Structured verification report (JSON or CSV) listing each image variant, its measured compressed size in GB, documented target range, and pass/fail verification status` (type: file, tolerance: hash)

## How your attempt will be scored

ASB defines seven rubrics in `workflow_rubric.py` (STEP_ORDERING, INTERMEDIATE_FIDELITY, END_TO_END_OUTPUT, TOOL_SELECTION, EFFICIENCY, CLAIM_VALIDATION, ADVERSARIAL_TRAP_AVOIDANCE). Which of them bind for *this* challenge depends on the tier and openness below.

### Tier evaluation profile

**Evaluator:** automated — filesystem presence + type-port resolution; END_TO_END_OUTPUT with declared per-output tolerance.
**Binding rubrics:** STEP_ORDERING, END_TO_END_OUTPUT (typed/tolerance), TOOL_SELECTION, CLAIM_VALIDATION.

### Openness stance

**Openness: closed — reproduction-first.** The deterministic rubrics above bind. A different method is acceptable ONLY if it appears under *Sanctioned method substitutions*; outputs are compared with the declared tolerance. Different is wrong here only when it departs from the sanctioned set or breaks an invariant.

## Workflow characterisation

_Suter et al. 2025 (DOI 10.1016/j.future.2025.107974)._

- **Coupling:** loose

- **Composition modularity:** hierarchical

- **Abstraction level:** intermediate

- **Orchestration planning:** static

- **Data transport:** file

- **Characterisation confidence:** inferred


## Submission

Produce two artifacts in your output directory:

1. The output files at the paths declared under **Final expected outputs**.
2. An `attempt.json` matching the schema below.
3. _(Optional)_ `attempt_metrics.json` with `wall_time_s`, `total_tokens`, `cost_usd` for the EFFICIENCY rubric.

### `attempt.json` schema

```json
{
  "workflow_id": "coll_aird_workflow",
  "agent_order": [
    "task_001",
    "task_002",
    "task_003"
  ],
  "intermediate_outputs": {
    "task_001": {
      "<output_name>": "<locator>"
    },
    "task_002": {
      "<output_name>": "<locator>"
    },
    "task_003": {
      "<output_name>": "<locator>"
    }
  },
  "final_outputs": {
    "Aird format output file produced by AirdPro conversion": "<locator>",
    "Wine startup time log documenting first-run initialization duration (>30 min)": "<locator>",
    "Container execution log showing successful CLI completion without errors": "<locator>",
    "Structured verification report (JSON or CSV) listing each image variant, its measured compressed size in GB, documented target range, and pass/fail verification status": "<locator>"
  },
  "chosen_tools": {
    "task_001": "<tool_name>",
    "task_002": "<tool_name>",
    "task_003": "<tool_name>"
  }
}
```

---
_Generated by `asb workflow-challenge` (see ASB docs/superpowers/specs/2026-05-12-workflow-evaluation-and-reviewer-ui-design.md)._
