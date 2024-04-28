

export function employeeDirectoryCard(employee) {

    const designationString = employee.designations ? employee.designations.map(d => d.abbreviation).join(', '): "";
    return `
    <div class="col-8 col-sm-10 col-md-10">
        <a  class="text-decoration-none">
            <div class="card h-100 clickable-card" data-type="employee" data-id=${employee.employee_id}>
                <div class="card-body">
                    <h5 class="card-title">${employee.first_name} ${employee.last_name}</h5>
                    <p class="card-text">
                        <strong>Employee ID:</strong> ${employee.employee_id}<br>
                        <strong>Department:</strong> ${employee.department}<br>
                        <strong>Designations:</strong> ${designationString}
                    </p>
                </div>
            </div>
        </a>
    </div>
    `;
}



export function specimenDirectoryCard(specimen) {
    return `
    <div class="col-8 col-sm-10 col-md-10">
        <a class="text-decoration-none">
            <div class="card h-100 clickable-card" data-type="specimen" data-id="${specimen.specimenId}">
                <div class="card-body">
                    <h5 class="card-title">${specimen.specimenName}</h5>
                    <p class="card-text">
                        <strong>Specimen ID:</strong> ${specimen.specimenId}<br>
                        <strong>Threat Level:</strong> ${specimen.threatLevel}<br>
                        <strong>Acquisition Date:</strong> ${specimen.acquisitionDate}<br>
                    </p>
                </div>
            </div>
        </a>
    </div>
    `;
}

export function originDirectoryCard(origin) {
    return `
    <div class="col-8 col-sm-10 col-md-10">
        <a class="text-decoration-none">
            <div class="card h-100 clickable-card" data-type="origin" data-id="${origin.originId}">
                <div class="card-body">
                    <h5 class="card-title">${origin.originName}</h5>
                    <p class="card-text">
                        <strong>Origin ID:</strong> ${origin.originId}<br>
                        <strong>Discovery Date:</strong> ${origin.discoveryDate}<br>
                        ${origin.description || "No description available."}
                    </p>
                </div>
            </div>
        </a>
    </div>
    `;
}


export function departmentDirectoryCard(department) {
    return `
    <div class="col-8 col-sm-10 col-md-10">
        <a class="text-decoration-none">
            <div class="card h-100 clickable-card" data-type="department" data-id=${department.departmentId}>
                <div class="card-body">
                    <h5 class="card-title">${department.departmentName}</h5>
                    <p class="card-text">${department.description || "No description available."}</p>
                </div>
            </div>
        </a>
    </div>
    `;
}

export function titleCard(title) {
    return `
    <div class="col-12">
        <div class="card h-100" data-type="title">
            <div class="card-body">
                <h4 class="card-title text-center">${title}</h4>
            </div>
        </div>
    </div>
    `;
}