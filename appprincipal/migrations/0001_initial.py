# Generated by Django 2.0.4 on 2018-04-18 21:32

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Curso',
            fields=[
                ('codigo', models.CharField(max_length=10, primary_key=True, serialize=False)),
                ('nombre', models.CharField(max_length=40)),
                ('creditos', models.IntegerField()),
                ('horas_clase_magistral', models.IntegerField()),
                ('horas_estudio_independiente', models.IntegerField()),
                ('tipo_curso', models.CharField(choices=[('Asignatura basica', 'Asignatura basica'), ('Asignatura profesional', 'Asignatura profesional'), ('Asignatura electiva complementaria', 'Asignatura electiva complementaria'), ('Asignatura electiva profesional', 'Asignatura electiva profesional')], max_length=50)),
                ('validable', models.CharField(choices=[('si', 'Si'), ('no', 'No')], max_length=2)),
                ('habilitable', models.CharField(choices=[('si', 'Si'), ('no', 'No')], max_length=2)),
                ('semestre', models.IntegerField()),
                ('docente', models.ForeignKey(default=False, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ('codigo',),
            },
        ),
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tipo', models.TextField(blank=True, choices=[('admin', 'Administrador'), ('decano', 'Decano'), ('director', 'Director'), ('profesor', 'Profesor')], max_length=500)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Programa',
            fields=[
                ('codigo', models.CharField(max_length=10, primary_key=True, serialize=False)),
                ('nombre_programa', models.CharField(max_length=50)),
                ('escuela', models.CharField(max_length=40)),
                ('numero_semestres', models.IntegerField()),
                ('numero_creditos_graduacion', models.IntegerField()),
                ('director', models.ForeignKey(default=False, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ('codigo',),
            },
        ),
        migrations.AddField(
            model_name='curso',
            name='programa',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='appprincipal.Programa'),
        ),
    ]
