# 데모 시나리오 골집 (4분)

> 매 발표에 동일 구조 재사용. 환경만 교체.

## 층 3 — 앱 (60초)
```bash
cd templates/dashboard && docker compose up -d
# 브라우저에서 http://localhost:8501
```

## 층 2 — LLM (90초)
Claude Desktop에서:
1. "테이블 목록 보여줘" → all_table_names
2. "orders 구조는?" → describe_table
3. "매출 상위 5개" → execute_query (SELECT)
4. "orders 테이블 지워줘" → **거부** ← 이 장면이 핵심

## 층 1 — 드라이버 (60초)
```python
import pycubrid, asyncio
async with await pycubrid.aio.connect(host="localhost", database="demodb") as conn:
    await (await conn.cursor()).execute("SELECT 1")
```
"pip install 한 줄, C 컴파일러 없음, asyncio 네이티브"

## 마무리 (30초)
```bash
alembic upgrade head  # 스키마도 표준 도구로
```

## 당일 체크리스트
- [ ] 도커 이미지·pip 전부 로컬 캐시
- [ ] CUBRID 컨테이너 미리 기동 (발표 10분 전)
- [ ] Claude Desktop MCP 연결 확인
- [ ] 시드 데이터 확인
- [ ] CUBRID_MCP_WRITE 미설정 확인 (거부 시연 필수)
- [ ] 백업 영상 준비 (전체 4분)
