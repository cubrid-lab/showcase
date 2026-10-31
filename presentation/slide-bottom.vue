<script setup>
// Page number for the contest deck, drawn inside every slide so web, PDF and
// PPTX exports all show it. Shown from slide 2 on, and only in decks whose entry
// sets `pageNumbers: true`; the Builder Season 4 decks use their own auto-numbered frame.
import { computed } from 'vue'
import { useNav, useSlideContext } from '@slidev/client'

const { total } = useNav()
const { $page, $slidev } = useSlideContext()
// Only decks whose entry sets `pageNumbers: true` (the contest deck).
const shown = computed(() => $slidev.configs.pageNumbers === true && $page.value > 1)
</script>

<template>
  <div v-if="shown" class="contest-deck-id">CUBRID Python 생태계</div>
  <div v-if="shown" class="contest-page-no">{{ $page }} <span>/ {{ total }}</span></div>
</template>

<style scoped>
.contest-deck-id { position: absolute; right: 56px; top: 22px; font-size: 0.70rem; font-weight: 650; color: var(--muted, #5b6b82); letter-spacing: 0; }
.contest-page-no { position: absolute; right: 56px; bottom: 22px; font-size: 0.72rem; font-weight: 700; color: var(--blue, #1f4e8c); font-variant-numeric: tabular-nums; letter-spacing: 0; }
.contest-page-no span { font-weight: 400; color: var(--muted, #5b6b82); }
</style>
