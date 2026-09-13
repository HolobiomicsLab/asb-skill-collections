# How offline skill selection works

The checkout CLI (`asbb search`), MCP search tools, the collection router and
`bin/semantic_search.py --mode keyword` share one selector. The package source is
`asb_skill_collections/asb_skill_index.py`; the standalone scripts carry the same
module so an installed collection can search without importing the checkout.

The behaviour described here is the integrated release behaviour: the package
module is the single source and the standalone scripts embed it verbatim, so the
four surfaces cannot drift. The worked examples below were executed against the
integration branch; source revision `600f4a5dc` predates the selector fixes and
is cited only as the revision the frozen labels were taken from.

## Ranking rule

The default selector is `asb-keyword` version `1.0.0`, rule `package`. It:

1. splits the query into lowercase alphanumeric terms;
2. removes domain-neutral stopwords and terms shorter than three characters;
3. counts occurrences in `name`, `description`, `tools` and `techniques`; and
4. adds three points when a term occurs in `name`.

Repeated query terms retain their weight. The score is therefore a lexical
ranking value, not a probability or a measure of scientific suitability.
Results are ordered by decreasing score, then increasing slug, then collection.
Thus equal scores are a real tie and the slug ordering is only a deterministic
tie-break, not evidence that the first method is better.

The older `router` rule remains as a temporary compatibility option. It uses
unique ASCII terms of at least two characters, token overlap over name,
description and tools, and a two-point exact tool-name bonus. Select it only
when reproducing an older result; the measured default is `package`.

## Reading an explanation

Every keyword hit has the same explanation fields on all four surfaces:

| Field | Meaning |
| --- | --- |
| `selector` | Selector name, version and active rule. |
| `collection` | Resolved collection/version, for example `metabolomics/v2`. |
| `target`, `slug` | Index kind and its original unqualified identifier. |
| `qualified_slug` | `collection/target/slug`; use this to avoid collisions. |
| `matched_fields` | Fields mapped to the query terms found in each field. |
| `score` | Lexical score used for ordering. Compare it only within one request. |
| `filters` | Effective `technique`, `tool`, `edam` and `max_tools` constraints. |
| `fallback` | `keyword`, or `keyword-after-semantic` when semantic retrieval was unavailable. |

Technique and tool filters match complete names without case sensitivity. EDAM
filters match an operation/topic IRI substring. Workflow `member_tools` and leaf
`tools` are treated consistently. By default, leaf skills advertising more than
25 tools are excluded; workflows and tool records are exempt. An empty query
browses or filters the index. A non-empty query containing only discarded terms
returns no match, and the selector does not fill the list with unrelated items.

## Three executed examples

The following commands were run from `collections/metabolomics/v2` on the
integration branch, and reproduce there. The `jq` projection keeps the real output readable.

An end-to-end request should search workflows first:

```bash
python3 -B bin/search_skills.py --collection . --target workflows --technique LC-MS --query "untargeted LC-MS/MS annotation" --json -k 3 | jq -r '.results[] | [.qualified_slug, .score, (.matched_fields | keys | join(","))] | @tsv'
```

```text
metabolomics/v2/workflows/untargeted-lcmsms-annotation  12.0  description,member_tools,name
metabolomics/v2/workflows/compound-class-annotation     6.0  description,name
metabolomics/v2/workflows/fbmn-annotation-propagation   5.0  description
```

A single-step request searches leaf skills:

```bash
python3 -B bin/search_skills.py --collection . --target skills --query "spectral library matching" --json -k 3 | jq -r '.results[] | [.qualified_slug, .score, (.matched_fields | keys | join(","))] | @tsv'
```

```text
metabolomics/v2/skills/spectral-library-matching-evaluation  15.0  description,name
metabolomics/v2/skills/spectral-library-annotation-matching  14.0  description,name
metabolomics/v2/skills/spectral-library-matching-gnps        14.0  description,name
```

The last two results tie at 14. Their order is alphabetical by slug; it does not
distinguish their scientific relevance.

A second tie is visible in a retention-time request:

```bash
python3 -B bin/search_skills.py --collection . --target skills --query "retention time prediction" --json -k 3 | jq -r '.results[] | [.qualified_slug, .score, (.matched_fields | keys | join(","))] | @tsv'
```

```text
metabolomics/v2/skills/retention-time-prediction-chromatography  17.0  description,name
metabolomics/v2/skills/retention-time-prediction-from-structures 16.0  description,name,tools
metabolomics/v2/skills/retention-time-prediction-optimization    16.0  description,name
```

## Asking for a different result

State the analytical platform, named tool or operation when the first result is
too broad. Change `--target` between `workflows`, `skills` and `tools`; add an
exact `--technique`, `--tool` or `--edam` filter; rephrase the task with a
discriminating term; or inspect more candidates with `-k`. Once chosen, request
or open the `qualified_slug` rather than relying on its position.

For example, adding the named tool GNPS changed the candidate set:

```bash
python3 -B bin/search_skills.py --collection . --target skills --tool GNPS --query "spectral library matching" --json -k 3 | jq -r '.results[] | [.qualified_slug, .score, (.filters.tool // ""), (.matched_fields | keys | join(","))] | @tsv'
```

```text
metabolomics/v2/skills/spectral-library-annotation-matching  14.0  gnps  description,name
metabolomics/v2/skills/spectral-library-matching-gnps        14.0  gnps  description,name
metabolomics/v2/skills/spectral-library-matching             13.0  gnps  description,name
```

The router accepts `--selector router`; package callers and MCP accept the same
selector value, while the checkout CLI can use `ASB_SELECTOR_RULE=router`. An
explicit selector takes precedence over the environment variable.

## Output shape and exit status

The router's normal text output keeps readable source paths and adds a JSON
explanation; `--json` returns the full shared dictionaries. Its no-match exit
status is 1, with an empty `results` array in JSON mode. `asbb search` keeps its
successful-query exit status of 0 for an empty array.

## Commands

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

The resolver accepts both locations for `skills`, `workflows` and `tools`, and a
flat `workflows_index.json` in a standalone unit. The historical
`workflows/bin/semantic_search.py` copy is outside this unification and keeps its
old behaviour — use the collection-level script above. Semantic embedding
computation and its result schema stay outside this keyword contract.

The `router` rule is deprecated and retained for one release after this change.
It uses the shared resolver and explanation contract; it does not restore
historical path bugs, missing fields or unqualified results.

```bash
python bin/search_skills.py --query "annotate spectra" --selector router --json
python bin/semantic_search.py --collection . --query "annotate spectra" --mode keyword --selector router
ASB_SELECTOR_RULE=router asbb search "annotate spectra" --collection metabolomics
```

MCP search tools and `asb_skill_index.search` accept `selector="router"`. The CLI
parser is unchanged, so its explicit compatibility option is the environment
variable.

## Regeneration

Refresh the canonical script and the eight pack copies through the generator:

```bash
python scripts/router_shape.py --scripts-only collections/metabolomics/v2 packs/metabolomics/*/
```

`--scripts-only` does not move leaves, regenerate indexes or rewrite `SKILL.md`.
The byte-identity test covers both canonical standalone scripts and all eight
pack routers, and fails if any embedded source differs from the package module.

## Measured limit

The default was compared with the previous rule using 22 labels frozen from
documentation at `600f4a5dc84c5c22762bd5156f08716e31635b0e`: all 21 workflow
“When to use” descriptions and one README example, each with one documented
answer. The package rule retrieved 22/22 labels at rank 1; the older router rule
retrieved 20/22. At rank 3 the package result is 22/66, whose ceiling is one
third because there is only one labelled answer per query.

The **22/22 precision-at-1 result measures agreement with frozen documentation
labels only**. It is not an evaluation of real user queries, independent
relevance judgements, scientific execution or method quality. The frozen labels
and source lines live in `tests/fixtures/selector_queries.json`.
