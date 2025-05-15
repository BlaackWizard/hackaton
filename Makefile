.PHONY: migrations
migrations:
	alembic -c backend/src/access_service/adapters/db/alembic/alembic.ini revision --autogenerate
.PHONY: upgrade-migrations
upgrade-migrations:
	alembic -c backend/src/access_service/adapters/db/alembic/alembic.ini upgrade head
.PHONY: run-api
run-api:
	cd backend/src/bootstrap/entrypoint/ && python fast_api.py
