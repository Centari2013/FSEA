<template>
  <div class="flex space-x-4 items-center mb-1">
      <h3 class="text-2xl">{{title}}</h3>
      <button>See More</button>
    </div>
    
    <hr class="mb-7">
    <table class="table-fixed w-full">
      <thead>
        <tr class="h-10 bg-zinc-900">
          <th class="w-1/6 pl-2">{{headerTitles[0]}}</th>
          <th v-for="n in headerTitles.length">{{headerTitles[n]}}</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="obj in dict" class="h-10 even:bg-zinc-800 border border-collapse border-l-0 border-r-0">
          <td class="pl-2">{{obj[keys[0]]}}</td>
            <template v-for="n in keys.length">
              <td>{{obj[keys[n]]}}</td>
            </template>
        </tr>
      </tbody>
    </table>
</template>
<script>
export default {
  props: {
    title: {
      type: String,
      default: 'TABLE',
    },
    headerTitles: {
      type: Array,
      default: [],
    },
    keys: {
      type: Array,
      default: [],
    },
    dict: {
      type: Object,
      default: {},
    }
  }
}
</script>