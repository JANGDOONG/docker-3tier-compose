# Docker Compose 3-Tier Practice (nginx + Flask + MySQL)

## 목적 (Why)
- Docker를 암기용이 아니라 구조 이해 관점으로 학습
- Docker Compose 기반 3-Tier(Web → App → DB) 요청 흐름을 직접 구성
- 왜 이런 구조를 선택했는지 설명 가능한 상태를 목표로 함

## 아키텍처 (Architecture)
외부 사용자 → nginx(web) → Flask(app) → MySQL(db)

External Client
  |
  v
nginx (web) :8080   [public]
  |
  v
Flask (app) :5000   [internal]
  |
  v
MySQL (db) :3306    [internal only]

## 구성 요소 (Services)
- web: nginx (외부 진입점, reverse proxy)
- app: Flask (요청 처리 API)
- db: MySQL (내부 전용 DB, 외부 미노출)
- db_data: MySQL 데이터 영속화를 위한 volume
- 민감정보는 .env로 관리하며 GitHub에는 포함하지 않음

## 구현된 API (구조 검증용)
- GET /api/health -> {"status":"ok"}
- GET /api/db -> {"db":"ok"}
- GET /api/time -> {"time":"YYYY-MM-DD HH:MM:SS"}
  * 기본 UTC
  * TZ=Asia/Seoul 설정 시 로컬 시간 가능

## 트러블슈팅
- /api/time 404 발생
  원인:
  - @app.route 데코레이터 누락
  - app.run() 아래에 라우트 정의
  해결:
  - 모든 라우트는 @app.route 사용
  - 모든 라우트는 app.run() 위에 정의

## 실행 방법
docker compose up -d --build
curl http://localhost:8080/api/health
curl http://localhost:8080/api/db
curl http://localhost:8080/api/time
docker compose down

## 보안 관점
- DB 포트 외부 미노출로 공격면 최소화
- 외부 노출은 nginx만 수행하여 역할 분리
- .env 사용 + .gitignore로 민감정보 보호
