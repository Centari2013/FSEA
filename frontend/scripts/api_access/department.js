const api = import.meta.env.VITE_API_ENDPOINT;
export async function fetchDepartmentData(department_id) {
    const response = await fetch(`${api}/departments/${department_id}`, { method: 'GET' });
    if (!response.ok) throw new Error('Failed to fetch employee department');
    return response.json();
}