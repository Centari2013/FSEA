const api = import.meta.env.VITE_API_ENDPOINT;
import { setupEventListeners } from "../search/clickableCardsFunctionality";
import { createAlphabeticDirectory } from "./alphabeticDirectory";

export function loadSpecimenDirectory() {
    fetch(api, { method: 'POST', 
    headers: {
        'Content-Type': 'application/json'
    },
    body: JSON.stringify({
        query: `query {
            allSpecimens{
              specimenId
              specimenName
              threatLevel
              acquisitionDate
            }
          }`
    })})
      .then(response => response.json())
      .then(({data: {allSpecimens: specimens}}) => {
  
       createAlphabeticDirectory(specimens, "specimenName", 'S', "Specimens");
        setupEventListeners();
      })
      .catch(error => {
        console.error('Error loading specimen directory:', error);
        document.getElementById('main-content').innerHTML = '<p>Error loading the directory.</p>';
      });
  }
  
  