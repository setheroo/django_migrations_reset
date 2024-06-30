This utility is aimed at helping those in the unique situation that they have lost Django Migration files and wish to extend their models and need to push new migrations to an already deployed database.
Assumptions:
You already know how migrations work in Django, and have lost the migration files and are in need of assistance faking the migration sets.
You can modify the script to work towards you unique environment, by supplying your app names in the APP_NAMES list and supplying Database credentials.
You're using a MySQL database. Likely can be quickly ported to Postgres using psycopg2.
How to use:
1. Keep your Models as is to what is current in the Database.
2. Create a file next to your models.py file named "new_models.py" - this file is all the models you have now plus whatever new attributes you are adding.
3. Run the migrations_automation.py and work through the inputs.
4. Voila, you now have reset the migrations chain and faked out the migration sets.

-- USE AT YOUR OWN RISK --
Django migration files are crucial to a Django project as they provide a systematic way to apply and track changes to the database schema. These files ensure that database structure alterations, such as adding or modifying tables and fields, are consistently and accurately applied across all environments. Migrations enable developers to version control the database schema alongside the application code, facilitating collaboration, rollback, and deployment processes. Without migration files, maintaining database integrity and synchronizing schema changes across different instances of the application would be error-prone and significantly more challenging.
