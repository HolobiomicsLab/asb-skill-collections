# SciTask Card: Reconstruct the Wine-mediated CLI conversion run and verify first-run initialisation behaviour

- Task ID: `task_002`
- Schema version: `0.18.0`
- Created at: `2026-06-15T14:04:46.383725+00:00`
- Source package: `/Users/nothiasl/git/AgenticScienceBuilder/outputs/asbb_pilot/coll_aird/synthesized_package`
- Domain: `mass-spectrometry / metabolomics`
- Subtask categories: `data-processing`, `benchmark-evaluation`
- GitHub: `CSi-Studio/AirdPro`
- Input from: `task_001`
- Quality: Score 2/5 — Coherent: false, placeholder, 6 grounding failures

## Classification

- Task kind: `component_reconstruction`
- Article type: `software-tool`
- Primary domain: `bioinformatics`

## Research Question
Does execution of AirdPro CLI against a vendor mass spectrometry raw file via the airdpro:cli Docker image complete Wine initialization and produce a converted Aird output file?

## Connected Finding
AirdPro converts vendor mass spectrometry files to Aird format; first-run execution requires Wine to initialize and download .NET Framework components, a process documented to take more than 30 minutes.

## Task Description
Execute the AirdPro CLI application within the pre-built airdpro:cli Docker container against a sample vendor mass spectrometry raw file, document the Wine initialization startup time (expected >30 min on first run), and verify successful conversion to an Aird output file.

## Inputs
- airdpro:cli Docker image (pre-built from build step)
- Sample vendor mass spectrometry raw file (e.g., .raw, .d format)
- run-cli.sh execution script from project root

## Expected Outputs
- Aird format output file produced by AirdPro conversion
- Wine startup time log documenting first-run initialization duration (>30 min)
- Container execution log showing successful CLI completion without errors

## Expected Output File

- `output.aird`

## Landmark Outputs

- `wine_startup_diagnostics.log`
- `cli_execution.log`
- `output.aird`

## Tools
- Docker Desktop for Mac
- Wine
- .NET Framework 4.8
- AirdPro V5
- AirdPro V6
- ProteoWizard

## Skills
- vendor-mass-spectrometry-file-format-handling
- aird-format-conversion-and-validation
- docker-container-runtime-execution-and-monitoring
- wine-windows-runtime-initialization-diagnostics
- cli-application-invocation-with-file-io-management
- container-volume-mounting-and-file-persistence

## Workflow Description
1. Launch the airdpro:cli container with volume mounts for input vendor raw data and output directory. 2. Trigger Wine initialization by executing run-cli.sh against a sample vendor mass spectrometry raw file (e.g., .raw format). 3. Monitor and record the first-run Wine startup and .NET Framework component download time. 4. Verify that the Aird conversion process completes and produces a named output Aird file in the mounted output directory. 5. Confirm file integrity by checking file existence, size, and format signature.

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
- No changelog documenting versioning, breaking changes, or runtime behavior differences between AirdPro versions available
- Wine initialization and .NET Framework download time documented in methods as >30 minutes, but no quantitative baseline or variance data provided for first-run execution
- Sample vendor mass spectrometry raw file location, format, and size not specified in provided section text; required as concrete input for run-cli.sh execution

## Domain Knowledge
- Wine initialization on first run involves downloading and configuring .NET Framework components, typically requiring >30 minutes depending on network bandwidth and system load.
- Vendor mass spectrometry raw files (Thermo .raw, Bruker .d, AB Sciex .wiff) require format-specific parsers integrated via ProteoWizard bindings to be successfully converted to the Aird format.
- AirdPro V6 (2024.4) supersedes V5 (2023.7); verify which version is embedded in the pre-built airdpro:cli image to ensure feature compatibility with the input raw file format.
- The Aird output file is a binary format; successful conversion is confirmed by file existence, non-zero size, and absence of error messages in the container execution log.
- Wine running in a Linux Docker container introduces 20-30% performance degradation compared to native Windows execution; CLI mode is lighter-weight than GUI and suitable for batch processing.

## Uncertainty Notes
- This card was generated by the LLM-assisted pipeline and needs scientific expert review.
- Each TracedClaim's evidence_span has been substring-checked against its source section; see logs/llm_calls.jsonl and capsules/<task_id>/quality_report.json for groundedness results.
- Synthesis grounding: the following tools/outputs were NOT found in the source paper and are inferred — verify before use: Docker Desktop for Mac, Wine, .NET Framework 4.8, AirdPro V5, AirdPro V6, Wine startup time log documenting first-run initialization duration (>30 min), Container execution log showing successful CLI completion without errors.

## Evidence Snippets
- `ev_001` from `agent2_synthesis` (agent2_traced): [intro] Does execution of AirdPro CLI against a vendor mass spectrometry raw file via the airdpro:cli Docker image complete Wine initialization and produce a converted Aird output file?: 'AirdPro is a GUI client for conversion from vendor files to Aird files'
- `ev_002` from `agent2_synthesis` (agent2_traced): [other] AirdPro converts vendor mass spectrometry files to Aird format; first-run execution requires Wine to initialize and download .NET Framework components, a process documented to take more than 30 minutes.: 'AirdPro is a GUI client for conversion from vendor files to Aird files. Wine needs to initialize and download .NET Framework components, taking more than 30 minutes'
- `ev_003` from `agent2_synthesis` (agent2_traced): [methods] airdpro:cli Docker image (pre-built from build step): 'CLI Version (For batch processing tasks)'
- `ev_004` from `agent2_synthesis` (agent2_traced): [methods] Sample vendor mass spectrometry raw file (e.g., .raw, .d format): 'File conversion example ./run-cli.sh -i data/input.raw -o data/output.mzML'
- `ev_005` from `agent2_synthesis` (agent2_traced): [methods] run-cli.sh execution script from project root: './run-cli.sh -i data/input.raw -o data/output.mzML'
- `ev_006` from `agent2_synthesis` (agent2_traced): [intro] Aird format output file produced by AirdPro conversion: 'AirdPro is a GUI client for conversion from vendor files to Aird files'
- `ev_007` from `agent2_synthesis` (agent2_traced): [methods] Wine startup time log documenting first-run initialization duration (>30 min): 'Wine needs to initialize and download .NET Framework components'
- `ev_008` from `agent2_synthesis` (agent2_traced): [methods] Container execution log showing successful CLI completion without errors: 'Container runtime logs'
- `ev_009` from `agent2_synthesis` (agent2_traced): [methods] Docker Desktop for Mac: 'Docker Desktop for Mac (version 20.10+)'
- `ev_010` from `agent2_synthesis` (agent2_traced): [methods] Wine: 'Wine to run Windows applications in Linux containers'
- `ev_011` from `agent2_synthesis` (agent2_traced): [methods] .NET Framework 4.8: '.NET Framework 4.8 installed and run through Wine'
- `ev_012` from `agent2_synthesis` (agent2_traced): [intro] AirdPro V5: 'AirdPro V5 is now available at 2023.7'
- `ev_013` from `agent2_synthesis` (agent2_traced): [intro] AirdPro V6: 'AirdPro V6 is now available at 2024.4'
- `ev_014` from `agent2_synthesis` (agent2_traced): [intro] ProteoWizard: 'pwiz_bindings_cli.dll from the ProteoWizard project'
- `ev_015` from `agent2_synthesis` (agent2_traced): [discussion] No changelog documenting versioning, breaking changes, or runtime behavior differences between AirdPro versions available: '_No changelog found._'
- `ev_016` from `agent2_synthesis` (agent2_traced): [methods] Wine initialization and .NET Framework download time documented in methods as >30 minutes, but no quantitative baseline or variance data provided for first-run execution: 'Wine needs to initialize and download .NET Framework components, taking more than 30 minutes'
- `ev_017` from `agent2_synthesis` (agent2_traced): [discussion] Sample vendor mass spectrometry raw file location, format, and size not specified in provided section text; required as concrete input for run-cli.sh execution: '[No vendor raw file source provided in section]'

## Evaluation Strategy
### Direct Checks
- verify file airdpro:cli Docker image exists in build artifact repository
- verify file run-cli.sh exists in package inputs or repository root
- verify file sample vendor mass spectrometry raw file (e.g., .raw, .d, .wiff format) is accessible as input
- script_runs: execute run-cli.sh with sample MS raw file in airdpro:cli container and capture stdout/stderr logs
- contains_substring: Wine initialization logs contain evidence of .NET Framework download/setup activity
- file_exists: verify converted Aird output file (.aird or .aird.gz) is created in expected output directory
- value_in_range: if result_wine_startup_time is logged, verify value is >30 min (parameter-sensitive to container overhead and network conditions)
- file_format_is: verify output file format matches Aird specification (robust to compression variant)

### Expert Review
- Examine Wine initialization logs to confirm .NET Framework 4.8 components were downloaded and installed
- Inspect converted Aird output file for structural integrity and compliance with Aird format specification
- Assess whether first-run initialization time documentation aligns with observed >30 min threshold and is reproducible across runs

## Review Questions
- Is the research question correctly identified and scoped?
- Does the connected finding have enough supporting evidence?
- Which artifacts are required before this can become an executable benchmark task?
- What direct, visual, textual, or expert-review checks should be used for evaluation?

## Execution Profile
- **Compute tier:** medium

## Methodology Summary
1. Prepare Docker container with airdpro:cli image and mount vendor raw file input directory and Aird output directory as volumes.
2. Execute run-cli.sh script with input vendor raw file path, capturing container stderr/stdout to log Wine initialization and framework download activity.
3. Record elapsed time from container start to first Wine prompt or .NET Framework component completion message.
4. Allow CLI conversion process to complete; monitor for successful Aird file generation in output directory.
5. Validation: confirm Aird output file exists with non-zero size, Wine startup time is ≥30 min on first run, and container exit code is 0 with no error messages in execution log.

## Workflow Ports

**Inputs:**

- `docker_image` — airdpro:cli Docker image ← `task_001/cli_image`
- `vendor_raw_file` — Sample vendor mass spectrometry raw data file
- `cli_script` — run-cli.sh execution script

**Outputs:**

- `aird_output` — Converted Aird format output file
- `wine_startup_log` — Wine initialization timing and startup diagnostics
- `execution_log` — Container execution and CLI operation log

## Provenance

- **Source kind:** github
- **Synthesized from:** `github:CSi-Studio__AirdPro`
- **Synthesized at:** 2026-06-15T14:09:39+00:00

## Extraction Quality
- Score: 2/5
- Coherent: false
- Placeholder detected: true
- Groundedness failures (6):
  - finding: evidence_span not found in section 'other' (value='AirdPro converts vendor mass spectrometry files to Aird form', span='AirdPro is a GUI client for conversion from vendor files to ')
  - tools[2]: evidence_span not found in section 'methods' (value='.NET Framework 4.8', span='.NET Framework 4.8 installed and run through Wine')
  - missing_information[1]: evidence_span not found in section 'methods' (value='Wine initialization and .NET Framework download time documen', span='Wine needs to initialize and download .NET Framework compone')
  - missing_information[2]: evidence_span not found in section 'discussion' (value='Sample vendor mass spectrometry raw file location, format, a', span='[No vendor raw file source provided in section]')
  - research_question: evidence_span references 'intro' section but span text is generic capability description, not specific answer to CLI+Docker+Wine completion question
  - expected_outputs[2]: evidence_span 'Container runtime logs' is generic placeholder, not article-specific evidence
- Notes: This card exhibits significant grounding failures and semantic incoherence. The research_question asks a specific technical question about CLI+Docker+Wine behavior, but the evidence_span only describes AirdPro's generic GUI-to-CLI capability without addressing containerization, Wine initialization, or Docker specifics. The finding's evidence_span is truncated and located in a non-existent 'other' section. Multiple inputs and outputs rely on generic placeholders ('CLI Version', 'Container runtime logs') rather than concrete, article-specific references. Critical task parameters are under-specified: (1) no vendor raw file source/format/size provided; (2) wine >30 min threshold cited as 'documented' but no quantitative baseline or system configuration bounds; (3) unclear which AirdPro version (V5 vs V6) is embedded in the pre-built image, affecting vendor format parser availability. The task is well-structured methodologically but severely hampered by weak evidentiary grounding and missing operational details. Recommend: (1) re-anchor all evidence_spans to concrete article sections with full quote inclusion; (2) replace generic tool/output descriptions with specific identifiers (Docker image tag, test file URL, log format spec); (3) provide explicit Wine >30 min baseline with system config and variance bounds; (4) clarify AirdPro version in pre-built image and justify vendor raw file choice.

---

*Card produced by **AgenticScienceBuilder (ASB)** — heuristic + LLM-assisted extraction from a research artifact. See the `ro-crate-metadata.json` in this capsule for full provenance.*
