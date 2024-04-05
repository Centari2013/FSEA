const api = import.meta.env.VITE_API_ENDPOINT;


document.getElementById('loginForm').addEventListener('submit', function(event) {
    event.preventDefault(); // Prevent the default form submission

    // Extracting the username and password from the form
    const username = document.getElementById('username').value;
    const password = document.getElementById('password').value;

    // Preparing the payload
    const payload = {
        username,
        password
    };
   
    // Sending the payload to the API endpoint using Fetch
    fetch(`${api}/login`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify(payload),
    })
    .then(response => response.json())
    .then(data => {
        if(data.token) {
            // Assuming the API response includes a token upon successful login
            // Store the session token
            localStorage.setItem('sessionToken', data.token);
            localStorage.setItem('employee_id', data.employee_id);

            // Redirect to the dashboard page
            window.location.href = '/dashboard';
        } else {
            // Handle login failure (e.g., show an error message)
            alert('Login failed, please check your credentials and try again.');
        }
    })
    .catch(error => {
        // Handle any errors that occurred during the fetch
        console.error('Error:', error);
    });
});


