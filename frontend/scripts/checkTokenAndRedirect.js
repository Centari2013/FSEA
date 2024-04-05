
async function verifyToken(token) {
    const api = import.meta.env.VITE_API_ENDPOINT; // Adjust this URL to your actual API endpoint
    const headers = {
      'Content-Type': 'application/json',
    };
    const body = JSON.stringify({ token: token });
  
    try {
      const response = await fetch(`${api}/token/verify`, {
        method: 'POST',
        headers: headers,
        body: body,
      });
  
      if (!response.ok) {
        // Server returned a HTTP status outside the 200 range (e.g., 401, 403, 404, 500)
        console.error('Error response from server:', response.status, response.statusText);
        return { valid: false, message: 'Failed to verify token due to server error.' };
      }
  
      // Assuming the server responds with JSON data
      const data = await response.json();
      return data; // This will be an object like { valid: true, message: 'Token is valid.' } or { valid: false, message: 'Invalid or expired token' }
  
    } catch (error) {
      console.error('Error verifying token:', error);
      return { valid: false, message: 'An error occurred while verifying the token.' };
    }
  }
  
async function checkSessionOnLoad() {
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


  