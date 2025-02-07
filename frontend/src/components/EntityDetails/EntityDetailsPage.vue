<template>
  <div class="h-full overflow-auto flex flex-col items-center">
    <component :is="component" :id="params.id"
       class="w-11/12 mt-10"
    />
  </div>
       
</template>

<script>
import { markRaw } from 'vue';
import DepartmentDetails from './views/DepartmentDetails.vue';
import EmployeeDetails from './views/EmployeeDetails.vue';
import MissionDetails from './views/MissionDetails.vue';
import OriginDetails from './views/OriginDetails.vue';
import SpecimenDetails from './views/MissionDetails.vue';

export default {
  data(){
    return {
      params: JSON.parse(localStorage.getItem('params')),
      component: null,
    }
  },
  mounted(){
    this.getEntityDetails();
  },
  methods: {
    getEntityDetails(){
      switch(this.params.type){
      case 'D':
        this.component = markRaw(DepartmentDetails);
        break;
      case 'E':
        this.component = markRaw(EmployeeDetails);
        break;
      case 'S':
        this.component = markRaw(SpecimenDetails);
        break;
      case 'O':
        this.component = markRaw(OriginDetails);
        break;
      case 'M':
        this.component = markRaw(MissionDetails);
        break;
      default:
        break;
    }

    this.loading = false;
    }
  }
}

</script>