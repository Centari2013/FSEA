<template>
  <div id="CardsContainer" ref="CardsContainer" class="flex flex-col items-center pb-40 pt-5 space-y-4 h-full overflow-auto">
    <template v-for="obj in preparedResults">
            <a class="card h-min-[17vh] border-1 rounded-md w-11/12 flex flex-col justify-center hover:shadow-md hover:cursor-pointer hover:scale-103 shadow-black" :data-type="obj.entityType" :class="getThreatCategory(obj.threat_level)">
                <div class="card-body flex flex-col items-start">
                    <h5 v-if="obj.entityType === 'E'" class="card-title text-xl font-bold">{{ `${obj.first_name} ${obj.last_name}`}}</h5>
                    <h5 v-if="obj.entityType === 'S'" class="card-title text-xl font-bold">{{ obj.specimen_name }}</h5>
                    <h5 v-if="obj.entityType === 'M'" class="card-title text-xl font-bold">{{obj.mission_name}}</h5>
                    <h5 v-if="obj.entityType === 'O'" class="card-title text-xl font-bold">{{obj.origin_name}}</h5>

                    <p class="card-text flex flex-col items-start text-left">
                        <template v-if="obj.entityType === 'E'">
                        <div><strong>Employee ID:</strong> {{ obj.employee_id }}</div>
                        <div><strong>Department:</strong> {{ obj.department }}</div>
                        <div><strong>Designations:</strong> {{ getDesignationString(obj) }}</div>
                        </template>

                        <template v-if="obj.entityType === 'S'">
                        <div><strong>Specimen ID:</strong> {{ obj.specimen_id }}</div>
                        <div><strong>Threat Level:</strong> {{ obj.threat_level }}</div>
                        <div><strong>Acquisition Date:</strong> {{ obj.acquisition_date }}</div>
                        </template>

                        <template v-if="obj.entityType === 'M'">
                        <div><strong>Mission ID:</strong> {{ obj.mission_id }}</div>
                        <div><strong>Start Date:</strong> {{ obj.start_date }}</div>
                        <div><strong>End Date:</strong> {{ obj.end_date }}</div>
                        <div>{{ obj.description || "No description available." }}</div>
                        </template>

                        <template v-if="obj.entityType === 'O'">
                        <div><strong>Origin ID:</strong> {{ obj.origin_id }}</div>
                        <div><strong>Discovery Date:</strong> {{ obj.discovery_date }}</div>
                        {{obj.description || "No description available."}}
                        </template>
                    </p>
                </div>
              </a>
       
    </template>
  </div>
</template>

<script>
import { client } from '../../../scripts/api_access/apollo_client';
import { gql } from "@apollo/client/core";

export default {
  props: {
    query: {
      type: String,
      required: true,
    }
  },
  data() {
    return {
      totalPages: 1,
      rawResults: [],
      preparedResults: [],
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
  watch: {
    rawResults(newResults){
      if (newResults.length == 0) {
        this.$emit("setHidePagination", true);
      }else {
        this.$emit("setHidePagination", false);
      }
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
    async performSearch() {
      const query = this.query.trim()
      if (query.length === 0) return;
      try {
          const { data: { search: { results } } } = await client.mutate({
              mutation: this.SEARCH_MUTATION,
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
      this.$refs.CardsContainer.scrollTo({ top: 0, behavior: "smooth" });
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

    getDesignationString(employee){
      return employee.designations ? employee.designations.map(d => d.abbreviation).join(', '): ""
    },
    getThreatCategory(threatLevel) {
      if (threatLevel <= 3) return "border-l-green-500";
      if (threatLevel <= 6) return "border-l-yellow-500";
      if (threatLevel > 6) return "border-l-red-500";
      return '';
    }
  }
}
</script>
