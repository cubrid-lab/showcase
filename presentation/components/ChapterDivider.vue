<script setup>
defineProps({
  number: { type: String, required: true },
  title: { type: String, required: true },
  subtitle: { type: String, default: '' },
})
</script>

<template>
  <section class="chapter-divider" aria-label="Chapter transition">
    <span class="chapter-divider-no">{{ number }}</span>
    <h1 class="chapter-divider-title">{{ title }}</h1>
    <p v-if="subtitle" class="chapter-divider-subtitle">{{ subtitle }}</p>
    <span class="chapter-divider-rule" aria-hidden="true"></span>
  </section>
</template>

<style scoped>
.chapter-divider {
  display: flex;
  flex-direction: column;
  align-items: flex-start;
  justify-content: center;
  width: 100%;
  min-height: 290px;
  gap: 15px;
}
.chapter-divider-no {
  color: var(--blue, #1f4e8c);
  font-size: 1.15rem;
  font-weight: 850;
  letter-spacing: .08em;
  line-height: 1.2;
  font-variant-numeric: tabular-nums;
}
.chapter-divider-title {
  color: var(--ink, #0f1b2d);
  font-size: clamp(2.8rem, 5vw, 4rem) !important;
  font-weight: 780;
  letter-spacing: -.045em;
  line-height: 1.15;
  word-break: keep-all;
}
.chapter-divider-subtitle {
  color: var(--muted, #5b6b82);
  font-size: 1.16rem;
  line-height: 1.45;
  text-wrap: balance;
  max-width: 48ch;
}
.chapter-divider-rule {
  width: 72px;
  height: 4px;
  border-radius: 2px;
  background: var(--blue, #1f4e8c);
  margin-top: 4px;
}
</style>
