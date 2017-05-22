#!/bin/bash

LOCATION_PATH="$1"

grass -c EPSG:32653 -e "$LOCATION_PATH"

