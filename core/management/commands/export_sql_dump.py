import os
import subprocess
from django.core.management.base import BaseCommand

class Command(BaseCommand):
    help = 'Exports a SQL dump file from the specified database'

    def handle(self, *args, **kwargs):
        db_name = input('Enter the database name: ')
        user = input('Enter the database user: ')
        password = input('Enter the database password: ')
        host = input('Enter the database host: ')
        port = input('Enter the database port: ')
        dump_file = input('Enter the output file name for the SQL dump: ') or f"{db_name}_dump.sql"

        # Specify the path to pg_dump if it's not in PATH
        pg_dump_command = [
            '/path/to/pg_dump',  # Replace with the full path if necessary
            f'--host={host}',
            f'--port={port}',
            f'--username={user}',
            f'--no-password',
            f'--file={dump_file}',
            db_name
        ]

        # Set the PGPASSWORD environment variable for authentication
        os.environ['PGPASSWORD'] = password

        try:
            result = subprocess.run(pg_dump_command, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
            self.stdout.write(self.style.SUCCESS(f"SQL dump has been saved to '{dump_file}'"))
            self.stdout.write(self.style.SUCCESS(f"Output:\n{result.stdout}"))
        except subprocess.CalledProcessError as e:
            self.stderr.write(self.style.ERROR(f"Error occurred: {e}"))
            self.stderr.write(self.style.ERROR(f"Output:\n{e.stderr}"))
        finally:
            # Clean up the PGPASSWORD environment variable
            del os.environ['PGPASSWORD']

