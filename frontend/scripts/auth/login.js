import { gql } from "@apollo/client/core";
import { client } from "../api_access/apollo_client";

const LOGIN_MUTATION = gql`
  mutation Login($username: String!, $password: String!) {
    login(username: $username, password: $password) {
      token
      employeeId
      message
    }
  }
`;

document.getElementById('loginForm').addEventListener('submit', async function(event) {
  event.preventDefault(); // Prevent the default form submission

  // Extracting the username and password from the form
  const username = document.getElementById('username').value;
  const password = document.getElementById('password').value;

  try {
    const result = await client.mutate({
      mutation: LOGIN_MUTATION,
      variables: { username: username, password: password },
    });

    const loginData = result.data.login;
    if (loginData.token) {
      // Assuming the API response includes a token upon successful login
      // Store the session token
      localStorage.setItem('sessionToken', loginData.token);
      localStorage.setItem('employee_id', loginData.employeeId);

      // Redirect to the dashboard page
      window.location.href = '/dashboard.html';
    } else {
      // Handle login failure (e.g., show an error message)
      alert(loginData.message);
    }
  } catch (error) {
    // Handle any errors that occurred during the mutation
    console.error('Error:', error);
  }
});
