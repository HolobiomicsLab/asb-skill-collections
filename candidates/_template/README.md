# Curator candidacy template

To file a candidacy:

```bash
cp candidates/_template/candidate.template.yaml candidates/<your-github-handle>.yaml
# Edit candidates/<your-github-handle>.yaml — fill in orcid + proof_publications
git checkout -b candidacy/<your-github-handle>
git add candidates/<your-github-handle>.yaml
git commit -m "candidacy: <Your Name> (intended collections: <list>)"
git push -u origin candidacy/<your-github-handle>
gh pr create --title "Curator candidacy: <Your Name>" --body "..."
```

`vet-curator.yml` runs on the PR and posts an identity-verification report. The
maintainers in `MAINTAINERS.md` make the final call.

## Pre-flight checklist

Before opening the PR, make sure:

1. Your ORCID public profile lists your GitHub URL in "Websites & Social Links"
   (`https://orcid.org/<your-orcid>` → edit → add `https://github.com/<your-handle>`)
2. Each `proof_publications` DOI resolves to a paper whose author list
   includes your ORCID (the action checks via OpenAlex)
3. For Lead Curator candidacy, you also need an ORCID employment entry
   matching the institutional email domain you'll list in candidacy YAML.
