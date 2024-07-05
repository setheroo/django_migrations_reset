from typing import List
import os
import json
import subprocess
import shutil
import traceback

import mysql.connector

# These will need to change to your databases credentials, this is written dynamically for environment
DB_KEYS = json.loads(os.getenv("DB_KEYS"))
DB_ENVIRONMENT = os.getenv("DB_ENVIRONMENT")

# This app names list will need to change to your django projects custom apps
APP_NAMES = ["APP1"]

DB = mysql.connector.connect(
    host=DB_KEYS[DB_ENVIRONMENT]["db_host"],
    port=DB_KEYS[DB_ENVIRONMENT]["db_port"],
    user=DB_KEYS[DB_ENVIRONMENT]["db_user"],
    password=DB_KEYS[DB_ENVIRONMENT]["db_pass"],
    database=DB_KEYS[DB_ENVIRONMENT]["db_name"],
)

CURSOR = DB.cursor(buffered=True)

def main():
    # Begin with stating that there aren't any model changes, lets scout the directories looking for those new models
    MODEL_CHANGES = False
    # This is to quit while were ahead - if there isnt a new_models file, we don't need this to even happen.
    for app in APP_NAMES:
        if os.path.isfile("{:s}/new_models.py".format(app)):
            print("Found new models for {:s}".format(app))
            MODEL_CHANGES = True

    if not MODEL_CHANGES:
        print("No Model changes on this run, quitting migrations automation...")
        quit()

    print("Preparing to query the database and clear out the migration states...")
    # First portion is that we need to clear out the DB of the migration states for the apps
    query = (
        "SELECT * "
        + "FROM django_migrations AS m "
        + f"WHERE m.app IN ({','.join(['%s']*len(APP_NAMES))})"
    )

    CURSOR.execute(query, APP_NAMES)

    migration_results = CURSOR.fetchall()

    # input request to see if we should continue or quit
    if migration_results:
        print("The following migrations will be deleted:")
        for row in migration_results:
            print(row)
        print("Would you like to continue? (y/n)")
        if input() == "n":
            print("Quitting migrations automation...")
            quit()

    print("Deleting the migration entries...")

    # This is how we are going to delete the migration entries - this is all done dynamically
    if migration_results:
        for row in migration_results:
            CURSOR.execute("DELETE FROM django_migrations WHERE id = %s", (row[0],))

        DB.commit()
    
    print("Checking if migration entries have been deleted!")

    CURSOR.execute(query, APP_NAMES)

    post_delete_migration_entries = CURSOR.fetchall()

    if len(post_delete_migration_entries) > 0:
        print("The following migration entries still exist:")
        for row in post_delete_migration_entries:
            print(row)
        print("something is very likely wrong if there are still entries... quitting for safety...")
        print("Quitting migrations automation after hitting any button...")
        input()
        quit()

    # We are done with the database steps, its all cleared up now
    # This next portion, is where are going to essentially fake out the migration state
    # We are not going to actually adjust anything in the database, we are simply making
    # a 0001 migration file, and faking into the DB - and since the DB is clear of all the
    # Migration entries, we can now do this safely - this now leaves us just 1 migration file
    # for each app.

    for app in APP_NAMES:
        subprocess.call(["python", "manage.py", "makemigrations", app, "--noinput"])
        print("Made the migration files for {:s}".format(app))

    print("Preparing to migrate the faked initial files to the DB...")
    subprocess.call(["python", "manage.py", "migrate", "--fake-initial", "--noinput"])

    # So what do we do now? We desire to make model changes right? Well this is how we plan to make that happen...
    # We are going to intelligently learn which models have the changes that we seek to apply... this should be fun
    # What we are going to do is simply look for if a set of files exists by an expected name, and if so, replace
    # the old existing models with the new ones, and make some new migration files that can actually be applied
    # this is going to be rinse repeated for every change ever, because this is far safer than keeping up with
    # migration files across code commits (this may not actually be true, but it sure is a chore to keep up with)

    for app in APP_NAMES:
        if os.path.isfile("{:s}/new_models.py".format(app)):
            try:
                shutil.copy("{:s}/new_models.py".format(app), "{:s}/models.py".format(app))
                print("Overwrote the {:s} models file the latest models...".format(app))
                subprocess.call(
                    [
                        "python",
                        "manage.py",
                        "makemigrations",
                        app,
                        "--noinput",
                    ]
                )
                print("Made the migrations files for {:s}".format(app))
            except:
                print("Encountered an error: {:s}".format(traceback.format_exc()))

    subprocess.call(["python", "manage.py", "migrate", "--noinput"])

    print("Model changes are complete!")

if __name__ == "__main__":
    main()
