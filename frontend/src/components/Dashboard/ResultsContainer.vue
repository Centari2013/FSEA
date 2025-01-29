<template>
  <div id="CardsContainer" class="flex flex-col justify-center pb-40">
    <template v-for="obj in results">
      <div class="">
        <a  class="">
            <div class="card h-50" data-type="employee" >
                <div class="card-body">
                    <h5 v-if="obj.entityType === 'E'" class="card-title">{{ `${obj.first_name} ${obj.last_name}`}} </h5>
                    <h5 v-if="obj.entityType === 'S'" class="card-title">{{ obj.specimen_name }}</h5>
                    <h5 v-if="obj.entityType === 'M'" class="card-title"> {{obj.mission_name}}</h5>
                    <h5 v-if="obj.entityType === 'O'" class="card-title"> {{obj.origin_name}}</h5>

                    <p class="card-text">
                      <template v-if="obj.entityType === 'E'">
                        <strong>Employee ID:</strong>{{ obj.employee_id }}<br>
                        <strong>Department:</strong> {{ obj.department }}<br>
                        <strong>Designations:</strong> {{ getDesignationString(obj) }}
                      </template>

                      <template v-if="obj.entityType === 'S'">
                        <strong>Specimen ID:</strong>{{ obj.specimen_id }}<br>
                        <strong>Threat Level:</strong> {{obj.threat_level}}<br>
                        <strong>Acquisition Date:</strong> {{obj.acquisition_date}}<br>
                      </template>

                      <template v-if="obj.entityType === 'M'">
                        <strong>Mission ID:</strong> {{obj.mission_id}}<br>
                        <strong>Start Date:</strong> {{obj.start_date}}<br>
                        <strong>End Date:</strong> {{obj.end_date}}<br>
                        {{obj.description || "No description available."}}
                      </template>

                      <template v-if="obj.entityType === 'O'">
                        <strong>Origin ID:</strong> {{obj.origin_id}}<br>
                        <strong>Discovery Date:</strong> {{obj.discovery_date}}<br>
                        {{obj.description || "No description available."}}
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
  },
  methods: {
    getDesignationString(employee){
      return employee.designations ? employee.designations.map(d => d.abbreviation).join(', '): ""
    }
  }
}
</script>