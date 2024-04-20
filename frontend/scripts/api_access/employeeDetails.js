const api = import.meta.env.VITE_API_ENDPOINT;
export async function fetchEmployeeData(employee_id) {
    const response = await fetch(api, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
            query: `
                query Employee($employeeId: String!){
                    employee(employeeId: $employeeId) {
                        departmentId
                        firstName
                        lastName
                        startDate
                        endDate
                    }
                }`,
            variables: {employeeId: employee_id}
        }),
    });
    if (!response.ok) throw new Error('Failed to fetch employee data');
    const jsonResponse = await response.json();
    return jsonResponse.data.employee;
}