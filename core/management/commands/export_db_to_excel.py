import os
import pandas as pd
from django.core.management.base import BaseCommand
from sqlalchemy import create_engine, text

class Command(BaseCommand):
    help = 'Exports all tables in the public schema to Excel files in the specified folder'

    def handle(self, *args, **kwargs):
        # Prompt the user for input
        db_name = input('Enter the database name: ')
        user = input('Enter the database user: ')
        password = input('Enter the database password: ')
        host = input('Enter the database host: ')
        port = input('Enter the database port: ')
        output_folder = input('Enter the output folder for Excel files (default is "table"): ') or 'table'

        db_connection_string = f'postgresql://{user}:{password}@{host}:{port}/{db_name}'
        engine = create_engine(db_connection_string)

        # Get a list of table names in the public schema
        with engine.connect() as connection:
            result = connection.execute(
                text("SELECT table_name FROM information_schema.tables WHERE table_schema = 'public';")
            )
            table_names = [row[0] for row in result]  # Use integer index to access the table name

        # Function to make datetime columns timezone-unaware
        def make_timezone_unaware(df):
            for column in df.select_dtypes(include=['datetimetz']).columns:
                df[column] = df[column].dt.tz_localize(None)
            return df

        # Create the folder for storing Excel files if it doesn't exist
        if not os.path.exists(output_folder):
            os.makedirs(output_folder)

        # Read each table and write to an Excel file in the folder
        for table_name in table_names:
            # Read the table into a DataFrame
            df = pd.read_sql_table(table_name, engine, schema='public')

            # Make datetime columns timezone-unaware
            df = make_timezone_unaware(df)

            # Write the DataFrame to an Excel file
            excel_filename = os.path.join(output_folder, f"{table_name}.xlsx")
            df.to_excel(excel_filename, index=False, engine='openpyxl')
            self.stdout.write(self.style.SUCCESS(f"Saved {table_name} to {excel_filename}"))

        self.stdout.write(self.style.SUCCESS("All tables have been saved to Excel files in the '{}' folder.".format(output_folder)))

