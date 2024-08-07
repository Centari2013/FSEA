import { client } from "./apollo_client";
import { gql } from "@apollo/client/core";


const query = gql`query Missions($mission_ids: [String]!){
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
                }`

export async function fetchMissionDetails(mission_ids) {
  try {
    const result = await client.query({
      query: query,
      variables: { mission_ids: mission_ids}
    });
    return result.data.missions;
  } catch (error) {
    console.error('GraphQL query error:', error);
    throw error;
  }
}
