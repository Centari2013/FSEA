const api = import.meta.env.VITE_API_ENDPOINT;
export async function fetchMissionDetails(mission_ids) {
    const response = await fetch(api, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
            query: `
                query Missions($mission_ids: [String]!){
                    missions(missionIds: $mission_ids){
                        missionId
                        missionName
                        startDate
                        endDate
                        commander{
                          employeeId
                          firstName
                          lastName
                        }
                            
                            supervisor{
                          employeeId
                          firstName
                          lastName
                        }
                        description
                        origins{
                          originId
                          originName
                        }
                        notes
                        departments{
                          departmentName
                        }
                        employees{
                          employeeId
                          firstName
                          lastName
                        }
                      }
                }`,
            variables: {mission_ids: mission_ids}
        }),
    });
    if (!response.ok) throw new Error('Failed to fetch mission data');
    const jsonResponse = await response.json();
    return jsonResponse.data.missions;
}