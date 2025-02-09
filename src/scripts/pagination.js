export default function setupPagination(dashboard) {
    const totalPages = dashboard.store.totalPages;
    const currentPage = dashboard.store.currentPage;
    const paginationContainer = dashboard.$refs.paginationContainer;
    paginationContainer.innerHTML = '';

    // Determine screen size
    const screenWidth = window.innerWidth;
    const maxVisiblePages = screenWidth >= 1024 ? 20 : screenWidth >= 768 ? 10 : 5; // lg: 20, md: 10, sm: 5

    // Helper to add a page item
    const addPageItem = (page, isCurrent = false) => {
        paginationContainer.appendChild(createPageItem(dashboard, page, isCurrent, page.toString()));
    };

    // Always show first page
    addPageItem(1, currentPage === 1);

    // Middle pages with ellipses logic
    if (totalPages <= maxVisiblePages) {
        // If total pages are within the limit, show all
        for (let i = 2; i < totalPages; i++) {
            addPageItem(i, currentPage === i);
        }
    } else {
        let startPage, endPage;
        const sidePages = Math.floor((maxVisiblePages - 2) / 2); // Pages to show on each side of current

        if (currentPage <= sidePages + 2) {
            // Close to the start
            startPage = 2;
            endPage = maxVisiblePages - 1;
        } else if (currentPage >= totalPages - sidePages - 1) {
            // Close to the end
            startPage = totalPages - maxVisiblePages + 2;
            endPage = totalPages - 1;
        } else {
            // Somewhere in the middle
            startPage = currentPage - sidePages;
            endPage = currentPage + sidePages;
        }

        if (startPage > 2) {
            paginationContainer.appendChild(createPageItem(dashboard, null, false, '...')); // Ellipsis before middle pages
        }

        for (let i = startPage; i <= endPage; i++) {
            addPageItem(i, currentPage === i);
        }

        if (endPage < totalPages - 1) {
            paginationContainer.appendChild(createPageItem(dashboard, null, false, '...')); // Ellipsis after middle pages
        }
    }

    // Always show last page if more than one page
    if (totalPages > 1) {
        addPageItem(totalPages, currentPage === totalPages);
    }
}

// Helper function to create page items (handles numbers and '...')
function createPageItem(dashboard, page, isCurrent, text) {
    const li = document.createElement('li');
    li.className = `page-item${isCurrent ? ' bg-gray-700 text-white' : ''}`;
    li.textContent = text;

    if (page && !isCurrent && text !== '...') {
        li.addEventListener('click', () => {
            dashboard.changePage(page);
        });
    } else if (text === '...') {
        li.classList.add('pointer-events-none', 'select-none', 'text-gray-500');
    }
    return li;
}
