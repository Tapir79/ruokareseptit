#!/bin/bash

# Remove database.db if exists
if [ -f "database.db" ]; then
    rm database.db
    echo "Olemassa oleva database.db poistettu."
fi

# Load schema and init SQL -files from install folder
sqlite3 database.db < install/schema.sql
echo "Skeema ladattu tietokantaan database.db."
sqlite3 database.db < install/init.sql
echo "Init.sql ladattu tietokantaan database.db."

# Optional: add test data
read -p "Haluatko lisätä testidataa? (y/n): " answer
if [[ "$answer" =~ ^[Yy]$ ]]; then
    sqlite3 database.db < install/test_data.sql
    echo "Testidata ladattu tietokantaan database.db."
    python install/upload_images.py 
    echo "Kuvatestidata ladattu."
else
    echo "Testidataa ei lisätty."
fi
