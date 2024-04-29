const api = import.meta.env.VITE_API_ENDPOINT;

export async function fetchOriginDetails(originId) {
    const response = await fetch(api, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
            query: `
                query Origin($originId: String!) {
                    origin(originId: $originId){
                        originId
                        originName
                        discoveryDate
                        description
                        notes
                        missions{
                          missionId
                          missionName
                          startDate
                          endDate
                        }
                        specimens{
                          specimenId
                          specimenName
                          acquisitionDate
                        }
                        
                      }
                }`,
            variables: { originId: originId }
        }),
    });

    if (!response.ok) throw new Error('Failed to fetch origin details');
    const jsonResponse = await response.json();
    return jsonResponse.data.origin;
}
