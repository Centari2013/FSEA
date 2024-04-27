const api = import.meta.env.VITE_API_ENDPOINT;

export async function fetchSpecimenDetails(specimenId) {
    const response = await fetch(api, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
            query: `
                query Specimen($specimenId: String!) {
                    specimen(specimenId: $specimenId){
                        specimenId
                        specimenName
                        originId
                        missionId
                        threatLevel
                        acquisitionDate
                        notes
                        description
                        containmentStatuses {
                            statusName
                        }
                        researchers {
                            employeeId
                            firstName
                            lastName
                        }
                    }
                }`,
            variables: { specimenId: specimenId }
        }),
    });

    if (!response.ok) throw new Error('Failed to fetch specimen details');
    const jsonResponse = await response.json();
    return jsonResponse.data.specimen;
}
