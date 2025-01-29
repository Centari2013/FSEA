<template>
  <div class="grid grid-cols-6 h-screen w-full overflow-hidden">
    <!-- Sidebar -->
    <div class="h-full pt-4 col-span-1 flex flex-col shadow-[2px_0px_5px_0px_rgba(0,0,0)]">
      <div class="h-1/8 mx-auto">
        <img src="../../assets/fsea_logo.png" alt="FSEA Logo" class="w-auto">
      </div>
      
      <ul id="menu" class="h-full flex flex-col space-y-4">
        <MenuButton name="Home"/>
        <MenuButton name="Department Directory"/>
        <MenuButton name="Origin Directory"/>
        <MenuButton name="Specimen Directory"/>
        <MenuButton name="Document Directory"/>
      </ul>
    </div>
    <!-- Main Content -->
    <div class="col-span-5">
      <div class="shadow-[3px_1px_5px_0px_rgba(0,0,0)] p-4 sticky top-0">
        <!-- Search Bar with Button -->
        <div class="">
          <form id="search-form" class="space-x-2">
            <input v-model="query" placeholder="General Search..." type="text" id="search-bar" required class="form-control h-1/2 w-3/7 rounded-sm p-2 border-1">
            <button @click.prevent="performSearch" id="search-button">Search</button>
          </form>
        </div>
        <!-- Pagination -->
        <nav>
          <ul>
            <li><a id="prevPage">Previous</a></li>
            <!-- Dynamically insert page numbers here -->
            <li><a id="nextPage">Next</a></li>
          </ul>
        </nav>
      </div>
      <div id="main-content" class="h-screen overflow-auto">
        <!-- Content will be loaded here -->
         <ResultsContainer :results="preparedResults" :RESULTS_PER_PAGE="RESULTS_PER_PAGE" ref="results-conatiner"/>
      </div>
    </div>
    
  </div>

  
</template>

<script>
import { client } from "../../scripts/api_access/apollo_client";
import { gql } from "@apollo/client/core";
import MenuButton from './MenuButton.vue';
import ResultsContainer from "./ResultsContainer.vue";

export default {
  components: { MenuButton, ResultsContainer },
  data() {
    return {
      rawResults: [],
      preparedResults: [],
      query: '',
      SEARCH_MUTATION: gql`
        mutation Search($query: String!) {
            search(query: $query) {
                results {
                    entityType
                    data
                }
            }
        }
    `,
    current_page: 1,
    RESULTS_PER_PAGE: 25,
    }

  },
  methods: {
    async performSearch() {
      try {
          const { data: { search: { results } } } = await client.mutate({
              mutation: this.SEARCH_MUTATION,
              variables: { query: this.query }
          });
          this.rawResults = results; // Store all results
          this.prepareResults();
          console.log(this.preparedResults)
      } catch (error) {
          console.error('Error:', error);
      }
    },
    prepareResults() {
      this.preparedResults = []; // clear prepared results
      const startIndex = (this.current_page - 1) * this.RESULTS_PER_PAGE;
      const endIndex = startIndex + this.RESULTS_PER_PAGE;
      const pageResults = this.rawResults.slice(startIndex, endIndex);

      if (pageResults.length) {
        pageResults.forEach(result => {
            if (typeof result.data === 'string') {
                result.data = JSON.parse(result.data); // Parse it to a JavaScript object

            }
            result = { "entityType": result.entityType, ...result.data } // flatten data for ease of use
            this.preparedResults.push(result);
          });
      }
    }
  }
}
</script>