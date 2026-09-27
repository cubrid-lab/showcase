<script setup>
import references from '../references.json'

// claim: one reference id, or several comma-separated (one footer per slide —
// the footer is absolutely positioned, so separate footers would overlap)
const props = defineProps({
  claim: { type: String, required: true }
})

const entries = props.claim.split(',').map(s => s.trim()).flatMap(id => {
  const entry = references.references[id]
  if (!entry) {
    console.warn(`EvidenceFooter: unknown claim id "${id}"`)
    return []
  }
  return [{ id, ...entry }]
})
</script>

<template>
  <div v-if="entries.length" class="evidence-footer">
    <template v-for="entry in entries" :key="entry.id">
      <span class="badge" :class="{ verified: entry.verified, unverified: !entry.verified }" :title="entry.claim">
        {{ entry.verified ? 'Verified' : 'Needs verification' }}
      </span>
      <a v-if="entry.source?.startsWith('http')" :href="entry.source" target="_blank" class="source-link" :title="entry.claim">
        Source
      </a>
      <span v-else class="source-text">{{ entry.source }}</span>
    </template>
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
