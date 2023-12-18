PROJECT_NAME ?= maintenance-tracker

start:
	${INFO} "Creating PostgreSQL database volume"
	@ docker volume create --name=${PROJECT_NAME}-data > /dev/null
	@ echo " "
	@ ${INFO} "Building required docker images"
	@ docker-compose -f docker-compose.yml build ${PROJECT_NAME}
	@ docker-compose -f docker-compose.yml build ${PROJECT_NAME}-api
	@
	@ ${INFO} "Starting the application"
	@ COMPOSE_HTTP_TIMEOUT=200 docker-compose -f docker-compose.yml up ${PROJECT_NAME} &> /dev/null &


stop:
	${INFO} "Stopping all containers"
	@ docker-compose -f docker-compose.yml down -v
	@ ${SUCCESS} "All containers stopped successfully"

clean:
	${INFO} "Cleaning your local environment"
	${INFO} "Note that all ephemeral volumes will be destroyed"
	@ docker-compose -f docker-compose.yml down -v
	@ docker volume rm ${PROJECT_NAME}-data
	@ ${INFO} "Removing dangling images"
	@ docker images -q -f label=application${PROJECT_NAME} | xargs -I ARGS docker rmi -f ARGS
	@ docker system prune
	@ ${SUCCESS} "Clean complete"

# COLORS
GREEN	:= $(shell tput -Txterm setaf 2)
YELLOW 	:= $(shell tput -Txterm setaf 3)
WHITE	:= $(shell tput -Txterm setaf 7)
NC		:= "\e[0m"
RESET 	:= $(shell tput -Txterm sgr0)

# SHELL FUNCTIONS
INFO 	:= @bash -c 'printf "\n"; printf $(YELLOW); echo "===> $$1"; printf "\n"; printf $(NC)' SOME_VALUE
SUCCESS	:= @bash -c 'printf "\n"; printf $(GREEN); echo "===> $$1"; printf "\n"; printf $(NC)' SOME_VALUE
