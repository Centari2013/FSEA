import * as emp_api from "./api_access/employee";
import { fetchDepartmentData } from "./api_access/department";
import { setWindowOpener } from "./utility";

document.addEventListener('DOMContentLoaded', async () => {
    setWindowOpener();
    const employeeDetailsContainer = document.getElementById('employeeDetailsContainer');
    const urlParams = new URLSearchParams(window.location.search);
    const employee_id = urlParams.get('employee_id');

    if (!employee_id) return;

    try {
        const employeeData = await emp_api.fetchEmployeeData(employee_id);
        // Fetch designation IDs for the employee and then the details
        const designationIdsResponse = await emp_api.fetchEmployeeDesignationIds(employee_id);
        const designationIds = designationIdsResponse.length > 0 ? designationIdsResponse.designations.map(item => item.designation_id): [];
        const designationDetails = await emp_api.fetchDesignationDetails(designationIds);
        const department = await fetchDepartmentData(employeeData.department_id);

        const missionIdsResponse = await emp_api.fetchEmployeeMissionIds(employee_id);
        console.log(missionIdsResponse)

        const missionIds = missionIdsResponse.missions.length > 0 ? missionIdsResponse.missions.map(item => item.mission_id): [];
        const missions = await emp_api.fetchEmployeeMissionData(missionIds);
        const medicalRecords = await emp_api.fetchEmployeeMedicalRecord(employee_id);
        const clearanceIdsResponse = await emp_api.fetchEmployeeClearances(employee_id);
        const clearanceIds = clearanceIdsResponse.clearances.map(item => item.clearance_id);
        const clearances = await emp_api.fetchClearanceData(clearanceIds);

        // Generate the HTML content for employee details
        const employeeContent = generateEmployeeContent(employeeData, designationDetails, missions, medicalRecords, clearances, department, missionIdsResponse.missions);
        
        // Insert the generated content into the page
        employeeDetailsContainer.innerHTML = employeeContent;

        const pdfButton = document.getElementById('generatePDFButton');
        if (pdfButton) {
            pdfButton.addEventListener('click', function() {
                const complete_missions = missions.missions.map(m => {
                    const summary = missionIdsResponse.missions.find(s => s.mission_id === m.mission_id);
                    m.summary = summary.involvement_summary;
                    return m;
                })

                const data = collectDataForPDF(employeeData, designationDetails, complete_missions, medicalRecords, clearances, department);
                console.log(JSON.stringify(data));  // For now, just log it. Replace with an API call as needed.
                
                // Example: Send data to server
                // fetch('/api/generate-pdf', {
                //     method: 'POST',
                //     headers: {
                //         'Content-Type': 'application/json'
                //     },
                //     body: JSON.stringify(data)
                // }).then(response => response.blob())
                // .then(blob => {
                //     // Handle the blob for downloading or whatever else
                // });
            });
    }

        setToggle();
    } catch (error) {
        console.error('Error fetching employee data:', error);
        employeeDetailsContainer.innerHTML = `<p>Error loading employee details.</p>`;
    }
});



function generateEmployeeContent(employeeData, designationDetails, missions, medicalRecords, clearances, department, missionInvolvementSummaries) {
    const designationNames = designationDetails.designations.map(d => `${d.designation_name} (${d.abbreviation})`).join(', ');

    const missionsContent = missions.missions.map(mission => {
        const summary = missionInvolvementSummaries.find(m => m.mission_id === mission.mission_id);
        return `
            <tr>
                <td>${mission.mission_id}</td>
                <td>${mission.mission_name}</td>
                <td>${summary ? summary.involvement_summary: ""}</td>
            </tr>`;
    }).join('');

    const medicalNotesContent = medicalRecords.notes && medicalRecords.notes.length > 0 
    ? medicalRecords.notes.map(noteObj => `<li><strong>${noteObj.timestamp}:</strong>&nbsp;&nbsp;&nbsp;&nbsp; ${noteObj.note}</li>`).join('')
    : '<li>None</li>';

    const medicalDataContent = `
        <div class="collapse" id="medicalDataCollapse">
            <div class="card card-body">
                <p><strong>Blood type:</strong> ${medicalRecords.bloodtype}</p>
                <p><strong>Height:</strong> ${medicalRecords.height_cm} cm</p>
                <p><strong>Weight:</strong> ${medicalRecords.kilograms} kg</p>
                <p><strong>Notes:</strong></p>
                <ul>${medicalNotesContent}</ul>
            </div>
        </div>`;

    const clearancesContent = clearances.clearances.map(clearance => `<li><strong>${clearance.clearance_name}:</strong> ${clearance.description}</li>`).join('');

    return `

    <div style="position: relative;">
    <button id="generatePDFButton" style="position: absolute; top: 0; right: 0; margin: 10px;" class="btn btn-primary">
        Generate PDF
    </button>
    <h2>Employee Details</h2>
    <p><strong>ID:</strong> ${employeeData.employee_id}</p>
    <p><strong>Name:</strong> ${employeeData.first_name} ${employeeData.last_name}</p>
        <p><strong>Department:</strong> ${department.department_name}</p>
        <p><strong>Designation(s):</strong> ${designationNames}</p>
        <p><strong>Start Date:</strong> ${employeeData.start_date}</p>
    </div>
        
        
        <!-- Clearances Section -->
        <h3>Clearances 
            <button class="btn btn-link" type="button" data-bs-toggle="collapse" data-bs-target="#clearancesCollapse" aria-expanded="false" aria-controls="clearancesCollapse">
                See More
            </button>
        </h3>
        <div class="collapse" id="clearancesCollapse">
            <ul>${clearancesContent}</ul>
        </div>
        
        <!-- Missions Section -->
        <h3>Missions
            <button class="btn btn-link" type="button" data-bs-toggle="collapse" data-bs-target="#missionsCollapse" aria-expanded="false" aria-controls="missionsCollapse">
                See More
            </button>
        </h3>
        <div class="collapse" id="missionsCollapse">
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
        </div>
        
        <!-- Medical Data Section -->
        <h3>Medical Data 
            <button class="btn btn-link" type="button" data-bs-toggle="collapse" data-bs-target="#medicalDataCollapse" aria-expanded="false" aria-controls="medicalDataCollapse">
                See More
            </button>
        </h3>
        ${medicalDataContent}

    `;
}

function collectDataForPDF(employeeData, designationDetails, missions, medicalRecords, clearances, department) {
    const jsonData = {
        employeeData,
        designationDetails,
        missions,
        medicalRecords,
        clearances,
        department
    };
    return jsonData;
}


function setToggle() {
    // Find all collapsible elements with buttons linked to them
    document.querySelectorAll('.btn-link[data-bs-toggle="collapse"]').forEach(button => {
        const targetId = button.getAttribute('data-bs-target');
        const collapseElement = document.querySelector(targetId);

        collapseElement.addEventListener('show.bs.collapse', () => {
            button.textContent = 'See Less'; // Change button text to "See Less" when expanded
        });

        collapseElement.addEventListener('hide.bs.collapse', () => {
            button.textContent = 'See More'; // Change back to "See More" when collapsed
        });
    });
}



