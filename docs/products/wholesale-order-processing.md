# Product Mission

Enable wholesale trading partners to submit purchase orders electronically and receive order acknowledgments while applying the publisher's customer, title, pricing, inventory, and order-handling rules.

# Product Details

## What is it?

Wholesale Order Processing is the publisher's legacy capability for receiving and processing wholesale purchase orders.

The supplied implementation artifacts establish a nightly EDI processing path that:

1. receives X12 850 purchase orders,
2. translates partner data into a normalized internal order record,
3. validates and prices order lines,
4. determines an order-line result/status,
5. generates outbound X12 855 purchase-order acknowledgments, and
6. produces a legacy Finance report.

The supplied artifacts do not establish the complete downstream persistence or fulfillment architecture.

## Inputs & Outputs

### Inputs

- X12 850 Purchase Orders from wholesale trading partners.
- Partner/customer cross-reference information.
- Customer-specific discount information and contract overrides.
- Partner-specific rush-order configuration.
- Customer, title, and inventory information referenced by the validation process.

### Outputs

- Normalized order records.
- Order validation results, including:
  - accepted (`OK`)
  - backordered (`BO`)
  - rejected (`RJ`)
- Calculated net price and line total.
- X12 855 Purchase Order Acknowledgments.
- `OLDPO` Finance report.

### Known Processing Flow

`EDI 850 → EDITRANS → ORDERS.NORMALIZED → ORDVALID → ORDERS.RESULTS → ORDACK → EDI 855`

A subsequent `OLDPOPRT` step produces the legacy Finance report.

Persistence into the relational order database and the downstream fulfillment handoff are not established by the supplied artifacts.

## Users & Stakeholders

Known stakeholders include:

- Customer Service
- Sales Operations
- Distribution
- Finance
- EDI Operations
- Application Support
- Engineering
- Wholesale trading partners

Direct human interaction with the core nightly processing capability is not established. Customer Service and Sales Operations use its results operationally, while trading partners consume the outbound acknowledgments.

## Where is it?

### Runtime / Environment

Legacy batch environment. The supplied JCL defines the nightly processing sequence.

### Repository / Source

- `/batch/` — nightly batch-control artifact
- `/cobol/` — order validation and acknowledgment logic
- `/cobol/copybooks/` — normalized input and result record definitions
- `/edi/` — representative X12 850 and 855 transactions
- `/sql/` — relational schema, sample data, and reconciliation query
- `/legacy-docs/` — surviving field mapping and operational notes

### Relevant Operational Locations

- `EDI.INBOUND.PO850`
- `ORDERS.NORMALIZED`
- `ORDERS.RESULTS`
- `EDI.OUTBOUND.PO855`

The physical/runtime locations and ownership of these datasets are not established.

# How to Use It

## Access

The core product appears to operate as an automated batch capability rather than a directly accessed user application.

Required operational permissions and the access-request process are not documented in the supplied artifacts.

## Usage

### Normal Operation

Wholesale partners transmit X12 850 purchase orders. Orders normally arrive overnight, although large partners may submit multiple batches during holiday periods.

The nightly batch translates, validates, prices, classifies, and acknowledges those orders.

### Operational Support

When researching a missing order, search by the customer's PO number before the internal order number.

For ISBN failures, verify the value supplied by the trading partner before modifying title data.

BookMart orders have special account handling and should not be manually released without consultation with Sales Operations.

READMORE pricing anomalies should be checked against the original PO and escalated to Sales Operations as needed.

## Support

Known support stakeholders:

- EDI Operations — EDI intake/acknowledgment concerns
- Application Support — legacy application support
- Sales Operations — pricing and special-account questions
- Customer Service — partner/order investigation

Formal product ownership and escalation paths are not established.

# Development

## Known Issues

- Partner-specific acknowledgment rules are referenced operationally, but the known spreadsheet containing them cannot currently be located.
- Partner-specific rush-order rules are referenced by the field map, but the partner profile is not included in the supplied artifacts.
- READMORE pricing has historically produced anomalous results requiring manual investigation.
- BookMart has special credit/account handling whose current business rationale requires validation.
- The supplied inventory validation logic uses a hard-coded available quantity of `99999`; the relationship to production inventory lookup is unclear.
- The current use of the `OLDPO` Finance report is unknown.
- The complete persistence and downstream fulfillment flow is not represented in the supplied artifacts.

## Ideas

Potential migration opportunities, subject to discovery and prioritization:

- Decouple external EDI contracts from the internal order model through a maintained integration/canonicalization layer.
- Centralize partner-specific configuration and rules rather than relying on undocumented external artifacts.
- Improve traceability from partner PO through internal order number, processing result, acknowledgment, and downstream fulfillment.
- Replace undocumented or hard-coded legacy behavior with explicit, testable business rules.

These are discovery candidates, not committed features.

## Development History

### 2026

#### Q3

| Type | Effort | Summary | Status |
|---|---|---|---|
| Migration | Wholesale Order Processing Modernization | Analyze the legacy capability and define requirements for replacement. | Discovery |

### Historical

The supplied artifacts identify at least two historical changes but do not provide sufficient project history to reconstruct a reliable chronology:

- A 2020 conversion introduced special handling for older imported orders.
- The `OLDPO` report was requested by Finance in 2009.

Further development history requires discovery.
