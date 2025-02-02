<template>
  <div id="CardsContainer" ref="CardsContainer" class="flex flex-col items-center pb-40 pt-5 space-y-4 h-full overflow-auto">
    <slot 
      @scrollToTop="scrollToTop()"
    ></slot>
  </div>
</template>

<script>
export default {
  methods: {
    scrollToTop(){
      this.$refs.CardsContainer.scrollTo({ top: 0, behavior: "smooth" });
    }
  }
};
</script>