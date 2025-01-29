import { employeeCard, specimenCard, departmentCard, missionCard, originCard} from "./pagination/cardTemplates";
import { employeeDirectoryCard, specimenDirectoryCard, originDirectoryCard, departmentDirectoryCard } from "./directories/directoryCardTemplates" ;
export function setWindowOpener(){
    if (window.history.length <= 1) { // If this page is the only entry in the history
        window.history.pushState(null, null, window.location.href); // Modify history state
        window.onpopstate = function(event) {
            if (window.opener && !window.opener.closed) {
                window.opener.focus(); // Focus the opener window
            }
            window.close(); // Close the current tab
        };
    }
}


export function setToggle() {
    // Find all collapsible elements with buttons linked to them
    document.querySelectorAll('.btn-link[data-bs-toggle="collapse"]').forEach(button => {
        const targetId = button.getAttribute('data-bs-target');
        const collapseElement = document.querySelector(targetId);

        collapseElement.addEventListener('show.bs.collapse', () => {
            button.textContent = 'See Less'; // Change button text to "See Less" when expanded
        });

        collapseElement.addEventListener('hide.bs.collapse', () => {
            button.textContent = 'See More'; // Change back to "See More" when collapsed
        });
    });
}

export function entityCardFactory(result) {
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

export function directoryEntityCardFactory(data, type) {
    
    switch(type) {
        case 'E': return employeeDirectoryCard(data);
        case 'S': return specimenDirectoryCard(data);
        case 'O': return originDirectoryCard(data);
        case 'D': return departmentDirectoryCard(data);
        default: throw new Error(`Unsupported entity type: ${type}`);
    }
}

export function showPaginationButtons(bool){
    const paginationContainer = document.querySelector('.pagination');

    paginationContainer.style.display = bool? 'flex' : 'none';
    

    
}