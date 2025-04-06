# core/management/commands/init_postgis.py
from django.contrib.gis.db.backends.postgis.operations import PostGISOperations
from django.core.management.base import BaseCommand
from django.db import connection

class Command(BaseCommand):
    def handle(self, *args, **options):
        with connection.cursor() as cursor:
            cursor.execute("CREATE EXTENSION IF NOT EXISTS postgis")
            cursor.execute("CREATE EXTENSION IF NOT EXISTS hstore")
            cursor.execute("CREATE EXTENSION IF NOT EXISTS pg_trgm")
        self.stdout.write("PostGIS extensions activated")