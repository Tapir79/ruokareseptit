#!/bin/bash

# Delete database.db if it exists
if [ -f "database.db" ]; then
    rm database.db
    echo "Oemassa oleva tietokanta database.db poistettu."
fi

# Create the database using the schema and initial data
sqlite3 database.db < schema.sql
echo "Skeema ladattu tietokantaan database.db."

sqlite3 database.db < init.sql
echo "Init.sql ladattu tietokantaan database.db."

# Ask user if they want to add test data
read -p "Haluatko lisätä testidataa? (y/n): " answer
if [[ "$answer" =~ ^[Yy]$ ]]; then
    sqlite3 database.db < test_data.sql
    echo "Testidata ladattu tietokantaan database.db."
else
    echo "Testidataa ei lisätty."
fi
