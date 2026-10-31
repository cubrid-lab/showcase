<script setup>
import { useNav, useSlideContext } from '@slidev/client'

defineProps({
  section: { type: String, required: true },
  source: { type: String, default: '' },
  sourceUrl: { type: String, default: '' },
})
const { total } = useNav()
const { $page } = useSlideContext()
</script>

<template>
  <article class="op-frame">
    <header class="op-header">
      <span class="op-section">{{ section }}</span>
      <span class="op-project">CUBRID K8s Operator</span>
    </header>
    <div class="op-body"><slot /></div>
    <footer class="op-footer">
      <span class="op-page">{{ $page }} <span>/ {{ total }}</span></span>
    </footer>
  </article>
</template>
