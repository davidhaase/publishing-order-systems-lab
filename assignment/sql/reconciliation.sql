-- Nightly support query. Author unknown.
SELECT
    o.order_number,
    o.customer_po,
    c.customer_name,
    COUNT(ol.line_number) AS line_count,
    SUM(ol.line_total) AS calculated_total
FROM orders o
JOIN customers c ON c.customer_id = o.customer_id
JOIN order_lines ol ON ol.order_number = o.order_number
WHERE o.order_date = CURRENT_DATE
GROUP BY o.order_number, o.customer_po, c.customer_name
ORDER BY o.order_number;

-- Used by EDI Operations when a partner reports a missing order.
SELECT
    o.order_number,
    o.customer_po,
    o.status,
    ol.line_number,
    ol.isbn,
    ol.line_status
FROM orders o
JOIN order_lines ol ON ol.order_number = o.order_number
WHERE o.customer_po = ?;
