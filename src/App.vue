<template>
      <RouterView/>
       <!-- <button @click="generatePdf">Generate</button> -->
       <!-- <iframe :src="pdf" class="h-full w-full"></iframe> -->
</template>
<script>
import generatePdf from './scripts/pdf_gen/pdf_gen';

export default {
      data(){
            return{
                  pdf: null
            }
      },
      methods:{
            async generatePdf(){
                  this.pdf = await generatePdf();
            }
      }
}
</script>
