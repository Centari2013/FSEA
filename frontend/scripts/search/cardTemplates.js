
export function employeeCard(employee){
    return `
    <div class="col">
        <div class="card h-100 clickable-card">
        <div class="card-body">
            <h5 class="card-title">${employee.first_name} ${employee.last_name}</h5>
            <p class="card-text">
            <strong>Employee ID:</strong> ${employee.employee_id}<br>
            <strong>Department:</strong> ${employee.department}<br>
            <strong>Designations:</strong> ${employee.designations}
            </p>
        </div>
        </div>
    </div>
    `;
}

export function departmentCard(department){
    return `
    <div class="col">
        <div class="card h-100 clickable-card">
        <div class="card-body">
            <h5 class="card-title">${department.deparment_name}</h5>
            <p class="card-text">
            <strong>Department ID:</strong> ${department.department_id}<br>
            <strong>Director:</strong> ${department.director}<br>
            ${department.description || "No description available."}
            </p>
        </div>
        </div>
    </div>
    `;
}


export function missionCard(mission){
    return `
  <div class="col">
    <div class="card h-100 clickable-card">
      <div class="card-body">
        <h5 class="card-title">${mission.mission_name}</h5>
        <p class="card-text">
          <strong>Mission ID:</strong> ${mission.mission_id}<br>
          <strong>Start Date:</strong> ${mission.start_date}<br>
          <strong>End Date:</strong> ${mission.end_date}<br>
          ${mission.description || "No description available."}
        </p>
      </div>
    </div>
  </div>
    `;
}
export function specimenCard(specimen){
    return `
    <div class="col">
        <div class="card h-100 clickable-card">
        <div class="card-body">
            <h5 class="card-title">${specimen.name}</h5>
            <p class="card-text">
            <strong>Specimen ID:</strong> ${specimen.specimen_id}<br>
            <strong>Threat Level:</strong> ${specimen.threat_level}<br>
            <strong>Acquisition Date:</strong> ${specimen.acquisition_date}<br>
            </p>
        </div>
        </div>
    </div>
    `;
}

export function departmentDirectoryCard(department){
    return `
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
}

export function originCard(origin){    
    return `
    <div class="col">
        <div class="card h-100 clickable-card">
        <div class="card-body">
            <h5 class="card-title">${origin.origin_name}</h5>
            <p class="card-text">
            <strong>Origin ID:</strong> ${origin.origin_id}<br>
            <strong>Discovery Date:</strong> ${origin.discovery_date}<br>
            ${origin.description || "No description available."}
            </p>
        </div>
        </div>
    </div>
    `;
}
