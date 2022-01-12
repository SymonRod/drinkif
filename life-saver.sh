#!/bin/bash

docker stop postgres

tar -cz  -f ../db.tar.gz db/

docker start postgres