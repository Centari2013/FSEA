import { fetchEmployeeData } from "./api_access/employeeDetails";
import { setWindowOpener } from "./utility";

document.addEventListener('DOMContentLoaded', async () => {
    setWindowOpener();
    const employeeDetailsContainer = document.getElementById('employeeDetailsContainer');
    const urlParams = new URLSearchParams(window.location.search);
    const employee_id = urlParams.get('employee_id');

    if (!employee_id) return;

    try {
        const employeeData = await fetchEmployeeData(employee_id);
        console.log(employeeData);
      
    

        // Generate the HTML content for employee details
        const employeeContent = generateEmployeeContent(employeeData);
        
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



function generateEmployeeContent(employeeData) {

    const missionsContent = employeeData.missions.map(mission => {
        
        return `
            <tr>
                <td>${mission.missionId}</td>
                <td>${mission.missionName}</td>
                <td>${mission.involvementSummary ? mission.involvementSummary: ""}</td>
            </tr>`;
    }).join('');

    const medicalRecord = employeeData.medicalRecord;
    const medicalNotesContent = medicalRecord.notes && medicalRecord.notes.length > 0
        ? JSON.parse(medicalRecord.notes).map(noteObj => `<li><strong>${noteObj.timestamp}:</strong>&nbsp;&nbsp;&nbsp;&nbsp;${noteObj.note}</li>`).join('')
        : '<li>None</li>';


    const medicalDataContent = `
        <div class="collapse" id="medicalDataCollapse">
            <div class="card card-body">
                <p><strong>Blood type:</strong> ${medicalRecord.bloodtype}</p>
                <p><strong>Height:</strong> ${medicalRecord.heightCm} cm</p>
                <p><strong>Weight:</strong> ${medicalRecord.kilograms} kg</p>
                <p><strong>Notes:</strong></p>
                <ul>${medicalNotesContent}</ul>
            </div>
        </div>`;

    const clearancesContent = employeeData.clearances.map(clearance => `<li><strong>${clearance.clearanceName}:</strong> ${clearance.description}</li>`).join('');

    const designationNames = employeeData.designations.map(d => `${d.designationName} (${d.abbreviation})`).join(', ');
    return `

    <div style="position: relative;">
    <button id="generatePDFButton" style="position: absolute; top: 0; right: 0; margin: 10px;" class="btn btn-primary">
        Generate PDF
    </button>
    <h2>Employee Details</h2>
    <p><strong>ID:</strong> ${employeeData.employeeId}</p>
    <p><strong>Name:</strong> ${employeeData.firstName} ${employeeData.lastName}</p>
        <p><strong>Department:</strong> ${employeeData.department.departmentName}</p>
        <p><strong>Designation(s):</strong> ${designationNames}</p>
        <p><strong>Start Date:</strong> ${employeeData.startDate}</p>
        <p><strong>End Date:</strong> ${employeeData.endDate}</p>
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



