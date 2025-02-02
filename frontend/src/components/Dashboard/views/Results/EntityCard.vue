<template>
  <a 
        class="card h-min-[17vh] border-1 rounded-md w-11/12 flex flex-col justify-center 
              hover:shadow-md hover:cursor-pointer hover:scale-103 shadow-black 
              transition-transform duration-300 ease-in-out" 
        :data-type="entity.entityType" 
        :class="getThreatCategory(entity.threat_level || entity.threatLevel)"
      >             
                    <!-- Search Result Card Titles -->
                    <div class="card-body flex flex-col items-start">
                    <h5 v-if="entity.entityType === 'E'" class="card-title text-xl font-bold">{{ `${entity.first_name} ${entity.last_name}`}}</h5>
                    <h5 v-if="entity.entityType === 'S'" class="card-title text-xl font-bold">{{ entity.specimen_name }}</h5>
                    <h5 v-if="entity.entityType === 'M'" class="card-title text-xl font-bold">{{entity.mission_name}}</h5>
                    <h5 v-if="entity.entityType === 'O'" class="card-title text-xl font-bold">{{entity.origin_name}}</h5>
                    <h5 v-if="entity.entityType === 'D'" class="card-title text-xl font-bold">{{entity.department_name}}</h5>

                    <!-- Directory Result Titles -->
                    <h5 v-if="entity.entityType === 'DDir'" class="card-title text-xl font-bold">{{entity.departmentName}}</h5>
                    <h5 v-if="entity.entityType === 'SDir'" class="card-title text-xl font-bold">{{ entity.specimenName }}</h5>

                    <p class="card-text flex flex-col items-start text-left">
                        <!-- Search Result Card Text -->
                        <template v-if="entity.entityType === 'E'">
                        <div><strong>Employee ID:</strong> {{ entity.employee_id }}</div>
                        <div><strong>Department:</strong> {{ entity.department }}</div>
                        <div><strong>Designations:</strong> {{ getDesignationString(entity) }}</div>
                        </template>

                        <template v-if="entity.entityType === 'S'">
                        <div><strong>Specimen ID:</strong> {{ entity.specimen_id }}</div>
                        <div><strong>Threat Level:</strong> {{ entity.threat_level }}</div>
                        <div><strong>Acquisition Date:</strong> {{ entity.acquisition_date }}</div>
                        </template>

                        <template v-if="entity.entityType === 'M'">
                        <div><strong>Mission ID:</strong> {{ entity.mission_id }}</div>
                        <div><strong>Start Date:</strong> {{ entity.start_date }}</div>
                        <div><strong>End Date:</strong> {{ entity.end_date }}</div>
                        <div>{{ entity.description || "No description available." }}</div>
                        </template>

                        <template v-if="entity.entityType === 'O'">
                        <div><strong>Origin ID:</strong> {{ entity.origin_id }}</div>
                        <div><strong>Discovery Date:</strong> {{ entity.discovery_date }}</div>
                        {{entity.description || "No description available."}}
                        </template>
                        
                        <template v-if="entity.entityType === 'D'">
                        <div><strong>Department ID:</strong> {{entity.department_id}}</div>
                        <div><strong>Director:</strong> {{ `${entity.director.first_name} ${entity.director.last_name}`}}</div>
                        {{entity.description || "No description available."}}
                        </template>
                        
                       
                        <!-- Directory Result Card Text -->
                        <template v-if="entity.entityType === 'DDir'">
                          {{entity.description || "No description available."}}
                        </template>

                        <template v-if="entity.entityType === 'SDir'">
                        <div><strong>Specimen ID:</strong> {{ entity.specimenId }}</div>
                        <div><strong>Threat Level:</strong> {{ entity.threatLevel }}</div>
                        <div><strong>Acquisition Date:</strong> {{ entity.acquisitionDate }}</div>
                        </template>

                        <template v-if="entity.entityType === 'ODir'">
                        <div><strong>Origin ID:</strong> {{ entity.originId }}</div>
                        <div><strong>Discovery Date:</strong> {{ entity.discoveryDate }}</div>
                        {{entity.description || "No description available."}}
                        </template>
                        
                    </p>
                </div>
              </a>
</template>

<script>
  export default {
    props: {
      entity: {
        type: Object,
        required: true
      }
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