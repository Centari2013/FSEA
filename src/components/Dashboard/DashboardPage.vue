<template>
  <div class="md:grid grid-cols-6 h-screen w-full overflow-clip">
    <!-- Sidebar -->
    <div class="hidden h-full pt-4 col-span-1 md:flex md:flex-col shadow-[2px_0px_5px_0px_rgba(0,0,0)]">
      <div class="h-1/8 mx-auto">
        <img src="../../assets/fsea_logo.png" alt="FSEA Logo" class="w-auto"/>
      </div>
      
      <ul id="menu" class="h-full flex flex-col items-center space-y-4">
        <MenuButton 
          v-for="item in menuItems" 
          :key="item" 
          :name="item" 
          :selected="currentMenuItem === item"
          @click="handleMenuClick(item)"
          class="justify-around w-full"
        />
      </ul>
    </div>
    <!-- Main Content -->
    <div class="col-span-5">
      <div class="shadow-[3px_1px_5px_0px_rgba(0,0,0)] p-4 sticky top-0 space-y-4">

        
        <div class="flex space-x-2">
          <!-- Hamburger Menu Button (Only Visible on Small Screens) -->
          <button @click="hamMenuisOpen = !hamMenuisOpen" class="md:hidden p-2 focus:outline-none">
            <svg v-if="!hamMenuisOpen" class="w-6 h-6" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
              <path stroke-linecap="round" stroke-linejoin="round" d="M4 6h16M4 12h16M4 18h16"></path>
            </svg>
            <svg v-else class="w-6 h-6" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
              <path stroke-linecap="round" stroke-linejoin="round" d="M6 18L18 6M6 6l12 12"></path>
            </svg>
          </button>

          <!-- Search Bar with Button -->
          <form id="search-form" class="space-x-2 w-full h-full">
            <input @keyup.enter="performSearch" v-model="query" placeholder="General Search..." type="text" id="search-bar" required class="form-control md:h-1/2 md:w-3/7 rounded-sm p-2 border-1">
            <button @click.prevent="performSearch" id="search-button">Search</button>
          </form>
        </div>
        
        <!-- Pagination -->
        <nav>
          <ul class="flex justify-center" :hidden="store.hidePagination">
            <li class="prev" :class="store.disablePrev ? 'disabled' : ''" @click.prevent="!disablePrev ? changePage(store.currentPage - 1) : null" id="prevPage">Previous</li>
              <div ref="paginationContainer" class=" flex justify-center">
                <!-- Dynamically insert page numbers here -->
              </div>
            <li class="next" :class="store.disableNext ? 'disabled' : ''" @click.prevent="!disableNext ? changePage(store.currentPage + 1) : null" id="nextPage">Next</li>
          </ul>
        </nav>

        <!--  Mobile Navigation Menu -->
        <nav :class="hamMenuisOpen ? 'block' : 'hidden'" class="absolute top-16 left-0 w-full bg-gray-900 shadow-md md:hidden md:bg-transparent md:shadow-none">
          <ul class="flex flex-col items-center md:flex-row md:space-x-6 space-y-4">
            <div class="h-1/8 mx-auto">
        <img src="../../assets/fsea_logo.png" alt="FSEA Logo" class="w-auto"/>
      </div>
            <MenuButton 
          v-for="item in menuItems" 
          :key="item" 
          :name="item" 
          :selected="currentMenuItem === item"
          @click="handleMenuClick(item)"
          class="h-16 w-full justify-around"
        />
          </ul>
        </nav>

      </div>
      <div ref="mainContent" class="h-screen">
        <!-- Content will be loaded here -->
        <ContentContainer> 
          <SearchResultCards v-if="!currentMenuItem" ref="activeCards" :query="query"/>
          <EntityDirectoryCards v-if="currentMenuItem" ref="activeCards" :currentDirectory="currentMenuItem"/>
        </ContentContainer>
      </div>
    </div>
  </div>
</template>

<script>
import MenuButton from './MenuButton.vue';
import SearchResultCards from "./views/Results/SearchResultCards.vue";
import ContentContainer from "./views/ContentContainer.vue";
import setupPagination from '../../scripts/pagination';
import EntityDirectoryCards from './views/Results/EntityDirectoryCards.vue';
import { usePaginationStore } from '../stores/paginationStore';

export default {
  components: { MenuButton, SearchResultCards, ContentContainer, EntityDirectoryCards },
  data() {
    return {
      // search vars
      query: '',
      store: usePaginationStore(),
      // directory selection vars
      menuItems: ["Home", "Department Directory", "Origin Directory", "Specimen Directory", "Document Directory"],
      currentMenuItem: "Home",
      hamMenuisOpen: false,
    }
  },
  computed: {
    totalPages() {
      return this.store.totalPages;
    },
    currentPage() {
      return this.store.currentPage;
    }
  },
  mounted() {
    window.addEventListener('resize', this.setupPagination);
  },
  watch: {
    totalPages(_new){
      this.setupPagination();
    },
    currentPage(_new){
      this.setupPagination()
    }
  },
  methods: {
    performSearch() {
      this.currentMenuItem = null; // show search results
      try {
        this.$refs.activeCards.performSearch(); 
      } catch (e) {
        // EntityDirectory does not have the above func
      }
    },
    setupPagination(){
      setupPagination(this);
    },
    changePage(newPage){
      this.store.setCurrentPage(newPage);
    },
    handleMenuClick(item){
      this.hamMenuisOpen = false;
      this.currentMenuItem = item;
      this.store.setTotalPages(0) // reset pagination
    }
  }
}
</script>

<style>
@reference "tailwindcss";

.page-item, .prev, .next {
  @apply border-1 rounded-none  h-10 flex justify-center items-center hover:bg-gray-800 hover:cursor-pointer;
}

.page-item {
  @apply border-l-0 w-8;
}

.prev, .next {
  @apply p-3;
}

.prev {
  @apply rounded-l-md;
}

.next {
  @apply rounded-r-md border-l-0;
}

.disabled {
  @apply bg-gray-900/50 pointer-events-none select-none;
}
</style>
