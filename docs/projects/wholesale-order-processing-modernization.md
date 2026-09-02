# Summary

Replace the legacy wholesale order-processing capability while preserving required business outcomes and trading-partner commitments, identifying obsolete behavior, and avoiding unnecessary replication of the legacy implementation architecture.

The effort begins with discovery because the supplied artifacts are incomplete, were created at different times, and contain behavior whose current business value has not yet been established.

# Goal & Success Metrics

## Goal

Deliver a maintainable replacement for wholesale order processing that preserves required partner and business behavior while making current business rules, dependencies, and integration contracts explicit.

## Success Metrics

Success metrics require stakeholder validation. Candidate measures include:

- Major trading partners migrate without avoidable interruption.
- Required inbound purchase orders continue to be accepted and processed correctly.
- Required outbound acknowledgments continue to be generated correctly.
- Historical order information remains discoverable after migration.
- Required pricing, customer, inventory, rush-order, and acknowledgment behavior is validated against agreed acceptance criteria.
- No legacy behavior is reproduced solely because it exists; retained behavior has an established requirement or rationale.
- Obsolesced behavior is explicitly documented rather than silently dropped.

# Scope

## Must Have

- Preserve required wholesale order-processing business capability.
- Preserve required trading-partner integration contracts.
- Preserve discoverability of historical order information.
- Establish required behavior for:
  - customer identification and validation
  - PO identification
  - title/ISBN validation
  - quantity and unit price
  - discounts and contract overrides
  - rush-order handling
  - inventory/backorder handling
  - order status/results
  - outbound purchase-order acknowledgments
- Identify partner-specific behavior before migration.
- Document unresolved requirements rather than inferring them from legacy implementation.

## Nice to Have

Subject to prioritization:

- Improved end-to-end traceability from inbound partner transaction through internal processing and acknowledgment.
- Centralized partner-specific configuration.
- Reduced coupling between EDI representation and the internal order-processing model.
- Improved observability and operational support tooling.

## Out of Scope

Unless separately established as requirements:

- Reproducing COBOL, JCL, flat-file, or DB2 implementation architecture solely for parity.
- Reproducing unused reports or operational processes solely because they exist today.
- Changing external trading-partner protocols without partner/business agreement.
- Redesigning downstream fulfillment behavior not yet established by discovery.

# Requirements

## Acceptance Criteria

At completion:

- Required X12 850 partner orders can be received without avoidable partner disruption.
- Required partner/customer identifiers are correctly mapped into the target order model.
- Customer PO, order date, ship-to, ISBN, quantity, unit price, discount, source, and rush information required by the business are represented appropriately.
- Required customer/account rules are applied consistently.
- Required title/ISBN validation behavior is implemented.
- Required pricing and discount calculations produce agreed results.
- Required inventory/backorder and rush-order behavior is implemented.
- Required X12 855 acknowledgments reflect agreed order outcomes and partner rules.
- Historical orders remain discoverable.
- Any intentionally retired behavior is documented and approved.
- Operational ownership and support paths are established.

## Assumptions

- EDI remains a required external integration mechanism for at least some major trading partners.
- The target architecture may differ materially from the legacy architecture.
- The supplied artifacts represent useful evidence but are not individually assumed to be complete or current.
- Current COBOL behavior is evidence of implementation behavior, not automatically evidence of a current business requirement.

## Open Questions

1. What component persists normalized/validated order results into the relational database?
2. What downstream system or process initiates fulfillment after order validation?
3. What is the authoritative customer/partner cross-reference used by EDI translation?
4. What are the complete partner-specific rush-order rules?
5. What are the complete partner-specific 855 acknowledgment rules?
6. What business agreement currently governs BookMart's special credit-hold behavior?
7. Is BookMart's legacy exception still required in the target state?
8. What inventory service/module supplies production available quantity?
9. Are `OK`, `BO`, and `RJ` the complete current internal status set?
10. What non-EDI order sources are represented by `ORDER-SOURCE`?
11. Is the `OLDPO` report still consumed by Finance or any downstream process?
12. What is the target-state requirement for READMORE pricing anomalies?
13. How are ship-to codes resolved to physical/customer locations?
14. Which historical orders must remain discoverable, for how long, and through what user experience?
15. What service-level expectations exist for order receipt and acknowledgment timing?

# Decisions

| Date | Decision | Rationale | Owner / Participants |
|---|---|---|---|
| 2026-08-27 | Treat current implementation behavior as evidence, not automatically as target-state requirements. | Prevent accidental preservation of obsolete legacy behavior. | Discovery / BA |
| 2026-08-27 | Preserve unresolved questions explicitly rather than filling gaps through inference. | The source corpus is intentionally incomplete. | Discovery / BA |
| 2026-08-27 | Treat EDI partner continuity as a target constraint while allowing internal architecture to change. | Major trading partners must not experience avoidable interruption. | Discovery / Architecture |

# Migration Analysis

| Capability | Disposition | Evidence / Rationale |
|---|---|---|
| Receive wholesale purchase orders electronically | Parity | Core current capability; partner interruption is explicitly constrained. |
| X12 850 intake for partners that require it | Parity | Existing external contract; partner continuity required. |
| Map partner identity to internal customer | Parity | Required by current normalized order processing. |
| Preserve customer PO for lookup/support | Parity | Operations explicitly use customer PO to locate missing orders. |
| Validate customer and ISBN | Parity | Current processing behavior; exact target rules require validation. |
| Calculate discounts/net price/line totals | Parity | Current business processing; detailed business rules require validation. |
| Backorder/rush handling | Parity | Current behavior exists; exact rules require validation. |
| Generate required X12 855 acknowledgments | Parity | Partners expect acknowledgments. |
| Preserve historical order discoverability | Parity | Explicit migration constraint. |
| Modern internal translation/canonicalization architecture | Exposed New | Target system need not reproduce legacy implementation; replacement requires an explicit integration boundary. |
| Explicit partner-rule configuration and ownership | Exposed New | Legacy process depends on partner profiles/rules that are missing or poorly discoverable. |
| Improved processing traceability/observability | Net New | Potential operational improvement; not established as a current requirement. |
| Additional order channels / APIs | Net New | Potential future capability only; not established by supplied evidence. |
| `OLDPO` printed report | Obsolesced Candidate | Current consumer is unknown; must validate with Finance before retirement. |
| BookMart hard-coded account exception | Undetermined | Current behavior is established; current business requirement is not. |
| Pre-2020 imported-order pricing exception | Undetermined | Legacy behavior exists; migration requirement has not been established. |
