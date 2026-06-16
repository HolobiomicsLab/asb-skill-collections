# Evaluation Strategy

## Direct Checks

- file_exists: README.md or equivalent documentation in github:NLeSC__MAGMa repository root
- contains_substring: README text includes at least one of the named components ('emetabolomics_site', 'job', 'joblauncher', 'pubchem', 'magmaweb')
- format_is: output manifest is a valid JSON or YAML structured record with fields 'name', 'role', and 'source_path' for each component entry
- row_count_equals: output manifest lists exactly 5 components (or documents if fewer are actually present in README with explicit naming)

## Expert Review

- Verify that extracted component roles and source paths accurately reflect the documented responsibilities and locations stated in the README (requires domain knowledge of MAGMa architecture)
- Assess whether any components are missing from the manifest despite being named and described in the README (completeness check)
