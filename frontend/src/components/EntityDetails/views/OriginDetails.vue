<template>
  <LoadSpinner v-if="loading"/>
  <div v-else
  class="shadow-xl bg-zinc-700 rounded-xl p-10 text-left space-y-5"
  >
    <h1>{{origin.name}}</h1>
    <p><strong>Origin ID:</strong> {{origin.originId}}</p>
    <p><strong>Discovery Date:</strong> {{origin.discoveryDate}}</p>
    <p><strong>Description:</strong> {{origin.description}}</p>

    <h3>Missions</h3>
    <Table
    :headerTitles="['Mission ID', 'Mission Name', 'Start Date', 'End Date']"
    :keys="['missionId', 'missionName', 'startDate', 'endDate']"
    :dictArr="origin.missions"
    />

    <h3>Specimens</h3>
    <Table
    :headerTitles="['Specimen ID', 'Specimen Name', 'Acquisition Date']"
    :keys="['specimenId', 'specimenName', 'acquisitionDate']"
    :dictArr="origin.specimens"
    />

    <p><strong>Notes</strong><br>
      <Table
      :headerTitles="['Timestamp', 'Note']"
      :keys="['timestamp', 'note']"
      :dictArr="origin.notes ? JSON.parse(origin.notes) : []"
      />
    </p>
  </div>
  
</template>

<script>
import fetchOriginDetails from '../../../scripts/api_access/fetchOriginDetails';
import LoadSpinner from "../../Dashboard/animations/LoadSpinner.vue";
import CollapsibleTable from "./components/CollapsibleTable.vue";
import CollapsibleDiv from './components/CollapsibleDiv.vue';
import Table from './components/Table.vue';

export default {
  components: { LoadSpinner, CollapsibleTable, CollapsibleDiv, Table },
  props: { id: String },
  data(){
    return {
      origin: null,
      loading: true,
    }
  },
  mounted(){
    this.fetchOriginDetails();
  },
  methods: {
    async fetchOriginDetails(){
  
      this.origin = await fetchOriginDetails(this.id); 
      this.loading = false;
    }
  }
};
</script>
