CREATE OR REPLACE FUNCTION search_employee_details(text)
RETURNS TABLE (
    employee_id VARCHAR(8),
    first_name TEXT,
    last_name TEXT,
    department TEXT,
    designations JSONB[],
    relevancy REAL
) AS $$
BEGIN
    RETURN QUERY WITH matched_employees AS (
        SELECT 
        e.employee_id,
        ts_rank(e.search_vector, to_tsquery($1)) AS relevancy
        FROM 
            employees e
        WHERE 
            e.search_vector @@ to_tsquery($1)
        
        UNION ALL
        
        SELECT 
            ed.employee_id,
            ts_rank(d.search_vector, to_tsquery($1)) AS relevancy
        FROM 
            employee_designations ed
        JOIN 
            designations d ON ed.designation_id = d.designation_id
        WHERE 
            d.search_vector @@ to_tsquery($1)
        
        UNION ALL
        
        SELECT 
            em.employee_id,
            ts_rank(m.search_vector, to_tsquery($1)) AS relevancy
        FROM 
            employee_missions em
        JOIN 
            missions m ON em.mission_id = m.mission_id
        WHERE 
        m.search_vector @@ to_tsquery($1)
    )
    SELECT 
        e.employee_id,
        e.first_name,
        e.last_name,
        d.department_name AS department,
        ARRAY_AGG(DISTINCT JSONB_BUILD_OBJECT(
                    'designation_name', des.designation_name,
                    'abbreviation', des.abbreviation
        )) FILTER (WHERE des.designation_id IS NOT NULL) AS designations,
        me.relevancy
    
    FROM 
        employees e
    JOIN departments d ON e.department_id = d.department_id
    LEFT JOIN employee_designations ed ON e.employee_id = ed.employee_id
    LEFT JOIN designations des ON ed.designation_id = des.designation_id
    JOIN matched_employees me ON e.employee_id = me.employee_id
    GROUP BY 
        e.employee_id, d.department_id, me.relevancy;
END;
$$ LANGUAGE plpgsql;



CREATE OR REPLACE FUNCTION search_department_details(text)
RETURNS TABLE (
    department_id INTEGER,
    department_name TEXT,
    director JSONB,
    description TEXT,
    relevancy REAL
) AS $$
BEGIN
    RETURN QUERY WITH matched_departments AS (
        SELECT 
        d.department_id,
        ts_rank(d.search_vector, to_tsquery($1)) AS relevancy
        FROM 
            departments d
        WHERE 
            d.search_vector @@ to_tsquery($1)
        
        UNION ALL
        
        SELECT 
            d.department_id,
            ts_rank(e.search_vector, to_tsquery($1)) AS relevancy
        FROM 
            departments d
        JOIN 
            employees e ON d.director_id = e.employee_id
        WHERE 
            e.search_vector @@ to_tsquery($1)
    )
    SELECT 
        d.department_id,
        d.department_name,
        JSONB_BUILD_OBJECT(
            'director_id', d.director_id,
            'director_first_name', e.first_name,
            'director_last_name', e.last_name
        ) AS director,
        d.description,
        md.relevancy
    FROM 
        departments d
    LEFT JOIN employees e ON e.employee_id = d.director_id
    JOIN matched_departments md ON d.department_id = md.department_id
    GROUP BY 
        d.department_id,
        e.employee_id,
        md.relevancy;
END;
$$ LANGUAGE plpgsql;

CREATE OR REPLACE FUNCTION search_origin_details(text)
RETURNS TABLE (
    origin_id VARCHAR(8),
    origin_name TEXT,
    discovery_date DATE,
    description TEXT,
    relevancy REAL
) AS $$
BEGIN
    RETURN QUERY WITH matched_origins AS (
        SELECT 
        o.origin_id,
        ts_rank(o.search_vector, to_tsquery($1)) AS relevancy
        FROM 
            origins o
        WHERE 
            o.search_vector @@ to_tsquery($1)
        
        UNION ALL
        
        SELECT 
            mo.origin_id,
            ts_rank(m.search_vector, to_tsquery($1)) AS relevancy
        FROM 
            mission_origins mo
        JOIN 
            missions m ON mo.mission_id = m.mission_id
        WHERE 
            m.search_vector @@ to_tsquery($1)
        
        UNION ALL
        
        SELECT 
            mo.origin_id,
            ts_rank(s.search_vector, to_tsquery($1)) AS relevancy
        FROM 
            specimen_missions sm
        JOIN 
            specimens s ON sm.specimen_id = s.specimen_id
        JOIN 
            missions m ON sm.mission_id = m.mission_id
        JOIN 
            mission_origins mo ON m.mission_id = mo.mission_id
        WHERE 
            s.search_vector @@ to_tsquery($1)
    )
    SELECT 
        o.origin_id,
        o.origin_name,
        o.discovery_date,
        o.description,
        mo.relevancy
    FROM 
        origins o

    JOIN matched_origins mo ON o.origin_id = mo.origin_id
    GROUP BY o.origin_id, mo.relevancy;
       

END;
$$ LANGUAGE plpgsql;

CREATE OR REPLACE FUNCTION search_mission_details(text)
RETURNS TABLE (
    mission_id VARCHAR(8),
    mission_name TEXT,
    start_date DATE,
    end_date DATE,
    description TEXT,
    relevancy REAL
) AS $$
BEGIN
    RETURN QUERY WITH matched_missions AS (
        SELECT 
        m.mission_id,
        ts_rank(m.search_vector, to_tsquery($1)) AS relevancy
        FROM 
            missions m
        WHERE 
            m.search_vector @@ to_tsquery($1)
        
        UNION ALL
        
        SELECT 
            m.mission_id,
            ts_rank(e.search_vector, to_tsquery($1)) AS relevancy
        FROM 
            missions m
        JOIN 
            employees e ON m.commander_id = e.employee_id
        WHERE 
            e.search_vector @@ to_tsquery($1)
        
        UNION ALL
        
        SELECT 
            m.mission_id,
            ts_rank(e.search_vector, to_tsquery($1)) AS relevancy
        FROM 
            missions m
        JOIN 
            employees e ON m.supervisor_id = e.employee_id
        WHERE 
            e.search_vector @@ to_tsquery($1)
    )
    SELECT 
        m.mission_id,
        m.mission_name,
        m.start_date,
        m.end_date,
        m.description,
        mm.relevancy
    FROM 
        missions m
    JOIN matched_missions mm ON m.mission_id = mm.mission_id
    GROUP BY m.mission_id, mm.relevancy;
END;
$$ LANGUAGE plpgsql;


CREATE OR REPLACE FUNCTION search_specimen_details(text)
RETURNS TABLE (
    specimen_id VARCHAR(8),
    specimen_name TEXT,
    threat_level REAL,
    acquisition_date DATE,
    relevancy REAL
) AS $$
BEGIN
RETURN QUERY WITH matched_specimens AS (
    SELECT 
        s.specimen_id,
        ts_rank(s.search_vector, to_tsquery($1)) AS relevancy
    FROM 
        specimens s
    WHERE 
        s.search_vector @@ to_tsquery($1)
    
    UNION ALL
    
    SELECT 
        sm.specimen_id,
        ts_rank(m.search_vector, to_tsquery($1)) AS relevancy
    FROM 
        specimen_missions sm
    JOIN 
        missions m ON sm.mission_id = m.mission_id
    WHERE 
        m.search_vector @@ to_tsquery($1)
    
    UNION ALL
    
    SELECT 
        rs.specimen_id,
        ts_rank(e.search_vector, to_tsquery($1)) AS relevancy
    FROM 
        researcher_specimens rs
    JOIN 
        employees e ON rs.employee_id = e.employee_id
    WHERE 
        e.search_vector @@ to_tsquery($1)
)
SELECT 
    s.specimen_id,
    s.specimen_name,
    s.threat_level,
    s.acquisition_date,
    ms.relevancy
FROM 
    specimens s

JOIN matched_specimens ms ON s.specimen_id = ms.specimen_id
GROUP BY s.specimen_id, ms.relevancy;

END;
$$ LANGUAGE plpgsql;
