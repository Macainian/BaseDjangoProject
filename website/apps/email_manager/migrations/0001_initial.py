# -*- coding: utf-8 -*-
# Generated by Django 1.10.3 on 2017-01-02 09:15
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('staff_member_manager', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='DoNotSendEmailList',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_deleted', models.BooleanField(default=False)),
                ('creation_datetime', models.DateTimeField(auto_now_add=True)),
                ('last_modified_datetime', models.DateTimeField(auto_now=True)),
                ('deletion_datetime', models.DateTimeField(blank=True, null=True)),
                ('name', models.TextField(default=None, unique=True)),
                ('created_by', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='created_do_not_send_email_lists', to='staff_member_manager.StaffMember')),
                ('updated_by', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='updated_do_not_send_email_lists', to='staff_member_manager.StaffMember')),
            ],
            options={
                'db_table': 'do_not_send_email_list',
                'verbose_name': 'Do Not Send Email List',
                'verbose_name_plural': 'Do Not Send Email Lists',
            },
        ),
        migrations.CreateModel(
            name='DoNotSendEmailListItem',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_deleted', models.BooleanField(default=False)),
                ('creation_datetime', models.DateTimeField(auto_now_add=True)),
                ('last_modified_datetime', models.DateTimeField(auto_now=True)),
                ('deletion_datetime', models.DateTimeField(blank=True, null=True)),
                ('email', models.TextField(default=None, unique=True)),
                ('created_by', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='created_do_not_send_email_list_items', to='staff_member_manager.StaffMember')),
                ('list', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='email_items', to='email_manager.DoNotSendEmailList')),
                ('updated_by', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='updated_do_not_send_email_list_items', to='staff_member_manager.StaffMember')),
            ],
            options={
                'db_table': 'do_not_send_email_list_item',
                'verbose_name': 'Do Not Send Email List Item',
                'verbose_name_plural': 'Do Not Send Email List Items',
            },
        ),
        migrations.CreateModel(
            name='EmailBatch',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_deleted', models.BooleanField(default=False)),
                ('creation_datetime', models.DateTimeField(auto_now_add=True)),
                ('last_modified_datetime', models.DateTimeField(auto_now=True)),
                ('deletion_datetime', models.DateTimeField(blank=True, null=True)),
                ('created_by', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='created_email_batches', to='staff_member_manager.StaffMember')),
            ],
            options={
                'db_table': 'email_batch',
                'verbose_name': 'Email Batch',
                'verbose_name_plural': 'Email Batches',
            },
        ),
        migrations.CreateModel(
            name='EmailBatchStatus',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_deleted', models.BooleanField(default=False)),
                ('creation_datetime', models.DateTimeField(auto_now_add=True)),
                ('last_modified_datetime', models.DateTimeField(auto_now=True)),
                ('deletion_datetime', models.DateTimeField(blank=True, null=True)),
                ('name', models.TextField(default=None, unique=True)),
                ('created_by', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='created_email_batch_statuses', to='staff_member_manager.StaffMember')),
                ('updated_by', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='updated_email_batch_statuses', to='staff_member_manager.StaffMember')),
            ],
            options={
                'db_table': 'email_batch_status',
                'verbose_name': 'Email Batch Status',
                'verbose_name_plural': 'Email Batch Statuses',
            },
        ),
        migrations.CreateModel(
            name='EmailBatchTemplate',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_deleted', models.BooleanField(default=False)),
                ('creation_datetime', models.DateTimeField(auto_now_add=True)),
                ('last_modified_datetime', models.DateTimeField(auto_now=True)),
                ('deletion_datetime', models.DateTimeField(blank=True, null=True)),
                ('name', models.TextField(default=None, unique=True)),
                ('from_code', models.TextField(default=None)),
                ('subject_code', models.TextField(default=None)),
                ('basic_message', models.TextField(default=None)),
                ('html_code', models.TextField(default=None)),
                ('is_active', models.BooleanField(default=True)),
                ('created_by', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='created_email_batch_templates', to='staff_member_manager.StaffMember')),
                ('updated_by', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='updated_email_batch_templates', to='staff_member_manager.StaffMember')),
            ],
            options={
                'db_table': 'email_batch_template',
                'verbose_name': 'Email Batch Template',
                'verbose_name_plural': 'Email Batch Templates',
            },
        ),
        migrations.CreateModel(
            name='EmailBatchType',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_deleted', models.BooleanField(default=False)),
                ('creation_datetime', models.DateTimeField(auto_now_add=True)),
                ('last_modified_datetime', models.DateTimeField(auto_now=True)),
                ('deletion_datetime', models.DateTimeField(blank=True, null=True)),
                ('name', models.TextField(default=None, unique=True)),
                ('created_by', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='created_email_batch_types', to='staff_member_manager.StaffMember')),
                ('updated_by', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='updated_email_batch_types', to='staff_member_manager.StaffMember')),
            ],
            options={
                'db_table': 'email_batch_type',
                'verbose_name': 'Email Batch Type',
                'verbose_name_plural': 'Email Batch Types',
            },
        ),
        migrations.CreateModel(
            name='EmailInstance',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_deleted', models.BooleanField(default=False)),
                ('creation_datetime', models.DateTimeField(auto_now_add=True)),
                ('last_modified_datetime', models.DateTimeField(auto_now=True)),
                ('deletion_datetime', models.DateTimeField(blank=True, null=True)),
                ('recipient_email', models.TextField(default=None)),
                ('sent_datetime', models.DateTimeField(blank=True, null=True)),
                ('batch', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='email_instances', to='email_manager.EmailBatch')),
                ('created_by', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='created_email_instances', to='staff_member_manager.StaffMember')),
            ],
            options={
                'db_table': 'email_instance',
                'verbose_name': 'Email Instance',
                'verbose_name_plural': 'Email Instances',
            },
        ),
        migrations.CreateModel(
            name='EmailInstanceStatus',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_deleted', models.BooleanField(default=False)),
                ('creation_datetime', models.DateTimeField(auto_now_add=True)),
                ('last_modified_datetime', models.DateTimeField(auto_now=True)),
                ('deletion_datetime', models.DateTimeField(blank=True, null=True)),
                ('name', models.TextField(default=None, unique=True)),
                ('created_by', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='created_email_instance_statuses', to='staff_member_manager.StaffMember')),
                ('updated_by', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='updated_email_instance_statuses', to='staff_member_manager.StaffMember')),
            ],
            options={
                'db_table': 'email_instance_status',
                'verbose_name': 'Email Instance Status',
                'verbose_name_plural': 'Email Instance Statuses',
            },
        ),
        migrations.AddField(
            model_name='emailinstance',
            name='status',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='email_manager.EmailInstanceStatus'),
        ),
        migrations.AddField(
            model_name='emailinstance',
            name='updated_by',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='updated_email_instances', to='staff_member_manager.StaffMember'),
        ),
        migrations.AddField(
            model_name='emailbatch',
            name='status',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='email_manager.EmailBatchStatus'),
        ),
        migrations.AddField(
            model_name='emailbatch',
            name='template',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='email_manager.EmailBatchTemplate'),
        ),
        migrations.AddField(
            model_name='emailbatch',
            name='type',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='email_manager.EmailBatchType'),
        ),
        migrations.AddField(
            model_name='emailbatch',
            name='updated_by',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='updated_email_batches', to='staff_member_manager.StaffMember'),
        ),
    ]