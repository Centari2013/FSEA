PREPARE search_employee_details(text) AS
WITH matched_employees AS (
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
),
aggregated_info AS (
    SELECT 
        e.employee_id,
        e.first_name,
        e.last_name,
        e.start_date,
        e.end_date,
        e.notes,
        JSONB_BUILD_OBJECT(
            'department_id', e.department_id,
            'department_name', d.department_name
        ) AS department,
        ARRAY_AGG(DISTINCT JSONB_BUILD_OBJECT(
                    'designation_name', des.designation_name,
                    'abbreviation', des.abbreviation
        )) FILTER (WHERE des.designation_id IS NOT NULL) AS designations,
        ARRAY_AGG(DISTINCT cl.clearance_name) FILTER (WHERE cl.clearance_id IS NOT NULL) AS clearances,
        ARRAY_AGG(DISTINCT JSONB_BUILD_OBJECT(
                    'mission_id', m.mission_id,
                    'mission_name', m.mission_name,
                    'involvement_summary', em.involvement_summary
        )) FILTER (WHERE m.mission_id IS NOT NULL) AS missions
    FROM 
        employees e
    LEFT JOIN departments d ON e.department_id = d.department_id
    LEFT JOIN employee_designations ed ON e.employee_id = ed.employee_id
    LEFT JOIN designations des ON ed.designation_id = des.designation_id
    LEFT JOIN employee_clearances ecl ON e.employee_id = ecl.employee_id
    LEFT JOIN clearances cl ON ecl.clearance_id = cl.clearance_id
    LEFT JOIN employee_missions em ON e.employee_id = em.employee_id
    LEFT JOIN missions m ON em.mission_id = m.mission_id
    WHERE 
        e.employee_id IN (SELECT employee_id FROM matched_employees)
    GROUP BY 
        e.employee_id, d.department_id
)
SELECT * FROM aggregated_info;



PREPARE search_department_details(text) AS
WITH matched_departments AS (
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
    d.department_id IN (SELECT department_id FROM matched_departments)
GROUP BY 
    d.department_id,
    e.employee_id;


PREPARE search_origin_details(text) AS
WITH matched_origins AS (
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
        sm.origin_id
    FROM 
        specimen_missions sm
    JOIN 
        specimens s ON sm.specimen_id = s.specimen_id
    WHERE 
        s.search_vector @@ TO_TSQUERY($1)
)
SELECT 
    o.origin_id,
    o.origin_name,
    o.discovery_date,
    o.description,
    o.notes,
    ARRAY_AGG(DISTINCT JSONB_BUILD_OBJECT(
                'mission_id', m.mission_id,
                'mission_name', m.mission_name
    )) FILTER (WHERE m.mission_id IS NOT NULL) AS missions,
    ARRAY_AGG(DISTINCT JSONB_BUILD_OBJECT(
                'specimen_id', s.specimen_id,
                'specimen_name', s.specimen_name
    )) FILTER (WHERE s.specimen_id IS NOT NULL) AS specimens
FROM 
    origins o
LEFT JOIN mission_origins mo ON o.origin_id = mo.origin_id
LEFT JOIN missions m ON m.mission_id = mo.mission_id
LEFT JOIN specimen_missions sm ON sm.mission_id = m.mission_id
LEFT JOIN specimens s ON s.specimen_id = sm.specimen_id
WHERE 
    o.origin_id IN (SELECT origin_id FROM matched_origins)
    OR o.origin_id IN (SELECT origin_id FROM matched_missions)
    OR o.origin_id IN (SELECT origin_id FROM matched_specimens)
GROUP BY 
    o.origin_id;


PREPARE search_mission_details(text) AS
WITH matched_missions AS (
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
    m.description,
    m.notes,
    JSONB_BUILD_OBJECT(
        'commander_id', m.commander_id,
        'commander_first_name', commander.first_name,
        'commander_last_name', commander.last_name
    ) AS commander,
    JSONB_BUILD_OBJECT(
        'supervisor_id', m.supervisor_id,
        'supervisor_first_name', supervisor.first_name,
        'supervisor_last_name', supervisor.last_name
    ) AS supervisor,
    ARRAY_AGG(DISTINCT JSONB_BUILD_OBJECT(
                'department_id', d.department_id,
                'department_name', d.department_name
    )) FILTER (WHERE d.department_id IS NOT NULL) AS departments,
    ARRAY_AGG(DISTINCT JSONB_BUILD_OBJECT(
                'operative_id', operatives.employee_id,
                'operative_first_name', operatives.first_name,
                'operative_last_name', operatives.last_name,
                'involvement_summary', em.involvement_summary
    )) FILTER (WHERE operatives.employee_id IS NOT NULL) AS operatives,
    ARRAY_AGG(DISTINCT JSONB_BUILD_OBJECT(
                'origin_id', o.origin_id,
                'origin_name', o.origin_name
    )) FILTER (WHERE o.origin_id IS NOT NULL) AS origins,
    ARRAY_AGG(DISTINCT JSONB_BUILD_OBJECT(
                'specimen_id', s.specimen_id,
                'specimen_name', s.specimen_name,
                'involvement_summary', sm.involvement_summary
    )) FILTER (WHERE s.specimen_id IS NOT NULL) AS specimens
FROM 
    missions m
LEFT JOIN employees commander ON commander.employee_id = m.commander_id
LEFT JOIN employees supervisor ON supervisor.employee_id = m.supervisor_id
LEFT JOIN employee_missions em ON em.mission_id = m.mission_id
LEFT JOIN employees operatives ON operatives.employee_id = em.employee_id
LEFT JOIN mission_origins mo ON mo.mission_id = m.mission_id
LEFT JOIN origins o ON o.origin_id = mo.origin_id
LEFT JOIN specimen_missions sm ON sm.mission_id = m.mission_id
LEFT JOIN specimens s ON s.specimen_id = sm.specimen_id
LEFT JOIN department_missions dm ON dm.mission_id = m.mission_id
LEFT JOIN departments d ON d.department_id = dm.department_id
WHERE 
    m.mission_id IN (SELECT mission_id FROM matched_missions)
    OR m.mission_id IN (SELECT mission_id FROM matched_commanders)
    OR m.mission_id IN (SELECT mission_id FROM matched_supervisors)
GROUP BY 
    m.mission_id, 
    commander.first_name, 
    commander.last_name, 
    supervisor.first_name, 
    supervisor.last_name;


PREPARE search_specimen_details(text) AS
WITH matched_specimens AS (
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
    s.origin_id,
    s.mission_id,
    s.threat_level,
    s.acquisition_date,
    s.notes,
    s.description,
    ARRAY_AGG(DISTINCT JSONB_BUILD_OBJECT(
                'containment_status_id', cs.containment_status_id,
                'containment_status_name', cs.status_name
    )) FILTER (WHERE cs.containment_status_id IS NOT NULL) AS containment_statuses,
    ARRAY_AGG(DISTINCT JSONB_BUILD_OBJECT(
                'mission_id', m.mission_id,
                'mission_name', m.mission_name,
                'involvement_summary', sm.involvement_summary
    )) FILTER (WHERE m.mission_id IS NOT NULL) AS missions,
    ARRAY_AGG(DISTINCT JSONB_BUILD_OBJECT(
                'researcher_id', researcher.department_id,
                'researcher_first_name', researcher.first_name,
                'researcher_last_name', researcher.last_name
    )) FILTER (WHERE researcher.employee_id IS NOT NULL) AS researchers
FROM 
    specimens s
LEFT JOIN specimen_containment_statuses scs ON s.specimen_id = scs.specimen_id
LEFT JOIN containment_statuses cs ON cs.containment_status_id = scs.containment_status_id
LEFT JOIN specimen_missions sm ON sm.specimen_id = s.specimen_id
LEFT JOIN missions m ON m.mission_id = sm.mission_id
LEFT JOIN researcher_specimens rs ON rs.specimen_id = s.specimen_id
LEFT JOIN employees researcher ON researcher.employee_id = rs.employee_id
WHERE 
    s.specimen_id IN (SELECT specimen_id FROM matched_specimens)
    OR s.specimen_id IN (SELECT specimen_id FROM matched_missions)
    OR s.specimen_id IN (SELECT specimen_id FROM matched_researchers)
GROUP BY 
    s.specimen_id;
