<template>
  <template v-for="obj in preparedResults">
    <EntityCard :entity="obj" />
  </template>
</template>

<script>
import { client } from '../../../../scripts/api_access/apollo_client';
import { gql } from "@apollo/client/core";
import EntityCard from './EntityCard.vue';

export default {
components: { EntityCard },
props: {
  currentDirectory: {
    type: String,
    required: true,
  },
  RESULTS_PER_PAGE: {
    type: Number,
    default: 25,
  },
},
data() {
  return {
    CURRENT_MUTATION: '',
    
    GET_ALL_DEPARTMENTS_QUERY: gql`
    query {
        allDepartments{
            departmentId
            departmentName
            description
        }
    }`,
    currentPage: 1,
    totalPages: 1,
    rawResults: [],
    preparedResults: [],
  }
},
emits: [
  "setHidePagination",
  "setDisableNext",
  "setDisablePrev",
  "newTotalPages",
  "pageChanged",
  "scrollToTop",
],
watch: {
  currentDirectory(newDirectory){
    switch(newDirectory) {
      case "Department Directory":
        this.CURRENT_MUTATION = this.GET_ALL_DEPARTMENTS_QUERY;
    }
    this.getEntities();
  },
  rawResults(newResults){
    if (newResults.length == 0) {
      this.$emit("setHidePagination", true);
    }else {
      this.$emit("setHidePagination", false);
    }

    this.$emit("scrollToTop");
  },
  currentPage(newPage){
    if (newPage == this.totalPages){
      this.$emit("setDisableNext", true);
    }else {
      this.$emit("setDisableNext", false);
    }

    if (newPage == 1){
      this.$emit("setDisablePrev", true);
    }else {
      this.$emit("setDisablePrev", false);
    }

    this.$emit("pageChanged", newPage);
  },
  totalPages(newTotalPages){
    this.$emit("newTotalPages", newTotalPages);
    
  }

},
methods: {
  async getEntities() {
    const query = this.query.trim()
    if (query.length === 0) return;
    try {
        const { data: { search: { results } } } = await client.mutate({
            mutation: this.CURRENT_MUTATION,
            variables: { query: query }
        });
        this.rawResults = results; // Store all results
        this.prepareResults();
        this.totalPages = Math.ceil(this.rawResults.length / this.RESULTS_PER_PAGE);

        // force watch trigger without moving emits into this function
        this.currentPage = null; 
        this.$nextTick(() => { 
          this.currentPage = 1; 
        });

    } catch (error) {
        console.error('Error:', error);
    }
  },
  prepareResults() {
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
  },
}
}
</script>
