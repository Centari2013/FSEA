import { client } from "../../apollo_client";
import { gql } from "@apollo/client/core";
import { setupEventListeners } from "../search/clickableCardsFunctionality";
import { createAlphabeticDirectory } from "./alphabeticDirectory";

// Define your GraphQL query using gql
const ORIGINS_QUERY = gql`
  query {
    allOrigins {
      originId
      originName
      discoveryDate
      description
    }
  }
`;

// Function to fetch and display the origin directory
export async function loadOriginDirectory() {
  try {
    // Fetch data using Apollo Client
    const result = await client.query({
      query: ORIGINS_QUERY
    });

    const origins = result.data.allOrigins;

    // Create the alphabetic directory with the fetched data
    createAlphabeticDirectory(origins, "originName", 'O', "Origins");
    setupEventListeners();
  } catch (error) {
    console.error('Error loading origin directory:', error);
    document.getElementById('main-content').innerHTML = '<p>Error loading the directory.</p>';
  }
}
