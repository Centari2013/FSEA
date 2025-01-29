<template>
  <li class="h-1/12 flex pl-5 items-center hover:bg-gray-700 text-white hover:text-blue-500">
    {{ name }}
  </li>
</template>

<script>
export default {
  props: {
    name: {
      type: String,
      default: "menu-button"
    }
  }
}
</script>