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

The default selector is `asb-keyword` version `1.0.0`, rule `router`. It:

1. splits the query into lowercase ASCII alphanumeric terms;
2. removes domain-neutral stopwords and terms shorter than two characters, and
   keeps each remaining term once;
3. scores one point per distinct term that reaches `name`, `description` or
   `tools`; and
4. adds two points when a term is exactly a tool name.

A repeated query term is counted once, so the score is a count of distinct
matched terms, not a frequency. It is a lexical ranking value, not a
probability or a measure of scientific suitability.

### Order, and what breaks a tie

Results are ordered by

1. decreasing score;
2. decreasing number of query terms that reached the candidate's **`name`**;
3. decreasing share of the candidate's **`name`** those terms are;
4. increasing slug; then
5. increasing collection.

Steps 2 and 3 are the tie-break. They only ever act inside a block of
equal-score candidates, and together they are the one relevance-bearing part of
the ordering: a query term that reaches a skill's title is stronger evidence
that the skill is *about* that term than the same term appearing somewhere in
its body, and a title that *is* the query is more precisely that thing than a
title which qualifies it with a platform or a variant. Step 2 is read straight
out of the `matched_fields` explanation each hit already carries; step 3 divides
it by the number of terms in `name`. Both are computed once per returned hit.

The tie-break does not resolve every tie, and it is not meant to. Candidates
that match the same terms in equally-long names survive into step 4 (see the
third example below). Slug and collection are the final deterministic fallback
so that a result set is reproducible; they carry no relevance. Where they
decide, the first result is not evidence that the first method is better.

The `package` rule remains as a temporary compatibility option. It uses repeated
Unicode alphanumeric terms of at least three characters, counts occurrences in
`name`, `description`, `tools` and `techniques`, and adds three points when a
term occurs in `name`. It keeps its historical score/slug order with no name
tie-break, so an older result reproduces exactly. Select it only for that; the
measured default is `router`.

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
metabolomics/v2/workflows/untargeted-lcmsms-annotation  4.0  description,member_tools,name
metabolomics/v2/workflows/compound-class-annotation     4.0  description,name
metabolomics/v2/workflows/lipidomics-lcms-annotation    4.0  description,member_tools,name
```

Five workflows score 4.0 here, so the title tie-break decides the block:
`untargeted` and `annotation` both reach the first workflow's name, one query
term reaches each of the next two, and none reaches the last two. Under a
slug-only order `compound-class-annotation` came first, which is the documented
wrong answer for this query.

A single-step request searches leaf skills:

```bash
python3 -B bin/search_skills.py --collection . --target skills --query "spectral library matching" --json -k 3 | jq -r '.results[] | [.qualified_slug, .score, (.matched_fields | keys | join(","))] | @tsv'
```

```text
metabolomics/v2/skills/spectral-library-matching        3.0  description,name
metabolomics/v2/skills/ms-ms-spectral-library-matching  3.0  name
metabolomics/v2/skills/ms-spectral-library-matching     3.0  description,name
```

All three score 3.0 and all three carry the same three query terms in their
names, so the count half of the tie-break cannot separate them. The coverage
half does: the first skill's name *is* those three terms and nothing else, while
the others qualify them with a platform. The equal-score block here holds 84
candidates, and a slug-only order returned
`candidate-neighbourhood-analysis-for-spectral-matching` first — two of the three
terms, in a much longer name, and a different question from the one asked.

A retention-time request shows the whole ladder:

```bash
python3 -B bin/search_skills.py --collection . --target skills --query "retention time prediction" --json -k 3 | jq -r '.results[] | [.qualified_slug, .score, (.matched_fields | keys | join(","))] | @tsv'
```

```text
metabolomics/v2/skills/retention-time-prediction                 3.0  description,name
metabolomics/v2/skills/retention-time-prediction-chromatography  3.0  description,name
metabolomics/v2/skills/retention-time-prediction-from-structures 3.0  description,name,tools
```

Equal score, equal name count; the exact-title skill wins on coverage, and the
last two are equal on coverage as well, so their order is alphabetical by slug
and says nothing about which is scientifically preferable.

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
metabolomics/v2/skills/spectral-library-matching             3.0  gnps  description,name
metabolomics/v2/skills/spectral-library-annotation-matching  3.0  gnps  description,name
metabolomics/v2/skills/spectral-library-matching-annotation  3.0  gnps  description,name
```

The router accepts `--selector package`; package callers and MCP accept the same
selector value, while the checkout CLI can use `ASB_SELECTOR_RULE=package`. An
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

The `package` rule is deprecated and retained for one release after this change.
It uses the shared resolver and explanation contract, and keeps its historical
score/slug order so an older result reproduces exactly.

```bash
python bin/search_skills.py --query "annotate spectra" --selector package --json
python bin/semantic_search.py --collection . --query "annotate spectra" --mode keyword --selector package
ASB_SELECTOR_RULE=package asbb search "annotate spectra" --collection metabolomics
```

MCP search tools and `asb_skill_index.search` accept `selector="package"`. The CLI
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

## What the default was measured on

Two label sets back the default. Both are documentation- or benchmark-derived,
not independent user queries; the limits are stated at the end of this section.

### 1. The 22 frozen documentation labels

22 labels frozen from documentation at
`600f4a5dc84c5c22762bd5156f08716e31635b0e`: all 21 workflow “When to use”
descriptions and one README example, each with one documented answer. They live
in `tests/fixtures/selector_queries.json` and are asserted by
`tests/test_selector_keyword_paths.py`.

| Rule and order | P@1 |
| --- | ---: |
| `package`, score then slug | 22/22 |
| `router`, score then slug | 20/22 |
| **`router`, score then name tie-break then slug (the default)** | **22/22** |

The name tie-break repairs both of `router`'s failures on this set. Both were
score ties that the alphabetical fallback lost to a lexically earlier slug, and
in both the documented answer is the only member of its tie block whose *name*
carries the query's discriminating term:

| Label | Tie block | Slug order returned | Name order returns |
| --- | --- | --- | --- |
| `readme_untargeted_lcmsms_annotation` | 3 workflows at 4.0 | `compound-class-annotation` (1 name term) | `untargeted-lcmsms-annotation` (2) |
| `workflow_untargeted_lcmsms_annotation` | 2 workflows at 8.0 | `lipidomics-lcms-annotation` (0 name terms) | `untargeted-lcmsms-annotation` (1) |

This is an n=22 agreement check against frozen documentation, and it is the set
the *previous* default was chosen on. It is kept as a regression guard, not as
the evidence for the default.

### 2. The 326 benchmark-card labels

`collections/metabolomics/v1/links.json` carries 336 promoted benchmark cards;
326 have at least one gold skill present in the corpus. Each card's title is the
query and its `skills` list is the gold set.
`scripts/promote_benchmark_layer.py` writes those labels from the card's own
authored field without importing or calling either scoring rule, so they are not
answers produced by the ranker under test. Card and skill were nonetheless built
from the same paper, so they can share its vocabulary; this probe is therefore
easier than routing a free-form request from a new user.

Hit@1, with the *whole* rank-1 tie block isolated per query. “shipped” resolves
whatever remains tied the way the code does, alphabetically; “random” resolves it
at random, which removes alphabetical luck and is the honest measure of the
ordering's relevance; “still tied” is the fraction of queries whose rank-1 block
survives the rule's own tie-break; lower and upper bound Hit@1 over the best and
worst possible resolution of that residue.

Full query title:

| Corpus | Order | Hit@1 shipped | Hit@1 random | lower | upper | still tied |
| --- | --- | ---: | ---: | ---: | ---: | ---: |
| canonical, 5,859 rows | `package` + slug | 0.3313 | 0.3302 | 0.2914 | 0.3834 | 22.70% |
| canonical, 5,859 rows | `router` + slug | 0.4571 | 0.4565 | 0.3374 | 0.6319 | 51.23% |
| canonical, 5,859 rows | **`router` + title + slug** | **0.4724** | **0.4750** | **0.4479** | **0.5061** | **12.58%** |
| installed unit, 1,478 rows | `package` + slug | 0.4908 | 0.4966 | 0.4601 | 0.5429 | 17.48% |
| installed unit, 1,478 rows | `router` + slug | 0.6074 | 0.6053 | 0.4939 | 0.7454 | 47.24% |
| installed unit, 1,478 rows | **`router` + title + slug** | **0.6534** | **0.6460** | **0.6258** | **0.6656** | **7.67%** |

Query truncated to its first 8 tokens:

| Corpus | Order | Hit@1 shipped | Hit@1 random | lower | upper | still tied |
| --- | --- | ---: | ---: | ---: | ---: | ---: |
| canonical, 5,859 rows | `package` + slug | 0.2883 | 0.2818 | 0.2485 | 0.3313 | 26.38% |
| canonical, 5,859 rows | `router` + slug | 0.3834 | 0.3703 | 0.2515 | 0.5890 | 63.19% |
| canonical, 5,859 rows | **`router` + title + slug** | **0.3988** | **0.3977** | **0.3681** | **0.4387** | **21.17%** |
| installed unit, 1,478 rows | `package` + slug | 0.4509 | 0.4531 | 0.4172 | 0.5031 | 25.46% |
| installed unit, 1,478 rows | `router` + slug | 0.5245 | 0.5216 | 0.3896 | 0.7239 | 56.75% |
| installed unit, 1,478 rows | **`router` + title + slug** | **0.5736** | **0.5757** | **0.5429** | **0.6135** | **14.72%** |

Under a relevance-neutral random tie-break applied identically to both rules and
averaged over 32 seeds, `router` leads `package` by +0.1263 on the canonical
corpus (bootstrap 95% CI [+0.0701, +0.1817]) and by +0.1087 on the installed
unit ([+0.0533, +0.1632]); McNemar is significant at every one of the 32 seeds,
worst p = 0.0038 and 0.0084 respectively. That comparison, not the 22 frozen
labels, is why `router` is the default.

Adding the title tie-break moves `router` a further +0.0185 on the canonical
corpus (95% CI [-0.0060, +0.0432]; 24 queries improved against 1 worsened) and
+0.0407 on the installed unit ([+0.0170, +0.0652]; 32 against 3). The canonical
interval touches zero, so on that corpus the tie-break's gain is suggestive
rather than established; the installed-unit interval does not.

### Why the tie-break is this and not something that resolves every tie

Ten candidate keys were measured against the alphabetical fallback on the same
326 labels, across both corpora and both query lengths: matched-name count, name
coverage, shortest name, shortest description, tool-match count, a name-weighted
field sum, and four lexicographic combinations of those. Two findings decided
the choice.

**Resolving a tie is not the same as deciding it well.** Ordering an equal-score
block by shortest description leaves only 1.5% of canonical queries tied — far
fewer than the shipped key — and yet its Hit@1 under a random residual pick is
0.4663 against the shipped key's 0.4750, and under 8-token truncation it falls
*below* the plain alphabetical fallback it replaced (0.3666 against 0.3703). A
key that resolves ties
without carrying relevance only replaces one arbitrary order with another, so a
low tie rate on its own was not accepted as evidence.

**Both halves of the shipped key were required.** The matched-name count alone
raises canonical Hit@1 slightly more than the full key (0.4788 against 0.4750,
a difference whose 95% CI is [-0.0138, +0.0057] and so is not distinguishable
from zero) but leaves 19.9% and 16.6% of full-title queries tied. Adding the
coverage half cuts that residue to 12.6% and 7.7%, and is significantly better
than the count alone in the arm that matters most for this switch — 8-token
queries against the installed unit, where it gains +0.0173 [+0.0055, +0.0304].
That is the arm where `router` was previously weakest. In the other three arms
the two are not distinguishable ([-0.0138, +0.0057], [-0.0082, +0.0092],
[-0.0126, +0.0138]), so coverage is kept for the tie reduction and for the one
arm where it is measurably better, not on a claim that it helps everywhere.

The shipped ordering still leaves 12.6% of canonical full-title queries tied at
rank 1, and that residue is deliberate: nothing in the index separates those
candidates, and the slug order that resolves them is arbitrary.

### What these numbers do not establish

- **Only metabolomics is measured.** Epigenomics and transcriptomics have no
  index the probe can subset, so the default is not a cross-domain result.
- **Neither label set is an independent user-query set.** The 22 are frozen
  documentation; the 326 are benchmark-card titles that can share a paper's
  vocabulary with the skills they label. Neither is an evaluation of scientific
  execution, method quality or independent relevance judgement.
- **The "decides less often" objection to `router` is answered, not inherited.**
  Ordered by score and slug alone, `router` left 47.2-63.2% of rank-1 blocks
  tied — the reason not to default to it. With the title tie-break it leaves
  7.7-21.2%, below `package`'s 17.5-26.4% in all four arms.
- **The bounds no longer overlap.** In all four arms `router` + title + slug has
  a lower bound above `package`'s upper bound — 0.4479 against 0.3834, 0.6258
  against 0.5429, 0.3681 against 0.3313, and 0.5429 against 0.5031 — so the
  undecided residue can no longer cost `router` the comparison, including under
  the 8-token truncation where it used to.
- The 326-label probe is conditional on the resolvable labels: seven gold slugs
  are absent from the corpus and empty the 10 excluded tasks, so the probe
  cannot say how either rule handles those generic task-level skills.
