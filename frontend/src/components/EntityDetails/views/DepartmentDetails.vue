<template>
  <LoadSpinner v-if="loading"/>
  <div v-else
  class="shadow-xl bg-zinc-700 rounded-xl p-10 text-left space-y-5"
  >
    <h1>{{ department.departmentName }} Department</h1>
    <p><strong>Director:</strong> {{ department.director.firstName }} {{ department.director.lastName }} (ID: {{department.director.employeeId }})</p>
    <p><strong>Description:</strong> {{ department.description }}</p>
    <div class="flex space-x-4 items-center mb-1">
      <h3 class="text-2xl">Missions</h3>
      <button>See More</button>
    </div>
    
    <hr class="mb-7">
    <table class="table-fixed w-full">
      <thead>
        <tr class="h-10 bg-zinc-900">
          <th class="w-1/6 pl-2">Mission ID</th>
          <th>Mission Name</th>
        </tr>
      </thead>
      <tbody>
        <tr class="h-10 even:bg-zinc-800 border border-collapse border-l-0 border-r-0" v-for="mission in department.missions" :key="mission.missionId">
          <td class="pl-2">{{ mission.missionId }}</td>
          <td>{{ mission.missionName }}</td>
        </tr>
      </tbody>
    </table>

    <h3>Employees
      <button>
            See More
        </button>
    </h3>
    <hr>
    <table class="table-fixed w-full">
      <thead>
        <tr>
          <th class="w-1/6">Last Name</th>
          <th class="w-1/6">First Name</th>
          <th>Designation</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="emp in sortedEmployees" :key="emp.employeeId">
          <td>{{ emp.lastName }}</td>
          <td>{{ emp.firstName }}</td>
          <td>{{ emp.designations.map(d => d.abbreviation).join(', ') }}</td>
        </tr>
      </tbody>
    </table>
  </div>
  
</template>

<script>
import fetchDepartmentDetails from "../../../scripts/api_access/fetchDepartmentDetails";
import LoadSpinner from "../../Dashboard/animations/LoadSpinner.vue";

export default {
  components: { LoadSpinner },
  props: { id: String },
  data(){
    return {
      department: null,
      sortedEmployees: [],
      loading: true,
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
      this.loading = false;
    }
  }
};
</script>
