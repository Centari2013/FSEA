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
    RESULTS_PER_PAGE: {
      type: Number,
      default: 25
    }
  },
  data() {
    return {
      currentPage: 1,
      totalPages: 1,
      rawResults: [],
      preparedResults: [],
      loading: false
    };
  },
  emits: [
    "setHidePagination",
    "setDisableNext",
    "setDisablePrev",
    "newTotalPages",
    "pageChanged",
    "scrollToTop"
  ],
  watch: {
    fetchTrigger(_data){
      this.fetchData();
    },
    rawResults(newResults) {
      this.$emit("setHidePagination", newResults.length === 0);
      this.$emit("scrollToTop");
    },
    currentPage(newPage) {
      this.$emit("setDisableNext", newPage === this.totalPages);
      this.$emit("setDisablePrev", newPage === 1);
      this.$emit("pageChanged", newPage);
    },
    totalPages(newTotalPages) {
      this.$emit("newTotalPages", newTotalPages);
    }
  },
  mounted() {
    this.fetchData();
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
        this.totalPages = Math.ceil(this.rawResults.length / this.RESULTS_PER_PAGE);
        this.prepareResults();

        this.$nextTick(() => { this.currentPage = 1; });

      } catch (error) {
        console.error("GraphQL Error:", error);
      } finally {
        this.loading = false;
      }
    },
    prepareResults() {
      if (!Array.isArray(this.rawResults)) return;
      const startIndex = (this.currentPage - 1) * this.RESULTS_PER_PAGE;
      const endIndex = startIndex + this.RESULTS_PER_PAGE;
      const pageResults = this.rawResults.slice(startIndex, endIndex);

      this.preparedResults = this.resultProcessor(pageResults);
    },
    changePage(page) {
      this.currentPage = page;
      this.prepareResults();
    }
  }
};
</script>
