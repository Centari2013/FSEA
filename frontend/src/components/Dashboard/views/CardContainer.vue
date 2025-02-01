<template>
  <div id="CardsContainer" ref="CardsContainer" class="flex flex-col items-center pb-40 pt-5 space-y-4 h-full overflow-auto">
    <slot 
      @setHidePagination="$emit('setHidePagination', $event)"
      @setDisableNext="$emit('setDisableNext', $event)"
      @setDisablePrev="$emit('setDisablePrev', $event)"
      @newTotalPages="$emit('newTotalPages', $event)"
      @pageChanged="$emit('pageChanged', $event)"
      @scrollToTop="scrollToTop()"
    ></slot>
  </div>
</template>

<script>
export default {
  emits: [
    "setHidePagination",
    "setDisableNext",
    "setDisablePrev",
    "newTotalPages",
    "pageChanged",
  ],
  methods: {
    scrollToTop(){
      this.$refs.CardsContainer.scrollTo({ top: 0, behavior: "smooth" });
    }
  }
};
</script>