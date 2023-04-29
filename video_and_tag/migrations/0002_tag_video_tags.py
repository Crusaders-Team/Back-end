# Generated by Django 4.2 on 2023-04-29 16:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('video_and_tag', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
            ],
        ),
        migrations.AddField(
            model_name='video',
            name='tags',
            field=models.ManyToManyField(blank=True, to='video_and_tag.tag'),
        ),
    ]
