const api = import.meta.env.VITE_API_ENDPOINT;
import { cardContainer, departmentDirectoryCard, titleCard } from "./search/cardTemplates";

export function loadEmployeeDirectory() {
    fetch(`${api}/departments`)
      .then(response => response.json())
      .then(departments => {
        const cardsContainer = cardContainer();

        
        cardsContainer.innerHTML += titleCard("Departments");
  
        departments.forEach(department => {
          const departmentCardHtml = departmentDirectoryCard(department);

          cardsContainer.innerHTML += departmentCardHtml;
        });
  
        const mainContentArea = document.getElementById('main-content');
        mainContentArea.appendChild(cardsContainer);
      })
      .catch(error => {
        console.error('Error loading department directory:', error);
        document.getElementById('main-content').innerHTML = '<p>Error loading the directory.</p>';
      });
  }
  
  