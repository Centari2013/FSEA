import { employeeCard, specimenCard, departmentCard, missionCard, originCard, noResultsCard, cardContainer} from "./cardTemplates";
const api = import.meta.env.VITE_API_ENDPOINT;

export function performSearch(query, page = 1) {
    console.log("Performing search for:", query);
    const payload = {
        "query": query,
        "page": page,  // Added page number to the payload
        "pageSize": 25  // Assuming pageSize is constant, adjust as necessary
    };

    fetch(`${api}/search`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify(payload),
    })
    .then(response => response.json())
    .then(results => {
        const cardsContainer = cardContainer();
        const mainContentArea = document.getElementById('main-content');
        mainContentArea.innerHTML = '';
        if (results["results"] && results["results"].length) {
            results["results"].forEach(result => {
                let entityCard = entityCardFactory(result);
                cardsContainer.innerHTML += entityCard;
            });

            mainContentArea.appendChild(cardsContainer);
            setupEventListeners();

            // Setup pagination controls
            if (results["totalPages"]) {
                setupPagination(results["totalPages"], page);
            }
        } else {
            showNoResultsMessage(cardsContainer);
        }
    })
    .catch(error => {
        console.error('Error:', error);
    });
}

function entityCardFactory(result) {
    switch(result.type) {
        case 'E': return employeeCard(result);
        case 'S': return specimenCard(result);
        case 'O': return originCard(result);
        case 'M': return missionCard(result);
        case 'D': return departmentCard(result);
        default: throw new Error(`Unsupported entity type: ${result.type}`);
    }
}

function setupEventListeners() {
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
