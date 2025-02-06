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
    <p><strong>End Date:</strong> {{employee.endDate}}</p>

    <CollapsibleDiv>
      <template v-for="c in employee.clearances">
        <li><strong>{{c.clearanceName}}: </strong> {{c.description}}</li>
      </template>
    </CollapsibleDiv>


  </div>
  
</template>

<script>
import fetchEmployeeDetails from '../../../scripts/api_access/fetchEmployeeDetails';
import LoadSpinner from "../../Dashboard/animations/LoadSpinner.vue";
import CollapsibleTable from "./components/CollapsibleTable.vue";
import CollapsibleDiv from './components/CollapsibleDiv.vue';

export default {
  components: { LoadSpinner, CollapsibleTable, CollapsibleDiv },
  props: { id: String },
  data(){
    return {
      employee: null,
      loading: true,
    }
  },
  mounted(){
    this.fetchDepartmentDetails();
  },
  methods: {
    async fetchEmployeeDetails(){
  
      this.employee = await fetchEmployeeDetails(this.id); 
      this.loading = false;
    }
  }
};
</script>
