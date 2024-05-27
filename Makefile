run:
	docker-compose up

.PHONY: migrate
db-upgrade:
	docker-compose run --rm web poetry run alembic upgrade head

.PHONY: migrate
db-downgrade:
	docker-compose run --rm web poetry run alembic downgrade -1

.PHONY: makemigrations
db-makemigrations:
	@read -p "Enter migration message: " msg; \
	docker-compose run --rm web poetry run alembic revision --autogenerate -m "$${msg}"

.PHONY: down
down:
	docker-compose down

.PHONY: test
test:
	docker-compose run --rm web poetry run pytest tests/$(MODULE) --disable-warnings

.PHONY: test-coverage
test-coverage:
	docker-compose exec -it web poetry run pytest --cov=api --cov-report=term-missing --cov-report=html $(test_path)