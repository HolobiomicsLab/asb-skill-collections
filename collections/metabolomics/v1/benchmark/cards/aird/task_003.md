# SciTask Card: Implement a Docker image size audit across all four airdpro image variants

- Task ID: `task_003`
- Schema version: `0.18.0`
- Created at: `2026-06-15T14:04:46.383725+00:00`
- Source package: `/Users/nothiasl/git/AgenticScienceBuilder/outputs/asbb_pilot/coll_aird/synthesized_package`
- Domain: `mass-spectrometry / metabolomics`
- Subtask categories: `data-processing`, `benchmark-evaluation`
- GitHub: `CSi-Studio/AirdPro`
- Input from: `task_001`
- Quality: Score 2/5 — Coherent: false, 3 grounding failures

## Classification

- Task kind: `component_reconstruction`
- Article type: `software-tool`
- Primary domain: `bioinformatics`

## Research Question
What are the documented compressed size ranges for each of the four AirdPro Docker image variants (cli, dev, linux, windows)?

## Connected Finding
The provided section text does not contain documented compressed size metrics or ranges for any Docker image variants (cli, dev, linux, windows).

## Task Description
After building all four Docker image variants (airdpro:cli, airdpro:dev, airdpro:linux, airdpro:windows) using the provided Dockerfile, programmatically query each image's compressed size via the Docker API and verify that each falls within its documented metric range (cli ~6–7 GB, dev ~9–11 GB, linux ~8–10 GB, windows ~4–5 GB). Produce a size-verification report.

## Inputs
- AirdPro project repository with Dockerfile and multi-stage build configuration
- Docker system with Docker Engine version 20.10 or higher installed and running
- Documented image size metrics from the methods section (cli ~6–7 GB, dev ~9–11 GB, linux ~8–10 GB, windows ~4–5 GB)

## Expected Outputs
- Structured verification report (JSON or CSV) listing each image variant, its measured compressed size in GB, documented target range, and pass/fail verification status

## Expected Output File

- `image_size_verification_report.json`

## Landmark Outputs

- `docker_build.log`
- `image_sizes_raw.csv`
- `image_size_verification_report.json`

## Tools
- AirdPro V5
- Docker (docker build, docker inspect, docker system df)
- Dockerfile (multi-stage build with --target flag)

## Skills
- docker-image-build-and-inspection
- containerized-application-deployment-validation
- artifact-size-measurement-and-range-verification
- multi-stage-dockerfile-interpretation

## Workflow Description
1. Execute the multi-stage Docker build process via `docker build --target runtime-cli`, `docker build --target runtime-dev`, `docker build --target runtime-linux`, and `docker build --target runtime-windows` to produce all four image variants. 2. Query each built image using `docker inspect --format='{{.Size}}'` to retrieve the uncompressed image size in bytes. 3. Query the compressed size of each image stored on disk using `docker system df` or equivalent Docker API calls to determine the actual storage footprint. 4. Convert byte sizes to gigabytes and compare each against the documented range (cli 6–7 GB, dev 9–11 GB, linux 8–10 GB, windows 4–5 GB). 5. Generate a structured verification report listing image name, measured size (GB), documented range, and pass/fail status for each variant.

## Available Artifacts
| Path | Role | Indexable |
|---|---|---|
| `figures/AIR.png` | figure | False |
| `figures/AIR_01.png` | figure | False |
| `figures/AirdManager.png` | figure | False |
| `figures/AirdPro.png` | figure | False |
| `figures/AirdProLogo.png` | figure | False |
| `figures/AirdProTrans.png` | figure | False |
| `figures/AirdPro_ 2.png` | figure | False |
| `figures/AirdPro_ 3.png` | figure | False |
| `figures/Arrows.png` | figure | False |
| `figures/CleanErrors.png` | figure | False |
| `figures/CleanFinished.png` | figure | False |
| `figures/Computation.png` | figure | False |
| `figures/Connected.png` | figure | False |
| `figures/Conversion.png` | figure | False |
| `figures/ConversionCenter.png` | figure | False |
| `figures/Help.png` | figure | False |
| `figures/MetaboLights.jpg` | figure | False |
| `figures/Proteomexchange.png` | figure | False |
| `figures/SearchEngine.png` | figure | False |
| `paper.md` | main_article | True |

## Missing Information
- No changelog found.

## Domain Knowledge
- Docker uncompressed image size (reported by `docker inspect --format='{{.Size}}'`) differs from compressed disk storage footprint; comparisons must account for compression algorithms applied by the storage driver (overlay2, aufs, etc.).
- A multi-stage Dockerfile produces a single final image per target, but intermediate build stages are cached separately; only the final stage's layer stack contributes to the reported image size.
- The documented size ranges (~6–7 GB for CLI, ~8–10 GB for Linux, ~9–11 GB for dev, ~4–5 GB for Windows) refer to compressed storage; uncompressed in-memory size will be larger.
- Docker size measurements via `docker system df` reflect the unique layers stored on disk, not the sum of all image layers (due to layer sharing across images and base image reuse).

## Uncertainty Notes
- This card was generated by the LLM-assisted pipeline and needs scientific expert review.
- Each TracedClaim's evidence_span has been substring-checked against its source section; see logs/llm_calls.jsonl and capsules/<task_id>/quality_report.json for groundedness results.
- Synthesis grounding: the following tools/outputs were NOT found in the source paper and are inferred — verify before use: Docker (docker build, docker inspect, docker system df), Dockerfile (multi-stage build with --target flag), Structured verification report (JSON or CSV) listing each image variant, its measured compressed size in GB, documented target range, and pass/fail verification status.

## Evidence Snippets
- `ev_001` from `agent2_synthesis` (agent2_traced): [intro] What are the documented compressed size ranges for each of the four AirdPro Docker image variants (cli, dev, linux, windows)?: 'AirdPro is a GUI client for conversion from vendor files to Aird files'
- `ev_002` from `agent2_synthesis` (agent2_traced): [intro] The provided section text does not contain documented compressed size metrics or ranges for any Docker image variants (cli, dev, linux, windows).: '_No examples found._'
- `ev_003` from `agent2_synthesis` (agent2_traced): [methods] AirdPro project repository with Dockerfile and multi-stage build configuration: 'Dockerfile uses an optimized build strategy: 1. **Build Stage**: Compile application using .NET Framework SDK 2. **macOS Runtime**: Based on Ubuntu 22.04, pre-configured with Wine and .NET Framework'
- `ev_004` from `agent2_synthesis` (agent2_traced): [methods] Docker system with Docker Engine version 20.10 or higher installed and running: 'Docker Desktop for Mac (version 20.10+)'
- `ev_005` from `agent2_synthesis` (agent2_traced): [methods] Documented image size metrics from the methods section (cli ~6–7 GB, dev ~9–11 GB, linux ~8–10 GB, windows ~4–5 GB): 'Image Variants: 1. Windows Native (`airdpro:windows`): Size: ~4-5GB. 2. Linux/macOS Wine (`airdpro:linux`, `airdpro:macos`): Size: ~8-10GB. 3. CLI Version (`airdpro:cli`): Size: ~6-7GB. 4.'
- `ev_006` from `agent2_synthesis` (agent2_traced): [methods] Structured verification report (JSON or CSV) listing each image variant, its measured compressed size in GB, documented target range, and pass/fail verification status: 'Image Variants: 1. Windows Native (`airdpro:windows`): Size: ~4-5GB. 2. Linux/macOS Wine (`airdpro:linux`, `airdpro:macos`): Size: ~8-10GB. 3. CLI Version (`airdpro:cli`): Size: ~6-7GB. 4.'
- `ev_007` from `agent2_synthesis` (agent2_traced): [methods] Docker (docker build, docker inspect, docker system df): 'Build all images (first build may take longer)'
- `ev_008` from `agent2_synthesis` (agent2_traced): [methods] Dockerfile (multi-stage build with --target flag): 'Dockerfile uses an optimized build strategy'
- `ev_009` from `agent2_synthesis` (agent2_traced): [discussion] No changelog found.: '_No changelog found._'

## Evaluation Strategy
### Direct Checks
- verify file exists for each of four built Docker images (airdpro:cli, airdpro:dev, airdpro:linux, airdpro:windows) in local Docker daemon or registry
- retrieve reported compressed size (in GB) for airdpro:cli image via 'docker images' or 'docker inspect' command; value_in_range [6, 7]
- retrieve reported compressed size (in GB) for airdpro:dev image via 'docker images' or 'docker inspect' command; value_in_range [9, 11]
- retrieve reported compressed size (in GB) for airdpro:linux image via 'docker images' or 'docker inspect' command; value_in_range [8, 10]
- retrieve reported compressed size (in GB) for airdpro:windows image via 'docker images' or 'docker inspect' command; value_in_range [4, 5]
- script_runs: docker build succeeds without error for all four image variants using Dockerfile(s) from github:CSi-Studio__AirdPro

### Expert Review
- verify that reported image sizes are consistent with documented compression method and base layers (Wine, .NET Framework 4.8, ProteoWizard bindings) across all four variants
- assess whether any image size falls outside its documented range and evaluate whether the discrepancy reflects a documentation error, image configuration drift, or legitimate variation in build artifact

## Review Questions
- Is the research question correctly identified and scoped?
- Does the connected finding have enough supporting evidence?
- Which artifacts are required before this can become an executable benchmark task?
- What direct, visual, textual, or expert-review checks should be used for evaluation?

## Execution Profile
- **Compute tier:** medium

## Methodology Summary
1. Build all four Docker image variants (cli, dev, linux, windows) using multi-stage Dockerfile with --target flags.
2. Query uncompressed and compressed image sizes using Docker API (`docker inspect`, `docker system df`).
3. Convert byte measurements to gigabytes and benchmark against documented ranges from methods section.
4. Generate structured verification report with image name, measured size, documented range, and pass/fail status.
5. Validation: each image's compressed size must fall within its documented range (±10% tolerance for minor variations in dependencies and build artifacts).

## Workflow Ports

**Inputs:**

- `dockerfile_and_project` — AirdPro project repository with Dockerfile and build configuration ← `task_001/cli_image`
- `docker_engine` — Docker Engine version 20.10+ with daemon running
- `documented_size_spec` — Image size specification (cli ~6–7 GB, dev ~9–11 GB, linux ~8–10 GB, windows ~4–5 GB)

**Outputs:**

- `size_verification_report` — Image size verification report with measured vs. documented ranges and pass/fail status

## Provenance

- **Source kind:** github
- **Synthesized from:** `github:CSi-Studio__AirdPro`
- **Synthesized at:** 2026-06-15T14:09:54+00:00

## Extraction Quality
- Score: 2/5
- Coherent: false
- Placeholder detected: false
- Groundedness failures (3):
  - finding: evidence_span '_No examples found._' is a placeholder, not actual text from 'intro' section
  - inputs[2]: evidence_span truncated and incomplete; actual text in 'methods' section ends abruptly ('4.') suggesting evidence was cut off or mismatched
  - expected_outputs[0]: evidence_span reuses truncated text from inputs[2]; same evidence section doesn't describe the expected output format (JSON/CSV verification report)
- Notes: This card exhibits fundamental coherence problems. The research_question asks 'what are the documented compressed size ranges' (assuming they exist in the source material), but the finding explicitly states these ranges are NOT documented in the intro section. This creates an unanswerable scenario. Additionally, the task objective shifts from 'finding documented ranges' to 'verifying measured sizes against ranges', which are different tasks. The evidence_spans for inputs[2] and expected_outputs[0] are truncated and identical, indicating copy-paste errors. The card would benefit from: (1) clarifying whether sizes are documented in the article or only in the task_description; (2) splitting this into two separate tasks if both retrieval and measurement are intended; (3) fixing truncated evidence spans; (4) aligning the research_question to match the actual task (measurement+verification rather than documentation retrieval).

---

*Card produced by **AgenticScienceBuilder (ASB)** — heuristic + LLM-assisted extraction from a research artifact. See the `ro-crate-metadata.json` in this capsule for full provenance.*
