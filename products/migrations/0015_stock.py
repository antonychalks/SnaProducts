# Generated by Django 3.2.25 on 2024-07-30 04:59

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0014_alter_review_rating'),
    ]

    operations = [
        migrations.CreateModel(
            name='Stock',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('size', models.CharField(default='Review', max_length=50)),
                ('quantity', models.IntegerField(default=0)),
                ('deal', models.IntegerField(choices=[(0, 5), (1, 10), (2, 20), (3, 25)], default=0)),
                ('date_created', models.DateTimeField(auto_now_add=True)),
                ('product', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='Stock', to='products.product')),
            ],
        ),
    ]