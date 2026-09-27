<script setup>
import references from '../references.json'

const props = defineProps({
  claim: { type: String, required: true }
})

const ref = references.references[props.claim]
</script>

<template>
  <div v-if="ref" class="evidence-footer">
    <span class="badge" :class="{ verified: ref.verified, unverified: !ref.verified }">
      {{ ref.verified ? 'Verified' : 'Needs verification' }}
    </span>
    <a v-if="ref.source?.startsWith('http')" :href="ref.source" target="_blank" class="source-link">
      Source
    </a>
    <span v-else class="source-text">{{ ref.source }}</span>
  </div>
</template>

<style scoped>
.evidence-footer {
  position: absolute;
  bottom: 1em;
  right: 1em;
  font-size: 0.65em;
  display: flex;
  gap: 0.5em;
  align-items: center;
}
.badge {
  padding: 0.15em 0.5em;
  border-radius: 4px;
  font-size: 0.85em;
}
.verified { background: #dcfce7; color: #166534; }
.unverified { background: #fef9c3; color: #854d0e; }
.source-link { color: #3b82f6; text-decoration: underline; }
.source-text { color: #94a3b8; }
</style>
