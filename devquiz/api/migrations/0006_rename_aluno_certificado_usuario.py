# Generated by Django 5.2.1 on 2025-06-03 19:48

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0005_rename_usuario_certificado_aluno'),
    ]

    operations = [
        migrations.RenameField(
            model_name='certificado',
            old_name='aluno',
            new_name='usuario',
        ),
    ]
