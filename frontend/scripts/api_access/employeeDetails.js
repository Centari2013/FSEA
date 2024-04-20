const api = import.meta.env.VITE_API_ENDPOINT;
export async function fetchEmployeeData(employee_id) {
    const response = await fetch(api, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
            query: `
                query Employee($employeeId: String!){
                    employee(employeeId: $employeeId){
                        employeeId
                        firstName
                        lastName
                        department{
                          departmentName
                        }
                        medicalRecord {
                          dob
                          bloodtype
                          sex
                          kilograms
                          heightCm
                          notes
                        }
                        startDate
                        endDate
                        clearances{
                          clearanceName
                          description
                        }
                        missions {
                          missionId
                          missionName
                          involvementSummary
                        }
                        notes
                        designations {
                          designationName
                          abbreviation
                        }
                        
                      }
                }`,
            variables: {employeeId: employee_id}
        }),
    });
    if (!response.ok) throw new Error('Failed to fetch employee data');
    const jsonResponse = await response.json();
    return jsonResponse.data.employee;
}