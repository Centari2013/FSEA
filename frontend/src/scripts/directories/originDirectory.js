const api = import.meta.env.VITE_API_ENDPOINT;
import { setupEventListeners } from "../search/clickableCardsFunctionality";
import { createAlphabeticDirectory } from "./alphabeticDirectory";

export function loadOriginDirectory() {
    fetch(api, { method: 'POST', 
    headers: {
        'Content-Type': 'application/json'
    },
    body: JSON.stringify({
        query: `query {
            allOrigins{
                originId
                originName
                discoveryDate
                description
              }
          }`
    })})
      .then(response => response.json())
      .then(({data: {allOrigins: origins}}) => {
  
       createAlphabeticDirectory(origins, "originName", 'O', "Origins");
        setupEventListeners();
      })
      .catch(error => {
        console.error('Error loading origin directory:', error);
        document.getElementById('main-content').innerHTML = '<p>Error loading the directory.</p>';
      });
  }
  
  