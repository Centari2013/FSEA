<template>
  <LoadSpinner v-if="loading"/>
  <div v-else
  class="shadow-xl bg-zinc-700 rounded-xl p-10 text-left space-y-5"
  >
    <h1>{{ mission.missionName }}</h1>
    <p><strong>Mission ID:</strong> {{mission.missionId}}</p>
    <p><strong>Departments Involved:</strong> {{mission.departments.map(dept => dept.departmentName).join(', ')}}</p>
    <p><strong>Start Date:</strong> {{mission.startDate}}</p>
    <p><strong>End Date:</strong> {{mission.endDate ? mission.endDate: 'Ongoing'}}</p>
    <p><strong>Commander:</strong> {{mission.commander.firstName}} {{mission.commander.lastName}}</p>
    <p><strong>Supervisor:</strong> {{mission.supervisor.firstName}} {{mission.supervisor.lastName}}</p>
    <p><strong>Description:</strong> {{mission.description}}</p>

    <p><strong>Origins:</strong><br>
        <ul>
          <li v-for="o in mission.origins"> {{ o.originId }} - {{ o.originName }}</li>
        </ul>
    </p>

    <p><strong>Employees Involved:</strong><br>
        <ul>
          <li v-for="e in mission.employees">{{e.employeeId}} - {{e.firstName}} {{e.lastName}}</li>
        </ul>
    </p>

    <p><strong>Notes</strong><br>
      <Table
      :headerTitles="['Timestamp', 'Note']"
      :keys="['timestamp', 'note']"
      :dictArr="mission.notes ? JSON.parse(mission.notes) : {}"
      />
    </p>

  </div>
  
</template>

<script>
import fetchMissionDetails from '../../../scripts/api_access/fetchMissionDetails';
import LoadSpinner from "../../Dashboard/animations/LoadSpinner.vue";
import CollapsibleTable from "./components/CollapsibleTable.vue";
import CollapsibleDiv from './components/CollapsibleDiv.vue';
import Table from './components/Table.vue';

export default {
  components: { LoadSpinner, CollapsibleTable, CollapsibleDiv, Table },
  props: { id: String },
  data(){
    return {
      mission: null,
      loading: true,
    }
  },
  mounted(){
    this.fetchMissionDetails();
  },
  methods: {
    async fetchMissionDetails(){
      this.mission = await fetchMissionDetails(this.id); 
      this.loading = false;
      console.log(this.mission)
    }
  }
};
</script>
