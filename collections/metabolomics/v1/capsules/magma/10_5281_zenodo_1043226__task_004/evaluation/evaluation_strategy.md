# Evaluation Strategy

## Direct Checks

- verify file exists in github:NLeSC__MAGMa repository at path containing metabolite generation logic (e.g., magma/job or similar job subproject directory)
- file_format_is: identify and confirm format of primary generation-logic artifact (Python source, JSON flowchart, XML call-graph, or annotated text file)
- script_runs: if artifact is executable code, verify that import statements and function definitions parse without syntax error
- field_present: if output is structured (JSON/XML), verify presence of expected keys documenting function call sequence, parameter names, and dependency order for metabolite candidate generation
- contains_substring: verify that documented workflow explicitly references chemo-informatics operations (e.g., 'fragment', 'generate', 'candidate', 'metabolite', 'in silico') — no canonical answer; multiple defensible phrasings acceptable

## Expert Review

- confirm that extracted workflow correctly represents the metabolite-generation stage and does not conflate it with MS annotation or matching stages
- assess whether the documented flowchart/call-graph captures sufficient detail for a computational agent to independently trace metabolite generation; multiple valid levels of abstraction exist
- evaluate whether chemo-informatics operations (functional group rules, fragmentation patterns, reaction templates) are correctly characterized
