---
name: massql-query-syntax-and-parameter-optimization
description: Design and refine MassQL query strings to match specific mass spectrometry patterns (isotope ratios, product ions, retention time windows) on a reference dataset before scaling to large repositories. This skill ensures queries capture target analytes while minimizing false positives through iterative parameter tuning.
when_to_use_negative:
- You do not have a reference dataset with known compounds to validate against; use domain knowledge or pilot data collection first.
- The target analytes exhibit highly variable MS fragmentation or isotope patterns across instrument vendors or ionization sources; MassQL is designed to be vendor-agnostic but may require separate query refinement for each instrument class.
- You have already executed a query at scale and are troubleshooting results post-hoc; redesign the query parameters and re-execute rather than applying this skill.
edam_operation: http://edamontology.org/operation_3631
edam_topics:
- http://edamontology.org/topic_0121
- http://edamontology.org/topic_3520
tools:
- name: MassQL
  role: Query language and reference engine for pattern matching in MS data; parses query syntax and executes filtering logic against spectral data
  repo: https://github.com/mwang87/MassQueryLanguage
- name: lark
  role: Python parser library used to transform MassQL query strings into internal parse tree data structures
  repo: https://github.com/lark-parser/lark
- name: pyteomics
  role: Python library for reading MS data files in mzML, mzXML, and MGF formats into memory for query execution
- name: pandas
  role: Data manipulation and filtering library; processes query logic over MS spectra represented as DataFrames
- name: GNPS spectral libraries
  role: Reference MS/MS library used to design and validate MassQL queries on known compounds before scaling
- name: MZmine
  role: Open-source MS data analysis software that has natively adopted and integrated MassQL for query execution
  repo: https://github.com/mzmine/mzmine
provenance:
  source_task_ids:
  - task_001
  source_papers:
  - doi: 10.1038/s41592-025-02660-z
    title: A universal language for finding mass spectrometry data patterns
schema_version: 0.2.0
metadata:
  merge_audit:
    n_source_runs: 2
    source_files:
    - outputs/audit_s41592_full/skills/massql-query-syntax-and-parameter-optimization/SKILL.md
    - outputs/audit_s41592_full/skills/massql-query-syntax-and-parameter-optimization/skill.md
    merged_at: '2026-05-25T07:15:30.958265+00:00'
    merge_kind: slug_match_union
  iri: https://w3id.org/holobiomicslab/asb-skill/massql-query-syntax-and-parameter-optimization@sha256:21941755216584435e5a0ba37a82bad1ce7f68509f0a90c65f110e2c0a86c26d
  related_workflows:
  - benchmark/tasks/audit_haffner_v2/workflow.smk
  - benchmark/tasks/audit_jeong_full/workflow.smk
  - benchmark/tasks/article_878_full_2026-05-10_v5/workflow.smk
  - benchmark/tasks/pesticide_full_2026-05-10_v2/workflow.smk
  - benchmark/tasks/audit_s41592_full/workflow.smk
derived_from:
- doi: 10.1038/s41592-025-02660-z
---

# MassQL Query Syntax and Parameter Optimization

## Summary

Design and refine MassQL query strings to match specific mass spectrometry patterns (isotope ratios, product ions, retention time windows) on a reference dataset before scaling to large repositories. This skill ensures queries capture target analytes while minimizing false positives through iterative parameter tuning.

## When to use

You have a reference MS dataset containing known compounds (e.g., GNPS spectral libraries) and want to define a pattern-matching query (e.g., iron-isotope ratios, characteristic product ions, retention time ranges) that will later be executed at scale across hundreds of millions of spectra. Use this skill to prototype and validate the query syntax and tolerance parameters before deployment.

## When NOT to use

- You do not have a reference dataset with known compounds to validate against; use domain knowledge or pilot data collection first.
- The target analytes exhibit highly variable MS fragmentation or isotope patterns across instrument vendors or ionization sources; MassQL is designed to be vendor-agnostic but may require separate query refinement for each instrument class.
- You have already executed a query at scale and are troubleshooting results post-hoc; redesign the query parameters and re-execute rather than applying this skill.

## Inputs

- MassQL query string (text) specifying MS1/MS2 filter criteria, m/z values, isotope pattern intensities, retention time ranges, charge state, polarity
- Reference mass spectrometry dataset in mzML, mzXML, or MGF format (e.g., GNPS spectral library subset with known compounds)
- Metadata or annotations mapping reference spectra to known compounds

## Outputs

- Validated MassQL query string with optimized tolerance parameters (m/z accuracy, intensity tolerance, RT bounds)
- Result set: MS scan records (scan number, precursor m/z, isotope pattern intensities, retention time) in JSON or CSV format, filtered by the optimized query
- Performance metrics: number of true positives, false negatives, and false positives on reference dataset

## How to apply

Begin by designing a MassQL query string that specifies MS1 or MS2 filter criteria (m/z ranges, isotope pattern intensities, product ion thresholds, retention time windows, charge state, polarity) using the MassQL grammar. Parse the query using the lark parser library into an internal data structure, then execute it against the reference dataset (loaded as pandas DataFrames via pyteomics from mzML/mzXML files) to identify true positives and false negatives. Iterate on key tolerance parameters—such as intensity tolerance (e.g., 25% for isotope pattern peaks), m/z accuracy (e.g., 10 ppm), and retention time bounds—by comparing MassQL results against known compound annotations or orthogonal methods (e.g., ion-identity molecular networking). Once sensitivity and specificity are acceptable on the reference set, the validated query is ready for scaling to the full repository.

## Related tools

- **MassQL** (Query language and reference engine for pattern matching in MS data; parses query syntax and executes filtering logic against spectral data) — https://github.com/mwang87/MassQueryLanguage
- **lark** (Python parser library used to transform MassQL query strings into internal parse tree data structures) — https://github.com/lark-parser/lark
- **pyteomics** (Python library for reading MS data files in mzML, mzXML, and MGF formats into memory for query execution)
- **pandas** (Data manipulation and filtering library; processes query logic over MS spectra represented as DataFrames)
- **GNPS spectral libraries** (Reference MS/MS library used to design and validate MassQL queries on known compounds before scaling)
- **MZmine** (Open-source MS data analysis software that has natively adopted and integrated MassQL for query execution) — https://github.com/mzmine/mzmine

## Examples

```
from lark import Lark; from pyteomics import mzml; import pandas as pd; from massql import main_functions as mql; query_str = 'MS1MZ=163.1 MS2PROD=120 POLARITY=Positive RTMIN=5 RTMAX=10'; parsed = Lark(query_str); results = mql.query_over_mzML(query_str, 'reference_dataset.mzML'); print(f'Matched {len(results)} spectra')
```

## Evaluation signals

- Query returns all (or nearly all) known reference compounds in the reference dataset; sensitivity is high (few false negatives).
- Query returns minimal off-target spectra that do not match the known compound list; specificity is high (few false positives).
- Results from MassQL on the reference dataset match or exceed the hit count and annotation rate from orthogonal methods (e.g., ion-identity molecular networking); agreement validates the query design.
- Tolerance parameters (m/z accuracy, intensity tolerance, RT bounds) are recorded and documented for reproducibility when the query is scaled.
- No edge-case spectra with atypical isotope pattern intensities or fragmentation within the reference set are unexpectedly missed after final parameter selection.

## Limitations

- MassQL has limited capability to leverage multiple consecutive MS spectra from a single chromatographic feature; it evaluates each spectrum independently, which may miss compounds with weak or fragmented isotope patterns.
- Compounds with low-intensity characteristic peaks (e.g., a 54Fe isotope peak below the 25% intensity tolerance threshold) may be missed despite being present in the data; the intensity tolerance is a hard filter.
- Query design is compound-class-specific; a query optimized for siderophores may not generalize to organophosphate esters or other analyte classes without re-parameterization.
- Performance and parameter tuning depend on the quality and representativeness of the reference dataset; biased or incomplete reference sets may lead to suboptimal queries.

## Evidence

- [full_text] we first used the GNPS spectral libraries (which contained 4,533 reference spectra of bile acids) to design and refine MassQL queries: "we first used the GNPS spectral libraries (which contained 4,533 reference spectra of bile acids) to design and refine MassQL queries"
- [full_text] The parsing is done by using the lark Python library and specific Python code to transform a MassQL query to a parse tree: "The parsing is done by using the lark Python library and specific Python code to transform a MassQL query to a parse tree"
- [full_text] The MassQL reference query engine is written in Python and utilizes pyteomics to read open MS data files from mzML, mzXML and MGF formats: "The MassQL reference query engine is written in Python and utilizes pyteomics to read open MS data files from mzML, mzXML and MGF formats"
- [full_text] The query engine itself processes the query over these data frames using the Python pandas library to perform data filtering and manipulations: "The query engine itself processes the query over these data frames using the Python pandas library to perform data filtering and manipulations"
- [full_text] The unique compound that was found using IIMN but not by the MassQL query was missed because the 54Fe peak intensity fell outside of the expected intensity tolerance of 25%: "The unique compound that was found using IIMN but not by the MassQL query was missed because the 54Fe peak intensity fell outside of the expected intensity tolerance of 25%"
- [readme] Lark can parse all context-free languages. To put it simply, it means that it is capable of parsing almost any programming language out there: "Lark can parse all context-free languages. To put it simply, it means that it is capable of parsing almost any programming language out there"
