CREATE VIEW employee_details AS
SELECT 
    e.employee_id,
    e.first_name,
    e.last_name,
    e.start_date,
    e.end_date,
    e.notes,
    e.department_id,
    d.department_name,
    ARRAY_AGG(DISTINCT des.name) AS designations,
    ARRAY_AGG(DISTINCT c.name) AS clearances
FROM employees e
LEFT JOIN 

