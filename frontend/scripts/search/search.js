import { employeeCard, specimenCard, departmentCard, missionCard, originCard} from "./cardTemplates";
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
        console.log(results);
        const cardsContainer = document.createElement('div');
        cardsContainer.id = "CardsContainer";
        cardsContainer.className = "row row-cols-1 g-4 justify-content-center";

        const mainContentArea = document.getElementById('main-content');
        mainContentArea.innerHTML = ''; // Clear existing content
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


    })
    .catch(error => {
        // Handle any errors that occurred during the fetch
        console.error('Error:', error);
    });
    // Implement your search logic here
    // This could involve making an AJAX request, updating the DOM with search results, etc.
}