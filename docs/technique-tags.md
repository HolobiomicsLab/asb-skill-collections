# Technique tags

Technique tags are tags by mention: they name the analytical platform that the
leaf's context uses. They are deterministic retrieval metadata, not assertions
that a paper used only that platform or that every procedure performs acquisition.
The declared vocabulary is in `scripts/technique_rules.yaml`.

## Preview and receipt

Run the tagger from the tooling checkout. The default is a dry run: it prints
per-tag counts and the numbers of tagged and untagged leaves without modifying
the collection.

```bash
python scripts/tag_techniques.py \
  --collection <domain checkout>/collections/<domain>/<version> \
  --rules scripts/technique_rules.yaml \
  --report <evidence directory>/technique-tags.json
```

The receipt records input and rules digests, counts, and the rule and field that
fired for every leaf. Use `--only CE-MS,direct-infusion-MS` to restrict evaluation
or writing to a subset. Unselected tags already present in a collection are kept.

## Human review packet

Generate one Markdown file per selected tag with seeded random examples and,
when the investigation evidence is available, its spot-check slugs:

```bash
python scripts/tag_techniques.py \
  --collection <domain checkout>/collections/<domain>/<version> \
  --rules scripts/technique_rules.yaml \
  --only CE-MS,direct-infusion-MS --sample 20 --seed 45045 \
  --out <evidence directory>/review-packet
```

`--spot-check-evidence <techniques.json>` selects another investigation receipt.
Review the matched excerpts before adopting low-recall tags.

## Write collection content

After review, add `--write` to update `metadata.techniques` in each leaf and
`techniques` in its index row. Values are sorted and restricted to the declared
vocabulary. The operation is idempotent and leaves other file bytes unchanged.
Keep the JSON receipt with the change.

A write on a released collection is a `release content:` change on the domain
repository, not a tooling-only update. Maintainers review and commit the changed
collection content and regenerate its receipt through the release process. The
tagger does not commit, publish, or modify release records itself.
