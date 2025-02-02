<template>

</template>

<script>
import { useRouter } from 'vue-router';

export default {
  data(){
    return {
      router: useRouter(),
      params: JSON.parse(localStorage.getItem('params')),
    }
  },
  mounted(){
    console.log(JSON.parse(localStorage.getItem('params')))
  }
}

</script>