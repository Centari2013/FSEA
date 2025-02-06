<template>
  <ContentContainer class="h-full">
    <component :is="component" :id="params.id"
       class="w-11/12 mt-10"
    />
  </ContentContainer>
       
</template>

<script>
import { markRaw } from 'vue';
import DepartmentDetails from './views/DepartmentDetails.vue';
import ContentContainer from '../Dashboard/views/ContentContainer.vue';


export default {
  components: { ContentContainer },
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
        break;
      case 'S':
        break;
      case 'O':
        break;
      case 'M':
        break;
      default:
        break;
    }

    this.loading = false;
    }
  }
}

</script>