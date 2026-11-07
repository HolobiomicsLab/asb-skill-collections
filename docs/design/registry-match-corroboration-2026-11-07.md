# Registry match corroboration measurement, 7 November 2026

## Recommendation

Expose this result as an advisory column, not as a gate. The measured signal
identified four of the five reviewed wrong matches, but it also contradicted 15
of the 89 accepted matches. Its contradiction precision was 28.6% on the tuning
split and 44.4% on the held-out positive split. That is not safe enough to
reject a licence source automatically.

The `corroborated` verdict was more selective: precision was 100% and recall was
64.5% on tuning, and precision was 100% and recall was 66.7% on held-out
positives. It is useful supporting evidence, but absence of corroboration must
not be treated as evidence that a match is wrong.

## Labelled set

The accepted set is every v2 tool whose `license_detection` is
`bioconductor-package` or `bioconda-package` in `tools_index.json`. This
reconstructs all 89 accepted matches: 49 from Bioconductor and 40 from bioconda.
The negative set is the five reviewed exclusions in
`governance/tool_registries.yaml`, giving the expected 94 labelled matches.

For each tool, the corpus comparison text contains the tool record's
`description` when present, every `evidence_spans` value, and every citing paper
title in `derived_from`. The registry comparison text contains `Title` and
`Description` for Bioconductor or `summary` and `description` for bioconda.
Ecosystem hints additionally inspect registry summary, description, home,
development URL, source URL, dependencies, and requirements. No inferred field
or network result is added.

## Signals and verdict

Ecosystem consistency recognises explicit R, Python, conda, Java, and Ruby
commands, URLs, and file extensions. Bioconductor is declared as R. For
bioconda, an ecosystem is assigned only when its package metadata contains an
explicit hint. Missing hints produce `insufficient`, not agreement or
contradiction.

Domain agreement tokenises the two description texts, removes the fixed
stopwords and all tokens derived from the tool and package names, and computes
binary cosine overlap. Removing identity tokens is essential: the exact name
match under evaluation cannot corroborate itself. Each side needs at least
three informative tokens. Otherwise the domain signal is `insufficient`.

The 89 accepted matches are shuffled with seed 48 into 62 tuning positives and
27 held-out positives. All five negatives occur in both splits because five are
too few to split. Consequently, held-out negative recall is not independent;
only the positive side is held out. The threshold is selected on the tuning
split by macro F1 for wrong-match contradiction and accepted-match
corroboration, then contradiction precision, corroboration recall, and the
lower threshold. The selected cosine threshold is 0.021713.

If one signal corroborates while the other contradicts, the combined verdict is
`insufficient`. Otherwise a contradiction wins over missing evidence, a
corroboration wins over missing evidence, and two missing signals remain
`insufficient`.

## Measurement

| Split | Accepted | Wrong | `contradicted` precision | `contradicted` recall | `corroborated` precision | `corroborated` recall | Insufficient |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| Tuning | 62 | 5 | 28.6% (4/14) | 80.0% (4/5) | 100.0% (40/40) | 64.5% (40/62) | 13 |
| Held-out positives | 27 | 5 | 44.4% (4/9) | 80.0% (4/5) | 100.0% (18/18) | 66.7% (18/27) | 5 |

Across all 94 labels, the verdicts are:

- Accepted matches: 58 corroborated, 15 contradicted, and 16 insufficient.
- Wrong matches: `bart`, `ggplot`, `meteor`, and `mist` contradicted; `grid` was
  insufficient because its corpus evidence contains only `grid` and a short
  citing-paper title.

The accepted matches contradicted by the signal were:

- Tuning: `alphatims`, `big-slice`, `ipapy2`, `massspecwavelet`, `neatms`,
  `pairkat`, `psims`, `psm-utils`, `singularity`, and `tqdm`.
- Held-out: `big-scape`, `bigscape`, `metabolabpy`, `msnbase`, and `pyhmmer`.

The large false-contradiction set is the reason not to gate. It largely reflects
sparse corpus spans and descriptions that use different vocabulary even for the
same entity. Ecosystem evidence did catch the R `library(MeTEor)` versus Python
package mismatch, while domain evidence caught four rich-text exclusions. The
one-token `grid` record demonstrates why an explicit insufficient category is
necessary.

## Fixed stopword list

The exact list, also serialised in the measurement JSON, is:

```text
a, about, after, again, against, all, allow, allows, also, am, an, analyses,
analysis, and, any, application, applications, approach, are, as, at, available,
based, be, because, been, before, being, between, both, but, by, can, could,
data, did, do, does, doing, down, during, each, few, for, framework, from,
further, had, has, have, having, he, her, here, hers, herself, him, himself,
his, how, i, if, implementation, in, include, includes, including, inference,
into, is, it, its, itself, just, me, method, methods, more, most, my, myself,
new, no, nor, not, now, of, off, on, once, only, open, or, other, our, ours,
ourselves, out, over, own, package, packages, perform, performed, performs,
provide, provides, same, she, should, so, software, some, source, such, system,
systems, than, that, the, their, theirs, them, themselves, then, there, these,
they, this, those, through, to, too, tool, tools, under, until, up, use, used,
uses, using, version, very, was, we, were, what, when, where, which, while, who,
whom, why, will, with, you, your, yours, yourself, yourselves
```

## Reproduction and artefacts

Run `scripts/corroborate_registry_match.py` with the v2 collection, the registry
governance file, and offline bioconda and Bioconductor JSON snapshots. The
script performs no network access and emits every tool's signals, score,
verdict, and compared texts.

- Machine-readable results:
  `docs/design/registry-match-corroboration-2026-11-07.json`
- Deterministic implementation: `scripts/corroborate_registry_match.py`
- Synthetic signal tests: `tests/test_corroborate_registry_match.py`

This measurement does not modify registry matching or licence derivation.
