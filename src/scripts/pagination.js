export default function setupPagination(dashboard) {
    const totalPages = dashboard.store.totalPages;
    const paginationContainer = dashboard.$refs.paginationContainer;
    // Ensure the container is empty before setting up new pagination
    paginationContainer.innerHTML = '';

    // Create and append page number buttons
    for (let i = 1; i <= totalPages; i++) {
        paginationContainer.appendChild(createPageItem(dashboard, i, i === dashboard.store.currentPage, i.toString()));
    }

}

// Helper function to create page items
function createPageItem(dashboard, page, isDisabled, text) {
    const li = document.createElement('li');
    li.className = `page-item${isDisabled ? ' disabled' : ''}`;
    li.textContent = text;
    li.setAttribute('data-page', page);

    if (!isDisabled) {
        li.addEventListener('click', (event) => {
            event.preventDefault();
            dashboard.changePage(parseInt(li.getAttribute('data-page'), 10));
        });
    }
    return li;
}

