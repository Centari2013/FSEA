import {checkSessionOnLoad} from './auth/checkTokenAndRedirect.js'
import { loadEmployeeDirectory } from './employeeDirectory.js';
import { performSearch } from './search/search.js';

document.addEventListener("DOMContentLoaded", function() {

    var searchForm = document.getElementById('searchForm');
    var searchInput = document.getElementById('search-bar');
    // Add search functionality
    searchForm.addEventListener('submit', function(e) {
        e.preventDefault(); // Prevent the default form submission behavior
        checkSessionOnLoad();
        performSearch(searchInput.value); // Execute search with the current input value
        window.scrollTo({
            top: 0,
            left: 0,
            behavior: 'smooth'
          });
          
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



function loadContentIntoMainArea(contentId) {
    const mainContentArea = document.getElementById('main-content');
    mainContentArea.innerHTML = ''; // Clear existing content
    
    switch(contentId) {
        case 'employeeDirectory':
            mainContentArea.innerHTML = '';
            loadEmployeeDirectory();
        default:
            mainContentArea.innerHTML = '';
            
    }
    
}
