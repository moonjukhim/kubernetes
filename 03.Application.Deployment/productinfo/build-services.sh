#!/bin/bash

set -o errexit

if [ "$#" -ne 2 ]; then
    echo "Incorrect parameters"
    echo "Usage: build-services.sh <version> <prefix>"
    exit 1
fi

VERSION=$1
PREFIX=$2
SCRIPTDIR=$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )

pushd "$SCRIPTDIR/productpage"
  docker build --pull -t "${PREFIX}/productinfo-productpage-v1:${VERSION}" -t "${PREFIX}/productinfo-productpage-v1:latest" .
  #flooding
  docker build --pull -t "${PREFIX}/productinfo-productpage-v-flooding:${VERSION}" -t "${PREFIX}/productinfo-productpage-v-flooding:latest" --build-arg flood_factor=100 .
popd

pushd "$SCRIPTDIR/details"
  #plain build -- no calling external book service to fetch topics
  docker build --pull -t "${PREFIX}/productinfo-details-v1:${VERSION}" -t "${PREFIX}/productinfo-details-v1:latest" --build-arg service_version=v1 .
  #with calling external book service to fetch topic for the book
  docker build --pull -t "${PREFIX}/productinfo-details-v2:${VERSION}" -t "${PREFIX}/productinfo-details-v2:latest" --build-arg service_version=v2 \
	 --build-arg enable_external_book_service=true .
popd

pushd "$SCRIPTDIR/reviews"
  #java build the app.
  docker run --rm -u root -v "$(pwd)":/home/gradle/project -w /home/gradle/project gradle:4.8.1 gradle clean build
  pushd reviews-wlpcfg
    #plain build -- no ratings
    docker build --pull -t "${PREFIX}/productinfo-reviews-v1:${VERSION}" -t "${PREFIX}/productinfo-reviews-v1:latest" --build-arg service_version=v1 .
    #with ratings black stars
    docker build --pull -t "${PREFIX}/productinfo-reviews-v2:${VERSION}" -t "${PREFIX}/productinfo-reviews-v2:latest" --build-arg service_version=v2 \
	   --build-arg enable_ratings=true .
    #with ratings red stars
    docker build --pull -t "${PREFIX}/productinfo-reviews-v3:${VERSION}" -t "${PREFIX}/productinfo-reviews-v3:latest" --build-arg service_version=v3 \
	   --build-arg enable_ratings=true --build-arg star_color=red .
  popd
popd

pushd "$SCRIPTDIR/ratings"
  docker build --pull -t "${PREFIX}/productinfo-ratings-v1:${VERSION}" -t "${PREFIX}/productinfo-ratings-v1:latest" --build-arg service_version=v1 .
  docker build --pull -t "${PREFIX}/productinfo-ratings-v2:${VERSION}" -t "${PREFIX}/productinfo-ratings-v2:latest" --build-arg service_version=v2 .
  docker build --pull -t "${PREFIX}/productinfo-ratings-v-faulty:${VERSION}" -t "${PREFIX}/productinfo-ratings-v-faulty:latest" --build-arg service_version=v-faulty .
  docker build --pull -t "${PREFIX}/productinfo-ratings-v-delayed:${VERSION}" -t "${PREFIX}/productinfo-ratings-v-delayed:latest" --build-arg service_version=v-delayed .
  docker build --pull -t "${PREFIX}/productinfo-ratings-v-unavailable:${VERSION}" -t "${PREFIX}/productinfo-ratings-v-unavailable:latest" --build-arg service_version=v-unavailable .
  docker build --pull -t "${PREFIX}/productinfo-ratings-v-unhealthy:${VERSION}" -t "${PREFIX}/productinfo-ratings-v-unhealthy:latest" --build-arg service_version=v-unhealthy .
popd

pushd "$SCRIPTDIR/mysql"
  docker build --pull -t "${PREFIX}/productinfo-mysqldb:${VERSION}" -t "${PREFIX}/productinfo-mysqldb:latest" .
popd

pushd "$SCRIPTDIR/mongodb"
  docker build --pull -t "${PREFIX}/productinfo-mongodb:${VERSION}" -t "${PREFIX}/productinfo-mongodb:latest" .
popd
