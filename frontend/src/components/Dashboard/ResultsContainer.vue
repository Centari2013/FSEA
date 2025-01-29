<template>
  <div id="CardsContainer" class="flex flex-col items-center pb-40 pt-5 space-y-4">
    <template v-for="obj in results">
            <a class="card h-min-[17vh] border-1 rounded-md w-11/12 flex flex-col justify-center hover:shadow-md hover:cursor-pointer hover:scale-103 shadow-black" :data-type="obj.entityType" :class="getThreatCategory(obj.threat_level)">
                <div class="card-body flex flex-col items-start">
                    <h5 v-if="obj.entityType === 'E'" class="card-title text-xl font-bold">{{ `${obj.first_name} ${obj.last_name}`}}</h5>
                    <h5 v-if="obj.entityType === 'S'" class="card-title text-xl font-bold">{{ obj.specimen_name }}</h5>
                    <h5 v-if="obj.entityType === 'M'" class="card-title text-xl font-bold">{{obj.mission_name}}</h5>
                    <h5 v-if="obj.entityType === 'O'" class="card-title text-xl font-bold">{{obj.origin_name}}</h5>

                    <p class="card-text flex flex-col items-start text-left">
                        <template v-if="obj.entityType === 'E'">
                        <div><strong>Employee ID:</strong> {{ obj.employee_id }}</div>
                        <div><strong>Department:</strong> {{ obj.department }}</div>
                        <div><strong>Designations:</strong> {{ getDesignationString(obj) }}</div>
                        </template>

                        <template v-if="obj.entityType === 'S'">
                        <div><strong>Specimen ID:</strong> {{ obj.specimen_id }}</div>
                        <div><strong>Threat Level:</strong> {{ obj.threat_level }}</div>
                        <div><strong>Acquisition Date:</strong> {{ obj.acquisition_date }}</div>
                        </template>

                        <template v-if="obj.entityType === 'M'">
                        <div><strong>Mission ID:</strong> {{ obj.mission_id }}</div>
                        <div><strong>Start Date:</strong> {{ obj.start_date }}</div>
                        <div><strong>End Date:</strong> {{ obj.end_date }}</div>
                        <div>{{ obj.description || "No description available." }}</div>
                        </template>

                        <template v-if="obj.entityType === 'O'">
                        <div><strong>Origin ID:</strong> {{ obj.origin_id }}</div>
                        <div><strong>Discovery Date:</strong> {{ obj.discovery_date }}</div>
                        {{obj.description || "No description available."}}
                        </template>
                    </p>
                </div>
              </a>
       
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
    },
    getThreatCategory(threatLevel) {
      if (threatLevel <= 3) return "border-l-green-500";
      if (threatLevel <= 6) return "border-l-yellow-500";
      if (threatLevel > 6) return "border-l-red-500";
      return '';
    }
  }
}
</script>
