const api = import.meta.env.VITE_API_ENDPOINT;
export async function fetchDepartmentDetails(department_id) {
    const response = await fetch(api, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
            query: `
                query Department($departmentId: Int!){
                    department(departmentId: $departmentId){
                        departmentId
                        departmentName
                        director{
                          employeeId
                          firstName
                          lastName
                        }
                        description
                        missions{
                          missionId
                          missionName
                        }
                      employees{
                        employeeId
                        firstName
                        lastName
                        designations{
                          abbreviation
                        }
                      }
                      
                      }
                }`,
            variables: {departmentId: department_id}
        }),
    });
    if (!response.ok) throw new Error('Failed to fetch department data');
    const jsonResponse = await response.json();
    return jsonResponse.data.department;
}