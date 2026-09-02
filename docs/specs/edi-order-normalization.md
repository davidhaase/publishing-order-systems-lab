# EDI Order Normalization

**Product:** [Wholesale Order Processing](../products/wholesale-order-processing.md)  
**Owner:** EDI Operations [ownership to validate]  
**Last Verified:** 2026-08-27  
**Implementation References:** `batch/ORDERNIGHT.jcl`, `legacy-docs/field-map.txt`, `cobol/copybooks/ORDREC.cpy`, `edi/`

---

## Purpose

Translate inbound wholesale X12 850 purchase orders into the normalized order representation consumed by legacy order validation.

## Processing Context

The nightly batch invokes `EDITRANS` against `EDI.INBOUND.PO850` and produces `ORDERS.NORMALIZED`.

The implementation of `EDITRANS` is not included in the supplied repository.

## Known Field Mapping

| Source | Normalized Field | Notes |
|---|---|---|
| `BEG03` | PO Number | Customer's purchase-order identifier |
| `BEG05` | Order Date | Observed as `YYYYMMDD` |
| `N1/ST N104` | Ship-To | Six-character normalized field |
| `PO107/08` | ISBN | 13-character normalized field |
| `PO102` | Quantity | Five-digit numeric field |
| `PO104` | Unit Price | Five digits plus two implied decimals |
| Partner ID | Customer ID | Uses a cross-reference table not supplied |
| System-derived | Order Source | `E` for EDI |
| Customer default / contract override | Discount % | Source logic not supplied |
| Partner profile | Rush Flag | Partner profile not supplied |

## Normalized Order Contract

The legacy `ORDER-RECORD` contains:

- internal order number
- customer ID
- customer PO number
- order date
- ship-to code
- ISBN
- quantity
- unit price
- discount percentage
- order source
- rush flag

## Known Gaps

- `EDITRANS` implementation is unavailable.
- Partner/customer cross-reference table is unavailable.
- Partner profiles governing rush behavior are unavailable.
- The process that assigns the internal order number is not established.
- The relationship between optional EDI product descriptions (`PID`) and internal processing is not established as a requirement.
- Line numbers exist in the later SQL model but were not present in the original normalized flat-file record.
