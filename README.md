# Publishing Order Systems Lab

A compact legacy publishing-order environment for systems-analysis practice.

## About This Lab

This repository is a time-boxed systems-analysis exercise exploring a
legacy COBOL / EDI / SQL wholesale order-processing environment.

It also serves as an experiment in AI-assisted systems analysis.

The goal was not to use AI to replace analysis, but to explore how far
an analyst and AI could move the starting line in less than two days:
learning an unfamiliar technology stack, investigating legacy artifacts,
organizing evidence, and producing a first-pass documentation corpus.

The working model evolved through five stages:

**Learn → Investigate → Synthesize → Review → Validate**

AI played different roles at different stages—from technology tutor and
simulated SME to synthesis and drafting partner.

The resulting documentation should not be considered finished analysis.
It is a reviewable starting point from which the higher-value analyst
work can proceed: challenging assumptions, resolving contradictions,
validating business rules with SMEs, determining future-state
requirements, and establishing what should—and should not—survive a
migration.

> [!IMPORTANT]
> **AI accelerated the work. The analyst remains accountable for the meaning.**

## Scenario
You have joined a publisher that is preparing to replace a long-running order-processing system. The supplied artifacts are incomplete and were created at different times by different teams. Your assignment is to determine what the system actually does and document what a replacement must preserve, change, add, or retire.

## Repository
- `cobol/` — legacy application code and copybooks
- `edi/` — representative inbound/outbound EDI
- `sql/` — database schema and sample data
- `batch/` — batch-control artifact
- `legacy-docs/` — surviving operational notes
- `assignment/` — analyst brief
- `docs/` - analyst-produced product, migration, and implementation documentation
  - `products/` — product-level documentation
  - `projects/` — migration projects and development history
  - `specs/` — implementation specifications and technical details

Do not assume every artifact is current or every comment is correct.
