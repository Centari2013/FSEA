import {cardContainer} from "./cardTemplates";
import { setupEventListeners } from "./clickableCardsFunctionality";
import { entityCardFactory, showPaginationButtons } from "../utility";
import { client } from "../api_access/apollo_client";
import { gql } from "@apollo/client/core";

let allResults = [];  // This will store all fetched results

const SEARCH_MUTATION = gql`
    mutation Search($query: String!) {
        search(query: $query) {
            results {
                entityType
                data
            }
        }
    }
`;

export async function performSearch(query) {
    console.log("Performing search for:", query);
    try {
        const { data: { search: { results } } } = await client.mutate({
            mutation: SEARCH_MUTATION,
            variables: { query: query }
        });
        allResults = results; // Store all results
        displayResults(1);  // Display the first page
    } catch (error) {
        console.error('Error:', error);
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
    // Ensure the container is empty before setting up new pagination
    paginationContainer.innerHTML = '';

    // Create and append 'Previous' button
    paginationContainer.appendChild(createPageItem(currentPage - 1, currentPage === 1, 'Previous', 'prevPage'));

    // Create and append page number buttons
    for (let i = 1; i <= totalPages; i++) {
        paginationContainer.appendChild(createPageItem(i, i === currentPage, i.toString()));
    }

    // Create and append 'Next' button
    paginationContainer.appendChild(createPageItem(currentPage + 1, currentPage === totalPages, 'Next', 'nextPage'));

    // Now that all elements are added to the DOM, add event listeners
    Array.from(paginationContainer.querySelectorAll('a')).forEach(link => {
        link.addEventListener('click', (event) => {
            event.preventDefault();
            const page = parseInt(event.target.getAttribute('data-page'), 10);
            changePage(page);
        });
    });

    showPaginationButtons(true);
}

// Helper function to create page items
function createPageItem(page, isDisabled, text, id = null) {
    const li = document.createElement('li');
    li.className = `page-item ${isDisabled ? 'disabled' : ''}`;

    const a = document.createElement('a');
    a.className = 'page-link';
    a.href = '#';
    a.textContent = text;
    a.setAttribute('data-page', page);
    if (id) a.id = id; // Set specific IDs for Previous and Next buttons

    if (!isDisabled) {
        a.addEventListener('click', (event) => {
            event.preventDefault();
            changePage(parseInt(a.getAttribute('data-page'), 10));
        });
    }

    li.appendChild(a);
    return li;
}


export function showNoResultsMessage(container) {
  container.innerHTML = `<p>No results found.</p>`;
  document.getElementById('main-content').appendChild(container);
}


function changePage(page) {
    currentPage = page;
    displayResults(currentPage); // Update display based on the new page number
}