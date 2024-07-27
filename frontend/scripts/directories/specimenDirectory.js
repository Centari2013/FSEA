import { client } from "../../apollo_client";
import { gql } from "@apollo/client/core";
import { setupEventListeners } from "../search/clickableCardsFunctionality";
import { createAlphabeticDirectory } from "./alphabeticDirectory";

// Define your GraphQL query using gql
const SPECIMENS_QUERY = gql`
  query {
    allSpecimens {
      specimenId
      specimenName
      threatLevel
      acquisitionDate
    }
  }
`;

// Function to fetch and display the specimen directory
export async function loadSpecimenDirectory() {
  try {
    // Fetch data using Apollo Client
    const result = await client.query({
      query: SPECIMENS_QUERY
    });

    const specimens = result.data.allSpecimens;

    // Create the alphabetic directory with the fetched data
    createAlphabeticDirectory(specimens, "specimenName", 'S', "Specimens");
    setupEventListeners();
  } catch (error) {
    console.error('Error loading specimen directory:', error);
    document.getElementById('main-content').innerHTML = '<p>Error loading the directory.</p>';
  }
}
