CREATE OR REPLACE FUNCTION search_employee_details(text)
RETURNS TABLE (
    employee_id VARCHAR(8),
    first_name TEXT,
    last_name TEXT,
    department TEXT,
    designations JSONB[]
) AS $$
BEGIN
    RETURN QUERY WITH matched_employees AS (
        SELECT 
            e.employee_id
        FROM 
            employees e
        WHERE 
            e.search_vector @@ TO_TSQUERY($1)
        UNION
        SELECT 
            ed.employee_id
        FROM 
            employee_designations ed
        JOIN 
            designations d ON ed.designation_id = d.designation_id
        WHERE 
            d.search_vector @@ TO_TSQUERY($1)
        UNION
        SELECT 
            em.employee_id
        FROM 
            employee_missions em
        JOIN 
            missions m ON em.mission_id = m.mission_id
        WHERE 
            m.search_vector @@ TO_TSQUERY($1)
    )
    SELECT 
        e.employee_id,
        e.first_name,
        e.last_name,
        d.department_name AS department,
        ARRAY_AGG(DISTINCT JSONB_BUILD_OBJECT(
                    'designation_name', des.designation_name,
                    'abbreviation', des.abbreviation
        )) FILTER (WHERE des.designation_id IS NOT NULL) AS designations
    
    FROM 
        employees e
    JOIN departments d ON e.department_id = d.department_id
    LEFT JOIN employee_designations ed ON e.employee_id = ed.employee_id
    LEFT JOIN designations des ON ed.designation_id = des.designation_id
    WHERE 
        e.employee_id IN (SELECT me.employee_id FROM matched_employees me)
    GROUP BY 
        e.employee_id, d.department_id;
END;
$$ LANGUAGE plpgsql;



CREATE OR REPLACE FUNCTION search_department_details(text)
RETURNS TABLE (
    department_id INTEGER,
    department_name TEXT,
    director JSONB,
    description TEXT
) AS $$
BEGIN
    RETURN QUERY WITH matched_departments AS (
        SELECT 
            d.department_id
        FROM 
            departments d
        LEFT JOIN employees e ON d.director_id = e.employee_id
        WHERE 
            d.search_vector @@ TO_TSQUERY($1) OR
            e.search_vector @@ TO_TSQUERY($1)
    )
    SELECT 
        d.department_id,
        d.department_name,
        JSONB_BUILD_OBJECT(
            'director_id', d.director_id,
            'director_first_name', e.first_name,
            'director_last_name', e.last_name
        ) AS director,
        d.description
    FROM 
        departments d
    LEFT JOIN employees e ON e.employee_id = d.director_id
    WHERE 
        d.department_id IN (SELECT md.department_id FROM matched_departments md)
    GROUP BY 
        d.department_id,
        e.employee_id;
END;
$$ LANGUAGE plpgsql;

CREATE OR REPLACE FUNCTION search_origin_details(text)
RETURNS TABLE (
    origin_id VARCHAR(8),
    origin_name TEXT,
    discovery_date DATE,
    description TEXT
) AS $$
BEGIN
    RETURN QUERY WITH matched_origins AS (
        SELECT 
            o.origin_id
        FROM 
            origins o
        WHERE 
            o.search_vector @@ TO_TSQUERY($1)
    ),
    matched_missions AS (
        SELECT DISTINCT 
            mo.origin_id
        FROM 
            mission_origins mo
        JOIN 
            missions m ON mo.mission_id = m.mission_id
        WHERE 
            m.search_vector @@ TO_TSQUERY($1)
    ),
    matched_specimens AS (
        SELECT DISTINCT 
            mo.origin_id
        FROM 
            specimen_missions sm
        JOIN 
            specimens s ON sm.specimen_id = s.specimen_id
        JOIN 
            missions m ON sm.mission_id = m.mission_id
        JOIN 
            mission_origins mo ON m.mission_id = mo.mission_id
        WHERE 
            s.search_vector @@ TO_TSQUERY($1)
    )
    SELECT 
        o.origin_id,
        o.origin_name,
        o.discovery_date,
        o.description
    FROM 
        origins o

    WHERE 
        o.origin_id IN (SELECT mo.origin_id FROM matched_origins mo)
        OR o.origin_id IN (SELECT mm.origin_id FROM matched_missions mm)
        OR o.origin_id IN (SELECT ms.origin_id FROM matched_specimens ms);

END;
$$ LANGUAGE plpgsql;

CREATE OR REPLACE FUNCTION search_mission_details(text)
RETURNS TABLE (
    mission_id VARCHAR(8),
    mission_name TEXT,
    start_date DATE,
    end_date DATE,
    description TEXT
) AS $$
BEGIN
    RETURN QUERY WITH matched_missions AS (
        SELECT 
            m.mission_id
        FROM 
            missions m
        WHERE 
            m.search_vector @@ TO_TSQUERY($1)
    ),
    matched_commanders AS (
        SELECT 
            m.mission_id
        FROM 
            missions m
        JOIN 
            employees e ON m.commander_id = e.employee_id
        WHERE 
            e.search_vector @@ TO_TSQUERY($1)
    ),
    matched_supervisors AS (
        SELECT 
            m.mission_id
        FROM 
            missions m
        JOIN 
            employees e ON m.supervisor_id = e.employee_id
        WHERE 
            e.search_vector @@ TO_TSQUERY($1)
    )
    SELECT 
        m.mission_id,
        m.mission_name,
        m.start_date,
        m.end_date,
        m.description
    FROM 
        missions m
    WHERE 
        m.mission_id IN (SELECT mm.mission_id FROM matched_missions mm)
        OR m.mission_id IN (SELECT mc.mission_id FROM matched_commanders mc)
        OR m.mission_id IN (SELECT ms.mission_id FROM matched_supervisors ms);
END;
$$ LANGUAGE plpgsql;


CREATE OR REPLACE FUNCTION search_specimen_details(text)
RETURNS TABLE (
    specimen_id VARCHAR(8),
    specimen_name TEXT,
    threat_level REAL,
    acquisition_date DATE
) AS $$
BEGIN
RETURN QUERY WITH matched_specimens AS (
    SELECT 
        s.specimen_id
    FROM 
        specimens s
    WHERE 
        s.search_vector @@ TO_TSQUERY($1)
),
matched_missions AS (
    SELECT DISTINCT 
        sm.specimen_id
    FROM 
        specimen_missions sm
    JOIN 
        missions m ON sm.mission_id = m.mission_id
    WHERE 
        m.search_vector @@ TO_TSQUERY($1)
),
matched_researchers AS (
    SELECT DISTINCT 
        rs.specimen_id
    FROM 
        researcher_specimens rs
    JOIN 
        employees e ON rs.employee_id = e.employee_id
    WHERE 
        e.search_vector @@ TO_TSQUERY($1)
)
SELECT 
    s.specimen_id,
    s.specimen_name,
    s.threat_level,
    s.acquisition_date
FROM 
    specimens s

WHERE 
    s.specimen_id IN (SELECT ms.specimen_id FROM matched_specimens ms)
    OR s.specimen_id IN (SELECT mm.specimen_id FROM matched_missions mm)
    OR s.specimen_id IN (SELECT mr.specimen_id FROM matched_researchers mr);

END;
$$ LANGUAGE plpgsql;
