import { client } from "../../apollo_client";
import { gql } from "@apollo/client/core";
import { cardContainer } from "../search/cardTemplates";
import { departmentDirectoryCard, titleCard } from "./directoryCardTemplates";
import { setupEventListeners } from "../search/clickableCardsFunctionality";

// Define your GraphQL query using gql
const DEPARTMENTS_QUERY = gql`
  query {
    allDepartments {
      departmentId
      departmentName
      description
    }
  }
`;

// Function to fetch and display department directory
export async function loadDepartmentDirectory() {
  try {
    // Fetch data using Apollo Client
    const result = await client.query({
      query: DEPARTMENTS_QUERY
    });

    const departments = result.data.allDepartments;

    // Create and populate the cards container
    const cardsContainer = cardContainer();
    cardsContainer.innerHTML += titleCard("Employee Departments");

    departments.forEach(department => {
      const departmentCardHtml = departmentDirectoryCard(department);
      cardsContainer.innerHTML += departmentCardHtml;
    });

    // Append the cards container to the main content area
    const mainContentArea = document.getElementById('main-content');
    mainContentArea.appendChild(cardsContainer);

    // Set up event listeners
    setupEventListeners();
  } catch (error) {
    console.error('Error loading department directory:', error);
    document.getElementById('main-content').innerHTML = '<p>Error loading the directory.</p>';
  }
}
