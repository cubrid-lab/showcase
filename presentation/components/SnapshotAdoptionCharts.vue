<script setup>
import BarChart from './BarChart.vue'
import { snapshot } from '../selectedSnapshot.js'

const charts = [
  { key: 'stars', label: 'GitHub star' },
  { key: 'mergedPRs', label: 'merged PR' },
  { key: snapshot.metrics.publishedReleases ? 'publishedReleases' : 'pypiReleases', label: snapshot.metrics.publishedReleases ? 'GitHub 릴리스' : 'PyPI 릴리스' },
].map(({ key, label }) => {
  const metric = snapshot.metrics[key]
  const rows = Object.entries(metric.perRepo)
    .filter(([, value]) => value !== null)
    .sort((a, b) => b[1] - a[1])
    .map(([repo, value], i) => ({ label: repo.replace('-python', ''), value, hl: i === 0 }))
  return { key, label, total: metric.total, rows }
})
</script>

<template>
  <p class="kicker">저장소 활동 지표 · 네 저장소 · GitHub API, {{ snapshot.snapshotDate }} 기준</p>
  <div class="adoption-charts">
    <div v-for="chart in charts" :key="chart.key" class="stack">
      <p class="chart-cap">{{ chart.label }} — 총 {{ chart.total.toLocaleString() }}</p>
      <BarChart :width="370" :label-width="150" :bar="14" :gap="8" :rows="chart.rows" />
    </div>
    <div class="stack scope-note">
      <p class="chart-cap">측정 범위</p>
      <p>star · 머지된 PR · 릴리스는 개발 활동을 보여 주는 숫자이며, 사용자 수가 아닙니다.</p>
      <p>fork는 스냅숏에 기록되지 않아 제외했고, 클론 수는 CI와 사용자를 구분할 수 없어 쓰지 않습니다.</p>
    </div>
  </div>
</template>

<style scoped>
.adoption-charts { display: grid; grid-template-columns: 1fr 1fr; gap: 22px 40px; }
.chart-cap { font-size: 0.85rem; font-weight: 700; }
.scope-note p { font-size: 0.85rem; }
</style>
