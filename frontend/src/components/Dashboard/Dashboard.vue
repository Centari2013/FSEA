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
      <div class="shadow-[3px_1px_5px_0px_rgba(0,0,0)] p-4 sticky top-0 space-y-4">
        <!-- Search Bar with Button -->
        <div class="">
          <form id="search-form" class="space-x-2">
            <input @keyup.enter="performSearch" v-model="query" placeholder="General Search..." type="text" id="search-bar" required class="form-control h-1/2 w-3/7 rounded-sm p-2 border-1">
            <button @click.prevent="performSearch" id="search-button">Search</button>
          </form>
        </div>
        <!-- Pagination -->
        <nav>
          <ul class="flex justify-center">
            <li class="prev" :class="isPrevDisabled() ? 'disabled' : ''" @click.prevent="!isPrevDisabled() ? changePage(currentPage - 1) : null" id="prevPage">Previous</li>
              <div ref="paginationContainer" class=" flex justify-center">
                <!-- Dynamically insert page numbers here -->
              </div>
            <li class="next" :class="isNextDisabled() ? 'disabled' : ''" @click.prevent="!isNextDisabled() ? changePage(currentPage + 1) : null" id="nextPage">Next</li>
          </ul>
        </nav>
      </div>
      <div ref="mainContent" class="h-screen overflow-auto">
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
import setupPagination from "../../scripts/pagination";

export default {
  components: { MenuButton, ResultsContainer },
  data() {
    return {
      totalPages: 0,
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
    currentPage: 1,
    RESULTS_PER_PAGE: 25,
    }

  },
  methods: {
    async performSearch() {
      this.currentPage = 1;
      this.query = this.query.trim()
      if (this.query.length === 0) return;
      try {
          const { data: { search: { results } } } = await client.mutate({
              mutation: this.SEARCH_MUTATION,
              variables: { query: this.query }
          });
          this.rawResults = results; // Store all results
          this.prepareResults();
          this.totalPages = Math.ceil(this.rawResults.length / this.RESULTS_PER_PAGE);
          setupPagination(this);
      } catch (error) {
          console.error('Error:', error);
      }
    },
    prepareResults() {
      this.$refs.mainContent.scrollTo({ top: 0, behavior: "smooth" });
      this.preparedResults = []; // clear prepared results
      const startIndex = (this.currentPage - 1) * this.RESULTS_PER_PAGE;
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
    },
    changePage(page) {
      this.currentPage = page;
      this.prepareResults(); // Update display based on the new page number
      setupPagination(this);
    },
    isNextDisabled(){
      return this.currentPage === this.totalPages;
    },
    isPrevDisabled(){
      return this.currentPage === 1;
    }
  }
}
</script>
<style>
@reference "tailwindcss";

.page-item, .prev, .next {
  @apply border-1 rounded-none  h-10 flex justify-center items-center hover:bg-gray-800 hover:cursor-pointer;
}

.page-item {
  @apply border-l-0 w-8;
}

.prev, .next {
  @apply p-3;
}

.prev {
  @apply rounded-l-md;
}

.next {
  @apply rounded-r-md;
}

.disabled {
  @apply bg-gray-900/50 pointer-events-none select-none;
}

</style>