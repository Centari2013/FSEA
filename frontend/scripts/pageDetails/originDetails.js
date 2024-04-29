import { fetchOriginDetails } from "../api_access/originDetails";
import { setWindowOpener, setToggle } from "../utility";

document.addEventListener('DOMContentLoaded', async () => {
    setWindowOpener()
    const urlParams = new URLSearchParams(window.location.search);
    const originId = urlParams.get('origin_id');
    const originContainer = document.getElementById('originContainer');

    if (!originId) return;

    try {
        const originData = await fetchOriginDetails(originId);

        const originContent = generateOriginContent(originData);

        originContainer.innerHTML = originContent;

        setToggle();
    } catch (error) {
        console.error('Error fetching origin data:', error);
        originContainer.innerHTML = `<p>Error loading origin details.</p>`;
    }
});

function generateOriginContent(originData) {
    const missionsContent = originData.missions.map(mission => `
        <tr>
            <td>${mission.missionId}</td>
            <td>${mission.missionName}</td>
            <td>${mission.startDate}</td>
            <td>${mission.endDate}</td>
        </tr>
    `).join('');

    const specimensContent = originData.specimens.map(specimen => `
        <tr>
            <td>${specimen.specimenId}</td>
            <td>${specimen.specimenName}</td>
            <td>${specimen.acquisitionDate}</td>
        </tr>
    `).join('');

    const notesContent = originData.notes ? originData.notes.map(note => `
        <tr>
            <td>${note.timestamp}</td>
            <td>${note.note}</td>
        </tr>
    `).join('') : '';

    return `
        <div style="position: relative;">
            <button id="generatePDFButton" style="position: absolute; top: 0; right: 0; margin: 10px;" class="btn btn-primary">
                Generate PDF
            </button>
            <h1>${originData.originName}</h1>
            <p><strong>Origin ID:</strong> ${originData.originId}</p>
            <p><strong>Discovery Date:</strong> ${originData.discoveryDate}</p>
            <p><strong>Description:</strong> ${originData.description}</p>
        </div>

        <h3>Missions</h3>
        <table class="table">
            <thead>
                <tr>
                    <th>Mission ID</th>
                    <th>Mission Name</th>
                    <th>Start Date</th>
                    <th>End Date</th>
                </tr>
            </thead>
            <tbody>${missionsContent}</tbody>
        </table>

        <h3>Specimens</h3>
        <table class="table">
            <thead>
                <tr>
                    <th>Specimen ID</th>
                    <th>Specimen Name</th>
                    <th>Acquisition Date</th>
                </tr>
            </thead>
            <tbody>${specimensContent}</tbody>
        </table>

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
}
