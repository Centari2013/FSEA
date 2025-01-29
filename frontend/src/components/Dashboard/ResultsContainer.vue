<template>
  <div id="CardsContainer" class="flex flex-col justify-center">
    <template v-for="obj in results">
      <div class="">
        <a  class="">
            <div class="card h-50" data-type="employee" >
                <div class="card-body">
                    <h5 v-if="obj.entityType === 'E'" class="card-title">{{ `${obj.first_name} ${obj.last_name}`}} </h5>
                    <p class="card-text">
                      <!-- Employee -->
                      <template v-if="obj.entityType === 'E'">
                        <strong>Employee ID:</strong>{{ obj.employee_id }}<br>
                        <strong>Department:</strong> {{ obj.department }}<br>
                        <strong>Designations:</strong> {{ getDesignationString(obj) }}
                      </template>

                    </p>
                </div>
            </div>
        </a>
    </div>
    </template>
  </div>
</template>

<script>
export default {
  props: {
    results: {
      type: Object,
    },
    RESULTS_PER_PAGE: {
      type: Number,
      required: true,
    }
  },
  methods: {
    getDesignationString(employee){
      return employee.designations ? employee.designations.map(d => d.abbreviation).join(', '): ""
    }
  }
}
</script>