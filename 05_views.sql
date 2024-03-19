/*
 * Considerations for Database Design Decision:
 *
 * 1. Dataset Size and Freshness:
 *    - The database's dataset is relatively small, which facilitates efficient query execution without the need for pre-aggregation or caching.
 *    - It is imperative that the data remains up-to-date as often as possible to reflect real-time changes and ensure data accuracy for operational and analytical purposes.
 *
 * 2. Organizational Growth Projections:
 *    - The fictional organization represented by this database is expected to experience a slow growth rate in employee population over several decades.
 *    - This gradual growth trajectory suggests that the dataset will remain manageable without necessitating the complexities introduced by materialized views and the overhead of routine updates.
 *
 * Decision Rationale:
 * Given the considerations above, I have opted for implementing simple views rather than materialized views. 
 * This decision is underpinned by the current and projected dataset size, the requirement for data to be as current as possible, and the anticipated slow growth rate of the organization's employee base. 
 * Simple views will thus provide the necessary data access efficiency and currency without the added complexity and maintenance overhead of materialized views and their routine updates.
 */

CREATE OR REPLACE VIEW employee_details AS
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
    )) AS designations,
    ARRAY_AGG(DISTINCT cl.clearance_name) AS clearances,
    ARRAY_AGG(DISTINCT JSONB_BUILD_OBJECT(
                'mission_id', m.mission_id,
                'mission_name', m.mission_name,
                'involvement_summary', em.involvement_summary
    )) AS missions
FROM employees e
INNER JOIN departments d ON d.department_id = e.department_id
LEFT JOIN employee_designations ed ON ed.employee_id = e.employee_id
INNER JOIN designations des ON des.designation_id = ed.designation_id
LEFT JOIN employee_clearances ecl ON ecl.employee_id = e.employee_id
INNER JOIN clearances cl ON cl.clearance_id = ecl.clearance_id
LEFT JOIN employee_missions em ON em.employee_id = e.employee_id
INNER JOIN missions m ON m.mission_id = em.mission_id
GROUP BY
    e.employee_id, d.department_id;

CREATE OR REPLACE VIEW department_details AS
SELECT
    d.department_id,
    d.department_name,
    JSONB_BUILD_OBJECT(
        'director_id', d.director_id,
        'director_first_name', e.first_name,
        'director_last_name', e.last_name
    ) AS director,
    d.description
FROM departments d
LEFT JOIN employees e ON e.employee_id = d.director_id
GROUP BY 
    d.department_id,
    e.employee_id;

CREATE OR REPLACE VIEW origin_details AS
SELECT
    o.origin_id,
    o.origin_name,
    o.discovery_date,
    o.description,
    o.notes,
    ARRAY_AGG(DISTINCT JSONB_BUILD_OBJECT(
                'mission_id', m.mission_id,
                'mission_name', m.mission_name
    )) AS missions,
    ARRAY_AGG(DISTINCT JSONB_BUILD_OBJECT(
                'specimen_id', s.specimen_id,
                'specimen_name', s.specimen_name
    )) AS specimens
FROM origins o
LEFT JOIN mission_origins mo ON mo.origin_id = o.origin_id
INNER JOIN missions m ON m.mission_id = mo.mission_id
LEFT JOIN specimen_missions sm ON sm.mission_id = m.mission_id
INNER JOIN specimens s ON s.specimen_id = sm.specimen_id
GROUP BY 
    o.origin_id;

CREATE OR REPLACE VIEW mission_details AS
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
    )) AS departments,
    ARRAY_AGG(DISTINCT JSONB_BUILD_OBJECT(
                'operative_id', operatives.employee_id,
                'operative_first_name', operatives.first_name,
                'operative_last_name', operatives.last_name,
                'involvement_summary', em.involvement_summary
    )) AS operatives,
    ARRAY_AGG(DISTINCT JSONB_BUILD_OBJECT(
                'origin_id', o.origin_id,
                'origin_name', o.origin_name
    )) AS origins,
    ARRAY_AGG(DISTINCT JSONB_BUILD_OBJECT(
                'specimen_id', s.specimen_id,
                'specimen_name', s.specimen_name,
                'involvement_summary', sm.involvement_summary
    )) AS specimens
FROM missions m
LEFT JOIN employees commander ON commander.employee_id = m.commander_id
LEFT JOIN employees supervisor ON supervisor.employee_id = m.supervisor_id
LEFT JOIN employee_missions em ON em.mission_id = m.mission_id
INNER JOIN employees operatives ON operatives.employee_id = em.employee_id
LEFT JOIN mission_origins mo ON mo.mission_id = m.mission_id
INNER JOIN origins o ON o.origin_id = mo.origin_id
LEFT JOIN specimen_missions sm ON sm.mission_id = m.mission_id
INNER JOIN specimens s ON s.specimen_id = sm.specimen_id
LEFT JOIN department_missions dm ON dm.mission_id = m.mission_id
INNER JOIN departments d ON d.department_id = dm.department_id
GROUP BY 
    m.mission_id, 
    commander.first_name, 
    commander.last_name, 
    supervisor.first_name, 
    supervisor.last_name;

CREATE OR REPLACE VIEW specimen_details AS
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
    )) AS containment_statuses,
    ARRAY_AGG(DISTINCT JSONB_BUILD_OBJECT(
                'mission_id', m.mission_id,
                'mission_name', m.mission_name,
                'involvement_summary', sm.involvement_summary
    )) AS missions,
    ARRAY_AGG(DISTINCT JSONB_BUILD_OBJECT(
                'researcher_id', researcher.department_id,
                'researcher_first_name', researcher.first_name,
                'researcher_last_name', researcher.last_name
    )) AS researchers
FROM specimens s
LEFT JOIN specimen_containment_statuses scs ON scs.specimen_id = s.specimen_id
INNER JOIN containment_statuses cs ON cs.containment_status_id = scs.containment_status_id
LEFT JOIN specimen_missions sm ON sm.specimen_id = s.specimen_id
INNER JOIN missions m ON m.mission_id = sm.mission_id
LEFT JOIN researcher_specimens rs ON rs.specimen_id = s.specimen_id
INNER JOIN employees researcher ON researcher.employee_id = rs.employee_id
GROUP BY 
    s.specimen_id;