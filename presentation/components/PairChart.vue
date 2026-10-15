<script setup>
import { computed } from 'vue'

// Before/after pairs on one shared axis (same unit for every row).
// Before = gray context, after = blue. Legend above; each bar labelled at its tip.
const props = defineProps({
  rows: { type: Array, required: true },   // [{ label, before, after, beforeText?, afterText? }]
  unit: { type: String, default: '' },
  beforeName: { type: String, default: '개선 전' },
  afterName: { type: String, default: '개선 후' },
  width: { type: Number, default: 520 },
  labelWidth: { type: Number, default: 130 },
  bar: { type: Number, default: 16 },
})

const pad = 70
const inner = 3        // 2px surface gap between the pair (+1 for antialiasing)
const group = 18       // space between rows
const legendH = 26
const plotW = computed(() => props.width - props.labelWidth - pad)
const top = computed(() => Math.max(...props.rows.flatMap(r => [r.before, r.after])))
const rowH = computed(() => props.bar * 2 + inner)
const height = computed(() => legendH + props.rows.length * (rowH.value + group) - group)
const len = v => (v / top.value) * plotW.value

function barPath(w, h) {
  const r = Math.min(4, w / 2, h / 2)
  return `M0,0 H${w - r} Q${w},0 ${w},${r} V${h - r} Q${w},${h} ${w - r},${h} H0 Z`
}
</script>

<template>
  <svg :viewBox="`0 0 ${width} ${height}`" :width="width" :height="height" class="pairs" role="img">
    <g class="legend">
      <rect :x="labelWidth" y="3" width="12" height="12" rx="2" class="ctx" />
      <text :x="labelWidth + 18" y="9" dominant-baseline="central">{{ beforeName }}</text>
      <rect :x="labelWidth + 110" y="3" width="12" height="12" rx="2" class="hl" />
      <text :x="labelWidth + 128" y="9" dominant-baseline="central">{{ afterName }}</text>
    </g>
    <g v-for="(r, i) in rows" :key="r.label" :transform="`translate(0 ${legendH + i * (rowH + group)})`">
      <text :x="labelWidth - 12" :y="rowH / 2" text-anchor="end" dominant-baseline="central" class="lab">{{ r.label }}</text>
      <path :d="barPath(len(r.before), bar)" :transform="`translate(${labelWidth} 0)`" class="ctx" />
      <text :x="labelWidth + len(r.before) + 8" :y="bar / 2" dominant-baseline="central" class="val">{{ r.beforeText ?? (r.before + unit) }}</text>
      <path :d="barPath(len(r.after), bar)" :transform="`translate(${labelWidth} ${bar + inner})`" class="hl" />
      <text :x="labelWidth + len(r.after) + 8" :y="bar + inner + bar / 2" dominant-baseline="central" class="val on">{{ r.afterText ?? (r.after + unit) }}</text>
    </g>
    <line :x1="labelWidth" :x2="labelWidth" :y1="legendH - 4" :y2="height + 4" class="base" />
  </svg>
</template>

<style scoped>
.pairs { display: block; max-width: 100%; height: auto; overflow: visible; font-family: var(--sans); }
.hl { fill: #1f4e8c; }
.ctx { fill: #7f8da3; }
.legend text { font-size: 13px; fill: var(--muted); }
.lab { font-size: 15px; fill: var(--ink); font-weight: 600; }
.val { font-size: 14px; fill: var(--muted); font-variant-numeric: tabular-nums; }
.val.on { fill: var(--ink); font-weight: 800; font-size: 15px; }
.base { stroke: var(--line); stroke-width: 1; }
</style>
