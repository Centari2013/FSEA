import { employeeCard, specimenCard, departmentCard, missionCard, originCard, noResultsCard, cardContainer} from "./cardTemplates";
const api = import.meta.env.VITE_API_ENDPOINT;
// Define the performSearch function
export function performSearch(query) {
    console.log("Performing search for:", query);
    const payload = {
        "query": query
    };

    // Sending the payload to the API endpoint using Fetch
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
        mainContentArea.innerHTML = ''; // Clear existing content
        if (results["results"]) {

            var entityCard = null;
            results["results"].forEach(result => {

            
                switch(result.type) {
                    case 'E':
                        entityCard = employeeCard(result);
                        break;
                    case 'S':
                        entityCard = specimenCard(result);
                        break;
                    case 'O':
                        entityCard = originCard(result);
                        break;
                    case 'M':
                        entityCard = missionCard(result);
                        break;
                    case 'D':
                        entityCard = departmentCard(result);
                        break;
                    default:
                        throw new Error(`Unsupported entity type: ${result.type}`);
                }


            cardsContainer.innerHTML += entityCard;
        });

        mainContentArea.appendChild(cardsContainer);
        document.querySelectorAll('.clickable-card').forEach(card => {
            card.addEventListener('click', function() {
                const card_type = card.getAttribute('data-type');
                const id = card.getAttribute('data-id');
                
                switch (card_type) {
                    case 'employee':
                        window.open(`/employeeDetails.html?employee_id=${id}`, '_blank');
                        break;
                    case 'department':
                        window.open(`/departmentDetails.html?department_id=${id}`, '_blank');
                        break;
                    case 'mission':
                        window.open(`/missionDetails.html?mission_id=${id}`, '_blank');
                        break;
                    case 'specimen':
                        window.open(`/specimenDetails.html?specimen_id=${id}`, '_blank');
                        break;
                    case 'origin':
                        window.open(`/originDetails.html?origin_id=${id}`, '_blank');
                        break;
                    case 'department-directory':
                        window.open(`/departmentDirectoryDetails.html?department_id=${id}`, '_blank');
                        break;
                    default:
                        console.log('Unknown type');
                }
                
            });
        });
        
        }else{
            showNoResultsMessage(cardsContainer);
        }
        


    })
    .catch(error => {
        // Handle any errors that occurred during the fetch
        console.error('Error:', error);
    });
    // Implement your search logic here
    // This could involve making an AJAX request, updating the DOM with search results, etc.
}

function showNoResultsMessage(div) {
    div.innerHTML += noResultsCard();
    const mainContent = document.getElementById('main-content');
    mainContent.appendChild(div);
}
