const api = import.meta.env.VITE_API_ENDPOINT;

export function loadDepartmentDirectory() {
    fetch(`${api}/departments`)
      .then(response => response.json())
      .then(departments => {
        const cardsContainer = document.createElement('div');
        cardsContainer.id = "CardsContainer";
        cardsContainer.className = "row row-cols-1 g-4 justify-content-center";
  
        departments.forEach(department => {
          const departmentCardHtml = `
            <div class="col">
              <a href="${department.url}" class="text-decoration-none">
                <div class="card h-100 clickable-card">
                    <div class="card-body">
                        <h5 class="card-title">${department.department_name}</h5>
                        <p class="card-text">${department.description || "No description available."}</p>
                    </div>
                </div>
              </a>
            </div>
          `;

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
  
  