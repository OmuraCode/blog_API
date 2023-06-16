# Generated by Django 4.2.2 on 2023-06-13 12:46

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='PostImage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(blank=True, max_length=100, null=True)),
                ('image', models.ImageField(upload_to='images/')),
                ('post', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='Images', to='posts.post')),
            ],
        ),
    ]
