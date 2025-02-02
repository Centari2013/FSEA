<template>
  <CardLoader 
  ref="CardLoader"
  :queryType="'mutation'" 
  :query="SEARCH_MUTATION"
  :variables="{ query: cleanQuery }"
  :resultProcessor="prepareResults"
  :responseParser="parseSearchResults"
  :RESULTS_PER_PAGE="RESULTS_PER_PAGE"
  :fetchTrigger="cleanQuery"
  @setHidePagination="$emit('setHidePagination', $event)"
  @setDisableNext="$emit('setDisableNext', $event)"
  @setDisablePrev="$emit('setDisablePrev', $event)"
  @newTotalPages="$emit('newTotalPages', $event)"
  @pageChanged="$emit('pageChanged', $event)"
  @scrollToTop="$emit('scrollToTop', $event)"
  />
</template>

<script>
import { gql } from "@apollo/client/core";
import CardLoader from './CardLoader.vue';

export default {
  components: { CardLoader },
  props: {
    query: {
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
      cleanQuery: '',
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
  methods: {
    async performSearch() {
      
      if (this.query.trim().length === 0) return;
      this.cleanQuery = this.query.trim(); //triggers CardLoader fetch
    
    },
    parseSearchResults(data) {
    // Extracts from nested mutation response
    return data?.search?.results || [];
    },
    prepareResults(pageResults) {
      let preparedResults = []; // clear prepared results

      if (pageResults.length) {
        pageResults.forEach(result => {
            if (typeof result.data === 'string') {
                result.data = JSON.parse(result.data); // Parse it to a JavaScript object

            }
            result = { "entityType": result.entityType, ...result.data } // flatten data for ease of use
            preparedResults.push(result);
          });
      }

      return preparedResults;
    },
    changePage(page) {
    this.$refs.CardLoader.changePage(page);
    }
  }
}
</script>
