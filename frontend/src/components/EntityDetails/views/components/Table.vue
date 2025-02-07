<template>  
    <table class="table-fixed w-full">
      <thead>
        <tr class="h-10 bg-zinc-900">
          <th class="w-auto pl-2">{{ headerTitles[0] }}</th>
          <th class="w-auto" v-for="(title, index) in headerTitles.slice(1)" :key="index">{{ title }}</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="(obj, index) in dictArr" :key="index" class="h-10 even:bg-zinc-800 border border-collapse border-l-0 border-r-0">
          <td class="pl-2">{{ obj[keys[0]] }}</td>
          <template v-for="(key, index) in keys.slice(1)" :key="index">
            <td>{{ obj[key] }}</td>
          </template>
        </tr>
      </tbody>
    </table>
</template>

<script>
export default {
  props: {
    headerTitles: {
      type: Array,
      default: () => [],
    },
    keys: {
      type: Array,
      default: () => [],
    },
    dictArr: {
      type: Array,
      default: () => [],
    }
  },
};
</script>
