import { fetchSpecimenDetails } from "../api_access/specimenDetails";
import { setWindowOpener, setToggle } from "../utility";

document.addEventListener('DOMContentLoaded', async () => {
    const urlParams = new URLSearchParams(window.location.search);
    const specimenId = urlParams.get('specimen_id');
    const specimenContainer = document.getElementById('specimenContainer');
    const specimen = await fetchSpecimenDetails(specimenId);

 
    const notesContent = specimen.notes ? JSON.parse(specimen.notes).map(note => `<tr><td>${note.timestamp}</td> <td>${note.note}</td></tr>`).join('') : "";

    const specimenContent = `
        <div style="position: relative;">
            <button id="generatePDFButton" style="position: absolute; top: 0; right: 0; margin: 10px;" class="btn btn-primary">
                Generate PDF
            </button>
            <h1>${specimen.specimenName}</h1>
            <p><strong>Specimen ID:</strong> ${specimen.specimenId}</p>
            <p><strong>Origin ID:</strong> ${specimen.originId}</p>
            <p><strong>Mission ID:</strong> ${specimen.missionId}</p>
            <p><strong>Threat Level:</strong> ${specimen.threatLevel}</p>
            <p><strong>Acquisition Date:</strong> ${specimen.acquisitionDate}</p>
            <p><strong>Description:</strong> ${specimen.description}</p>
            <p><strong>Containment Statuses:</strong> ${specimen.containmentStatuses.map(status => status.statusName).join(', ')}</p>
        </div>

        <p><strong>Researchers Involved:</strong><br>
            <ul>
                ${specimen.researchers.map(res => `<li>${res.employeeId} - ${res.firstName} ${res.lastName}</li>`).join('')}
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
    

    specimenContainer.innerHTML = specimenContent;
    setWindowOpener();
    setToggle();
});
