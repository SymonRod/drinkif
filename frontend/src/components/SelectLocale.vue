<template>
      <select v-model="$i18n.locale" class="select ml-2" id="select-language">
        <option v-for="(lang, i) in langs" :key="`lang-${i.value}`" :value="lang.value">
          {{ lang.description }}
        </option>
      </select>
    
</template>

<script>
export default {
  name: "SelectLocale",
  data() {
    return { langs: [ {value:"en-US", description:"English 🇺🇸"}, {value:"it-IT", description:"Italiano 🇮🇹"}] };
  },
};
</script>