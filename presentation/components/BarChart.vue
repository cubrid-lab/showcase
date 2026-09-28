<script setup>
import { computed } from 'vue'

// Horizontal bars for projected slides: one highlighted row (blue), the rest as
// context (gray). Every bar is labelled at its tip, so no hover layer is needed.
const props = defineProps({
  rows: { type: Array, required: true },      // [{ label, value, hl?, text? }]
  max: { type: Number, default: 0 },          // axis max; defaults to largest value
  unit: { type: String, default: '' },        // appended to tip labels
  width: { type: Number, default: 520 },
  labelWidth: { type: Number, default: 120 },
  bar: { type: Number, default: 22 },
  gap: { type: Number, default: 14 },
})

const pad = 64 // room right of the longest bar for its label
const plotW = computed(() => props.width - props.labelWidth - pad)
const top = computed(() => Math.max(props.max, ...props.rows.map(r => r.value)))
const height = computed(() => props.rows.length * (props.bar + props.gap) - props.gap)
const len = v => (v / top.value) * plotW.value

// 4px rounded data-end, square at the baseline
function barPath(w, h) {
  const r = Math.min(4, w / 2, h / 2)
  return `M0,0 H${w - r} Q${w},0 ${w},${r} V${h - r} Q${w},${h} ${w - r},${h} H0 Z`
}
</script>

<template>
  <svg :viewBox="`0 0 ${width} ${height}`" :width="width" :height="height" class="bars" role="img">
    <g v-for="(r, i) in rows" :key="r.label" :transform="`translate(0 ${i * (bar + gap)})`">
      <text :x="labelWidth - 12" :y="bar / 2" text-anchor="end" dominant-baseline="central" class="lab" :class="{ on: r.hl }">{{ r.label }}</text>
      <path :d="barPath(Math.max(len(r.value), 2), bar)" :transform="`translate(${labelWidth} 0)`" :class="r.hl ? 'hl' : 'ctx'" />
      <text :x="labelWidth + len(r.value) + 8" :y="bar / 2" dominant-baseline="central" class="val" :class="{ on: r.hl }">{{ r.text ?? (r.value + unit) }}</text>
    </g>
    <line :x1="labelWidth" :x2="labelWidth" y1="-4" :y2="height + 4" class="base" />
  </svg>
</template>

<style scoped>
.bars { display: block; max-width: 100%; height: auto; overflow: visible; font-family: var(--sans); }
.hl { fill: #1f4e8c; }
.ctx { fill: #7f8da3; }
.lab { font-size: 15px; fill: var(--muted); }
.lab.on { fill: var(--ink); font-weight: 700; }
.val { font-size: 15px; fill: var(--muted); font-variant-numeric: tabular-nums; }
.val.on { fill: var(--ink); font-weight: 800; font-size: 17px; }
.base { stroke: var(--line); stroke-width: 1; }
</style>
