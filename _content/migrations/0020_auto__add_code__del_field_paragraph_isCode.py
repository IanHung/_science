# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Code'
        db.create_table(u'_content_code', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('code', self.gf('django.db.models.fields.TextField')()),
            ('originalStructureNode', self.gf('mptt.fields.TreeForeignKey')(blank=True, related_name='original_code_content', null=True, to=orm['_content.StructureNode'])),
        ))
        db.send_create_signal(u'_content', ['Code'])

        # Deleting field 'Paragraph.isCode'
        db.delete_column(u'_content_paragraph', 'isCode')


    def backwards(self, orm):
        # Deleting model 'Code'
        db.delete_table(u'_content_code')

        # Adding field 'Paragraph.isCode'
        db.add_column(u'_content_paragraph', 'isCode',
                      self.gf('django.db.models.fields.BooleanField')(default=False),
                      keep_default=False)


    models = {
        u'_content.code': {
            'Meta': {'object_name': 'Code'},
            'code': ('django.db.models.fields.TextField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'originalStructureNode': ('mptt.fields.TreeForeignKey', [], {'blank': 'True', 'related_name': "'original_code_content'", 'null': 'True', 'to': u"orm['_content.StructureNode']"})
        },
        u'_content.dataset': {
            'Meta': {'object_name': 'Dataset'},
            'caption': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'data': ('jsonfield.fields.JSONField', [], {'null': 'True', 'blank': 'True'}),
            'dataFile': ('django.db.models.fields.files.FileField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'originalStructureNode': ('mptt.fields.TreeForeignKey', [], {'blank': 'True', 'related_name': "'original_dataset_content'", 'null': 'True', 'to': u"orm['_content.StructureNode']"})
        },
        u'_content.image': {
            'Meta': {'object_name': 'Image'},
            'caption': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'linkSource': ('django.db.models.fields.URLField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'localSource': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'originalStructureNode': ('mptt.fields.TreeForeignKey', [], {'blank': 'True', 'related_name': "'original_image_content'", 'null': 'True', 'to': u"orm['_content.StructureNode']"})
        },
        u'_content.paragraph': {
            'Meta': {'object_name': 'Paragraph'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'originalStructureNode': ('mptt.fields.TreeForeignKey', [], {'blank': 'True', 'related_name': "'original_paragraph_content'", 'null': 'True', 'to': u"orm['_content.StructureNode']"}),
            'text': ('django.db.models.fields.TextField', [], {})
        },
        u'_content.rating': {
            'Meta': {'object_name': 'Rating'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'rating': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'structureNode': ('mptt.fields.TreeOneToOneField', [], {'to': u"orm['_content.StructureNode']", 'unique': 'True'})
        },
        u'_content.structurenode': {
            'Meta': {'object_name': 'StructureNode'},
            'author': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.User']", 'null': 'True', 'blank': 'True'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['contenttypes.ContentType']", 'null': 'True', 'blank': 'True'}),
            'end': ('django.db.models.fields.PositiveIntegerField', [], {'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'isComment': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'isDraft': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'isLabnote': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'isPublished': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'isUpdate': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            u'lft': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            'mptt_level': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            'object_id': ('django.db.models.fields.PositiveIntegerField', [], {'null': 'True', 'blank': 'True'}),
            'parent': ('mptt.fields.TreeForeignKey', [], {'blank': 'True', 'related_name': "'children'", 'null': 'True', 'to': u"orm['_content.StructureNode']"}),
            'position': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'pubDate': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            u'rght': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '200', 'blank': 'True'}),
            'start': ('django.db.models.fields.PositiveIntegerField', [], {'null': 'True', 'blank': 'True'}),
            'subscribedUser': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'related_name': "'subscribedArticles'", 'null': 'True', 'symmetrical': 'False', 'to': u"orm['auth.User']"}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            u'tree_id': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            'url': ('django.db.models.fields.URLField', [], {'unique': 'True', 'max_length': '255', 'blank': 'True'})
        },
        u'_content.tag': {
            'Meta': {'object_name': 'Tag'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'nodes': ('mptt.fields.TreeManyToManyField', [], {'to': u"orm['_content.StructureNode']", 'symmetrical': 'False'})
        },
        u'_content.timelike': {
            'Meta': {'object_name': 'Timelike'},
            'caption': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'linkSource': ('django.db.models.fields.URLField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'localSource': ('django.db.models.fields.files.FileField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'originalStructureNode': ('mptt.fields.TreeForeignKey', [], {'blank': 'True', 'related_name': "'original_timelike_content'", 'null': 'True', 'to': u"orm['_content.StructureNode']"})
        },
        u'_content.usersfollowingrelation': {
            'Meta': {'object_name': 'UsersFollowingRelation'},
            'following': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'followers'", 'symmetrical': 'False', 'to': u"orm['auth.User']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'primaryUser': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['auth.User']", 'unique': 'True'})
        },
        u'_content.viewcount': {
            'Meta': {'object_name': 'ViewCount'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'structureNode': ('mptt.fields.TreeOneToOneField', [], {'to': u"orm['_content.StructureNode']", 'unique': 'True'}),
            'viewCount': ('django.db.models.fields.PositiveIntegerField', [], {})
        },
        u'auth.group': {
            'Meta': {'object_name': 'Group'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        u'auth.permission': {
            'Meta': {'ordering': "(u'content_type__app_label', u'content_type__model', u'codename')", 'unique_together': "((u'content_type', u'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['contenttypes.ContentType']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        u'auth.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Group']", 'symmetrical': 'False', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        u'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        }
    }

    complete_apps = ['_content']