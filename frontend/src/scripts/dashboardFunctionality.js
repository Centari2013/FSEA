import { checkSessionOnLoad } from './auth/checkTokenAndRedirect.js'
import { loadDepartmentDirectory } from './directories/departmentDirectory.js';
import { performSearch } from './search/search.js';
import { loadSpecimenDirectory } from './directories/specimenDirectory.js';
import { loadOriginDirectory } from './directories/originDirectory.js';
import { showPaginationButtons } from './utility.js';

document.addEventListener("DOMContentLoaded", function() {
    showPaginationButtons(false);

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
            deacticateNavItems();

            // Add active class to clicked item
            setActiveNavLink(this);
        });
    });

    const savedContentId = localStorage.getItem('activeNavLink');
    if (savedContentId) {
        const navItemToActivate = document.querySelector(`.nav-item a[href="${savedContentId}"]`);
        if (navItemToActivate) {
            setActiveNavLink(navItemToActivate);
        }
    }else{
        // Automatically load content for "Home" and mark it as active
        const homeNavItem = document.querySelector('.nav-item a[href="#"]'); // Adjust the selector as needed
        if(homeNavItem) {
            setActiveNavLink(homeNavItem);
        }
    }
    
});



function deacticateNavItems() {
    var navItems = document.querySelectorAll('.nav-item a'); // Select all nav-link elements within nav-items
    navItems.forEach(function(item) {
        navItems.forEach(function(item) {
            item.classList.remove('active');
        });
    });
}


function setActiveNavLink (item) {
    deacticateNavItems();
    console.log(item.getAttribute('href'));
    localStorage.setItem('activeNavLink', item.getAttribute('href'));
    item.classList.add('active');
    const itemContentId = item.getAttribute('href').substring(1);
    loadContentIntoMainArea(itemContentId);
}



function loadContentIntoMainArea(contentId) {
    showPaginationButtons(false);
    const mainContentArea = document.getElementById('main-content');
    mainContentArea.innerHTML = ''; // Clear existing content
    
    switch(contentId) {
        case 'departmentDirectory':
            mainContentArea.innerHTML = '';
            loadDepartmentDirectory();
            break;
        case 'specimenDirectory':
            mainContentArea.innerHTML = '';
            loadSpecimenDirectory();
            break;
        case 'originDirectory':
            mainContentArea.innerHTML = '';
            loadOriginDirectory();
            break;
        default:
            mainContentArea.innerHTML = '';
            break;
            
    }
    
}

