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
    <slot></slot>
  </div>
</template>

<script>
export default {
  props: {
    title: {
      type: String,
      default: 'TABLE',
    },
  },
  data() {
    return {
      isExpanded: false, // State to track if content is expanded or collapsed
    };
  }
};
</script>
