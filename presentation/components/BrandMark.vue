<script setup>
import { computed } from 'vue'

// An approved CUBRID Lab mark, shown whole and unmodified. The SVG files in
// public/brand/ are byte-identical copies of the pinned brand revision recorded
// in public/brand/README.md (brand decision 6); scale it, never restyle it.
const props = defineProps({
  name: { type: String, required: true },
  alt: { type: String, required: true },
  height: { type: Number, default: 48 },
})
const marks = import.meta.glob('../public/brand/*.svg', { eager: true, query: '?url', import: 'default' })
const source = computed(() => marks[`../public/brand/${props.name}.svg`])
</script>

<template>
  <img v-if="source" class="brand-mark" :src="source" :alt="props.alt" :style="{ height: `${props.height}px` }">
</template>

<style scoped>
.brand-mark { display: block; width: auto; max-width: 100%; }
</style>
