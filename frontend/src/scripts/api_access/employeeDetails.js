import { client } from "./apollo_client";
import { gql } from "@apollo/client/core";


const query = gql`
                query Employee($employeeId: String!){
                    employee(employeeId: $employeeId){
                        employeeId
                        firstName
                        lastName
                        department{
                          departmentName
                        }
                        medicalRecord {
                          dob
                          bloodtype
                          sex
                          kilograms
                          heightCm
                          notes
                        }
                        startDate
                        endDate
                        clearances{
                          clearanceName
                          description
                        }
                        missions {
                          missionId
                          missionName
                          involvementSummary
                        }
                        notes
                        designations {
                          designationName
                          abbreviation
                        }
                        
                      }
                }`

export async function fetchEmployeeData(employee_id) {
  try {
    const result = await client.query({
      query: query,
      variables: { employeeId: employee_id }
    });
    return result.data.employee;
  } catch (error) {
    console.error('GraphQL query error:', error);
    throw error;
  }
}
  