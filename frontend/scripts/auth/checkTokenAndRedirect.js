
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
      const response = await fetch((api), {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          query: query,
          variables: variables // Send variables separately from the query
      }),
      });
  
      if (!response.ok) {
        // Server returned a HTTP status outside the 200 range (e.g., 401, 403, 404, 500)
        console.error('Error response from server:', response.status, response.statusText);
        return { valid: false, message: 'Failed to verify token due to server error.' };
      }
  
      // Assuming the server responds with JSON data
      const data = await response.json();
      return data.data; // This will be an object like { valid: true, message: 'Token is valid.' } or { valid: false, message: 'Invalid or expired token' }
  
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


  