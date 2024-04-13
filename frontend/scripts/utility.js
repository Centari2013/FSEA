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