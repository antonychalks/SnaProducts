# Generated by Django 3.2.25 on 2024-06-04 19:18

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('profiles', '0001_initial'),
        ('saved_products', '0003_alter_savedproductslist_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='savedproductslist',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='saved_items_list', to='profiles.userprofile'),
        ),
    ]