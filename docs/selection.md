# Offline selection

`asbb search`, the MCP search tools, the collection's `bin/search_skills.py`,
and `bin/semantic_search.py --mode keyword` use the same selector. The package
imports `asb_skill_collections/asb_skill_index.py`; the standalone scripts embed
that module verbatim and require only the standard library for retrieval.

## Rule and measured choice

The default is `package`, identified as `asb-keyword` version `1.0.0`. It splits
the query into lowercase alphanumeric terms, removes its domain-neutral
stopwords and terms shorter than three characters, and scores each row by term
occurrences in its name, description, tools and techniques. A term occurring in
the name receives three additional points. Repeated query terms retain their
historical weight. This is lexical retrieval, not a probability or a measure of
scientific suitability.

The previous `router` rule uses unique ASCII terms of at least two characters,
counts token overlap in names, descriptions and tools, and adds two points for
an exact tool-name match. Both rules use the same resolver, field builder,
filters, result schema and ordering: descending score, then ascending slug,
then collection to disambiguate equal slugs.

The default was selected using 22 independently labelled queries from the
repository's documentation at `600f4a5dc84c5c22762bd5156f08716e31635b0e`. Labels
were frozen before scoring; neither vocabulary nor weights were tuned to them.
The criterion was highest precision at 1, then precision at 3, retaining the
package rule on a tie.

| Rule | Precision at 1 | Precision at 3 | Answer in first 3 |
| --- | ---: | ---: | ---: |
| Original package | 22/22 (100%) | 22/66 (33.33%) | 22/22 |
| Original router | 20/22 (90.91%) | 21/66 (31.82%) | 21/22 |
| Unified package | 22/22 (100%) | 22/66 (33.33%) | 22/22 |

Precision at *k* is the number of relevant returned slots divided by
`queries × k`; missing slots count as irrelevant. Each query has one documented
answer, so precision at 3 has a ceiling of one third. The last column reports
the distinct, often more useful question of whether that answer is in the first
three results.

The labels and source lines are in
[`tests/fixtures/selector_queries.json`](../tests/fixtures/selector_queries.json).
They cover all 21 workflow `When to use` descriptions and one README example.
The leaf examples in the cited guides name tools or candidate sets, without a
unique answer slug, so they were not assigned invented labels. These figures
measure agreement with documented workflow choices, not skill-selection quality
on independent user queries or scientific execution. Separate parity tests cover
skills, workflows, filters, no matches and unrelated scientific domains.

## Results and filters

Every keyword result has the same dictionary shape across the four surfaces.
Alongside `name`, `description`, `tools` and `techniques`, it contains:

| Field | Meaning |
| --- | --- |
| `selector` | `{name: "asb-keyword", version: "1.0.0", rule: "package"}` |
| `collection` | Resolved collection and version, such as `metabolomics/v2` |
| `target`, `slug` | Index kind and the original unqualified slug |
| `qualified_slug` | `collection/target/slug`, avoiding cross-collection collisions |
| `matched_fields` | Source field names mapped to the matched query terms |
| `score` | Numeric lexical score, ordered highest first |
| `filters` | Normalised `technique`, `tool`, `edam` and effective `max_tools` |
| `fallback` | `keyword` for a direct request; `keyword-after-semantic` after an unavailable semantic result |

Technique and tool filters match complete names without case sensitivity. EDAM
filters match an operation/topic IRI substring. Workflow `member_tools` and leaf
`tools` feed the same tool accessor, including explanations. By default skills
advertising more than 25 tools are excluded, preserving the package's registry
guard; workflows and tool records are exempt. An empty query browses or filters
the index; nonempty queries containing only discarded tokens return no matches.
Results with no lexical match are never filled with unrelated candidates.

The router's normal text output retains readable source paths and adds a JSON
explanation. Use `--json` to obtain the full shared dictionaries. Its no-match
exit status remains 1, with an empty `results` array in JSON mode; `asbb search`
retains its existing successful-query exit status of 0 for an empty array.

## Commands and temporary compatibility option

From the collection root:

```bash
python bin/search_skills.py --query "untargeted LC-MS/MS annotation" --target workflows --json -k 3
python bin/semantic_search.py --collection . --target workflows --mode keyword \
  --query "untargeted LC-MS/MS annotation" --k 3
```

From inside `workflows/`, call the collection's canonical script:

```bash
python ../bin/semantic_search.py --collection . --target workflows --mode keyword \
  --query "untargeted LC-MS/MS annotation" --k 3
```

The resolver accepts both locations for `skills`, `workflows` and `tools`. It
also accepts a flat `workflows_index.json` in a standalone unit. The historical
`workflows/bin/semantic_search.py` copy is outside this unification and retains
its old behaviour; use the collection-level script shown above. Semantic
embedding computation and its result schema remain outside this keyword
contract.

The `router` scoring option is deprecated and retained for one release after
this change. It uses the shared resolver and explanation contract; it does not
restore historical path bugs, missing fields or unqualified results.

```bash
python bin/search_skills.py --query "annotate spectra" --selector router --json
python bin/semantic_search.py --collection . --query "annotate spectra" --mode keyword --selector router
ASB_SELECTOR_RULE=router asbb search "annotate spectra" --collection metabolomics
```

MCP search tools and `asb_skill_index.search` accept `selector="router"`.
An explicit selector parameter takes precedence over `ASB_SELECTOR_RULE`.
Unset that environment option to use the measured default. The CLI parser is
unchanged, so its explicit compatibility option is the environment variable.

## Regeneration

Refresh the canonical script and the eight pack copies through the generator:

```bash
python scripts/router_shape.py --scripts-only collections/metabolomics/v2 packs/metabolomics/*/
```

`--scripts-only` does not move leaves, regenerate indexes or rewrite `SKILL.md`.
The byte-identity test covers both canonical standalone scripts and all eight
pack routers, and fails if any embedded source differs from the package module.
