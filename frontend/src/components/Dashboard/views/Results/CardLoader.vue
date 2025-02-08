<template>
  <LoadSpinner v-if="loading" />
  <template v-else v-for="obj in preparedResults">
    <EntityCard :entity="obj" />
  </template>
</template>

<script>
import { client } from "../../../../scripts/api_access/apollo_client";
import EntityCard from "./EntityCard.vue";
import LoadSpinner from "../../animations/LoadSpinner.vue";
import { usePaginationStore } from "../../../stores/paginationStore";

export default {
  components: { EntityCard, LoadSpinner },
  props: {
    queryType: {
      type: String, // "query" or "mutation"
      required: true
    },
    query: {
      type: Object, // GraphQL query or mutation
      required: true
    },
    variables: {
      type: Object, // Variables for GraphQL call
      default: () => ({})
    },
    fetchTrigger: {
      type: [String, Number, Object, Array], // Can be anything
      default: null
    },
    resultProcessor: {
      type: Function, // A function to process raw results
      required: true
    },
    responseParser: {
      type: Function,
      required: true,
    },
    blockFetch: {
      type: Boolean,
      default: false,
    }
    
  },
  data() {
    return {
      store: usePaginationStore(),
      rawResults: [],
      preparedResults: [],
      loading: false
    }
  },
  computed: {
    currentPage() {
      return this.store.currentPage;
    },
  },
  watch: {
    fetchTrigger(_data){
      if (!this.blockFetch){
        this.fetchData();
      }else{
        this.preparedResults = [];
      }
    },
    rawResults(newResults) {
      this.store.setHidePagination(newResults.length === 0);
    },
    currentPage(newPage) {
      console.log('poop')
      this.prepareResults();
      this.store.setDisableNext(newPage === this.store.totalPages)
      this.store.setDisablePrev(newPage === 1);
    },
  },
  mounted() {
    if (!this.blockFetch) {
      this.fetchData();
    }
    
  },
  methods: {
    async fetchData() {
      this.loading = true;
      this.preparedResults = [];

      try {
        //console.log("Fetching data with:", this.queryType, this.query, this.variables);

        const { data } = this.queryType === "mutation"
          ? await client.mutate({ mutation: this.query, variables: this.variables })
          : await client.query({ query: this.query, variables: this.variables });

        // Use the provided responseParser function to correctly extract results
        this.rawResults = this.responseParser(data);
        this.store.setTotalPages(Math.ceil(this.rawResults.length / this.store.resultsPerPage));
        this.prepareResults();

        this.store.setCurrentPage(999);
        this.$nextTick(() => { this.store.setCurrentPage(1) }); // force currentPage watcher to fire
        

      } catch (error) {
        console.error("GraphQL Error:", error);
      } finally {
        this.loading = false;
      }
    },
    prepareResults() {
      if (!Array.isArray(this.rawResults)) return;
      const startIndex = (this.store.currentPage - 1) * this.store.resultsPerPage;
      const endIndex = startIndex + this.store.resultsPerPage;
      const pageResults = this.rawResults.slice(startIndex, endIndex);

      this.preparedResults = this.resultProcessor(pageResults);
    },
  }
};
</script>
