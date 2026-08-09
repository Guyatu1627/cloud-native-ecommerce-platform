.PHONY: up down migrate seed test logs

up:
	docker-compose up -d --build

down:
	docker-compose down -v

migrate:
	docker-compose exec web alembic upgrade head

seed:
	docker-compose exec web python app/db/seed.py

test:
	docker-compose exec web pytest

logs:
	docker-compose logs -f web
