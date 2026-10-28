<script setup>
// Page number for the contest deck, drawn inside every slide so web, PDF and
// PPTX exports all show it. Shown from slide 2 on, and only in decks whose entry
// sets `pageNumbers: true`; the Builder Season 4 decks number their own pages.
import { computed } from 'vue'
import { useNav, useSlideContext } from '@slidev/client'

const { total } = useNav()
const { $page, $slidev } = useSlideContext()
// Only decks whose entry sets `pageNumbers: true` (the contest deck).
const shown = computed(() => $slidev.configs.pageNumbers === true && $page.value > 1)
</script>

<template>
  <div v-if="shown" class="contest-page-no">{{ $page }} <span>/ {{ total }}</span></div>
</template>

<style scoped>
.contest-page-no { position: absolute; right: 56px; bottom: 22px; font-size: 0.72rem; font-weight: 700; color: var(--blue); font-variant-numeric: tabular-nums; letter-spacing: 0; }
.contest-page-no span { font-weight: 400; color: var(--muted); }
</style>
