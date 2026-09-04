CREATE TABLE customers (
    customer_id      INTEGER PRIMARY KEY,
    customer_name    VARCHAR(80) NOT NULL,
    edi_partner_id   VARCHAR(20),
    default_discount DECIMAL(5,2) NOT NULL DEFAULT 0,
    credit_hold      CHAR(1) NOT NULL DEFAULT 'N',
    active_flag      CHAR(1) NOT NULL DEFAULT 'Y'
);

CREATE TABLE titles (
    isbn              CHAR(13) PRIMARY KEY,
    title_name        VARCHAR(120) NOT NULL,
    list_price        DECIMAL(9,2) NOT NULL,
    active_flag       CHAR(1) NOT NULL DEFAULT 'Y'
);

CREATE TABLE orders (
    order_number      INTEGER PRIMARY KEY,
    customer_id       INTEGER NOT NULL,
    customer_po       VARCHAR(15),
    order_date        DATE NOT NULL,
    ship_to_code      VARCHAR(6),
    order_source      CHAR(1) NOT NULL,
    rush_flag         CHAR(1) NOT NULL DEFAULT 'N',
    status            VARCHAR(12) NOT NULL,
    FOREIGN KEY (customer_id) REFERENCES customers(customer_id)
);

CREATE TABLE order_lines (
    order_number      INTEGER NOT NULL,
    line_number       INTEGER NOT NULL,
    isbn              CHAR(13) NOT NULL,
    quantity          INTEGER NOT NULL,
    sent_unit_price   DECIMAL(9,2),
    discount_pct      DECIMAL(5,2),
    net_unit_price    DECIMAL(9,2),
    line_total        DECIMAL(11,2),
    line_status       VARCHAR(12),
    PRIMARY KEY (order_number, line_number),
    FOREIGN KEY (order_number) REFERENCES orders(order_number),
    FOREIGN KEY (isbn) REFERENCES titles(isbn)
);

CREATE TABLE inventory (
    isbn              CHAR(13) PRIMARY KEY,
    available_qty     INTEGER NOT NULL,
    warehouse_code    VARCHAR(6) NOT NULL
);
