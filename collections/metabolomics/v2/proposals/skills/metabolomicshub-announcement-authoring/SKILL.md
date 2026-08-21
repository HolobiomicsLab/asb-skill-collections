---
name: metabolomicshub-announcement-authoring
description: Use when publishing a metabolomics dataset into the MetabolomicsHub index
  — building the common-model file, deriving and validating the announcement against
  the right profile, minting an identifier, and submitting a revision whose outcome
  only a polled task reports.
license: CC-BY-4.0
status: hold
metadata:
  tools:
  - MetabolomicsHub
  - mhd-cli
  techniques:
  - LC-MS
  - GC-MS
  repo_url: https://github.com/MetabolomicsHub/mhd-model
  service_url: https://www.metabolomicshub.org/api/submission
  related_skills:
  - metabolomicshub-cross-repository-dataset-search
  license_tier: open
  provenance_tier: repository
  tool_license:
    tier: open
    requires_ack: false
    ref: Apache-2.0
    url: https://github.com/MetabolomicsHub/mhd-model/blob/main/LICENSE
  verified_against:
    package: mhd-model
    api_version: v0.0.1
    observed: '2026-08-21'
schema_version: 0.2.0
---

# metabolomicshub-announcement-authoring

Turn a dataset's metadata into an MHD announcement that the hub will accept, and
find out that it will not before submitting rather than after.

## When this applies

A repository, a consortium partner or a submitter with a large deposit needs a
study to appear in the MetabolomicsHub index. The route is not a web form: it is
a common-model file, an announcement derived from it, a validation pass, an
identifier, and a submitted revision. Each of those has a failure mode of its
own, and two of them are asynchronous.

This is the depositor's side of the hub. Reading the index is a different job.

## The two artefacts, in the order they exist

1. **The MHD common data model file** — the full description of the study:
   samples, assays, protocols, parameters, instruments, publications.
2. **The announcement file** — derived from the model file, and the thing the
   hub actually ingests. It references the model file by URL.

Deriving the second from the first is a command, not an editing task. Writing an
announcement by hand and keeping it consistent with a model file is the mistake
this ordering exists to prevent.

## Procedure

1. **Choose the profile before writing anything.** Two model versions (v0.1,
   v1.0) each carry two profiles: `ms-profile` and `legacy-profile`. The MS
   profile expects structured acquisition metadata; the legacy profile is the
   reduced shape for studies migrated from an existing repository. Both the
   announcement file and the common-model file have their own schema per
   profile, so there are four schemas in play and picking the wrong one produces
   validation errors that read as missing data.
   `GET /v0_1/schemas` returns the profiles the server currently enforces, and
   `GET /v0_1/server-info` reports which is the default. Ask the server; the
   defaults move with releases.

2. **Validate the model file first.**

   ```
   mhd-cli validate mhd <mhd_study_id> <mhd_model_file_path>
   ```

   Fixing the model file after deriving an announcement means deriving again.

3. **Derive the announcement.**

   ```
   mhd-cli create announcement [--output-dir DIR] [--output-filename NAME] \
       <mhd_study_id> <mhd_model_file_path> <target_mhd_model_file_url>
   ```

   The third argument is where the model file *will be* publicly readable. The
   hub checks that URL for accessibility when the announcement is shared, so a
   placeholder or a private link fails at submission rather than at derivation.
   Publish the model file before you submit, not before you derive.

4. **Validate the announcement.**

   ```
   mhd-cli validate announcement [--output-path FILE] <mhd_study_id> \
       <announcement_file_path>
   ```

   Use `--output-path` in any automated pipeline: it writes the result where a
   later step can read it, instead of leaving it in a log.

5. **Mint an identifier in the test lane first.** `POST /v0_1/identifiers`,
   or `MhdClient.get_new_mhd_accession(dataset_repository_identifier, accession_type)`.
   The accepted accession types are `mhd`, `legacy`, `test-mhd`, `test-legacy`
   and `dev`. Do a full dry run on a test accession before requesting a real
   one; identifiers are the part of this process you cannot take back.

6. **Submit the revision, then poll.** `POST /v0_1/datasets/{accession}/announcements`
   is a multipart upload authenticated with an `x-api-token` header, and it
   returns a `taskId` rather than a verdict. The outcome is read from
   `GET /v0_1/datasets/{accession}/tasks/{task_id}`. The shipped client polls it
   for you (ten attempts, five seconds apart); anything you write yourself must
   poll too. A 200 on the upload means the file was accepted for validation, not
   that the dataset was announced.

7. **Record the revision.** Announcements are versioned: every submission takes
   an `announcement_reason` and `GET /v0_1/datasets/{accession}/announcements`
   lists the revisions. The reason string is the only human-readable account of
   why a dataset's public record changed, so write it for someone reading it in
   two years.

## Related outputs from the same model file

`mhd-cli create sdrf` and `mhd-cli create neo4j-input` emit an SDRF table and a
graph-import form of the same study. Both take the model file, so they stay
consistent with the announcement by construction — worth preferring over
exporting from the announcement or from a repository's own metadata.

## Verification

- The model file validates under the same profile the announcement declares.
- `target_mhd_model_file_url` resolves publicly and returns the model file that
  was used to derive the announcement, not a later edit of it.
- The submission task reached a terminal state and was read; the upload's own
  status code was not treated as the result.
- The study appears in the search index under the expected repository, and the
  fields you care about are populated rather than merely present.

## Limitations

- The announcement carries what the model file carried. Fields the source
  repository never recorded stay empty, and the hub cannot infer them; this is
  the origin of the uneven field coverage seen from the search side.
- Identifier minting and submission need an API token issued to a repository.
  A submitter without one goes through their repository, not directly.
- The client and the schemas move together. Pin the `mhd-model` version used for
  a deposit, and re-validate rather than assuming an older announcement still
  conforms.
- The accession types accepted by the client are the five listed above. The
  package README's example passes `test`, which is not among them.
