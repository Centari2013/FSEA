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