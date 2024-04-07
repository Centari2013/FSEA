const api = import.meta.env.VITE_API_ENDPOINT;

document.addEventListener('DOMContentLoaded', async () => {
    const employeeDetailsContainer = document.getElementById('employeeDetailsContainer');
    const urlParams = new URLSearchParams(window.location.search);
    const employee_id = urlParams.get('employee_id');

    if (!employee_id) return;

    try {
        const employeeData = await fetchEmployeeData(employee_id);
        // Fetch designation IDs for the employee and then the details
        const designationIdsResponse = await fetchEmployeeDesignationIds(employee_id);
        const designationIds = designationIdsResponse.designations.map(item => item.designation_id);
        const designationDetails = await fetchDesignationDetails(designationIds);

        const missions = await fetchEmployeeMissions(employee_id);
        const medicalRecords = await fetchEmployeeMedicalRecord(employee_id);
        const clearances = await fetchEmployeeClearances(employee_id);

        // Generate the HTML content for employee details
        const employeeContent = generateEmployeeContent(employeeData, designationDetails, missions, medicalRecords, clearances);
        
        // Insert the generated content into the page
        employeeDetailsContainer.innerHTML = employeeContent;
    } catch (error) {
        console.error('Error fetching employee data:', error);
        employeeDetailsContainer.innerHTML = `<p>Error loading employee details.</p>`;
    }
});


async function fetchEmployeeData(employee_id) {
    const response = await fetch(`${api}/employees/${employee_id}`, {
        method: 'GET',
        headers: { 'Content-Type': 'application/json' },
    });
    if (!response.ok) throw new Error('Failed to fetch employee data');
    return response.json();
}

async function fetchDesignationDetails(designationIds) {
    // Join the IDs into a comma-separated string
    console.log(designationIds);
    const idsParam = designationIds.join(',');
    const response = await fetch(`${api}/designations?ids=${idsParam}`, { method: 'GET' });
    if (!response.ok) throw new Error('Failed to fetch designation details');
    return response.json();
}

async function fetchEmployeeDesignationIds(employee_id) {
    const response = await fetch(`${api}/employees/${employee_id}/designations`, { 
        method: 'GET',
        headers: { 'Content-Type': 'application/json' },
    });
    if (!response.ok) throw new Error('Failed to fetch employee designation IDs');
    return response.json(); // This should return an array of objects, e.g., [{designation_id: 1}, {designation_id: 2}]
}



async function fetchEmployeeMissions(employee_id) {
    const response = await fetch(`${api}/employees/${employee_id}/missions`, { method: 'GET' });
    if (!response.ok) throw new Error('Failed to fetch employee missions');
    return response.json();
}

async function fetchEmployeeMedicalRecord(employee_id) {
    const response = await fetch(`${api}/employees/${employee_id}/medical_record`, { method: 'GET' });
    if (!response.ok) throw new Error('Failed to fetch employee medical record');
    return response.json();
}

async function fetchEmployeeClearances(employee_id) {
    const response = await fetch(`${api}/employees/${employee_id}/clearances`, { method: 'GET' });
    if (!response.ok) throw new Error('Failed to fetch employee clearances');
    return response.json();
}

function generateEmployeeContent(employeeData, designationDetails, missions, medicalRecords, clearances) {
    // Convert designation details to readable formats for display
    const designationNames = designationDetails.map(d => `${d.designation_name} (${d.abbreviation})`).join(', ');

    const missionsContent = missions.map(mission => `
        <tr>
            <td>${mission.mission_id}</td>
            <td>${mission.mission_name}</td>
            <td>${mission.involvement_summary}</td>
        </tr>
    `).join('');

    // Assuming the medicalRecords and clearances data structures are directly compatible with how you want to display them
    const medicalDataContent = `
        <p>Blood type: ${medicalRecords.bloodtype}</p>
        <p>Height: ${medicalRecords.height_cm} cm</p>
        <p>Weight: ${medicalRecords.kilograms} kg</p>
        <p>Notes: ${medicalRecords.notes ? medicalRecords.notes : 'None'}</p>
    `;

    const clearancesContent = clearances.map(clearance => `<li>${clearance.clearance_name}: ${clearance.description}</li>`).join('');

    return `
        <h2>Employee Details</h2>
        <p><strong>ID:</strong> ${employeeData.employee_id}</p>
        <p><strong>Name:</strong> ${employeeData.first_name} ${employeeData.last_name}</p>
        <p><strong>Department:</strong> ${employeeData.department_name}</p>
        <p><strong>Designation(s):</strong> ${designationNames}</p>
        <p><strong>Start Date:</strong> ${employeeData.start_date}</p>
        <p><strong>Notes:</strong> ${employeeData.notes ? employeeData.notes : 'None'}</p>
        
        <!-- Clearance Section -->
        <h3>Clearances</h3>
        <ul>${clearancesContent}</ul>
        
        <!-- Missions Section -->
        <h3>Missions</h3>
        <table class="table">
            <thead>
                <tr>
                    <th>Mission ID</th>
                    <th>Mission Name</th>
                    <th>Employee Involvement</th>
                </tr>
            </thead>
            <tbody>${missionsContent}</tbody>
        </table>
        
        <!-- Medical Data Section -->
        <h3>Medical Data <button class="btn btn-link" type="button" data-bs-toggle="collapse" data-bs-target="#medicalDataCollapse" aria-expanded="false" aria-controls="medicalDataCollapse">Toggle</button></h3>
        <div class="collapse" id="medicalDataCollapse">
            <div class="card card-body">
                ${medicalDataContent}
            </div>
        </div>
    `;
}
