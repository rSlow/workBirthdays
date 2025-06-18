start:
	docker compose --profile services --profile runners --profile starters up --build -d

stop:
	docker compose --profile services --profile runners --profile starters down --remove-orphans

update: stop pull start

pull:
	git pull
