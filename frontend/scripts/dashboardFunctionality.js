import {checkSessionOnLoad} from './checkTokenAndRedirect.js'
import { loadDepartmentDirectory } from './departmentDirectory.js';
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
            setActiveNavLink(this);
        });
    });
    const savedContentId = localStorage.getItem('activeNavLink');
    if (savedContentId) {
        const navItemToActivate = document.querySelector(`.nav-item a[href="#${savedContentId}"]`);
        if (navItemToActivate) {
            setActiveNavLink(navItemToActivate);
        }
    }
    // Automatically load content for "Home" and mark it as active
    const homeNavItem = document.querySelector('.nav-item a[href="#"]'); // Adjust the selector as needed
    if(homeNavItem) {
        setActiveNavLink(homeNavItem);
    }
});

function setActiveNavLink (item) {
    item.classList.add('active');
    const itemContentId = item.getAttribute('href').substring(1);
    loadContentIntoMainArea(itemContentId);
}

// Define the performSearch function
function performSearch(query) {
    console.log("Performing search for:", query);
    // Implement your search logic here
    // This could involve making an AJAX request, updating the DOM with search results, etc.
}

function loadContentIntoMainArea(contentId) {
    const mainContentArea = document.getElementById('main-content');
    mainContentArea.innerHTML = ''; // Clear existing content
    
    switch(contentId) {
        case 'departmentDirectory':
            mainContentArea.innerHTML = '';
            loadDepartmentDirectory();
        default:
            mainContentArea.innerHTML = '';
            
    }
    
}
