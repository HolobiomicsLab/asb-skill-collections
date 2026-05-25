# Gold-Tier Claims

Gold-tier claims are a human-verified subset of the silver-tier claims.

## How to populate

In your `reviews/<paper-doi>.yaml` attestation file, add the field:

```yaml
verified_claim_ids:
  - claim_001
  - claim_003
```

The `asb collection promote` command will populate `gold_truth.jsonl` from your attestation's `verified_claim_ids[]` list.
