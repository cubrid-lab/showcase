<script setup>
import { computed } from 'vue'
import snapshot from '../snapshots/2026-09-12.json'

const props = defineProps({
  category: { type: String, required: true }
})

const data = computed(() => {
  if (props.category === 'adoption') {
    const m = snapshot.metrics
    return [
      { label: 'GitHub stars (4 repos)', value: m.stars.total },
      { label: 'Unique clones (14d, per-repo sum)', value: `~${m.uniqueClones14d.total}`, note: m.uniqueClones14d.note },
      { label: 'Merged PRs', value: m.mergedPRs.total },
      { label: 'PyPI releases', value: m.pypiReleases.total },
      { label: 'Tests (CI-enforced)', value: m.tests.total.toLocaleString() },
    ]
  }
  if (props.category === 'performance') {
    const p = snapshot.performance
    return [
      { label: 'Native ping (CHECK_CAS)', value: p.nativePing.improvement },
      { label: 'SA pool_pre_ping', value: p.poolPrePing.improvement },
      { label: 'Bulk insert (1000 rows)', value: p.bulkInsert1000.improvement },
      { label: 'Query select-all', value: p.querySelectAll.improvement },
    ]
  }
  return []
})

const collectionInfo = computed(() => {
  return `Snapshot: ${snapshot.snapshotDate} | Source: GitHub/PyPI APIs`
})
</script>

<template>
  <div class="snapshot-metrics">
    <table>
      <thead>
        <tr><th>Metric</th><th>Value</th></tr>
      </thead>
      <tbody>
        <tr v-for="item in data" :key="item.label">
          <td>{{ item.label }}</td>
          <td class="value">{{ item.value }}</td>
        </tr>
      </tbody>
    </table>
    <div class="collection-info">{{ collectionInfo }}</div>
  </div>
</template>

<style scoped>
.snapshot-metrics table {
  width: 100%;
  border-collapse: collapse;
  font-size: 0.9em;
}
.snapshot-metrics th, .snapshot-metrics td {
  padding: 0.4em 0.8em;
  text-align: left;
  border-bottom: 1px solid #e2e8f0;
}
.snapshot-metrics .value {
  font-weight: bold;
  font-size: 1.1em;
  text-align: right;
}
.collection-info {
  font-size: 0.7em;
  color: #94a3b8;
  margin-top: 0.5em;
  text-align: right;
}
</style>
