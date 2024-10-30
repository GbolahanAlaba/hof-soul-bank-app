# Generated by Django 5.1.1 on 2024-10-30 13:48

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('App_Auth', '0003_alter_role_created_by_alter_sector_created_by_and_more'),
    ]

    operations = [
        migrations.DeleteModel(
            name='AuthCode',
        ),
        migrations.RemoveField(
            model_name='sector',
            name='created_by',
        ),
        migrations.RemoveField(
            model_name='team',
            name='created_by',
        ),
        migrations.AlterModelOptions(
            name='user',
            options={'ordering': ['-date_joined']},
        ),
        migrations.DeleteModel(
            name='Role',
        ),
        migrations.DeleteModel(
            name='Sector',
        ),
        migrations.DeleteModel(
            name='Team',
        ),
    ]