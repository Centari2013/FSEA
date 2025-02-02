<template>
  <div class="grid grid-cols-6 h-screen w-full overflow-hidden">
    <!-- Sidebar -->
    <div class="h-full pt-4 col-span-1 flex flex-col shadow-[2px_0px_5px_0px_rgba(0,0,0)]">
      <div class="h-1/8 mx-auto">
        <img src="../../assets/fsea_logo.png" alt="FSEA Logo" class="w-auto">
      </div>
      
      <ul id="menu" class="h-full flex flex-col space-y-4">
        <MenuButton 
          v-for="item in menuItems" 
          :key="item" 
          :name="item" 
          :selected="currentMenuItem === item"
          @click="currentMenuItem = item"
        />
        
      </ul>
    </div>
    <!-- Main Content -->
    <div class="col-span-5">
      <div class="shadow-[3px_1px_5px_0px_rgba(0,0,0)] p-4 sticky top-0 space-y-4">
        <!-- Search Bar with Button -->
        <div class="">
          <form id="search-form" class="space-x-2">
            <input @keyup.enter="performSearch" v-model="query" placeholder="General Search..." type="text" id="search-bar" required class="form-control h-1/2 w-3/7 rounded-sm p-2 border-1">
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
      </div>
      <div ref="mainContent" class="h-screen">
        <!-- Content will be loaded here -->
        <CardContainer> 
          <SearchResultCards v-if="!currentMenuItem" ref="activeCards" :query="query"/>
          <EntityDirectory v-if="currentMenuItem" ref="activeCards" :currentDirectory="currentMenuItem"/>
        </CardContainer>
      </div>
    </div>
    
  </div>

  
</template>

<script>
import MenuButton from './MenuButton.vue';
import SearchResultCards from "./views/Results/SearchResultCards.vue";
import CardContainer from "./views/CardContainer.vue";
import setupPagination from '../../scripts/pagination';
import EntityDirectory from './views/Results/EntityDirectory.vue';
import { usePaginationStore } from '../stores/paginationStore';

export default {
  components: { MenuButton, SearchResultCards, CardContainer, EntityDirectory },
  data() {
    return {
      // search vars
      query: '',
      store: usePaginationStore(),
      // directory selection vars
      menuItems: ["Home", "Department Directory", "Origin Directory", "Specimen Directory", "Document Directory"],
      currentMenuItem: "Home",
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
  @apply rounded-r-md;
}

.disabled {
  @apply bg-gray-900/50 pointer-events-none select-none;
}

</style>