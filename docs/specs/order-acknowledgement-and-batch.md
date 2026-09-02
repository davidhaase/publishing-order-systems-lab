# Order Acknowledgment and Nightly Batch

**Product:** [Wholesale Order Processing](../products/wholesale-order-processing.md)  
**Owner:** EDI Operations / Application Support [ownership to validate]  
**Last Verified:** 2026-08-27  
**Implementation References:** `batch/ORDERNIGHT.jcl`, `cobol/ORDACK.cbl`, `edi/`, `legacy-docs/operations-notes.txt`

---

## Purpose

Coordinate nightly wholesale order processing and translate internal processing results into outbound partner acknowledgments.

## Nightly Batch Sequence

| Step | Program | Input | Output | Purpose |
|---|---|---|---|---|
| 1 | `EDITRANS` | `EDI.INBOUND.PO850` | `ORDERS.NORMALIZED` | Translate inbound EDI orders |
| 2 | `ORDVALID` | `ORDERS.NORMALIZED` | `ORDERS.RESULTS` | Validate and price orders |
| 3 | `ORDACK` | `ORDERS.RESULTS` | `EDI.OUTBOUND.PO855` | Generate acknowledgments |
| 4 | `OLDPOPRT` | Not established | Printer/SYSOUT | Legacy Finance report |

EDI orders normally arrive overnight; large partners may send multiple batches during holiday periods.

## Acknowledgment Status Mapping

`ORDACK` maps internal result status to acknowledgment code:

| Internal Status | Acknowledgment Code |
|---|---|
| `OK` | `IA` |
| `BO` | `IB` |
| `RJ` | `IR` |
| Other / unexpected | `IR` with `SYSTEM ERROR` |

Representative outbound X12 855 transactions are available under `/edi/`.

## Partner-Specific Behavior

Operations notes state that EDI acknowledgments are expected by partners.

A historical spreadsheet reportedly contained partner-specific acknowledgment rules, but its location is unknown.

Therefore the status mapping represented in `ORDACK` must not be assumed to constitute the complete partner acknowledgment requirement.

## OLDPO Report

`OLDPOPRT` runs after acknowledgment generation.

The JCL comment states that Finance requested the report in 2009. Operations notes state that Finance formerly collected the printed report but that current use is unknown.

**Migration disposition:** Obsolesced Candidate — validate with Finance before removal.

## Open Implementation Questions

- What schedules/triggers initiate `ORDERNIGHT`?
- Are additional daytime or holiday runs scheduled differently?
- What complete partner-specific acknowledgment rules exist?
- Where/how are outbound 855 files transmitted after creation?
- Does acknowledgment generation depend on persistence not represented in this batch?
- Is `OLDPOPRT` still consumed?
- What monitoring/recovery process exists when a batch step fails?
