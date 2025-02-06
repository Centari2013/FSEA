import { fetchDepartmentDetails } from "../api_access/fetchDepartmentDetails";
import { setToggle, setWindowOpener } from "../utility";

document.addEventListener('DOMCon tentLoaded', async () => {
    setWindowOpener();
    const departmentDetailsContainer = document.getElementById('departmentDetailsContainer');
    const urlParams = new URLSearchParams(window.location.search);
    const departmentId = urlParams.get('department_id');

    if (!departmentId) return;

    try {
        const departmentData = await fetchDepartmentDetails(departmentId);


        const departmentContent = generateDepartmentContent(departmentData);
        departmentDetailsContainer.innerHTML = departmentContent;
        setToggle();
    } catch (error) {
        console.error('Failed to load department details:', error);
        departmentDetailsContainer.innerHTML = `<p>Error loading department details.</p>`;
    }
});

function generateDepartmentContent(departmentData) {
    console.log('Generating content for:', departmentData);
    if (!departmentData.missions || !Array.isArray(departmentData.missions)) {
        console.error('Missions data is invalid:', departmentData.missions);
        return `<p>Error: Invalid missions data.</p>`;
    }
    const missionsContent = departmentData.missions.map(mission => `
        <tr>
            <td>${mission.missionId}</td>
            <td>${mission.missionName}</td>
        </tr>
    `).join('');

    departmentData.employees.toSorted(function(a, b) {
        var textA = a.lastName.toUpperCase();
        var textB = b.lastName.toUpperCase();
        return (textA < textB) ? -1 : (textA > textB) ? 1 : 0;
    });

    const employeesContent = departmentData.employees.map(emp => `
        <tr>
            <td>${emp.lastName}</td>
            <td>${emp.firstName}</td>
            <td>${emp.designations.map(desig => desig.abbreviation).join(', ')}</td>
        </tr>
    `).join('');

    return `
    <div style="position: relative;">
        <button id="generatePDFButton" style="position: absolute; top: 0; right: 0; margin: 10px;" class="btn btn-primary">
            Generate PDF
        </button>
        <h1>${departmentData.departmentName} Department</h1>
        <p><strong>Director:</strong> ${departmentData.director.firstName} ${departmentData.director.lastName} (ID: ${departmentData.director.employeeId})</p>
        <p><strong>Description:</strong> ${departmentData.description}</p>
        
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
                    </tr>
                </thead>
                <tbody>${missionsContent}</tbody>
            </table>
        </div>
        <h3>Employees
        <button class="btn btn-link" type="button" data-bs-toggle="collapse" data-bs-target="#employeesCollapse" aria-expanded="false" aria-controls="missionsCollapse">
        See More
    </button>
        </h3>
        <div class="collapse" id="employeesCollapse">
            <table class="table">
                <thead>
                    <tr>
                        <th>Last Name</th>
                        <th>First Name</th>
                        <th>Designation</th>
                    </tr>
                </thead>
                <tbody>${employeesContent}</tbody>
            </table>
            </div>
    `;
}
