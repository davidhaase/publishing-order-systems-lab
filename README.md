# Publishing Order Systems Lab

This repo serves as a lab for experimentation with AI-assisted analysis, formed within the context of an imaginary legacy publishing-order environment.

## Initial Goal: Can AI assist in systems analysis?
### Scenario

*You have joined a publisher that is preparing to replace a long-running order-processing system. The supplied artifacts are incomplete and were created at different times by different teams. Your assignment is to determine what the system actually does and document what a replacement must preserve, change, add, or retire. Do not assume every artifact is current or every comment is correct.*

The initial goal was not to use AI to replace analysis, but to explore how far an analyst and AI could move the starting line in less than two days: learning an unfamiliar technology stack, investigating legacy artifacts, organizing evidence, and producing a first-pass documentation corpus.

### Conclusion
> **AI accelerated the work. The analyst remains accountable for the meaning.**

### Procedures
This repository began as a time-boxed systems-analysis exercise exploring a legacy COBOL / EDI / SQL wholesale order-processing environment.
-  No special agents were used
-  Simple human-to-AI/LLM natural language chat

The working model evolved through five stages:

**Learn → Investigate → Synthesize → Review → Validate**

AI played different roles at different stages—from technology tutor and simulated SME to synthesis and drafting partner.

### Outcomes

The resulting documentation is available in the [docs](./docs) directory of this repo represented by three classes of documentation:
1. Resulting product definitions of what exists: [docs/products](./docs/products)
2. Resulting project requirements for migrating: [docs/projects](./docs/projects)
3. Resulting system specs: [docs/specs](./docs/specs)

The resulting documentation should not be considered finished analysis. It is a reviewable starting point from which the higher-value analyst work can proceed: challenging assumptions, resolving contradictions, validating business rules with SMEs, determining future-state requirements, and establishing what should—and should not—survive a migration.

## Evolved Goal: Can AI assist in eliciting requirements?
The lab subsequently evolved into a second experiment.
### Scenario

*The Change Analyst extension adds a second scenario: stakeholders continue to request changes while that environment is being understood and modernized. Those requests may arrive incomplete, ambiguous, or expressed entirely in business language. The analyst must turn them into reviewable requirements without treating assumptions as facts or forcing stakeholders to understand the underlying implementation.*

If an LLM can help an analyst investigate a system and draft its documentation, can it also become part of the interface through which a change request is understood?

#### Conclusion
> **The LLM does not replace requirements discipline. It moves the structure behind the conversational interface.**

### Procedures
I coded a **Change Analyst Agent** to explore that question.  

A requester begins with an ordinary **GitHub Issue** written in natural language. Rather than requiring the requester to complete a comprehensive requirements form, the agent analyzes the request, identifies materially missing information, and conducts an adaptive conversation through GitHub Issue comments.

Behind that conversational interface, the agent maintains a structured change-request model containing confirmed requirements, assumptions, exceptions, affected systems, acceptance criteria, and open questions.

A deterministic readiness policy—not the number of conversational turns—determines when enough information exists to produce a useful draft.

When that threshold is reached, the workflow:

1. Generates a structured Markdown change specification.
2. Creates a dedicated Git branch for the proposed artifact.
3. Commits the specification under `docs/change-requests/`.
4. Opens a **Draft Pull Request** for human review.
5. Links the proposed change back to the originating Issue.

The Issue remains the requirements conversation. The structured model provides rigor behind the conversation. The Markdown specification becomes the proposed artifact. The Draft Pull Request becomes the human review and governance boundary.

```text
Natural-language change request
            ↓
       GitHub Issue
            ↓
 Adaptive AI elicitation
            ↓
 Structured requirements state
            ↓
 Deterministic readiness check
            ↓
  Draft change specification
            ↓
    Draft Pull Request
            ↓
       Human review
            ↓
           Merge
```

This changes the role of AI in the lab. It is no longer only helping generate documentation after analysis has occurred. It is participating in the elicitation process itself.

The underlying principle, however, has not changed:

The agent may identify ambiguity, ask questions, organize evidence, and draft artifacts. It does not invent business rules, silently resolve unanswered questions, or approve its own work. Uncertainty remains visible, and the human analyst remains accountable for review and acceptance.

In that sense, the second experiment is an extension of the first:

> **AI can move the starting line. It should not move the accountability boundary.**

### Outcomes

Once the requester reviews and merges the PR draft created by the agent, the resulting, formalized change requests are merged into the [docs/change-requests](./docs/change-requests) directory of this repo.

## Repository

- `assignment/` — analyst brief
  - `cobol/` — legacy application code and copybooks
  - `edi/` — representative inbound/outbound EDI
  - `sql/` — database schema and sample data
  - `batch/` — batch-control artifact
  - `legacy-docs/` — surviving operational notes
- `change_analyst/` — Change Analyst Agent, structured requirements model, prompts, and specification generation
- `.github/workflows/` — GitHub Actions automation for conversational requirements elicitation
- `docs/` — analyst-produced product, migration, implementation, and change documentation
  - `products/` — product-level documentation
  - `projects/` — migration projects and development history
  - `specs/` — implementation specifications and technical details
  - `change-requests/` — AI-elicited draft change specifications submitted through pull requests
- `tests/` — automated tests and behavioral scenarios for the Change Analyst


