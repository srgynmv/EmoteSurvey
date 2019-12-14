# Generated by Django 2.2.7 on 2019-12-14 14:15

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Answer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.CharField(max_length=300)),
            ],
        ),
        migrations.CreateModel(
            name='Question',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type', models.IntegerField(choices=[(0, 'Single'), (1, 'Multiple'), (2, 'Text')])),
                ('text', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='Session',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
        ),
        migrations.CreateModel(
            name='Survey',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Result',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('answers', models.ManyToManyField(to='survey.Answer')),
                ('question', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='survey.Question')),
                ('session', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='survey.Session')),
            ],
        ),
        migrations.CreateModel(
            name='RecordedData',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('timestamp', models.TimeField()),
                ('surprise', models.FloatField()),
                ('fear', models.FloatField()),
                ('happiness', models.FloatField()),
                ('anger', models.FloatField()),
                ('disgust', models.FloatField()),
                ('sadness', models.FloatField()),
                ('neutral', models.FloatField()),
                ('result', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='recorded_data_set', to='survey.Result')),
            ],
        ),
        migrations.AddField(
            model_name='question',
            name='survey',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='survey.Survey'),
        ),
        migrations.AddField(
            model_name='answer',
            name='question',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='answers', to='survey.Question'),
        ),
    ]
