<template>
  <div>
    <h1>{{ department.departmentName }} Department</h1>
    <p><strong>Director:</strong> {{ department.director.firstName }} {{ department.director.lastName }}</p>
    <p><strong>Description:</strong> {{ department.description }}</p>

    <h3>Missions</h3>
    <table class="table">
      <thead>
        <tr>
          <th>Mission ID</th>
          <th>Mission Name</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="mission in department.missions" :key="mission.missionId">
          <td>{{ mission.missionId }}</td>
          <td>{{ mission.missionName }}</td>
        </tr>
      </tbody>
    </table>

    <h3>Employees</h3>
    <table class="table">
      <thead>
        <tr>
          <th>Last Name</th>
          <th>First Name</th>
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

export default {
  props: { departmentId: String },
  data(){
    return {
      department: null,
    }
  },
  mounted(){
    this.department = await fetchDepartmentDetails(this.departmentId);

    const sortedEmployees = computed(() => {
      return department?.employees
        ? [...department.employees].sort((a, b) => a.lastName.localeCompare(b.lastName))
        : [];
    });

    return { department, sortedEmployees };
  },
};
</script>
