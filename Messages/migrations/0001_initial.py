# Generated by Django 2.2.13 on 2020-10-05 19:12

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('contenttypes', '0002_remove_content_type_name'),
    ]

    operations = [
        migrations.CreateModel(
            name='ReplyMessage',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('msg', models.CharField(max_length=128, verbose_name='留言')),
                ('user', models.CharField(max_length=255, null=True, verbose_name='点赞用户ID')),
                ('platform', models.CharField(max_length=10, null=True, verbose_name='平台')),
                ('create_time', models.DateTimeField(auto_now_add=True, verbose_name='发布时间')),
                ('floor', models.PositiveIntegerField(default=1, editable=False, verbose_name='第几楼')),
                ('object_id', models.PositiveIntegerField()),
                ('is_delete', models.BooleanField(default=False, verbose_name='是否删除')),
                ('reply_user', models.CharField(max_length=255, null=True, verbose_name='点赞用户ID')),
                ('reply_platform', models.CharField(max_length=10, null=True, verbose_name='平台')),
                ('content_type', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='contenttypes.ContentType')),
            ],
            options={
                'verbose_name': '留言回复',
                'verbose_name_plural': '留言回复',
                'ordering': ['create_time'],
            },
        ),
        migrations.CreateModel(
            name='MainMessage',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('msg', models.CharField(max_length=128, verbose_name='留言')),
                ('user', models.CharField(max_length=255, null=True, verbose_name='点赞用户ID')),
                ('platform', models.CharField(max_length=10, null=True, verbose_name='平台')),
                ('create_time', models.DateTimeField(auto_now_add=True, verbose_name='发布时间')),
                ('floor', models.PositiveIntegerField(default=1, editable=False, verbose_name='第几楼')),
                ('object_id', models.PositiveIntegerField()),
                ('is_delete', models.BooleanField(default=False, verbose_name='是否删除')),
                ('content_type', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='contenttypes.ContentType')),
            ],
            options={
                'verbose_name': '留言',
                'verbose_name_plural': '留言',
                'ordering': ['create_time'],
            },
        ),
    ]
