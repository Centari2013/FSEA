import { employeeCard, specimenCard, departmentCard, missionCard, originCard, noResultsCard, cardContainer} from "./cardTemplates";
import { setupEventListeners } from "./clickableCardsFunctionality";
const api = import.meta.env.VITE_API_ENDPOINT;

let allResults = [];  // This will store all fetched results

export function performSearch(query) {
    console.log("Performing search for:", query);
    const payload = {
        "query": `
            mutation Search($query: String!) {
                search(query: $query) {
                    results {
                        entityType
                        data
                    }
                }
            }`,
        "variables": { query: query }
    };

    fetch(api, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify(payload),
    })
    .then(response => response.json())
    .then(({data: {search: {results}}}) => {
        allResults = results; // Store all results
        displayResults(1);  // Display the first page
    })
    .catch(error => {
        console.error('Error:', error);
    });
}


function entityCardFactory(result) {
    const data = result.data;
    switch(result.entityType) {
        case 'E': return employeeCard(data);
        case 'S': return specimenCard(data);
        case 'O': return originCard(data);
        case 'M': return missionCard(data);
        case 'D': return departmentCard(data);
        default: throw new Error(`Unsupported entity type: ${result.entityType}`);
    }
}

const RESULTS_PER_PAGE = 25;

function displayResults(page) {
    const cardsContainer = cardContainer();
    const mainContentArea = document.getElementById('main-content');
    mainContentArea.innerHTML = '';

    const startIndex = (page - 1) * RESULTS_PER_PAGE;
    const endIndex = startIndex + RESULTS_PER_PAGE;
    const pageResults = allResults.slice(startIndex, endIndex);

    if (pageResults.length) {
        pageResults.forEach(result => {
            if (typeof result.data === 'string') {
                result.data = JSON.parse(result.data); // Parse it to a JavaScript object
            }
            let entityCard = entityCardFactory(result);
            cardsContainer.innerHTML += entityCard;
        });

        mainContentArea.appendChild(cardsContainer);
        setupEventListeners();
        setupPagination(Math.ceil(allResults.length / RESULTS_PER_PAGE), page);
    } else {
        showNoResultsMessage(cardsContainer);
    }
}

let currentPage = 1;
let currentFilter = '';

export function setupPagination(totalPages, currentPage) {
  const paginationContainer = document.querySelector('.pagination');
  paginationContainer.innerHTML = `<li class="page-item ${currentPage === 1 ? 'disabled' : ''}">
    <a class="page-link" href="#" data-page="${currentPage - 1}">Previous</a></li>`;

  for (let i = 1; i <= totalPages; i++) {
    paginationContainer.innerHTML += `<li class="page-item ${i === currentPage ? 'active' : ''}">
      <a class="page-link" href="#" data-page="${i}">${i}</a></li>`;
  }

  paginationContainer.innerHTML += `<li class="page-item ${currentPage === totalPages ? 'disabled' : ''}">
    <a class="page-link" href="#" data-page="${currentPage + 1}">Next</a></li>`;

  // Add event listeners to all pagination links
  Array.from(paginationContainer.querySelectorAll('a')).forEach(link => {
    link.addEventListener('click', (event) => {
      event.preventDefault();
      const page = parseInt(event.target.getAttribute('data-page'), 10);
      changePage(page);
    });
  });
}


export function showNoResultsMessage(container) {
  container.innerHTML = `<p>No results found.</p>`;
  document.getElementById('main-content').appendChild(container);
}


function changePage(page) {
    currentPage = page;
    displayResults(currentPage); // Update display based on the new page number
  }