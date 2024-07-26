import { client } from "../api_access/apollo_client";
import { gql } from "@apollo/client/core";
const VALIDATE_TOKEN_MUTATION = gql`
  mutation ValidateToken($token: String!) {
    validateToken(token: $token) {
      valid
    }
  }
`;

async function verifyToken(token) {
  try {
    const result = await client.mutate({
      mutation: VALIDATE_TOKEN_MUTATION,
      variables: { token: token },
    });

    if (result.errors) {
      console.error('GraphQL errors:', result.errors);
      return { valid: false, message: 'GraphQL error occurred' };
    }

    return result.data.validateToken; // Adjust based on actual data structure
  } catch (error) {
    console.error('Error verifying token:', error);
    return { valid: false, message: 'An error occurred while verifying the token.' };
  }
}
  
export async function checkSessionOnLoad() {
  const token = localStorage.getItem('sessionToken');
  if (token) {
    const result = await verifyToken(token);
    if (!result.valid) {
      window.location.href = '/login.html';
    }else{
      document.body.style.visibility = 'visible';
    }
  
  } else {
    window.location.href = '/login.html';
  }
}

checkSessionOnLoad();


  