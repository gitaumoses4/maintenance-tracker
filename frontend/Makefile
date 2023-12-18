PROJECT_NAME ?= maintenance-tracker

start:
	@ echo " "
	@ ${INFO} "Building required docker images"
	@ docker-compose -f docker-compose.yml build maintenance-tracker
	@
	@ ${INFO} "Starting the application"
	@ COMPOSE_HTTP_TIMEOUT=200 docker-compose -f docker-compose.yml up maintenance-tracker_frontend &> /dev/null &
