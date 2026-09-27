<script setup>
// Storyline tracker shown top-right on every slide: where this slide sits in the talk.
const props = defineProps({
  n: { type: Number, required: true }
})
const acts = ['만남', '발견', '만들기', '방법', '증명', '신뢰', '다음']
</script>

<template>
  <ol class="acts" aria-label="발표 흐름">
    <li v-for="(a, i) in acts" :key="a" :class="{ on: i + 1 === props.n, past: i + 1 < props.n }">{{ a }}</li>
  </ol>
</template>

<style scoped>
.acts {
  position: absolute; top: 34px; right: 56px;
  display: flex; gap: 10px; list-style: none; margin: 0; padding: 0;
  font-size: 0.62rem; font-weight: 600; letter-spacing: 0.02em;
}
.acts li { margin: 0; padding: 0 0 3px; color: var(--line); border-bottom: 2px solid transparent; }
.acts li.past { color: var(--muted); }
.acts li.on { color: var(--blue); border-bottom-color: var(--blue); }
:global(.navy) .acts li { color: #2a3d58; }
:global(.navy) .acts li.past { color: var(--on-navy-muted); }
:global(.navy) .acts li.on { color: #7fb0ec; border-bottom-color: #7fb0ec; }
</style>
