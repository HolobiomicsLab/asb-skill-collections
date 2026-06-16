# Evaluation Strategy

## Direct Checks

- verify file exists: output PNG or PDF treemap file in expected location
- file_format_is: treemap output is valid PNG or PDF (byte-for-byte magic number check)
- script_runs: R script executing qc_summary() aggregation, per-status ion count/percentage computation, and treemap rendering completes without error
- contains_substring: rendered treemap PNG/PDF file size > 10 KB (confirms non-trivial graphical content generated)
- expert_review: treemap visual structure matches vignette exemplar — Greens palette applied, geom_treemap() and geom_treemap_text() layers present, legend absent as specified

## Expert Review

- treemap aesthetic and layout match the vignette reference (Greens color scheme, text labels readable, tile proportions reflect per-status ion percentages correctly)
- per-status ion counts and percentages computed from qc_summary() data.table are numerically consistent with source filtering pipeline state
