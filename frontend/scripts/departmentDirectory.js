const api = import.meta.env.VITE_API_ENDPOINT;
import { cardContainer, departmentDirectoryCard, titleCard } from "./search/cardTemplates";
import { setupEventListeners } from "./search/clickableCardsFunctionality";

export function loadDepartmentDirectory() {
    fetch(api, { method: 'POST', 
    headers: {
        'Content-Type': 'application/json'
    },
    body: JSON.stringify({
        query: `query {
            allDepartments{
                departmentName
                description
            }
        }`
    })})
      .then(response => response.json())
      .then(({data: {allDepartments: departments}}) => {
        const cardsContainer = cardContainer();

        
        cardsContainer.innerHTML += titleCard("Employee Departments");
  
        departments.forEach(department => {
          const departmentCardHtml = departmentDirectoryCard(department);

          cardsContainer.innerHTML += departmentCardHtml;
        });
  
        const mainContentArea = document.getElementById('main-content');
        mainContentArea.appendChild(cardsContainer);
        setupEventListeners();
      })
      .catch(error => {
        console.error('Error loading department directory:', error);
        document.getElementById('main-content').innerHTML = '<p>Error loading the directory.</p>';
      });
  }
  
  