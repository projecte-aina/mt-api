build:
	docker build -t projecteaina/mt-api:latest .
deploy:
	docker compose up -d
undeploy:
	docker compose down
stop:
	docker compose stop


	

act-run-tests:
	gh act -j test -W '.github/workflows/tests.yml'
