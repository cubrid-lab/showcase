<script setup>
import { computed, ref } from 'vue'

// Team photo slot. Drop the file into public/photos/ under the given name.
// Until it exists (or if it fails to load) nothing is rendered, so the
// surrounding .frame is empty and style.css hides it; no placeholder shows.
const props = defineProps({
  src: { type: String, required: true },
  label: { type: String, default: '' },
})
const photos = import.meta.glob('../public/photos/*.{jpg,jpeg,png,webp,avif}', { eager: true, query: '?url', import: 'default' })
const source = computed(() => photos[`../public${props.src}`])
const ok = ref(true)
</script>

<template>
  <figure v-if="ok && source" class="photo">
    <img :src="source" :alt="props.label" @error="ok = false">
  </figure>
</template>

<style scoped>
.photo { margin: 0; width: 100%; height: 100%; border-radius: 14px; overflow: hidden; background: var(--blue-soft); }
.photo img { width: 100%; height: 100%; object-fit: cover; display: block; }
</style>
