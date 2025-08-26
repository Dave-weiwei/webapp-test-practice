# Makefile - 自動化測試工作指令

# 啟動 Web 容器（Flask）
up:
	docker compose up -d web

# 關閉所有容器
down:
	docker compose down

# 執行測試（依照 .env 變數）
test:
	docker compose run --rm tests

# Chrome 測試
test-chrome:
	docker compose run --rm tests --mybrowser=chrome

# Firefox 測試
test-firefox:
	docker compose run --rm tests --mybrowser=firefox