CREATE TEMP TABLE test_ids (
    e_id VARCHAR(8)
);

DO $$
DECLARE
    v_employee_id VARCHAR(8);
BEGIN
  
    INSERT INTO employees (first_name, last_name, department_id, start_date)
    VALUES ('testing', 'testing', 1, CURRENT_DATE)
    RETURNING employee_id INTO v_employee_id;
  
  
    INSERT INTO test_ids (e_id)
    VALUES (v_employee_id);

END;
$$;

-- delete employee
DELETE FROM employees e
WHERE e.employee_id = (SELECT e_id FROM test_ids);

SELECT plan(1);

-- employee_medical employee(employee_id) on delete cascade
SELECT ok (
    NOT EXISTS (
        SELECT 1
        FROM employee_medical_records
        WHERE employee_id = (SELECT e_id FROM test_ids)
        ),
        'employees cascade deletion on employee_medical_records success.');



SELECT * FROM finish();