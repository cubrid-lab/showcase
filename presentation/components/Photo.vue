<script setup>
import { ref } from 'vue'

// Team photo slot. Drop the file into public/photos/ under the given name;
// until it exists the slide shows a quiet frame instead of a broken image.
const props = defineProps({
  src: { type: String, required: true },
  label: { type: String, default: '' },
})
const ok = ref(true)
</script>

<template>
  <figure class="photo">
    <img v-if="ok" :src="props.src" :alt="props.label" @error="ok = false">
    <div v-else class="empty">
      <span>{{ props.label }}</span>
      <code>public{{ props.src }}</code>
    </div>
  </figure>
</template>

<style scoped>
.photo { margin: 0; width: 100%; height: 100%; border-radius: 14px; overflow: hidden; background: var(--blue-soft); }
.photo img { width: 100%; height: 100%; object-fit: cover; display: block; }
.empty {
  width: 100%; height: 100%; display: grid; place-content: center; gap: 6px; text-align: center;
  border: 2px dashed var(--line); border-radius: 14px; color: var(--muted);
}
.empty span { font-size: 0.9rem; font-weight: 600; }
.empty code { font-size: 0.62rem; opacity: 0.7; }
</style>
