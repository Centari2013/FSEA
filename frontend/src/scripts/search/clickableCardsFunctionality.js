export function setupEventListeners() {
    document.querySelectorAll('.clickable-card').forEach(card => {
        card.addEventListener('click', function() {
            const card_type = card.getAttribute('data-type');
            const id = card.getAttribute('data-id');
            openDetailsPage(card_type, id);
        });
    });
}

function openDetailsPage(card_type, id) {
    switch (card_type) {
        case 'employee': window.open(`/employeeDetails.html?employee_id=${id}`, '_blank'); break;
        case 'department': window.open(`/departmentDetails.html?department_id=${id}`, '_blank'); break;
        case 'mission': window.open(`/missionDetails.html?mission_id=${id}`, '_blank'); break;
        case 'specimen': window.open(`/specimenDetails.html?specimen_id=${id}`, '_blank'); break;
        case 'origin': window.open(`/originDetails.html?origin_id=${id}`, '_blank'); break;
        default: console.log('Unknown type');
    }
}