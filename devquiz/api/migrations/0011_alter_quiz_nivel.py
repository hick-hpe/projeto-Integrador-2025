# Generated by Django 5.2.1 on 2025-06-04 16:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0010_remove_questao_explicacao'),
    ]

    operations = [
        migrations.AlterField(
            model_name='quiz',
            name='nivel',
            field=models.CharField(choices=[('Iniciante', 'Iniciante'), ('Intermediário', 'Intermediário'), ('Avançado', 'Avançado')], default='iniciante', max_length=13),
        ),
    ]
