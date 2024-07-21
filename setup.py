from setuptools import setup, find_packages

setup(
    name='db_to_excel',
    version='0.1',
    packages=find_packages(),
    install_requires=[
        'pandas',
        'sqlalchemy',
        'openpyxl',
        'psycopg2-binary',  # Add this if you're using PostgreSQL
        'django'
    ],
    entry_points={
        'console_scripts': [
            'export_db_to_excel=db_to_excel.management.commands.export_db_to_excel:Command.handle',
            'export_sql_dump=db_to_excel.management.commands.export_sql_dump:Command.handle',
        ],
    },
    author='Ali Mohammadnia',
    author_email='alimohammadnia127@gmail.com',
    description='A package to export database tables to Excel files',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/psymoniko/auto-doc-collector',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Framework :: Django',
    ],
    python_requires='>=3.6',
)

