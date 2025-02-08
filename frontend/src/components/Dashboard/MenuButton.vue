<template>
  <li 
  class="h-1/12 flex pl-5 items-center hover:bg-gray-700 text-button hover:text-text-hover hover:cursor-pointer"
  :class="selected ? 'bg-gray-700 text-text-hover' : ''"
  >
    <strong>{{ name }}</strong>
  </li>
</template>

<script>
export default {
  props: {
    name: {
      type: String,
      default: "menu-button"
    },
    selected: {
      type: Boolean,
      default: false,
    }
  },
}
</script>