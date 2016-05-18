#!/bin/bash
mongoimport --db saferide --collection rides --drop --file rides_data.json
