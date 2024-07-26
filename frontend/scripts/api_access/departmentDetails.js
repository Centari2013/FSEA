import { client } from "./apollo_client";
import { gql } from "@apollo/client/core";


const query = gql`
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
  }`

export async function fetchDepartmentDetails(departmentId) {
  try {
    const result = await client.query({
      query: query,
      variables: { departmentId: departmentId }
    });
    return result.data.department;
  } catch (error) {
    console.error('GraphQL query error:', error);
    throw error;
  }
}
  