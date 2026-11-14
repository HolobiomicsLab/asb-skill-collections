# Evaluation definitions in the build capsules

## Status

The build capsules hold evaluation definitions only. **No validation of these definitions exists.** None has
been run end to end, none has reference outputs produced or labelled by an expert, no agent result has been
scored against one, and no ranking exists. The counts below describe what the files contain, not what they
have been shown to measure.

The capsules records are prepared and not deposited: the counts are those of the packs generated on 2026-11-13, and a pack rebuilt before deposit replaces them.

## What a definition is

Each capsule is one task derived from one published article. Its `eval.json` names the task, the inputs it
expects, the outputs it expects and the checks to apply to them. A definition is counted **complete** when
it carries the four keys `task_id`, `inputs`, `expected_outputs` and `checks`, at least one check, and no
recorded validation error; otherwise it is **partial**. Complete is a statement about structure. It does not
say that the task can be run, that its inputs can be retrieved, or that its checks can be scored by a
machine. `benchmark-manifest.json` of each record lists the complete definitions and carries this sentence.

## Counts

Checks, unresolved references and input entries are those of the complete definitions. Machine is
every kind other than `expert_review`.

| Domain | Builds | Builds left out | Capsules | Complete | Partial | Checks | Expert review | Machine | Unresolved references | Input entries | With hash | With download hint |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| agentic-ai | 28 | 1 | 195 | 14 | 181 | 100 | 97 | 3 | 56 | 40 | 0 | 3 |
| astronomy | 100 | 0 | 594 | 19 | 575 | 120 | 108 | 12 | 69 | 31 | 0 | 0 |
| epigenomics | 92 | 0 | 666 | 21 | 645 | 129 | 129 | 0 | 93 | 48 | 0 | 1 |
| genomics | 137 | 0 | 1,003 | 39 | 964 | 272 | 266 | 6 | 173 | 96 | 0 | 0 |
| metabarcoding | 29 | 0 | 210 | 14 | 196 | 96 | 87 | 9 | 61 | 38 | 0 | 2 |
| metabolomics | 387 | 4 | 2,714 | 190 | 2,524 | 1,037 | 1,037 | 0 | 738 | 415 | 0 | 12 |
| metagenomics | 116 | 1 | 799 | 35 | 764 | 232 | 228 | 4 | 141 | 81 | 0 | 1 |
| multi-omics | 29 | 0 | 211 | 3 | 208 | 19 | 19 | 0 | 14 | 8 | 0 | 1 |
| proteomics | 28 | 0 | 179 | 3 | 176 | 16 | 16 | 0 | 17 | 5 | 0 | 0 |
| transcriptomics | 447 | 3 | 3,301 | 99 | 3,202 | 678 | 674 | 4 | 405 | 240 | 0 | 8 |
| **Total** | **1,393** | **9** | **9,872** | **437** | **9,435** | **2,699** | **2,661** | **38** | **1,767** | **1,002** | **0** | **28** |

## Readiness

The `readiness` column of `capsules.jsonl` sorts every capsule by what its files contain. It is computed
from the validation label, the evaluation state and the inputs; it is not a validation and not a maturity
grade. **documented**: a validation file is present. **validated**: validation is `clean` or `strict` and the
evaluation definition is partial. **evaluable**: validation is `clean` or `strict` and the evaluation
definition is complete. **executable**: evaluable, with at least one input, every input carrying a content
hash and a download hint, and a certified reproducibility tier.

| Domain | documented | validated | evaluable | executable |
| --- | ---: | ---: | ---: | ---: |
| agentic-ai | 102 | 84 | 9 | 0 |
| astronomy | 309 | 275 | 10 | 0 |
| epigenomics | 239 | 411 | 16 | 0 |
| genomics | 415 | 568 | 20 | 0 |
| metabarcoding | 68 | 132 | 10 | 0 |
| metabolomics | 1,132 | 1,469 | 113 | 0 |
| metagenomics | 313 | 462 | 24 | 0 |
| multi-omics | 83 | 126 | 2 | 0 |
| proteomics | 95 | 83 | 1 | 0 |
| transcriptomics | 1,322 | 1,926 | 53 | 0 |
| **Total** | **4,078** | **5,536** | **258** | **0** |

## How to read them

- 437 of 9,872 capsules (4.4 %) carry a complete definition.
- 2,661 of their 2,699 checks (98.6 %) are of kind `expert_review`: a rubric for a human reader, not a test a program can decide. The other 38 are: `contains_substring` 8, `field_present` 8, `file_exists` 4, `file_format_is` 1, `row_count_equals` 7, `script_runs` 10.
- 0 of the 1,002 input entries carry a content hash and 28 a download hint. The inputs of a task are therefore named, not pinned.
- 1,767 references of the complete definitions are recorded as unresolved in the definitions themselves.
- 9 builds are left out of the records, because a required file is missing or because the screen found a residue it could not remove; their capsules are in no count above.

## What `validation.json` is, and is not

Each capsule also carries a `validation.json`. It records an automated comparison, made when the capsule was
built, between the statements the capsule makes about its article and passages retrieved from that article.
The labels derived from it (`present`, `clean`, `strict`) describe the grounding of the capsule's text in
its source. They are not a validation of the evaluation definition, and they were not reviewed by a person.
Over all capsules: `present` 4,078, `clean` 3,225, `strict` 2,569.

## Using the capsules in an evaluation

- Treat a capsule as a task statement with a rubric. Most checks are rubrics for a human reader or a judge
  model; a program can decide only the few of the other kinds counted above.
- Score a file-existence check on what an attempt produced, not on a workspace that already holds the
  inputs: an input file whose name fits the expected output satisfies the check without any work.
- Inputs are named, not pinned. If you supply a code repository as an input, read it first: a repository
  can hold the article's own results, which turns a reproduction into a lookup.
- A capsule's guide, claims and excerpts can answer the task it poses. Build the statement given to an
  attempt from the question, the objective, the tools and pointers to the inputs only.

## What does not exist

- An end-to-end runnable example with frozen inputs.
- Reference outputs for any task, and expert labels on any output.
- A calibrated judge or a final scoring policy.
- Scored agent results, and therefore any leaderboard.

## Provenance of this card

This file is generated by `scripts/render_evaluation_card.py` from the descriptive files of the packs
(`MANIFEST.json`, `capsules.jsonl`, `benchmark-manifest.json`), packed with tooling commit `cbc2eb14e`. Collection versions the packs describe:

- agentic-ai: 10.5281/zenodo.24122112
- astronomy: 10.5281/zenodo.24122111
- epigenomics: 10.5281/zenodo.24122116
- genomics: 10.5281/zenodo.24122105
- metabarcoding: 10.5281/zenodo.24122109
- metabolomics: 10.5281/zenodo.24122117
- metagenomics: 10.5281/zenodo.24122106
- multi-omics: 10.5281/zenodo.24122110
- proteomics: 10.5281/zenodo.24122102
- transcriptomics: 10.5281/zenodo.24122113
