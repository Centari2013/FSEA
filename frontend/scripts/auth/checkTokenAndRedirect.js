
async function verifyToken(token) {
    const api = import.meta.env.VITE_API_ENDPOINT; // Adjust this URL to your actual API endpoint
    const query = `
      mutation ValidateToken($token: String!){
       validateToken(token: $token){
          valid
        }
      }`
      const variables = {
        token: token
      }
  
    try {
      const response = await fetch(api, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          query: query,
          variables: variables // Send variables separately from the query
      }),
      });
      const data = await response.json();
      if (data.errors) {
          console.error('GraphQL errors:', data.errors);
          return { valid: false, message: 'GraphQL error occurred' };
      }
      return data.data.validateToken; // Adjust based on actual data structure

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


  