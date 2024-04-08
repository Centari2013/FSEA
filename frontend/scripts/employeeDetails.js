import * as emp_api from "./api_access/employee";
import { fetchDepartmentData } from "./api_access/department";


document.addEventListener('DOMContentLoaded', async () => {
    const employeeDetailsContainer = document.getElementById('employeeDetailsContainer');
    const urlParams = new URLSearchParams(window.location.search);
    const employee_id = urlParams.get('employee_id');

    if (!employee_id) return;

    try {
        const employeeData = await emp_api.fetchEmployeeData(employee_id);
        // Fetch designation IDs for the employee and then the details
        const designationIdsResponse = await emp_api.fetchEmployeeDesignationIds(employee_id);
        const designationIds = designationIdsResponse.designations.map(item => item.designation_id);
        const designationDetails = await emp_api.fetchDesignationDetails(designationIds);
        const department = await fetchDepartmentData(employeeData.department_id);

        const missionIdsResponse = await emp_api.fetchEmployeeMissionIds(employee_id);
        const missionIds = missionIdsResponse.missions.map(item => item.mission_id);
        const missions = await emp_api.fetchEmployeeMissionData(missionIds);
        const medicalRecords = await emp_api.fetchEmployeeMedicalRecord(employee_id);
        const clearanceIdsResponse = await emp_api.fetchEmployeeClearances(employee_id);
        const clearanceIds = clearanceIdsResponse.clearances.map(item => item.clearance_id);
        const clearances = await emp_api.fetchClearanceData(clearanceIds);

        console.log(missions)

        // Generate the HTML content for employee details
        const employeeContent = generateEmployeeContent(employeeData, designationDetails, missions, medicalRecords, clearances, department);
        
        // Insert the generated content into the page
        employeeDetailsContainer.innerHTML = employeeContent;
        setToggle();
    } catch (error) {
        console.error('Error fetching employee data:', error);
        employeeDetailsContainer.innerHTML = `<p>Error loading employee details.</p>`;
    }
});



function generateEmployeeContent(employeeData, designationDetails, missions, medicalRecords, clearances, department) {
    // Convert designation details to readable formats for display
    const designationNames = designationDetails.designations.map(d => `${d.designation_name} (${d.abbreviation})`).join(', ');
    
    const missionsContent = missions.missions.map(mission => `
        <tr>
            <td>${mission.mission_id}</td>
            <td>${mission.mission_name}</td>
            <td>${mission.involvement_summary}</td>
        </tr>
    `).join('');

    const employeeNotesContent = employeeData.notes && employeeData.notes.length > 0
    ? employeeData.notes.map(noteObj => `<li><strong>${noteObj.timestamp}:</strong>&nbsp;&nbsp;&nbsp;&nbsp; ${noteObj.note}</li>`).join('')
    : '<li>None</li>';


    const medicalNotesContent = medicalRecords.notes && medicalRecords.notes.length > 0 
    ? medicalRecords.notes.map(noteObj => `<li><strong>${noteObj.timestamp}:</strong>&nbsp;&nbsp;&nbsp;&nbsp; ${noteObj.note}</li>`).join('')
    : '<li>None</li>';


    const medicalDataContent = `
        <p><strong>Blood type:</strong> ${medicalRecords.bloodtype}</p>
        <p><strong>Height:</strong> ${medicalRecords.height_cm} cm</p>
        <p><strong>Weight:</strong> ${medicalRecords.kilograms} kg</p>
        <p><strong>Notes:</strong></p>
        <ul>${medicalNotesContent}</ul>
    `;
    const clearancesContent = clearances.clearances.map(clearance => `<li><strong>${clearance.clearance_name}:</strong> ${clearance.description}</li>`).join('');
    
    return `
        <h2>Employee Details</h2>
        <p><strong>ID:</strong> ${employeeData.employee_id}</p>
        <p><strong>Name:</strong> ${employeeData.first_name} ${employeeData.last_name}</p>
        <p><strong>Department:</strong> ${department.department_name}</p>
        <p><strong>Designation(s):</strong> ${designationNames}</p>
        <p><strong>Start Date:</strong> ${employeeData.start_date}</p>
        <ul><strong>Notes:</strong> ${employeeNotesContent}</ul>
        
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
        <h3>Medical Data 
            <button id="toggleMedicalDataButton" class="btn btn-link" type="button" data-bs-toggle="collapse" data-bs-target="#medicalDataCollapse" aria-expanded="false" aria-controls="medicalDataCollapse">
                See More
            </button>
        </h3>
        <div class="collapse" id="medicalDataCollapse">
            <div class="card card-body">
                ${medicalDataContent}
            </div>
        </div>

    `;
}

function setToggle() {
    const medicalDataCollapse = document.getElementById('medicalDataCollapse');
    const toggleButton = document.getElementById('toggleMedicalDataButton');

    // Listen for the 'show.bs.collapse' event - when the collapsible starts to show
    medicalDataCollapse.addEventListener('show.bs.collapse', () => {
        toggleButton.textContent = 'See Less';
    });

    // Listen for the 'hide.bs.collapse' event - when the collapsible starts to hide
    medicalDataCollapse.addEventListener('hide.bs.collapse', () => {
        toggleButton.textContent = 'See More';
    });
}


