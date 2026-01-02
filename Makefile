.PHONY: test lint fix deploy

test:
	pytest tests/ -v

lint:
	ruff check .claude/hooks/
	shellcheck scripts/*.sh 2>/dev/null || true

fix:
	ruff check --fix .claude/hooks/

deploy:
	./scripts/deploy.sh
