.PHONY: migrations
migrations:
	alembic -c backend/src/adapters/db/alembic/alembic.ini revision --autogenerate

.PHONY: upgrade-migrations
upgrade-migrations:
	alembic -c backend/src/adapters/db/alembic/alembic.ini upgrade head
