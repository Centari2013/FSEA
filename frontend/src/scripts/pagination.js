export default function setupPagination(dash) {
    const totalPages = dash.totalPages;
    const paginationContainer = dash.$refs.paginationContainer;
    // Ensure the container is empty before setting up new pagination
    paginationContainer.innerHTML = '';

    // Create and append page number buttons
    for (let i = 1; i <= totalPages; i++) {
        paginationContainer.appendChild(createPageItem(dash, i, i === dash.currentPage, i.toString()));
    }

}

// Helper function to create page items
function createPageItem(dash, page, isDisabled, text, id = null) {
    const li = document.createElement('li');
    li.className = `page-item${isDisabled ? ' disabled' : ''}`;
    li.textContent = text;
    li.setAttribute('data-page', page);
    if (id) a.id = id; // Set specific IDs for Previous and Next buttons

    if (!isDisabled) {
        li.addEventListener('click', (event) => {
            event.preventDefault();
            dash.changePage(parseInt(li.getAttribute('data-page'), 10));
        });
    }
    return li;
}

