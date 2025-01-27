import { fetchMissionDetails } from "../api_access/missionDetails";
import { setWindowOpener, setToggle } from "../utility";

document.addEventListener('DOMContentLoaded', async () => {
    const urlParams = new URLSearchParams(window.location.search);
    const missionId = urlParams.get('mission_id');
    const missionsContainer = document.getElementById('missionsContainer');
    const missionDetails = await fetchMissionDetails([missionId]); // example mission ID array
    
    const missionsContent = missionDetails.map(mission => {
        const notesContent = mission.notes ? JSON.parse(mission.notes).map(note => `<tr><td>${note.timestamp}</td> <td>${note.note}</td></tr>`).join(''): "";
        
        return `
            <div style="position: relative;">
                <button id="generatePDFButton" style="position: absolute; top: 0; right: 0; margin: 10px;" class="btn btn-primary">
                    Generate PDF
                </button>
                <h1>${mission.missionName}</h1>
                <p><strong>Mission ID:</strong> ${mission.missionId}</p>
                <p><strong>Departments Involved:</strong> ${mission.departments.map(dept => dept.departmentName).join(', ')}</p>
                <p><strong>Start Date:</strong> ${mission.startDate}</p>
                <p><strong>End Date:</strong> ${mission.endDate}</p>
                <p><strong>Commander:</strong> ${mission.commander.firstName} ${mission.commander.lastName}</p>
                <p><strong>Supervisor:</strong> ${mission.supervisor.firstName} ${mission.supervisor.lastName}</p>
                <p><strong>Description:</strong> ${mission.description}</p>
            
            </div>

            <p><strong>Origins:</strong><br>
                <ul>
                    ${mission.origins.map(origin => `<li>${origin.originId} - ${origin.originName}</li>`).join('')}
                </ul>
            </p>

            <p><strong>Employees Involved:</strong><br>
                <ul>
                    ${mission.employees.map(emp => `<li>${emp.employeeId} - ${emp.firstName} ${emp.lastName}</li>`).join('')}
                </ul>
            </p>

            <p><strong>Notes</strong><br>
            <table class="table">
                <thead>
                    <tr>
                        <th>Timestamp</th>
                        <th>Note</th>
                    </tr>
                </thead>
                <tbody>${notesContent}</tbody>
            </table>
            
        `;
    }).join('');

    missionsContainer.innerHTML = missionsContent;
    setWindowOpener();
    setToggle();
});
