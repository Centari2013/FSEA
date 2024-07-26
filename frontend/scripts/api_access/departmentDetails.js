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

export async function fetchDepartmentDetails(department_id) {
  const result = await client
    .query({
      query: query,
      variables: {department_id: department_id}
    });
  console.log(result);
 
}