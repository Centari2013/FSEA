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
    ARRAY_AGG(CONCAT(des.designation_name, ' (', des.abbreviation, ')')) AS designations,
    ARRAY_AGG(cl.clearance_name) AS clearances
FROM employees e
LEFT JOIN departments d ON d.department_id = e.department_id
LEFT JOIN employee_designations ed ON ed.employee_id = e.employee_id
LEFT JOIN designations des ON des.designation_id = ed.designation_id
LEFT JOIN employee_clearances ecl ON ecl.employee_id = e.employee_id
LEFT JOIN clearances cl ON cl.clearance_id = ecl.clearance_id
GROUP BY
    e.employee_id, d.department_id;


