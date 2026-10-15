<script setup>
import { computed } from 'vue'

// One series over time as columns; the latest point is highlighted.
// Single series → no legend box; the slide text names it.
const props = defineProps({
  points: { type: Array, required: true },   // [{ x, y }]
  unit: { type: String, default: '' },
  width: { type: Number, default: 360 },
  height: { type: Number, default: 200 },
  col: { type: Number, default: 24 },
})

const axisH = 24   // year labels under the baseline
const valH = 22    // headroom for the value on the cap
const plotH = computed(() => props.height - axisH - valH)
const top = computed(() => Math.max(...props.points.map(p => p.y)))
const step = computed(() => props.width / props.points.length)
const h = v => (v / top.value) * plotH.value
const last = computed(() => props.points.length - 1)

// 4px rounded cap, square at the baseline
function colPath(w, hh) {
  const r = Math.min(4, w / 2, hh / 2)
  return `M0,${hh} V${r} Q0,0 ${r},0 H${w - r} Q${w},0 ${w},${r} V${hh} Z`
}
</script>

<template>
  <svg :viewBox="`0 0 ${width} ${height}`" :width="width" :height="height" class="trend" role="img">
    <g v-for="(p, i) in points" :key="p.x" :transform="`translate(${i * step + (step - col) / 2} 0)`">
      <path :d="colPath(col, h(p.y))" :transform="`translate(0 ${valH + plotH - h(p.y)})`" :class="i === last ? 'hl' : 'ctx'" />
      <text :x="col / 2" :y="valH + plotH - h(p.y) - 7" text-anchor="middle" class="val" :class="{ on: i === last }">{{ p.y }}{{ unit }}</text>
      <text :x="col / 2" :y="height - 6" text-anchor="middle" class="x" :class="{ on: i === last }">{{ p.x }}</text>
    </g>
    <line x1="0" :x2="width" :y1="valH + plotH" :y2="valH + plotH" class="base" />
  </svg>
</template>

<style scoped>
.trend { display: block; max-width: 100%; height: auto; overflow: visible; font-family: var(--sans); }
.hl { fill: #1f4e8c; }
.ctx { fill: #7f8da3; }
.val { font-size: 13px; fill: var(--muted); font-variant-numeric: tabular-nums; }
.val.on { fill: var(--ink); font-weight: 800; font-size: 15px; }
.x { font-size: 13px; fill: var(--muted); }
.x.on { fill: var(--ink); font-weight: 700; }
.base { stroke: var(--line); stroke-width: 1; }
</style>
