const api = import.meta.env.VITE_API_ENDPOINT;
export async function fetchEmployeeData(employee_id) {
    const response = await fetch(`${api}/employees/${employee_id}`, {
        method: 'GET',
        headers: { 'Content-Type': 'application/json' },
    });
    if (!response.ok) throw new Error('Failed to fetch employee data');
    return response.json();
}

export async function fetchDesignationDetails(designationIds) {
    // Join the IDs into a comma-separated string
    const idsParam = designationIds.join(',');
    const response = await fetch(`${api}/designations?ids=${idsParam}`, 
        { method: 'GET',
        headers: { 'Content-Type': 'application/json' }, });
    if (!response.ok) {
        if (response.status === 404) {
            console.log('No designations found for employee');
            return {"designations": []};
        }
        throw new Error('Failed to fetch designation details');
    }
    return response.json();
}

export async function fetchEmployeeDesignationIds(employee_id) {
    const response = await fetch(`${api}/employees/${employee_id}/designations`, { 
        method: 'GET',
        headers: { 'Content-Type': 'application/json' },
    });
    if (!response.ok) throw new Error('Failed to fetch employee designation IDs');
    return response.json(); // This should return an array of objects, e.g., [{designation_id: 1}, {designation_id: 2}]
}



export async function fetchEmployeeMissionIds(employee_id) {
    const response = await fetch(`${api}/employees/${employee_id}/missions`, { method: 'GET' });
    if (!response.ok){
        if (response.status === 404){
            console.log('No missions found for employee');
            return {"missions": []};
        }

        throw new Error('Failed to fetch employee missions');
    }
    return response.json();
}

export async function fetchEmployeeMissionData(missionIds) {
    const idsParam = missionIds.join(',');
    const response = await fetch(`${api}/missions?ids=${idsParam}`, 
        { method: 'GET',
        headers: { 'Content-Type': 'application/json' }, });
    if (!response.ok) {
        if (response.status === 404) {
            console.log('No missions found for employee');
            return {"missions": []};
        }
        throw new Error('Failed to fetch mission details');
    }
    return response.json();
}


export async function fetchEmployeeMedicalRecord(employee_id) {
    const response = await fetch(`${api}/employees/${employee_id}/medical_record`, { method: 'GET' });
    if (!response.ok) throw new Error('Failed to fetch employee medical record');
    return response.json();
}

export async function fetchEmployeeClearances(employee_id) {
    const response = await fetch(`${api}/employees/${employee_id}/clearances`, { method: 'GET' });
    if (!response.ok) {
        if (response.status === 404){
            console.log('No clearances found for employee');
            return [];
        }
        throw new Error('Failed to fetch employee clearances');
    }
    return response.json();
}

export async function fetchClearanceData(clearanceIds) {
    const idsParam = clearanceIds.join(',');
    const response = await fetch(`${api}/clearances?ids=${idsParam}`, 
        { method: 'GET',
        headers: { 'Content-Type': 'application/json' }, });
    if (!response.ok) {
        if (response.status === 404) {
            console.log('No clearances found for employee');
            return [];
        }
        throw new Error('Failed to fetch clearance details');
    }
    return response.json();

    
}

export async function fetchDepartmentData(department_id) {
    const response = await fetch(api, { method: 'GET', 
                                        headers: {
                                            'Content-Type': 'application/json'
                                        },
                                        body: JSON.stringify({
                                            query: `query {
                                                department($departmentId: Int!){
                                                    departmentName
                                                }
                                            }`,
                                            variables: {'departmentId': department_id}
                                        })});
    if (!response.ok) throw new Error('Failed to fetch employee department');
    return response.json();
}