# Order Validation and Pricing

**Product:** [Wholesale Order Processing](../products/wholesale-order-processing.md)  
**Owner:** Application Support / Engineering [ownership to validate]  
**Last Verified:** 2026-08-27  
**Implementation References:** `cobol/ORDVALID.cbl`, `cobol/copybooks/ORDREC.cpy`, `cobol/copybooks/OUTREC.cpy`, `legacy-docs/operations-notes.txt`

---

## Purpose

Validate normalized wholesale order lines, calculate pricing results, and classify each processed result for downstream acknowledgment/processing.

## Processing Sequence

`ORDVALID` processes a normalized order in this sequence:

1. Copy identifying/input fields into the result record.
2. Check customer.
3. If no status has been assigned, check title/ISBN.
4. If still valid, calculate pricing.
5. If still valid, check inventory/rush behavior.
6. If no exception assigned a status, mark the result `OK / ACCEPTED`.

A populated result status therefore also acts as a short-circuit preventing later validation stages.

## Customer Validation

- Customer ID `00000000` results in:
  - Status: `RJ`
  - Reason: `UNKNOWN CUSTOMER`
- Production customer lookup is referenced as being supplied by a DB2 module; that module is not included.
- Legacy account `00001042` bypasses credit hold.
- Operations notes identify BookMart as a special account with its own agreement.

The current business requirement behind the account-1042 exception is unresolved.

## Title / ISBN Validation

A blank ISBN results in:

- Status: `RJ`
- Reason: `MISSING ISBN`

Operations guidance instructs support staff to verify the ISBN actually supplied by the partner before modifying title-master data.

## Pricing

Gross amount:

`Unit Price × Quantity`

Discount amount:

`Gross Amount × (Discount % / 100)`

Line total:

`Gross Amount - Discount Amount`

Net unit price:

`Unit Price - (Unit Price × Discount % / 100)`

For orders dated before `20200101`, the legacy program retains the submitted unit price as net price.

The business rationale and continued target-state requirement for this historical exception are unresolved.

## Inventory & Rush Processing

The supplied program sets available quantity to `99999`.

If order quantity exceeds available quantity:

- Status: `BO`
- Reason: `BACKORDER`

If an order is both rush (`Y`) and backordered:

- Status: `RJ`
- Reason: `RUSH-NO-STOCK`

Operations notes confirm that rush orders should not remain in `BO` status.

The production source of available inventory is unresolved.

## Successful Result

If no validation stage assigns a status:

- Status: `OK`
- Reason: `ACCEPTED`

## Open Implementation Questions

- What DB2 module performs production customer lookup?
- What component supplies actual available inventory?
- Is account 1042 definitively BookMart in the authoritative customer master?
- What business rule governs BookMart's credit-hold exception?
- Is the pre-2020 pricing behavior still required?
- Are additional validation/status paths present in production code not represented here?
