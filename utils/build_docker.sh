set -e

docker build --tag irondome:latest .
docker run --init --rm irondome