const api = import.meta.env.VITE_API_ENDPOINT;


document.getElementById('loginForm').addEventListener('submit', function(event) {
    event.preventDefault(); // Prevent the default form submission

    // Extracting the username and password from the form
    const username = document.getElementById('username').value;
    const password = document.getElementById('password').value;

    // GraphQL mutation with variables
    const query = `
        mutation Login($username: String!, $password: String!) {
            login(username: $username, password: $password) {
                token
                employeeId
                message
            }
        }`;

    // Variables object to safely pass data
    const variables = {
        username: username,
        password: password,
    };

    // Sending the GraphQL mutation using Fetch
    fetch(api, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({
            query: query,
            variables: variables // Send variables separately from the query
        }),
    })
    .then(response => response.json())
    .then(data => {
        const response = data.data.login;
        if(response.token) {
            // Assuming the API response includes a token upon successful login
            // Store the session token
            localStorage.setItem('sessionToken', response.token);
            localStorage.setItem('employee_id', response.employeeId);

            // Redirect to the dashboard page
            window.location.href = '/dashboard';
        } else {
            // Handle login failure (e.g., show an error message)
            alert(response.message);
        }
    })
    .catch(error => {
        // Handle any errors that occurred during the fetch
        console.error('Error:', error);
    });
});


