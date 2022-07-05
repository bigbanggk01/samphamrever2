# Generated by Django 4.0.4 on 2022-06-22 10:26

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0009_rename_name_product_product_name'),
    ]

    operations = [
        migrations.RunSQL(
            sql='''
            CREATE TRIGGER vector_column_trigger
            BEFORE INSERT OR UPDATE OF product_name, vector_column
            ON api_product
            FOR EACH ROW EXECUTE PROCEDURE
            tsvector_update_trigger(vector_column,'pg_catalog.english',product_name);
            UPDATE api_product SET vector_column = NULL;
            ''',

            reverse_sql='''
            DROP TRIGGER IF EXISTS product_update_trigger
            ON api_product;
            '''),
    ]
