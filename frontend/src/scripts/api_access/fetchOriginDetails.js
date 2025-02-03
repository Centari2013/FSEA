import { client } from "./apollo_client";
import { gql } from "@apollo/client/core";


const query = gql`
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
                }`

export default async function fetchOriginDetails(origin_id) {
  try {
    const result = await client.query({
      query: query,
      variables: { originId: origin_id}
    });
    return result.data.origin;
  } catch (error) {
    console.error('GraphQL query error:', error);
    throw error;
  }
}
  

