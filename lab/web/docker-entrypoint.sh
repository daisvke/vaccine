#!/bin/bash

# Initialize the SQLite Database

set -e

SQLITE_DB="/var/www/html/data/VaccineLab.db"

if [ ! -f "$SQLITE_DB" ]; then
    echo "[SQLite] Initializing database..."

    mkdir -p /var/www/html/data

    php /var/www/html/init-sqlite.php

    echo "[SQLite] Database initialized."
else
    echo "[SQLite] Database already exists."
fi

exec apache2-foreground
