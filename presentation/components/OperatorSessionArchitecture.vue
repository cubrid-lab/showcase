<template>
  <svg class="session-architecture" viewBox="0 0 870 300" role="img" aria-labelledby="session-arch-title session-arch-desc">
    <title id="session-arch-title">CUBRID Operator의 제어 경로와 데이터 경로</title>
    <desc id="session-arch-desc">Kubernetes API의 요청을 받은 Operator는 Instance Manager로 역할을 관찰하고, 불확실하면 RW Broker를 0개로 줄입니다. 앱의 SQL은 Broker에서 CUBRID로 직접 흐릅니다. 재구축 요청 시 현재 master의 백업을 대상 멤버에 복원합니다.</desc>
    <defs><marker id="session-arrow" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="6" markerHeight="6" orient="auto"><path d="M0 0L10 5L0 10Z" fill="#a8bdd4"/></marker><marker id="session-orange" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="6" markerHeight="6" orient="auto"><path d="M0 0L10 5L0 10Z" fill="#ffad5c"/></marker></defs>
    <text class="lane" x="0" y="20">제어 경로</text>
    <rect class="arch-node" x="0" y="38" width="200" height="65" rx="7"/><text x="100" y="65">Kubernetes API</text><text class="arch-note" x="100" y="87">구성 · 재구축 요청</text>
    <path class="link" d="M200 70H320"/>
    <rect class="arch-node accent" x="325" y="38" width="210" height="65" rx="7"/><text x="430" y="65">Operator</text><text class="arch-note" x="430" y="87">관찰 · 격리 · 복구 조정</text>
    <path class="control" d="M535 70H650"/><text class="label" x="592" y="52">① 역할 조회</text>
    <rect class="arch-node" x="655" y="38" width="215" height="65" rx="7"/><text x="762" y="65">Instance Manager</text><text class="arch-note" x="762" y="87">각 멤버의 역할 · 작업 상태</text>
    <path class="control" d="M430 103V174"/><text class="label" x="535" y="144">② 불확실하면 0개로</text>
    <path class="dotted" d="M762 103V174"/>
    <text class="lane" x="0" y="155">데이터 경로</text>
    <rect class="arch-node" x="0" y="179" width="200" height="65" rx="7"/><text x="100" y="218">애플리케이션</text>
    <path class="link" d="M200 211H320"/><text class="label muted" x="260" y="197">SQL</text>
    <rect class="arch-node accent" x="325" y="179" width="210" height="65" rx="7"/><text x="430" y="207">읽기-쓰기 Broker</text><text class="arch-note" x="430" y="229">쓰기 경로의 차단 지점</text>
    <path class="link" d="M535 211H650"/>
    <rect class="arch-node" x="655" y="179" width="215" height="65" rx="7"/><text x="762" y="207">CUBRID HA · 3멤버</text><text class="arch-note" x="762" y="229">master 선출 · 복제</text>
    <path class="control" d="M762 244V278H585"/>
    <text class="label" x="680" y="270">master 백업</text>
    <rect class="arch-node" x="350" y="258" width="230" height="40" rx="7"/><text x="465" y="284" style="font-size:15px">③ 대상 멤버 재구축</text>
  </svg>
</template>
<style scoped>
.session-architecture { display:block; width:100%; height:auto; }
text { fill:#f2f6fc; font:650 18px var(--sans); text-anchor:middle; }
.arch-note { fill:#afbed0; font-size:13px; font-weight:450; }
.lane { text-anchor:start; font-size:13px; fill:#a8bdd4; }
.label { fill:#ffad5c; font-size:13px; font-weight:550; }
.muted { fill:#a8bdd4; }
.arch-node { fill:#17283c; stroke:#597087; stroke-width:1.3; }
.accent { stroke:#ffad5c; stroke-width:2; }
.link { fill:none; stroke:#a8bdd4; stroke-width:2; marker-end:url(#session-arrow); }
.control { fill:none; stroke:#ffad5c; stroke-width:2; stroke-dasharray:6 4; marker-end:url(#session-orange); }
.dotted { stroke:#597087; stroke-width:1.5; stroke-dasharray:3 4; }
</style>
