# tf-blast-radius-gate
- **Date / Artifact:** 2026-11-27 — Terraform Plan Blast-Radius Gate (`tf-blast-radius-gate`)
- **Who bleeds from this:** Series A–C infra/platform teams using GitHub Actions + Terraform without paid policy-as-code suites (Spacelift/Env0/TFC).
- **Wedge insight:** Teams either have zero guardrails (accidental `rds`/`vector-db` replacements) or over-engineered OPA setups engineers bypass. Opinionated blast-radius scoring + governed break-glass PR labels is a high-leverage wedge.
