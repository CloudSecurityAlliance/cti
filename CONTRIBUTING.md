# Contributing to the CSA CTI (CAVEaT) corpus

This repository is **data, not software**. It holds the Cloud Security Alliance's
CAVEaT corpus — Cloud Adversarial Vectors, Exploits and Threats — as STIX 2.1
JSON objects. There is nothing to build or run; contributing means adding or
correcting JSON.

Read this before opening a pull request. CI enforces the structural half of it
automatically; the first two sections it cannot enforce, and those are the ones
that get submissions rejected.

## 1. Scope — cloud only

CAVEaT covers **cloud** adversarial techniques and their **provider-specific**
mitigations for AWS, Azure and GCP. As `README.md` puts it, this is deliberately
unlike traditional CTI, which "focuses primarily on indicators and general
mitigations across hundreds of different security products."

**In scope:** a technique against cloud infrastructure, control planes, identity
systems, or managed services — paired with remediation expressed as actual
console paths, CLI commands, API calls, or infrastructure-as-code.

**Out of scope**, and the most common reason a PR is closed:

- A vulnerability in a vendor product that happens to run somewhere
  (firewalls, endpoint agents, on-prem management consoles). A CVE alone is not
  a cloud adversarial vector.
- Generic advice — "patch promptly", "enable MFA" — with no provider-specific
  implementation.
- Indicator dumps, IP/hash lists, or feeds.

Hardware-level threats are in scope where they are cloud-relevant: the corpus
carries a technique targeting AMD EPYC, because it undermines confidential
computing in cloud tenancy. The test is *does this change how a cloud environment
is attacked or defended*, not *is it a security bug*.

If you are unsure whether something is in scope, open an issue before writing the
JSON.

## 2. Every claim needs a source, and the source must actually say it

This is a security-relevant public record. People make patching decisions from
it, so a wrong detail is worse than a missing one.

- Every object needs at least one entry in `external_references`. CI enforces
  the presence of a citation; it cannot check that the citation supports the
  claim. **You must.**
- Cite the **authoritative record**, not a landing page. For a CVE that means
  the CVE record itself (`https://www.cve.org/CVERecord?id=CVE-…` or the CVE
  Services API), the vendor's specific advisory (e.g. a Fortinet `FG-IR-…`
  page), and the CISA KEV entry if you assert exploitation. A link to
  `https://www.cisa.gov/known-exploited-vulnerabilities-catalog` proves nothing.
- **Copy affected versions, CVSS scores and severity from the record**, do not
  restate them from memory or from a summary. Version numbers in particular:
  naming the wrong versions inverts the guidance, telling people who are exposed
  that they are safe.
- If you claim active exploitation or ransomware use, cite the source that says
  so. CISA KEV records ransomware use explicitly as
  `knownRansomwareCampaignUse`; "Unknown" is not "yes".
- Do not present figures from a private environment as measured evidence. If a
  number cannot be independently checked, leave it out.

Content generated or drafted with an LLM is fine **if you have verified every
factual claim against the primary source yourself.** Unverified generated
content is the main thing this document exists to keep out, and it is usually
obvious: confident formatting, plausible numbers, citations to homepages.

## 3. Data model

Three object types, one directory each, one object per file:

```
caveat/attack-pattern/     techniques   — what the adversary does
caveat/course-of-action/   mitigations  — the provider-specific fix
caveat/relationship/       edges        — course-of-action mitigates attack-pattern
```

The corpus is a **graph**. A technique with no mitigation and no relationship is
half an entry — CI warns about orphaned attack-patterns. A useful contribution
is normally **three files**: the attack-pattern, the course-of-action, and the
relationship joining them.

`course-of-action` carries the field that makes CAVEaT worth having,
`x_mitre_implementation`: named blocks (`Console_Method`, `CLI_Method`,
`API_Method`, or topic names like `Software_Updates`), each with a `description`
and either `steps` or a single `command`.

Authoritative field lists live in [`schema/`](schema/).

## 4. Filenames

**No file extension.** The filename is the object's STIX `id` with the `--`
separator collapsed to a single `-`:

```
id:       attack-pattern--0193c168-4fec-0000-9549-cfc21de144e5
filename: caveat/attack-pattern/attack-pattern-0193c168-4fec-0000-9549-cfc21de144e5
```

Generate a fresh UUIDv4 per object (`python3 -c "import uuid; print(uuid.uuid4())"`).
Placeholder or descriptive ids are never valid.

Data files at the repository root are not part of the corpus and will be
rejected.

> Some existing files predate this convention — a few filenames don't match their
> ids, and two are STIX bundles rather than bare objects. CI reports these as
> warnings and does not fail on them. Don't copy them; new files are held to the
> convention above.

## 5. Validate before you open the PR

```bash
pip install jsonschema
python3 scripts/validate_caveat.py --all              # whole corpus (audit)
python3 scripts/validate_caveat.py --changed <files>  # what CI runs
```

CI runs the validator against **changed files only** on every pull request. It
checks placement, filename/id agreement, UUID-shaped ids, the schema, and that
relationship refs resolve to objects that exist. It cannot check whether what you
wrote is true.

## 6. Tooling note

`README.md` and `CLAUDE.md` point at
[WG-CAVEaT](https://github.com/CloudSecurityAlliance-WG/WG-CAVEaT) for authoring
and validation tooling. **That repository is archived** (last activity
2026-02-19). Its `STIX-2.1-Validation-Guide.md` is still a useful reference and
points at the OASIS schemas at
[oasis-open/cti-stix2-json-schemas](https://github.com/oasis-open/cti-stix2-json-schemas),
but the validator in `scripts/` is what actually runs here.

## 7. Questions

Open an issue. For scope questions especially, ask before writing JSON — it is
much cheaper than having a finished PR closed as out of scope.
