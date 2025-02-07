<template>
  <LoadSpinner v-if="loading"/>
  <div v-else
  class="shadow-xl bg-zinc-700 rounded-xl p-10 text-left space-y-5"
  >
  <h1>{{specimen.specimenName}}</h1>
  <p><strong>Specimen ID:</strong> {{specimen.specimenId}}</p>
  <p><strong>Origin ID:</strong> {{specimen.originId}}</p>
  <p><strong>Mission ID:</strong> {{specimen.missionId}}</p>
  <p><strong>Threat Level:</strong> {{specimen.threatLevel}}</p>
  <p><strong>Acquisition Date:</strong> {{specimen.acquisitionDate}}</p>
  <p><strong>Description:</strong> {{specimen.description}}</p>
  <p><strong>Containment Statuses:</strong> {{specimen.containmentStatuses.map(status => status.statusName).join(', ')}}</p>

  <p>
  <SectionTitle :title="'Researchers Involved'"/>
      <ul class="space-y-4">
        <template v-for="r in specimen.researchers">
          <hr><li >{{r.employeeId}} - {{r.firstName}} {{r.lastName}}</li>
        </template>
      </ul>
  </p>

  <p>
    <Table
    :title="'Notes'"
    :headerTitles="['Timestamp', 'Note']"
    :keys="['timestamp', 'note']"
    :dictArr="specimen.notes ? JSON.parse(specimen.notes) : []"
    />
  </p>
  
  </div>
</template>

<script>
import fetchSpecimenDetails from '../../../scripts/api_access/fetchSpecimenDetails';
import LoadSpinner from "../../Dashboard/animations/LoadSpinner.vue";
import Table from './components/Table.vue';
import SectionTitle from './components/SectionTitle.vue';


export default {
  components: { LoadSpinner, Table, SectionTitle },
  props: { id: String },
  data(){
    return {
      specimen: null,
      loading: true,
    }
  },
  mounted(){
    this.fetchSpecimenDetails();
  },
  methods: {
    async fetchSpecimenDetails(){
  
      this.specimen = await fetchSpecimenDetails(this.id); 
      this.loading = false;
    }
  }
};
</script>
