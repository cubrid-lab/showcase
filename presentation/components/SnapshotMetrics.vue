<script setup>
import { computed } from 'vue'
import snapshot from '../snapshots/2026-09-12.json'

const props = defineProps({
  category: { type: String, required: true }
})

// Tiles: num = headline figure, k = what it is, v = how to read it.
// hl marks the one tile the slide is about.
const tiles = computed(() => {
  if (props.category === 'adoption') {
    const m = snapshot.metrics
    return [
      { num: m.mergedPRs.total, k: 'Merged PRs', v: 'AI 작성 · 사람 리뷰 · CI 게이트 후 병합', hl: true },
      { num: m.tests.total.toLocaleString(), k: 'Tests', v: 'CI 강제 · 3개 패키지 합계' },
      { num: 20, k: 'CI 조합', v: 'Python 5 × CUBRID 4 · 라이브 DB' },
      { num: m.pypiReleases.total, k: 'PyPI releases', v: `pycubrid ${m.pypiReleases.perRepo.pycubrid} · sqlalchemy-cubrid ${m.pypiReleases.perRepo['sqlalchemy-cubrid']}` },
      { num: m.stars.total, k: 'GitHub stars', v: '4개 저장소 합계' },
    ]
  }
  if (props.category === 'performance') {
    const p = snapshot.performance
    return [
      { num: p.poolPrePing.improvement, k: 'SQLAlchemy pool_pre_ping', v: '처리량 · ping 최적화', hl: true },
      { num: p.nativePing.improvement, k: 'Native ping (CHECK_CAS)', v: '처리량 · SELECT 1 대비' },
      { num: p.bulkInsert1000.improvement, k: 'Bulk insert 1,000행', v: `${p.bulkInsert1000.before} → ${p.bulkInsert1000.after}` },
      { num: p.querySelectAll.improvement, k: 'Query select-all', v: `${p.querySelectAll.before} → ${p.querySelectAll.after}` },
    ]
  }
  return []
})
</script>

<template>
  <div class="snap">
    <div class="stats" :style="{ gridTemplateColumns: `repeat(${tiles.length}, 1fr)` }">
      <div v-for="t in tiles" :key="t.k" class="stat" :class="{ hl: t.hl }">
        <span class="num">{{ t.num }}</span>
        <span class="k">{{ t.k }}</span>
        <span class="v">{{ t.v }}</span>
      </div>
    </div>
    <p class="src">Snapshot {{ snapshot.snapshotDate }} · GitHub / PyPI API · 발표 당일 재측정</p>
  </div>
</template>

<style scoped>
.snap { display: grid; gap: 10px; }
.src { text-align: right; }
</style>
