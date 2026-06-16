# Evaluation Strategy

## Direct Checks

- verify file exists at github.com/mwang87/GNPS_MASST or equivalent public repository URL
- verify GNPS_MASST repository contains routing logic code (script_runs: clone repository and search for routing/dispatcher functions)
- verify routing logic accepts user-selected domain parameter as input (contains_substring: 'domain' or 'MASST' in routing function signature)
- verify routing logic maps domain selection to at least the six documented applications: microbeMASST, plantMASST, tissueMASST, microbiomeMASST, foodMASST, metadataMASST (output_matches_reference: routing table or conditional logic enumerates all six)
- verify implemented routing logic can be instantiated with a test spectrum and a domain parameter without error (script_runs: execute routing function with valid inputs)

## Expert Review

- assess whether routing logic correctly implements domain-spectrum matching semantics (does microbe spectrum route to microbeMASST, plant to plantMASST, etc.)
- assess whether routing logic gracefully handles edge cases: unrecognized domain, null/missing domain parameter, null/invalid spectrum input
- assess whether routing implementation follows GNPS_MASST architectural conventions and is maintainable for future domain additions
