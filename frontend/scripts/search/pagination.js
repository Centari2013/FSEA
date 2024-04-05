let currentPage = 1;
let currentFilter = '';

function setupPagination(totalPages, currentPage) {
    const paginationContainer = document.querySelector('.pagination');
    paginationContainer.innerHTML = `<li class="page-item ${currentPage === 1 ? 'disabled' : ''}">
      <a class="page-link" href="#" onclick="changePage(${currentPage - 1})">Previous</a></li>`;
  
    // Dynamically generate page numbers based on totalPages...
    for (let i = 1; i <= totalPages; i++) {
      paginationContainer.innerHTML += `<li class="page-item ${i === currentPage ? 'active' : ''}">
        <a class="page-link" href="#" onclick="changePage(${i})">${i}</a></li>`;
    }
  
    paginationContainer.innerHTML += `<li class="page-item ${currentPage === totalPages ? 'disabled' : ''}">
      <a class="page-link" href="#" onclick="changePage(${currentPage + 1})">Next</a></li>`;
}

function changePage(page) {
    currentPage = page;
    loadDepartmentDirectory(); // Reload directory with the new page
}

function filterDepartments() {
    currentFilter = document.getElementById('filterQuery').value;
    loadDepartmentDirectory(); // Reload directory with the new filter
}