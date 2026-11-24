<template>
  <svg class="write-isolation-diagram" viewBox="0 0 870 245" role="img" aria-labelledby="write-isolation-title write-isolation-desc">
    <title id="write-isolation-title">Operator의 역할 관찰과 읽기-쓰기 Broker 차단</title>
    <desc id="write-isolation-desc">클라이언트는 읽기-쓰기 Broker를 통해 CUBRID 멤버에 연결합니다. Operator는 Instance Manager로 역할을 관찰하고, master가 불확실하면 Broker Deployment를 0으로 줄입니다. CUBRID HA가 승격을 결정합니다.</desc>
    <defs>
      <marker id="write-sql-arrow" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse"><path d="M0 0 L10 5 L0 10Z" fill="#142033" /></marker>
      <marker id="write-control-arrow" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse"><path d="M0 0 L10 5 L0 10Z" fill="#245893" /></marker>
    </defs>
    <rect class="control-box" x="320" y="6" width="225" height="59" rx="8" />
    <text x="432" y="31" text-anchor="middle">Operator</text>
    <text class="small" x="432" y="51" text-anchor="middle">master 불확실 → 격리 기록</text>
    <path class="control-line" d="M400 65 V144" marker-end="url(#write-control-arrow)" />
    <text class="label" x="315" y="98" text-anchor="end">② Broker를 0개로</text>
    <path class="control-line" d="M545 35 H745 V88" marker-end="url(#write-control-arrow)" />
    <text class="label" x="645" y="23" text-anchor="middle">① 역할 조회</text>
    <rect class="control-box" x="632" y="90" width="225" height="40" rx="7" />
    <text class="small" x="744" y="115" text-anchor="middle">Instance Manager · 멤버별</text>
    <path class="control-line" d="M744 130 V144" />
    <rect class="box" x="8" y="148" width="185" height="66" rx="8" />
    <text x="100" y="187" text-anchor="middle">클라이언트</text>
    <path class="sql-line" d="M193 180 H318" marker-end="url(#write-sql-arrow)" />
    <text class="small" x="256" y="165" text-anchor="middle">쓰기 요청</text>
    <rect class="control-box" x="320" y="148" width="225" height="66" rx="8" />
    <text x="432" y="175" text-anchor="middle">읽기-쓰기 Broker</text>
    <text class="small" x="432" y="197" text-anchor="middle">격리 시 Pod 종료</text>
    <path class="sql-line" d="M545 180 H630" marker-end="url(#write-sql-arrow)" />
    <rect class="box" x="632" y="148" width="225" height="66" rx="8" />
    <text x="744" y="175" text-anchor="middle">CUBRID 멤버</text>
    <text class="small" x="744" y="197" text-anchor="middle">승격은 CUBRID HA가 결정</text>
    <text class="small" x="8" y="241">실선: SQL 경로 · 파란 점선: 관찰·제어</text>
  </svg>
</template>

<style scoped>
.write-isolation-diagram { width: 100%; height: auto; display: block; }
text { fill: #142033; font-size: 19px; font-weight: 700; }
.small { fill: #536781; font-size: 15px; font-weight: 500; }
.label { fill: #245893; font-size: 16px; }
.box { fill: white; stroke: #9eacbf; stroke-width: 1.5; }
.control-box { fill: #edf4fc; stroke: #245893; stroke-width: 1.5; }
.sql-line { fill: none; stroke: #142033; stroke-width: 2; }
.control-line { fill: none; stroke: #245893; stroke-width: 2; stroke-dasharray: 6 4; }
</style>
