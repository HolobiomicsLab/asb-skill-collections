# Security policy

## Reporting a vulnerability

Report a vulnerability privately through the GitHub advisory form of this
repository:
<https://github.com/HolobiomicsLab/asb-skill-collections/security/advisories/new>
(Security tab, "Report a vulnerability"). Do not open a public issue, pull
request or discussion about it.

If the form is not available, open an issue that asks the maintainers for a
private contact and leaves out every detail of the vulnerability.

A useful report names:

- the affected file, command, package version or collection version;
- the steps that reproduce the problem;
- what an attacker, or an agent following the content, could do with it;
- whether the problem is already public anywhere.

## Scope

In scope:

- the Python package `asb-skill-collections` (`asb_skill_collections/`): the
  `asbb` command and the `asb-mcp` server;
- the scripts under `scripts/` and the workflows under `.github/workflows/`;
- the helper scripts shipped inside a collection (`collections/<slug>/v<N>/bin/`);
- collection content that causes harm when an agent follows it as written: an
  instruction to run a destructive or data-exfiltrating command, a credential,
  personal data, or a link to a compromised resource.

Not in scope here:

- a skill that misrepresents its source paper, which follows
  [governance/DISPUTE_RESOLUTION.md](governance/DISPUTE_RESOLUTION.md);
- a vulnerability in a third-party tool that a skill describes, which belongs
  to that tool's maintainers.

## Versions

Fixes are made on `main` and ship with the next release of the affected package
or collection. A collection version deposited on Zenodo cannot be changed in
place: a fix there is a new version, and the advisory names the affected
versions.

Conduct matters are covered by [CODE_OF_CONDUCT.md](CODE_OF_CONDUCT.md).
