import {checkSessionOnLoad} from './checkTokenAndRedirect.js'
document.addEventListener("DOMContentLoaded", function() {

    var searchForm = document.getElementById('searchForm');
    var searchInput = document.getElementById('search-bar');
    // Add search functionality
    searchForm.addEventListener('submit', function(e) {
        e.preventDefault(); // Prevent the default form submission behavior
        checkSessionOnLoad();
        performSearch(searchInput.value); // Execute search with the current input value
    });


    var navItems = document.querySelectorAll('.nav-item a'); // Select all nav-link elements within nav-items
    navItems.forEach(function(item) {
        item.addEventListener('click', function(e) {
            e.preventDefault();
            checkSessionOnLoad();
            // Remove active class from all items
            navItems.forEach(function(item) {
                item.classList.remove('active');
            });

            // Add active class to clicked item
            this.classList.add('active');

            const contentId = this.getAttribute('href').substring(1); // Assuming 'href' contains an identifier.
            loadContentIntoMainArea(contentId);
        });
    });

    // Automatically load content for "Home" and mark it as active
    const homeNavItem = document.querySelector('.nav-item a[href="#"]'); // Adjust the selector as needed
    if(homeNavItem) {
        homeNavItem.classList.add('active'); // Set "Home" as active
        const homeContentId = homeNavItem.getAttribute('href').substring(1);
        loadContentIntoMainArea(homeContentId); // Load "Home" content
    }
});

// Define the performSearch function
function performSearch(query) {
    console.log("Performing search for:", query);
    // Implement your search logic here
    // This could involve making an AJAX request, updating the DOM with search results, etc.
}

function loadContentIntoMainArea(contentId) {
    const mainContentArea = document.getElementById('main-content');
    mainContentArea.innerHTML = ''; // Clear existing content
  
    // Fetch new content based on 'contentId' and append it to 'mainContentArea'
    // This is where you'd make an AJAX call or load content directly, depending on your app's structure
    // For demonstration, simply setting placeholder text
    mainContentArea.textContent = `Content for ${contentId}`;
}
