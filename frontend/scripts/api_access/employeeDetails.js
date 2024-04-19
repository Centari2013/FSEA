const api = import.meta.env.VITE_API_ENDPOINT;
export async function fetchEmployeeData(employee_id) {
    const response = await fetch(api, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
            query: `
                query Employee($employeeId: String!){
                    employee(employeeId: $employeeId) {
                        departmentId
                        firstName
                        lastName
                        startDate
                        endDate
                    }
                }`,
            variables: {employeeId: employee_id}
        }),
    });
    if (!response.ok) throw new Error('Failed to fetch employee data');
    const jsonResponse = await response.json();
    return jsonResponse.data.employee;
}


export async function fetchDesignationDetails(designationIds) {
    // Join the IDs into a comma-separated string
    const response = await fetch(api, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
            query: `
                query Designation($designationIds: [Int!]){
                    designation(designationIds: $designationIds) {
                        designationName
                        abbreviation
                    }
                }`,
            variables: {designationIds: designationIds}
        }),
    });
    if (!response.ok) {
        if (response.status === 404) {
            console.log('No designations found for employee');
            return {"designations": []};
        }
        throw new Error('Failed to fetch designation details');
    }
    return response.json();
}


export async function fetchDepartmentData(department_id) {
    const response = await fetch(api, {
        method: 'POST', 
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            query: `
                query Department($departmentId: Int!){
                    department(departmentId: $departmentId){
                        departmentName
                    }
                }`,
            variables: {'departmentId': department_id}
        })
    });
    if (!response.ok) throw new Error('Failed to fetch department data');
    const jsonResponse = await response.json();
    return jsonResponse.data.department;
}

export async function fetchEmployeeDesignationIds(employee_id) {
    const query = `
        query GetEmployeeDesignations($employeeId: Int!) {
            employeeDesignations(employee_id: $employeeId) {
                designation_id
            }
        }
    `;

    const variables = { employeeId: employee_id };
    const response = await fetch(`${api}/graphql`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ query, variables })
    });

    if (!response.ok) throw new Error('Failed to fetch employee designation IDs');
    return response.json();
}

export async function fetchEmployeeMissionIds(employee_id) {
    const query = `
        query GetEmployeeMissions($employeeId: Int!) {
            employeeMissions(employee_id: $employeeId) {
                mission_id
            }
        }
    `;

    const variables = { employeeId: employee_id };
    const response = await fetch(`${api}/graphql`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' }
    });

    if (!response.ok) {
        if (response.status === 404) {
            console.log('No missions found for employee');
            return {"missions": []};
        }
        throw new Error('Failed to fetch employee missions');
    }
    return response.json();
}


export async function fetchEmployeeMissionData(missionIds) {
    const query = `
        query GetMissionDetails($missionIds: [Int!]!) {
            missions(mission_ids: $missionIds) {
                mission_id
                // other details
            }
        }
    `;

    const variables = { missionIds: missionIds };
    const response = await fetch(`${api}/graphql`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ query, variables })
    });

    if (!response.ok) throw new Error('Failed to fetch mission details');
    return response.json();
}


export async function fetchEmployeeMedicalRecord(employee_id) {
    const query = `
        query GetEmployeeMedicalRecord($employeeId: Int!) {
            employeeMedicalRecord(employee_id: $employeeId) {
                record_id
                // additional medical record fields
            }
        }
    `;

    const variables = { employeeId: employee_id };
    const response = await fetch(`${api}/graphql`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ query, variables })
    });

    if (!response.ok) throw new Error('Failed to fetch employee medical record');
    return response.json();
}


export async function fetchEmployeeClearances(employee_id) {
    const query = `
        query GetEmployeeClearances($employeeId: Int!) {
            employeeClearances(employee_id: $employeeId) {
                clearance_id
                // additional clearance fields
            }
        }
    `;

    const variables = { employeeId: employee_id };
    const response = await fetch(`${api}/graphql`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' }
    });

    if (!response.ok) {
        if (response.status === 404) {
            console.log('No clearances found for employee');
            return [];
        }
        throw new Error('Failed to fetch employee clearances');
    }
    return response.json();
}


export async function fetchClearanceData(clearanceIds) {
    const query = `
        query GetClearanceDetails($clearanceIds: [Int!]!) {
            clearances(clearance_ids: $clearanceIds) {
                clearance_id
                // other details
            }
        }
    `;

    const variables = { clearanceIds: clearanceIds };
    response = await fetch(`${api}/graphql`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ query, variables })
    });

    if (!response.ok) {
        if (response.status === 404) {
            console.log('No clearances found for employee');
            return [];
        }
        throw new Error('Failed to fetch clearance details');
    }
    return response.json();
}
