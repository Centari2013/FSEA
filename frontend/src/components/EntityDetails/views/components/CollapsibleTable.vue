<template>
  <div class="flex space-x-4 items-center mb-1">
    <h3 class="text-2xl">{{ title }}</h3>
    <div @click="isExpanded = !isExpanded" class="px-3 py-1 text-blue-400 hover:underline cursor-pointer">
      {{ isExpanded ? "See Less" : "See More" }}
    </div>
  </div>

  <hr class="mb-7">

  <!-- Collapsible Content -->
  <div v-if="isExpanded">
    <Table 
   :headerTitles="headerTitles"
   :keys="keys"
   :dictArr="dictArr"
   />
  </div>
</template>

<script>
import Table from './Table.vue';

export default {
  components: {Table},
  props: {
    title: {
      type: String,
      default: 'TABLE',
    },
    headerTitles: {
      type: Array,
      default: () => [],
    },
    keys: {
      type: Array,
      default: () => [],
    },
    dictArr: {
      type: Array,
      default: () => [],
    }
  },
  data() {
    return {
      isExpanded: false, // State to track if content is expanded or collapsed
    };
  }
};
</script>
