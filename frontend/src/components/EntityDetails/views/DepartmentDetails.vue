<template>
  <LoadSpinner v-if="loading"/>
  <div v-else
  class="shadow-xl bg-zinc-700 rounded-xl p-10 text-left space-y-5"
  >
    <h1>{{ department.departmentName }} Department</h1>
    <p><strong>Director:</strong> {{ department.director.firstName }} {{ department.director.lastName }} (ID: {{department.director.employeeId }})</p>
    <p><strong>Description:</strong> {{ department.description }}</p>
    
    <CollapsibleTable :title="'Missions'"
    :headerTitles="['Mission ID', 'Mission Name']"
    :dictArr="department.missions"
    :keys="['missionId', 'missionName']"
    />
    
    <CollapsibleTable :title="'Employees'" 
    :headerTitles="['Last Name', 'First Name', 'Designation']"
    :dictArr="sortedEmployees"
    :keys="['lastName', 'firstName', 'designations']"
    />

  </div>
  
</template>

<script>
import fetchDepartmentDetails from "../../../scripts/api_access/fetchDepartmentDetails";
import LoadSpinner from "../../Dashboard/animations/LoadSpinner.vue";
import CollapsibleTable from "./components/CollapsibleTable.vue";

export default {
  components: { LoadSpinner, CollapsibleTable },
  props: { id: String },
  data(){
    return {
      department: null,
      sortedEmployees: [],
      loading: true,
      sortedAbbreviations: null,
    }
  },
  mounted(){
    this.fetchDepartmentDetails();
  },
  methods: {
    async fetchDepartmentDetails(){
  
      this.department = await fetchDepartmentDetails(this.id); 
      this.sortedEmployees = this.department?.employees
        ? [...this.department.employees].sort((a, b) => a.lastName.localeCompare(b.lastName))
        : [];

        this.sortedEmployees = this.sortedEmployees.length
          ? this.sortedEmployees.map(emp => ({
              ...emp,
              designations: emp.designations.map(d => d.abbreviation).join(', ')
            }))
          : [];
  
      this.loading = false;
    }
  }
};
</script>
