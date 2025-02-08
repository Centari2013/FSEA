import { client } from "./apollo_client";
import { gql } from "@apollo/client/core";


const query = gql`
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
                }`

export default async function fetchSpecimenDetails(specimen_id) {
  try {
    const result = await client.query({
      query: query,
      variables: { specimenId: specimen_id }
    });
    return result.data.specimen;
  } catch (error) {
    console.error('GraphQL query error:', error);
    throw error;
  }
}
  

