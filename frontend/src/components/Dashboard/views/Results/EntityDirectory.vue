<template>
  <CardLoader 
  ref="CardLoader"
  :queryType="'query'" 
  :query="CURRENT_QUERY"
  :resultProcessor="prepareResults"
  :responseParser="parseEntityResults"
  :fetchTrigger="CURRENT_QUERY"
  />
</template>

<script>
import { gql } from "@apollo/client/core";
import CardLoader from './CardLoader.vue';

export default {
components: { CardLoader },
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
    CURRENT_QUERY: gql`
    query {
        allDepartments{
            departmentId
            departmentName
            description
        }
    }`,
    
    GET_ALL_DEPARTMENTS_QUERY: gql`
    query {
        allDepartments{
            departmentId
            departmentName
            description
        }
    }`,
    GET_ALL_ORIGINS_QUERY: gql`
    query {
      allOrigins{
          originId
          originName
          discoveryDate
          description
        }
    }`,
    GET_ALL_SPECIMENS_QUERY: gql`
    query {
      allSpecimens{
        specimenId
        specimenName
        threatLevel
        acquisitionDate
      }
    }`,
    TEST_QUERY: gql`{
      allClearances{
        clearanceId
        clearanceId
        description
      }
    }`,
    
  }
},
emits: [
  "scrollToTop",
],
watch: {
  currentDirectory(newDirectory){
    this.setQuery(newDirectory);
  },

},
mounted() {
  this.setQuery(this.currentDirectory);
  this.$refs.CardLoader.fetchData();
},
methods: {
  setQuery(newDirectory){
    switch(newDirectory) {
      case "Department Directory":
        this.CURRENT_QUERY = this.GET_ALL_DEPARTMENTS_QUERY;
        break;
      case "Origin Directory":
        this.CURRENT_QUERY = this.GET_ALL_ORIGINS_QUERY;
        break;
      case "Specimen Directory":
        this.CURRENT_QUERY = this.GET_ALL_SPECIMENS_QUERY;
        break;
      default:
        this.CURRENT_QUERY = this.TEST_QUERY;
        break;
    }
  },
  
  parseEntityResults(data) {
    // Extracts the first key from the query response
    const resultKey = Object.keys(data)[0];
    return data[resultKey] || [];
  },
  mapKeytoEntityType(result){
    let newResult = { ...result }
    // Determine entity type based on ID prefix
    for (const key in result) {
      if (key.endsWith("Id")) {
        const prefix = key.replace("Id", ""); // Extract the prefix
        const entityMapping = {
          //employee: "EDir",
          specimen: "SDir",
          //mission: "MDir", 
          origin: "ODir",
          department: "DDir"
        };

        // Check if prefix matches one of the expected entity types
        if (entityMapping[prefix]) {
          newResult.entityType = entityMapping[prefix];
          break; // Stop once we find the correct ID
        }
      }
    }
    return newResult;
  },
  prepareResults(pageResults) {
    let preparedResults = [];
    if (pageResults.length) {
      pageResults.forEach(result => {
          if (typeof result.data === 'string') {
              result.data = JSON.parse(result.data); // Parse it to a JavaScript object

          }
          result = this.mapKeytoEntityType(result);
          preparedResults.push(result);
        });
    }
    return preparedResults;
  },
}
}
</script>
