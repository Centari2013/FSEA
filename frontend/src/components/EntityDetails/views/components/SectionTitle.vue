<template>
  <h3 class="text-2xl">{{ title }}</h3>
</template>

<script>
export default {
  props: {
    title: {
      type: String,
    }
  }
}
</script>