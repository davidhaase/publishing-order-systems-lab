# Change Analyst Workflow

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

# Design Principles

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

# Current Scope

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

# Human Accountability

The purpose of the lab is not to demonstrate that an LLM can independently perform systems analysis.

It is to explore a different division of labor.

AI can accelerate unfamiliar-technology learning, artifact investigation, synthesis, requirements elicitation, structured documentation, and workflow automation. That can move substantial mechanical work earlier in the process and give the analyst a more developed starting point.

The analyst's responsibility therefore becomes more—not less—important at the points where judgment matters: evaluating evidence, challenging assumptions, recognizing contradictions, resolving business decisions, validating requirements, and approving what becomes part of the system record.

> **AI accelerated the work. The analyst remains accountable for the meaning.**

And as the experiment evolved:

> **AI can move the starting line. It should not move the accountability boundary.**
