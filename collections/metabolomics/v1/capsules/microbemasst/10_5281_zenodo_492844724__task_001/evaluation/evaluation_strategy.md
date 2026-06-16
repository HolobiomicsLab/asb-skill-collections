# Evaluation Strategy

## Direct Checks

- verify file README.md exists in github.com/robinschmid/microbe_masst repository
- verify file README.md exists in the domainMASSTs repository (github.com/mwang87/GNPS_MASST or equivalent root repo)
- extract from README.md a structured table or list containing columns: [application_name, live_url, publication_link]; row_count_equals 6 (one per tool: microbeMASST, plantMASST, tissueMASST, microbiomeMASST, foodMASST, metadataMASST)
- field_present: each row must have non-empty application_name matching one of the six known tool names
- field_present: each row must have live_url field with a valid URL format (http:// or https://)
- field_present: each row must have publication_link field (may be empty if tool is not yet published, but field structure must be present)
- verify that all six application names appear exactly once in the extracted table — no duplicates, no missing entries
- robust to whitespace/formatting variations in README rendering across git platforms

## Expert Review

- verify that each live_url actually resolves and serves the advertised web application (human or automated browser check required)
- verify that each publication_link (where provided) is a valid and active DOI, PubMed ID, or persistent URL
- confirm that the table/list structure in README.md is the canonical, current, and complete inventory of domainMASSTs tools — no tools listed elsewhere in README should be missing
