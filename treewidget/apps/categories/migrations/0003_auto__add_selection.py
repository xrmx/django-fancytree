# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Selection'
        db.create_table(u'categories_selection', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=50)),
        ))
        db.send_create_signal(u'categories', ['Selection'])

        # Adding M2M table for field categories on 'Selection'
        m2m_table_name = db.shorten_name(u'categories_selection_categories')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('selection', models.ForeignKey(orm[u'categories.selection'], null=False)),
            ('category', models.ForeignKey(orm[u'categories.category'], null=False))
        ))
        db.create_unique(m2m_table_name, ['selection_id', 'category_id'])


    def backwards(self, orm):
        # Deleting model 'Selection'
        db.delete_table(u'categories_selection')

        # Removing M2M table for field categories on 'Selection'
        db.delete_table(db.shorten_name(u'categories_selection_categories'))


    models = {
        u'categories.category': {
            'Meta': {'ordering': "('tree_id', 'lft')", 'unique_together': "(('name', 'slug', 'parent'),)", 'object_name': 'Category'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            u'level': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            u'lft': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'parent': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'children'", 'null': 'True', 'to': u"orm['categories.Category']"}),
            u'rght': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            'slug': ('django_extensions.db.fields.AutoSlugField', [], {'allow_duplicates': 'False', 'max_length': '50', 'separator': "u'-'", 'blank': 'True', 'populate_from': "'name'", 'overwrite': 'True'}),
            u'tree_id': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            'url': ('django.db.models.fields.TextField', [], {})
        },
        u'categories.selection': {
            'Meta': {'object_name': 'Selection'},
            'categories': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['categories.Category']", 'symmetrical': 'False'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        }
    }

    complete_apps = ['categories']