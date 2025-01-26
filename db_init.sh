#!/bin/bash

# Load environment variables from .env file
if [ -f .env ]; then
    export $(cat .env | xargs)
else
    echo ".env file not found! Exiting."
    exit 1
fi

# Directory containing SQL scripts and other files
SCRIPT_DIR="./"

# List of SQL files to execute in order (excluding 01_schema_creation.sql, as it's handled separately)
SQL_FILES=(
    "02_1_initial_data_load.sql"
    "03_table_functions.sql"
    "04_triggers.sql"
    "05_indexes_and_search.sql"
    "06_search_functions.sql"
)

# Step 0: Truncate Database
echo "Truncating database..."
psql "$DB_CONN" -f /Users/spicykneecaps/Projects/FSEA/database_setup/truncate_database.sql
if [ $? -ne 0 ]; then
    echo "Error occurred while truncating database. Exiting."
    exit 1
fi

