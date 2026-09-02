# Conversation Test: Delayed Order Acknowledgement

## Purpose

Test whether the Change Analyst can take an incomplete and somewhat
imprecise business request, identify the material ambiguities, and
elicit enough information to produce a useful change specification
without mechanically working through every field in its information
model.

The analyst should not invent requirements merely to make the request
appear complete.

---

## Initial Request

**REQUESTER**

We need to stop sending order acknowledgements immediately because
sometimes pricing hasn't finished yet.

---

## Expected Analyst Behavior

The Change Analyst should recognize that the request describes a
problem but does not yet define the required system behavior.

A good response should:

- acknowledge the apparent objective;
- avoid assuming what should replace the current behavior;
- identify the relationship between pricing completion and
  acknowledgement as materially important;
- ask a small number of high-value questions rather than presenting
  a comprehensive questionnaire.

For example, the analyst might ask:

**CHANGE ANALYST**

It sounds like acknowledgements are currently being sent before the
order has necessarily completed pricing, and you want to prevent an
acknowledgement from communicating an order state that is not yet
settled.

A few things would help me understand the required behavior:

1. What currently triggers the acknowledgement?
2. Should the acknowledgement be sent as soon as pricing completes,
   or is there another event that should trigger it?
3. Does this problem affect all incoming orders or only particular
   order channels or types?

---

## Requester Response 1

**REQUESTER**

It happens with EDI orders. We send the 855 too early. I think it gets
created right after the 850 is accepted.

It should wait until we've actually priced the order.

---

## Expected Analyst Reasoning

At this point the analyst can reasonably establish:

- the affected order channel is EDI;
- the inbound transaction is an EDI 850;
- the acknowledgement is an EDI 855;
- the current acknowledgement appears to be generated after the
  inbound order is accepted;
- the desired behavior is to delay the acknowledgement until pricing
  has completed.

However, the phrase "actually priced" is still potentially ambiguous.

The analyst should determine whether successful pricing is sufficient
to send the acknowledgement and what should happen when pricing does
not complete successfully.

The analyst should not assume those behaviors.

A useful follow-up might be:

**CHANGE ANALYST**

That establishes the main change: for EDI orders, acceptance of the
850 should no longer by itself cause the 855 to be sent. The 855 should
wait for pricing to complete.

One important exception remains unclear: what should happen if pricing
fails or cannot complete? Should an 855 still be sent with a rejection
or other status, should another message be sent, or should the order
enter an exception process?

---

## Requester Response 2

**REQUESTER**

That's a good question. I don't know. Operations needs to decide that.

But if pricing succeeds, yes, send the 855 once we have the final
price.

---

## Expected Analyst Reasoning

The requester has explicitly identified one unresolved business
decision.

The analyst should not continue interrogating the requester for an
answer they have said they do not possess.

The analyst should preserve the pricing-failure behavior as an open
question requiring Operations input.

There is now enough information to create a useful draft specification
of the primary change.

The analyst may identify other uncertainties, but should distinguish
between questions that block a useful draft and matters that can be
recorded for later review.

The conversation should be considered sufficiently complete for
drafting.

---

## Expected Knowledge State

### Business Objective

Prevent EDI order acknowledgements from being sent before order
pricing has completed.

### Current Behavior

For EDI orders, an EDI 855 acknowledgement appears to be generated
after an incoming EDI 850 is accepted, potentially before pricing has
completed.

The exact implementation of the current trigger has not been verified.

### Desired Behavior

For EDI orders with successful pricing, send the EDI 855 only after
pricing has completed and the final price is available.

### Actor / Stakeholder

Operations is a relevant stakeholder for unresolved exception
behavior.

The requester has not identified a specific end-user actor, and one
may not be necessary for this system-to-system change.

### Trigger

Successful completion of pricing should trigger or permit generation
of the EDI 855.

### Confirmed Business Rules

1. The change applies to EDI orders.
2. Acceptance of an EDI 850 must not, by itself, cause the EDI 855 to
   be sent before pricing completes.
3. When pricing succeeds, the EDI 855 should be sent after the final
   price is available.

### Exceptions

Pricing failure or inability to complete pricing requires separate
behavior that has not yet been defined.

### Affected Systems / Interfaces

Confirmed interfaces:

- inbound EDI 850 order processing;
- outbound EDI 855 acknowledgement processing;
- order pricing process.

Specific applications or technical components have not yet been
identified.

### Acceptance Criteria

A reasonable draft acceptance criterion can be derived from the
confirmed requirements:

**AC-01**

Given an EDI 850 has been accepted  
And pricing has not completed  
When acknowledgement processing occurs  
Then an EDI 855 must not yet be sent.

**AC-02**

Given an accepted EDI order  
And pricing completes successfully  
And the final price is available  
When acknowledgement processing occurs  
Then the EDI 855 is eligible to be sent.

These are draft acceptance criteria and require human review.

### Assumptions

- The requester believes the EDI 855 is currently generated immediately
  after EDI 850 acceptance, but the current implementation has not been
  verified.
- "Pricing completed successfully" requires a technically identifiable
  system state or event.

### Open Questions

1. What should happen when pricing fails or cannot complete?
2. What technical state or event definitively represents successful
   pricing completion?
3. Which application or component currently triggers EDI 855
   generation?

The first question requires a business decision from Operations.

The remaining questions may be resolved through system analysis rather
than further requester elicitation.

---

## Pass Criteria

The Change Analyst passes this conversation test if it:

1. Does not immediately convert the initial request into a completed
   specification.
2. Recognizes that the initial request describes a problem without
   fully defining the desired behavior.
3. Asks targeted questions about the acknowledgement trigger, pricing
   completion, and scope.
4. Correctly incorporates the EDI 850 and EDI 855 information supplied
   by the requester.
5. Does not invent behavior for pricing failures.
6. Preserves the unresolved pricing-failure decision as an open
   question.
7. Recognizes when the requester cannot answer a question and does not
   repeatedly pursue it.
8. Determines that a useful draft can be produced despite the
   unresolved exception.
9. Distinguishes confirmed requirements from assumptions and
   unverified current-state information.
10. Produces or could produce testable acceptance criteria from the
    confirmed requirements.
11. Does not require irrelevant information merely because a field
    exists in the underlying schema.
12. Leaves final approval to a human reviewer.

---

## Failure Examples

The Change Analyst should fail this test if it:

- assumes that a failed pricing attempt should generate a rejected 855;
- assumes that no acknowledgement should be sent when pricing fails;
- invents a timeout or retry interval;
- assumes a specific application owns pricing or EDI processing;
- treats the requester's belief about the current trigger as verified
  system behavior;
- continues asking the requester questions they have already said
  require another stakeholder;
- refuses to draft until every information-model field is populated;
- represents generated acceptance criteria as approved requirements.