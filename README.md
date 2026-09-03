# Publishing Order Systems Lab

A compact legacy publishing-order environment for systems-analysis practice and experimentation with AI-assisted analysis.

## About This Lab

This repository began as a time-boxed systems-analysis exercise exploring a legacy COBOL / EDI / SQL wholesale order-processing environment.

The initial goal was not to use AI to replace analysis, but to explore how far an analyst and AI could move the starting line in less than two days: learning an unfamiliar technology stack, investigating legacy artifacts, organizing evidence, and producing a first-pass documentation corpus.

The working model evolved through five stages:

**Learn → Investigate → Synthesize → Review → Validate**

AI played different roles at different stages—from technology tutor and simulated SME to synthesis and drafting partner.

The resulting documentation should not be considered finished analysis. It is a reviewable starting point from which the higher-value analyst work can proceed: challenging assumptions, resolving contradictions, validating business rules with SMEs, determining future-state requirements, and establishing what should—and should not—survive a migration.

> **AI accelerated the work. The analyst remains accountable for the meaning.**

## From AI-Assisted Analysis to AI-Assisted Requirements Elicitation

The lab subsequently evolved into a second experiment.

If an LLM can help an analyst investigate a system and draft its documentation, can it also become part of the interface through which a change request is understood?

The **Change Analyst Agent** explores that question.

A requester begins with an ordinary GitHub Issue written in natural language. Rather than requiring the requester to complete a comprehensive requirements form, the agent analyzes the request, identifies materially missing information, and conducts an adaptive conversation through GitHub Issue comments.

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

> **The LLM does not replace requirements discipline. It moves the structure behind the conversational interface.**

The agent may identify ambiguity, ask questions, organize evidence, and draft artifacts. It does not invent business rules, silently resolve unanswered questions, or approve its own work. Uncertainty remains visible, and the human analyst remains accountable for review and acceptance.

In that sense, the second experiment is an extension of the first:

> **AI can move the starting line. It should not move the accountability boundary.**

## Scenario

You have joined a publisher that is preparing to replace a long-running order-processing system. The supplied artifacts are incomplete and were created at different times by different teams. Your assignment is to determine what the system actually does and document what a replacement must preserve, change, add, or retire.

The Change Analyst extension adds a second scenario: stakeholders continue to request changes while that environment is being understood and modernized. Those requests may arrive incomplete, ambiguous, or expressed entirely in business language. The analyst must turn them into reviewable requirements without treating assumptions as facts or forcing stakeholders to understand the underlying implementation.

## Repository

- `cobol/` — legacy application code and copybooks
- `edi/` — representative inbound/outbound EDI
- `sql/` — database schema and sample data
- `batch/` — batch-control artifact
- `legacy-docs/` — surviving operational notes
- `assignment/` — analyst brief
- `change_analyst/` — Change Analyst Agent, structured requirements model, prompts, and specification generation
- `.github/workflows/` — GitHub Actions automation for conversational requirements elicitation
- `docs/` — analyst-produced product, migration, implementation, and change documentation
  - `products/` — product-level documentation
  - `projects/` — migration projects and development history
  - `specs/` — implementation specifications and technical details
  - `change-requests/` — AI-elicited draft change specifications submitted through pull requests
- `tests/` — automated tests and behavioral scenarios for the Change Analyst

Do not assume every artifact is current or every comment is correct.

## Change Analyst Workflow

The Change Analyst is intentionally conversational rather than form-driven.

A stakeholder can begin with an incomplete natural-language request such as:

> Customers are getting confirmations before we've figured out what they're actually going to pay.

The agent does not require the stakeholder to know the implementation, identify every affected component, or translate the request into technical terminology before the analysis can begin.

Instead, it distinguishes among:

- information that should be elicited from the stakeholder;
- information that can later be discovered through technical analysis;
- assumptions that require validation; and
- unresolved business decisions that must remain visible for an accountable human decision-maker.

The conversation is open-ended. There is no fixed number of questions or turns. The workflow continues until the structured requirements state satisfies the application's readiness policy.

At that point, the agent produces a draft—not an approved requirement.

```text
Issue opened
    ↓
Agent analyzes request
    ↓
Material information missing?
    ├── Yes → Ask adaptive follow-up question
    │          ↓
    │       User replies
    │          ↓
    │       Re-analyze full conversation
    │
    └── No → Generate change specification
                ↓
             Create Draft PR
                ↓
             Human review
                ↓
             Ready for review
                ↓
             Merge
```

The originating Issue remains open while the specification is under review. When an accepted Pull Request is merged, the linked Issue can close as part of the normal GitHub lifecycle.

## Design Principles

The Change Analyst is built around several deliberately simple principles:

**Conversation is the interface; structure remains underneath.**  
Natural language replaces the rigid questionnaire, not the structured requirements model.

**Missing information is not automatically blocking information.**  
A technical component may be unknown without preventing a useful business requirements draft.

**Evidence and inference are different.**  
Statements such as “I think,” “probably,” or “it may happen when…” remain qualified rather than silently becoming facts.

**Unresolved decisions remain unresolved.**  
The agent does not invent exception handling or business rules merely to make a specification appear complete.

**Readiness is an application decision.**  
The LLM helps interpret the conversation and populate structured state, while deterministic application logic determines whether the minimum requirements for a useful draft have been satisfied.

**Generation is not approval.**  
Specifications are submitted as Draft Pull Requests so that human review remains an explicit part of the workflow.

## Current Scope

The current implementation demonstrates a working vertical slice:

**GitHub Issue → conversational elicitation → structured requirements → deterministic readiness → generated specification → Draft Pull Request → human review**

The emphasis is intentionally on requirements elicitation, traceability, and governance rather than autonomous software development.

Potential future extensions include:

- repository-assisted impact analysis;
- identification of relevant code paths, schemas, interfaces, and dependencies;
- requirements-to-implementation traceability;
- documentation consistency and linting;
- automated diagram generation;
- richer behavioral evaluation scenarios; and
- controlled progression from approved requirements into implementation planning.

These are extensions of the experiment rather than prerequisites for the current workflow.

## Human Accountability

The purpose of the lab is not to demonstrate that an LLM can independently perform systems analysis.

It is to explore a different division of labor.

AI can accelerate unfamiliar-technology learning, artifact investigation, synthesis, requirements elicitation, structured documentation, and workflow automation. That can move substantial mechanical work earlier in the process and give the analyst a more developed starting point.

The analyst's responsibility therefore becomes more—not less—important at the points where judgment matters: evaluating evidence, challenging assumptions, recognizing contradictions, resolving business decisions, validating requirements, and approving what becomes part of the system record.

> **AI accelerated the work. The analyst remains accountable for the meaning.**

And as the experiment evolved:

> **AI can move the starting line. It should not move the accountability boundary.**
