<template>
  <LoadSpinner v-if="loading"/>
  <div v-else
  class="shadow-xl bg-zinc-700 rounded-xl p-10 text-left space-y-5"
  >
    <h1>{{ employee.firstName}} {{ employee.lastName }}</h1>
    <p><strong>Employee ID:</strong> {{employee.employeeId}}</p>
    <p><strong>Department:</strong> {{employee.department.departmentName}}</p>
    <p><strong>Designation(s):</strong> {{employee.designations.map(d => `${d.designationName} (${d.abbreviation})`).join(', ')}}</p>
    <p><strong>Start Date:</strong> {{employee.startDate}}</p>
    <p><strong>End Date:</strong> {{employee.endDate ? employee.endDate: 'N/A'}}</p>

    <CollapsibleDiv :title="'Clearances'">
      <template v-for="c in employee.clearances">
        <li><strong>{{c.clearanceName}}: </strong> {{c.description}}</li>
      </template>
    </CollapsibleDiv>
    
    <CollapsibleTable
    :title="'Missions'"
    :headerTitles="['Mission ID', 'Mission Name', 'Employee Involvement']"
    :dictArr="employee.missions"
    :keys="['missionId', 'missionName', 'involvementSummary']"
    />

    <CollapsibleDiv :title="'Medical Data'">
      <div class="w-11/12 h-11/12 space-y-4 bg-zinc-600 p-5 rounded-xl ">
        <p><strong>Blood type:</strong> {{employee.medicalRecord.bloodtype}}</p>
        <p><strong>Height:</strong> {{employee.medicalRecord.heightCm}} cm</p>
        <p><strong>Weight:</strong> {{employee.medicalRecord.kilograms}} kg</p>
        
        <div class="mt-5 overflow-x-scroll">
        <Table
        :title="'Notes'"
        :headerTitles="['Timestamp', 'Note']"
        :keys="['timestamp', 'note']"
        :dictArr="employee.medicalRecord.notes ? JSON.parse(employee.medicalRecord.notes) : []"
        />
      </div>
      </div>
    </CollapsibleDiv>

  </div>
  
</template>

<script>
import fetchEmployeeDetails from '../../../scripts/api_access/fetchEmployeeDetails';
import LoadSpinner from "../../Dashboard/animations/LoadSpinner.vue";
import CollapsibleTable from "./components/CollapsibleTable.vue";
import CollapsibleDiv from './components/CollapsibleDiv.vue';
import Table from './components/Table.vue';

export default {
  components: { LoadSpinner, CollapsibleTable, CollapsibleDiv, Table },
  props: { id: String },
  data(){
    return {
      employee: null,
      loading: true,
    }
  },
  mounted(){
    this.fetchEmployeeDetails();
  },
  methods: {
    async fetchEmployeeDetails(){
  
      this.employee = await fetchEmployeeDetails(this.id); 
      this.loading = false;
    }
  }
};
</script>
