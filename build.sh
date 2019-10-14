#!/usr/bin/env bash
set -e
export PYTHONDONTWRITEBYTECODE=1
PIPENV_CMD=${PIPENV_CMD:-pipenv}

function check_container_status {
  status=$(docker inspect -f {{.State.Status}} $1)
  echo $status
}

function check_neo4j_container() {
    if [[ $(check_container_status neo4j) == *"No such object: neo4j"* ]] || [[ $(check_container_status neo4j) != "running" ]]; then
      echo "command requires neo4j to be running, please run docker-compose up in another terminal"
      exit 1
    fi
}

case "$1" in

    clean)
        venv=$(pipenv --venv)
        rm -rf $venv || true
        rm -f Pipfile.lock || true
    ;;
    install-test)
        yes | $PIPENV_CMD install
        yes | $PIPENV_CMD install --dev
        $PIPENV_CMD run python -m pytest -s -v -m "not integration"
     ;;
     run-local)
        check_neo4j_container
        FLASK_ENV=development $PIPENV_CMD run python manage.py
     ;;
     test)
        $PIPENV_CMD run python -m pytest -s -v -m "not integration"
     ;;
     integration-test)
        check_neo4j_container
        $PIPENV_CMD run python -m pytest -s -v -m "integration" --cov=. .
     ;;
    *)
    echo $"Usage: $0 {clean|install-test|run-local|test|integration-test}"
esac
