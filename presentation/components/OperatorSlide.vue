<script setup>
defineProps({
  section: { type: String, required: true },
  index: { type: String, required: true },
  total: { type: String, default: '17' },
  source: { type: String, default: '' },
  sourceUrl: { type: String, default: '' },
})
</script>

<template>
  <article class="op-frame">
    <header class="op-header">
      <span class="op-project">CUBRID Kubernetes Operator</span>
      <span>{{ section }}</span>
    </header>
    <div class="op-body"><slot /></div>
    <footer class="op-footer">
      <a v-if="source && sourceUrl" :href="sourceUrl" target="_blank" rel="noopener noreferrer">{{ source }}</a>
      <span v-else>{{ source }}</span>
      <span class="op-page">{{ index }} <span>/ {{ total }}</span></span>
    </footer>
  </article>
</template>
