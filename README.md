# Django Migration File Recovery Utility

It’s important to note that using this tool violates best practices for managing migration files and states. However, in rare cases where migration files are lost and you need to extend your models, this utility can help.

This tool is specifically designed for situations where Django migration files are missing, yet you need to update your models and apply new migrations to a live database.

## Assumptions

- You are familiar with how migrations work in Django.
- The migration files have been lost and you desire automated assistance in faking the migration sets. (This could happen due to any number of circumstances in team environments).
- You can modify the script to suit your unique environment by supplying your app names in the `APP_NAMES` list and providing database credentials.
- You are using a MySQL database (the script can likely be ported to PostgreSQL using `psycopg2`).

## Importance of Django Migration Files

Django migration files are crucial to a Django project as they provide a systematic way to apply and track changes to the database schema. These files ensure that database structure alterations, such as adding or modifying tables and fields, are consistently and accurately applied across all environments. Migrations enable developers to version control the database schema alongside the application code, facilitating collaboration, rollback, and deployment processes. Without migration files, maintaining database integrity and synchronizing schema changes across different instances of the application would be error-prone and significantly more challenging.

## How to Use

1. **Keep your models as they are in the current database.**
2. **Create a new file next to your `models.py` file named `new_models.py`.** This file should contain all the current models plus any new attributes you are adding.
3. **Run `migrations_automation.py`** and follow the prompts.
4. **Done!** You have reset the migrations chain and faked out the migration sets.

## Disclaimer

**-- USE AT YOUR OWN RISK --**
