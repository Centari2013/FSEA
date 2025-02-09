import { defineStore } from 'pinia'


export const usePaginationStore = defineStore('dashboardPagination', {
  state: () => ({ 
    hidePagination: true,
    disablePrev: true,
    disableNext: true,
    currentPage: 1,
    totalPages: 0,
    resultsPerPage: 25,
  }),
  getters: {
    
  },
  actions: {
    setHidePagination(bool){
      this.hidePagination = bool;
    },
    setDisableNext(bool){
      this.disableNext = bool;
    },
    setDisablePrev(bool){
      this.disablePrev = bool;
    },
    setTotalPages(count){
      this.totalPages = count;
    },
    setCurrentPage(int){
      this.currentPage = int;
    },
    setResultsPerPage(int){
      this.resultsPerPage = int;
    }

  },
})