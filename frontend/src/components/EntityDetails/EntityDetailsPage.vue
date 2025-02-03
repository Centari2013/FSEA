<template>r
    <ContentContainer>
      <!-- Entity details will be inserted here dynamically -->
      <!-- Department -->
       
      <LoadSpinner v-if="loading"/>
    </ContentContainer>
</template>

<script>
import { useRouter } from 'vue-router';
import DepartmentDetails from './views/DepartmentDetails.vue';
import ContentContainer from '../Dashboard/views/ContentContainer.vue';
import LoadSpinner from '../Dashboard/animations/LoadSpinner.vue';

export default {
  components: { LoadSpinner, ContentContainer, DepartmentDetails },
  data(){
    return {
      router: useRouter(),
      params: JSON.parse(localStorage.getItem('params')),
      entityDetails: null,
      loading: true,
    }
  },
  mounted(){
    switch(this.params.type){
      case 'D':
        this.entityDetails = await fetchDepartmentDetails(this.params.id);
        break;
      case 'E':
        this.entityDetails = await fetchEmployeeDetails(this.params.id);
        break;
      case 'S':
        this.entityDetails = await fetchSpecimenDetails(this.params.id);
        break;
      case 'O':
        this.entityDetails = await fetchOriginDetails(this.params.id);
        break;
      case 'M':
        this.entityDetails = await fetchMissionDetails(this.params.id);
        break;
      default:
        break;
    }

    this.loading = false;
  }
}

</script>