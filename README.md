# FSEA API Documentation

This document outlines the usage of the FSEA API endpoints.

## Authentication

### Login

- **POST** `/login`
  - Description: Authenticate a user.
  - Request Body: 
    ``` json
    {
        "username": "string", 
        "password": "string"
    }
  - Response: ```json
  { "token": "string" }

## Clearances

### Post Clearance

- **POST** `/clearances`
  - Description: Create a new clearance.
  - Request Body: 
    ```json 
    {
        "clearance_name": "string",
        "description": "string"
    } 
  - Response: 
    ```json
    {
        "clearance_id": 123
    }
### Get Clearance

- **GET** `/clearances/<int:clearance_id>`
  - Description: Retrieve details of a specific clearance.
  - Response: Returns clearance details.

### Patch Clearance

- **PATCH** `/clearances/<int:clearance_id>`
  - Description: Update specific fields of a clearance.
  - Request Body: Fields to be updated.
  - Response: Returns updated clearance details.

### Delete Clearance

- **DELETE** `/clearances/<int:clearance_id>`
  - Description: Remove a clearance from the database.
  - Response: Confirmation of deletion.

## Containment Statuses

(Similar structure as Clearances)

## Departments

### Post Department

- **POST** `/departments`
  - Description: Create a new department.
  - Request Body: Includes the department name, director_id (optional), and description.
  - Response: Returns the created department details.

### Get Department

- **GET** `/departments/<int:department_id>`
  - Description: Retrieve details of a specific department.
  - Response: Returns department details.

(Continue with Patch, Delete, AssociateMissionWithDepartment, etc., following the same structure)

## Designations

(Similar structure as Departments)

## Employees

(Similar structure, but ensure to include all the specific actions like associating clearances, designations, managing medical records, etc.)

## Missions

(Include actions for posting, getting, patching, deleting missions, associating origins, managing specimens, employees, etc.)

## Origins

(Similar structure as Missions)

## Specimens

(Include actions for posting, getting, patching, deleting specimens, associating containment statuses, medical records, missions, researchers, etc.)

## Other Endpoints

### Get Specimens For Containment Status

- **GET** `/containment_statuses/<int:containment_status_id>/specimens`
  - Description: Get all specimens associated with a containment status.
  - Response: Returns a list of specimens.

---

This template provides a basic structure. For each endpoint, you might also want to include:

- **URL Parameters**: For routes that require them (e.g., `<int:clearance_id>`).
- **Success Response**: Include a sample success response.
- **Error Response**: Include common error statuses (e.g., `404 Not Found`) with explanations.
- **Headers**: Mention any required headers (e.g., `Content-Type: application/json`).
- **Authentication**: Note if an endpoint requires authentication or specific permissions.

Remember, thorough documentation is invaluable for future you and any other developers working with your API!
