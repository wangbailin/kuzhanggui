# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Page'
        db.create_table('page', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('enable', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('real_type', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['contenttypes.ContentType'])),
            ('wx', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['framework.WXAccount'])),
            ('tab_name', self.gf('django.db.models.fields.CharField')(max_length=20)),
            ('template_name', self.gf('django.db.models.fields.CharField')(max_length=260)),
            ('icon', self.gf('django.db.models.fields.files.ImageField')(max_length=255, blank=True)),
            ('message_cover', self.gf('django.db.models.fields.files.ImageField')(max_length=255, blank=True)),
            ('message_description', self.gf('django.db.models.fields.TextField')(max_length=1000, blank=True)),
            ('position', self.gf('django.db.models.fields.IntegerField')(default=0)),
        ))
        db.send_create_signal('microsite', ['Page'])

        # Adding model 'App'
        db.create_table('app', (
            (u'page_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['microsite.Page'], unique=True, primary_key=True)),
            ('app_template_name', self.gf('django.db.models.fields.CharField')(max_length=260)),
        ))
        db.send_create_signal('microsite', ['App'])

        # Adding model 'HomePage'
        db.create_table(u'homepage', (
            (u'page_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['microsite.Page'], unique=True, primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('template_type', self.gf('django.db.models.fields.IntegerField')(default=1)),
            ('pic1', self.gf('django.db.models.fields.files.ImageField')(max_length=255)),
            ('exp1', self.gf('django.db.models.fields.CharField')(max_length=255, blank=True)),
            ('pic2', self.gf('django.db.models.fields.files.ImageField')(max_length=255, blank=True)),
            ('exp2', self.gf('django.db.models.fields.CharField')(max_length=255, blank=True)),
            ('pic3', self.gf('django.db.models.fields.files.ImageField')(max_length=255, blank=True)),
            ('exp3', self.gf('django.db.models.fields.CharField')(max_length=255, blank=True)),
            ('pic4', self.gf('django.db.models.fields.files.ImageField')(max_length=255, blank=True)),
            ('exp4', self.gf('django.db.models.fields.CharField')(max_length=255, blank=True)),
        ))
        db.send_create_signal(u'microsite', ['HomePage'])

        # Adding model 'IntroPage'
        db.create_table(u'intropage', (
            (u'page_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['microsite.Page'], unique=True, primary_key=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('content', self.gf('django.db.models.fields.TextField')(blank=True)),
        ))
        db.send_create_signal(u'microsite', ['IntroPage'])

        # Adding model 'JoinPage'
        db.create_table(u'joinpage', (
            (u'page_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['microsite.Page'], unique=True, primary_key=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('content', self.gf('django.db.models.fields.TextField')(blank=True)),
        ))
        db.send_create_signal(u'microsite', ['JoinPage'])

        # Adding model 'ContactApp'
        db.create_table(u'contactapp', (
            (u'app_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['microsite.App'], unique=True, primary_key=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=50)),
        ))
        db.send_create_signal(u'microsite', ['ContactApp'])

        # Adding model 'TrendsApp'
        db.create_table(u'trendsapp', (
            (u'app_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['microsite.App'], unique=True, primary_key=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=50)),
        ))
        db.send_create_signal(u'microsite', ['TrendsApp'])

        # Adding model 'TeamApp'
        db.create_table(u'teamapp', (
            (u'app_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['microsite.App'], unique=True, primary_key=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=50)),
        ))
        db.send_create_signal(u'microsite', ['TeamApp'])

        # Adding model 'CaseApp'
        db.create_table(u'case_app', (
            (u'app_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['microsite.App'], unique=True, primary_key=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=20)),
        ))
        db.send_create_signal(u'microsite', ['CaseApp'])

        # Adding model 'CaseClass'
        db.create_table(u'case_class', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('case_app', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['microsite.CaseApp'])),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=20)),
            ('pub_time', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
        ))
        db.send_create_signal(u'microsite', ['CaseClass'])

        # Adding model 'CaseItem'
        db.create_table(u'case_item', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('case_app', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['microsite.CaseApp'])),
            ('cls', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['microsite.CaseClass'], null=True, blank=True)),
            ('pub_time', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('case_pic1', self.gf('django.db.models.fields.files.ImageField')(max_length=255, blank=True)),
            ('case_pic2', self.gf('django.db.models.fields.files.ImageField')(max_length=255, blank=True)),
            ('case_pic3', self.gf('django.db.models.fields.files.ImageField')(max_length=255, blank=True)),
            ('case_pic4', self.gf('django.db.models.fields.files.ImageField')(max_length=255, blank=True)),
            ('case_intro', self.gf('django.db.models.fields.TextField')()),
        ))
        db.send_create_signal(u'microsite', ['CaseItem'])

        # Adding model 'ProductApp'
        db.create_table(u'product_app', (
            (u'app_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['microsite.App'], unique=True, primary_key=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=20)),
        ))
        db.send_create_signal(u'microsite', ['ProductApp'])

        # Adding model 'ProductClass'
        db.create_table(u'product_class', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('product_app', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['microsite.ProductApp'])),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=20)),
            ('pub_time', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
        ))
        db.send_create_signal(u'microsite', ['ProductClass'])

        # Adding model 'ProductItem'
        db.create_table(u'product_item', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('product_app', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['microsite.ProductApp'])),
            ('cls', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['microsite.ProductClass'], null=True, blank=True)),
            ('pub_time', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('product_pic1', self.gf('django.db.models.fields.files.ImageField')(max_length=255, blank=True)),
            ('product_pic2', self.gf('django.db.models.fields.files.ImageField')(max_length=255, blank=True)),
            ('product_pic3', self.gf('django.db.models.fields.files.ImageField')(max_length=255, blank=True)),
            ('product_pic4', self.gf('django.db.models.fields.files.ImageField')(max_length=255, blank=True)),
            ('product_intro', self.gf('django.db.models.fields.TextField')()),
        ))
        db.send_create_signal(u'microsite', ['ProductItem'])

        # Adding model 'TrendItem'
        db.create_table(u'trend_item', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('trend', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['microsite.TrendsApp'])),
            ('pub_time', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('content', self.gf('django.db.models.fields.TextField')()),
            ('cover', self.gf('django.db.models.fields.files.ImageField')(max_length=255, blank=True)),
            ('summary', self.gf('django.db.models.fields.CharField')(max_length=255, blank=True)),
        ))
        db.send_create_signal(u'microsite', ['TrendItem'])

        # Adding model 'TeamItem'
        db.create_table(u'team_item', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('team', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['microsite.TeamApp'])),
            ('pub_time', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('job_title', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('picture', self.gf('django.db.models.fields.files.ImageField')(max_length=255)),
            ('person_digest', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('person_content', self.gf('django.db.models.fields.TextField')()),
        ))
        db.send_create_signal(u'microsite', ['TeamItem'])

        # Adding model 'ContactItem'
        db.create_table(u'contact_item', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('contact', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['microsite.ContactApp'])),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('lat', self.gf('django.db.models.fields.FloatField')()),
            ('lng', self.gf('django.db.models.fields.FloatField')()),
            ('address', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('mail_code', self.gf('django.db.models.fields.CharField')(max_length=20, blank=True)),
            ('fax_code', self.gf('django.db.models.fields.CharField')(max_length=30, blank=True)),
        ))
        db.send_create_signal(u'microsite', ['ContactItem'])

        # Adding model 'ContactPeople'
        db.create_table(u'contact_people', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('contact_item', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['microsite.ContactItem'])),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=10)),
            ('email', self.gf('django.db.models.fields.CharField')(max_length=50, blank=True)),
            ('phone', self.gf('django.db.models.fields.CharField')(max_length=20)),
            ('qq', self.gf('django.db.models.fields.CharField')(max_length=20, blank=True)),
        ))
        db.send_create_signal(u'microsite', ['ContactPeople'])

        # Adding model 'CulturePage'
        db.create_table(u'culture', (
            (u'page_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['microsite.Page'], unique=True, primary_key=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('content', self.gf('django.db.models.fields.TextField')(blank=True)),
        ))
        db.send_create_signal(u'microsite', ['CulturePage'])

        # Adding model 'BusinessPage'
        db.create_table(u'business', (
            (u'page_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['microsite.Page'], unique=True, primary_key=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('content', self.gf('django.db.models.fields.TextField')(blank=True)),
        ))
        db.send_create_signal(u'microsite', ['BusinessPage'])

        # Adding model 'WeiboPage'
        db.create_table(u'official_weibo', (
            (u'page_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['microsite.Page'], unique=True, primary_key=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('url', self.gf('django.db.models.fields.URLField')(max_length=100)),
        ))
        db.send_create_signal(u'microsite', ['WeiboPage'])

        # Adding model 'ContentPage'
        db.create_table(u'content_page', (
            (u'page_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['microsite.Page'], unique=True, primary_key=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('content', self.gf('django.db.models.fields.TextField')(blank=True)),
        ))
        db.send_create_signal(u'microsite', ['ContentPage'])

        # Adding model 'LinkPage'
        db.create_table(u'link_page', (
            (u'page_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['microsite.Page'], unique=True, primary_key=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('url', self.gf('django.db.models.fields.URLField')(max_length=200)),
        ))
        db.send_create_signal(u'microsite', ['LinkPage'])

        # Adding model 'HelpPage'
        db.create_table(u'helppage', (
            (u'page_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['microsite.Page'], unique=True, primary_key=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('content', self.gf('django.db.models.fields.TextField')(blank=True)),
        ))
        db.send_create_signal(u'microsite', ['HelpPage'])

        # Adding model 'Menu'
        db.create_table(u'menus', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('wx', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['framework.WXAccount'])),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=4)),
        ))
        db.send_create_signal(u'microsite', ['Menu'])

        # Adding model 'PageGroup'
        db.create_table(u'menus_pages', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('menu', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['microsite.Menu'])),
            ('page', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['microsite.Page'])),
            ('position', self.gf('django.db.models.fields.IntegerField')(default=0)),
        ))
        db.send_create_signal(u'microsite', ['PageGroup'])


    def backwards(self, orm):
        # Deleting model 'Page'
        db.delete_table('page')

        # Deleting model 'App'
        db.delete_table('app')

        # Deleting model 'HomePage'
        db.delete_table(u'homepage')

        # Deleting model 'IntroPage'
        db.delete_table(u'intropage')

        # Deleting model 'JoinPage'
        db.delete_table(u'joinpage')

        # Deleting model 'ContactApp'
        db.delete_table(u'contactapp')

        # Deleting model 'TrendsApp'
        db.delete_table(u'trendsapp')

        # Deleting model 'TeamApp'
        db.delete_table(u'teamapp')

        # Deleting model 'CaseApp'
        db.delete_table(u'case_app')

        # Deleting model 'CaseClass'
        db.delete_table(u'case_class')

        # Deleting model 'CaseItem'
        db.delete_table(u'case_item')

        # Deleting model 'ProductApp'
        db.delete_table(u'product_app')

        # Deleting model 'ProductClass'
        db.delete_table(u'product_class')

        # Deleting model 'ProductItem'
        db.delete_table(u'product_item')

        # Deleting model 'TrendItem'
        db.delete_table(u'trend_item')

        # Deleting model 'TeamItem'
        db.delete_table(u'team_item')

        # Deleting model 'ContactItem'
        db.delete_table(u'contact_item')

        # Deleting model 'ContactPeople'
        db.delete_table(u'contact_people')

        # Deleting model 'CulturePage'
        db.delete_table(u'culture')

        # Deleting model 'BusinessPage'
        db.delete_table(u'business')

        # Deleting model 'WeiboPage'
        db.delete_table(u'official_weibo')

        # Deleting model 'ContentPage'
        db.delete_table(u'content_page')

        # Deleting model 'LinkPage'
        db.delete_table(u'link_page')

        # Deleting model 'HelpPage'
        db.delete_table(u'helppage')

        # Deleting model 'Menu'
        db.delete_table(u'menus')

        # Deleting model 'PageGroup'
        db.delete_table(u'menus_pages')


    models = {
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
        },
        u'framework.account': {
            'Meta': {'object_name': 'Account', 'db_table': "u'account'"},
            'expired_time': ('django.db.models.fields.DateTimeField', [], {}),
            'has_wx_bound': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_expired': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'phone': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'qq': ('django.db.models.fields.CharField', [], {'max_length': '20', 'null': 'True', 'blank': 'True'}),
            'user': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['auth.User']", 'unique': 'True'})
        },
        u'framework.wxaccount': {
            'Meta': {'object_name': 'WXAccount', 'db_table': "u'wx_account'"},
            'account': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['framework.Account']"}),
            'app_id': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'app_secret': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'avatar': ('django.db.models.fields.files.ImageField', [], {'max_length': '255', 'blank': 'True'}),
            'bind_time': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'follower_count': ('django.db.models.fields.IntegerField', [], {'default': '0', 'max_length': '11'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'message_count': ('django.db.models.fields.IntegerField', [], {'default': '0', 'max_length': '11'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '20', 'null': 'True', 'blank': 'True'}),
            'state': ('django.db.models.fields.IntegerField', [], {'default': '1', 'max_length': '2'}),
            'token': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'url': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'username': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'wsite_template': ('django.db.models.fields.IntegerField', [], {'default': '1'}),
            'wxid': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'})
        },
        'microsite.app': {
            'Meta': {'object_name': 'App', 'db_table': "'app'", '_ormbases': ['microsite.Page']},
            'app_template_name': ('django.db.models.fields.CharField', [], {'max_length': '260'}),
            u'page_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['microsite.Page']", 'unique': 'True', 'primary_key': 'True'})
        },
        u'microsite.businesspage': {
            'Meta': {'object_name': 'BusinessPage', 'db_table': "u'business'", '_ormbases': ['microsite.Page']},
            'content': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            u'page_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['microsite.Page']", 'unique': 'True', 'primary_key': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        u'microsite.caseapp': {
            'Meta': {'object_name': 'CaseApp', 'db_table': "u'case_app'", '_ormbases': ['microsite.App']},
            u'app_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['microsite.App']", 'unique': 'True', 'primary_key': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '20'})
        },
        u'microsite.caseclass': {
            'Meta': {'object_name': 'CaseClass', 'db_table': "u'case_class'"},
            'case_app': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['microsite.CaseApp']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'pub_time': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'})
        },
        u'microsite.caseitem': {
            'Meta': {'object_name': 'CaseItem', 'db_table': "u'case_item'"},
            'case_app': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['microsite.CaseApp']"}),
            'case_intro': ('django.db.models.fields.TextField', [], {}),
            'case_pic1': ('django.db.models.fields.files.ImageField', [], {'max_length': '255', 'blank': 'True'}),
            'case_pic2': ('django.db.models.fields.files.ImageField', [], {'max_length': '255', 'blank': 'True'}),
            'case_pic3': ('django.db.models.fields.files.ImageField', [], {'max_length': '255', 'blank': 'True'}),
            'case_pic4': ('django.db.models.fields.files.ImageField', [], {'max_length': '255', 'blank': 'True'}),
            'cls': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['microsite.CaseClass']", 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'pub_time': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        u'microsite.contactapp': {
            'Meta': {'object_name': 'ContactApp', 'db_table': "u'contactapp'", '_ormbases': ['microsite.App']},
            u'app_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['microsite.App']", 'unique': 'True', 'primary_key': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        u'microsite.contactitem': {
            'Meta': {'object_name': 'ContactItem', 'db_table': "u'contact_item'"},
            'address': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'contact': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['microsite.ContactApp']"}),
            'fax_code': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'lat': ('django.db.models.fields.FloatField', [], {}),
            'lng': ('django.db.models.fields.FloatField', [], {}),
            'mail_code': ('django.db.models.fields.CharField', [], {'max_length': '20', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        u'microsite.contactpeople': {
            'Meta': {'object_name': 'ContactPeople', 'db_table': "u'contact_people'"},
            'contact_item': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['microsite.ContactItem']"}),
            'email': ('django.db.models.fields.CharField', [], {'max_length': '50', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '10'}),
            'phone': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'qq': ('django.db.models.fields.CharField', [], {'max_length': '20', 'blank': 'True'})
        },
        u'microsite.contentpage': {
            'Meta': {'object_name': 'ContentPage', 'db_table': "u'content_page'", '_ormbases': ['microsite.Page']},
            'content': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            u'page_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['microsite.Page']", 'unique': 'True', 'primary_key': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        u'microsite.culturepage': {
            'Meta': {'object_name': 'CulturePage', 'db_table': "u'culture'", '_ormbases': ['microsite.Page']},
            'content': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            u'page_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['microsite.Page']", 'unique': 'True', 'primary_key': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        u'microsite.helppage': {
            'Meta': {'object_name': 'HelpPage', 'db_table': "u'helppage'", '_ormbases': ['microsite.Page']},
            'content': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            u'page_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['microsite.Page']", 'unique': 'True', 'primary_key': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        u'microsite.homepage': {
            'Meta': {'object_name': 'HomePage', 'db_table': "u'homepage'", '_ormbases': ['microsite.Page']},
            'exp1': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'exp2': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'exp3': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'exp4': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            u'page_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['microsite.Page']", 'unique': 'True', 'primary_key': 'True'}),
            'pic1': ('django.db.models.fields.files.ImageField', [], {'max_length': '255'}),
            'pic2': ('django.db.models.fields.files.ImageField', [], {'max_length': '255', 'blank': 'True'}),
            'pic3': ('django.db.models.fields.files.ImageField', [], {'max_length': '255', 'blank': 'True'}),
            'pic4': ('django.db.models.fields.files.ImageField', [], {'max_length': '255', 'blank': 'True'}),
            'template_type': ('django.db.models.fields.IntegerField', [], {'default': '1'})
        },
        u'microsite.intropage': {
            'Meta': {'object_name': 'IntroPage', 'db_table': "u'intropage'", '_ormbases': ['microsite.Page']},
            'content': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            u'page_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['microsite.Page']", 'unique': 'True', 'primary_key': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        u'microsite.joinpage': {
            'Meta': {'object_name': 'JoinPage', 'db_table': "u'joinpage'", '_ormbases': ['microsite.Page']},
            'content': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            u'page_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['microsite.Page']", 'unique': 'True', 'primary_key': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        u'microsite.linkpage': {
            'Meta': {'object_name': 'LinkPage', 'db_table': "u'link_page'", '_ormbases': ['microsite.Page']},
            u'page_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['microsite.Page']", 'unique': 'True', 'primary_key': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'url': ('django.db.models.fields.URLField', [], {'max_length': '200'})
        },
        u'microsite.menu': {
            'Meta': {'object_name': 'Menu', 'db_table': "u'menus'"},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '4'}),
            'wx': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['framework.WXAccount']"})
        },
        'microsite.page': {
            'Meta': {'object_name': 'Page', 'db_table': "'page'"},
            'enable': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'icon': ('django.db.models.fields.files.ImageField', [], {'max_length': '255', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'message_cover': ('django.db.models.fields.files.ImageField', [], {'max_length': '255', 'blank': 'True'}),
            'message_description': ('django.db.models.fields.TextField', [], {'max_length': '1000', 'blank': 'True'}),
            'position': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'real_type': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['contenttypes.ContentType']"}),
            'tab_name': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'template_name': ('django.db.models.fields.CharField', [], {'max_length': '260'}),
            'wx': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['framework.WXAccount']"})
        },
        u'microsite.pagegroup': {
            'Meta': {'object_name': 'PageGroup', 'db_table': "u'menus_pages'"},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'menu': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['microsite.Menu']"}),
            'page': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['microsite.Page']"}),
            'position': ('django.db.models.fields.IntegerField', [], {'default': '0'})
        },
        u'microsite.productapp': {
            'Meta': {'object_name': 'ProductApp', 'db_table': "u'product_app'", '_ormbases': ['microsite.App']},
            u'app_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['microsite.App']", 'unique': 'True', 'primary_key': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '20'})
        },
        u'microsite.productclass': {
            'Meta': {'object_name': 'ProductClass', 'db_table': "u'product_class'"},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'product_app': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['microsite.ProductApp']"}),
            'pub_time': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'})
        },
        u'microsite.productitem': {
            'Meta': {'object_name': 'ProductItem', 'db_table': "u'product_item'"},
            'cls': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['microsite.ProductClass']", 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'product_app': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['microsite.ProductApp']"}),
            'product_intro': ('django.db.models.fields.TextField', [], {}),
            'product_pic1': ('django.db.models.fields.files.ImageField', [], {'max_length': '255', 'blank': 'True'}),
            'product_pic2': ('django.db.models.fields.files.ImageField', [], {'max_length': '255', 'blank': 'True'}),
            'product_pic3': ('django.db.models.fields.files.ImageField', [], {'max_length': '255', 'blank': 'True'}),
            'product_pic4': ('django.db.models.fields.files.ImageField', [], {'max_length': '255', 'blank': 'True'}),
            'pub_time': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        u'microsite.teamapp': {
            'Meta': {'object_name': 'TeamApp', 'db_table': "u'teamapp'", '_ormbases': ['microsite.App']},
            u'app_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['microsite.App']", 'unique': 'True', 'primary_key': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        u'microsite.teamitem': {
            'Meta': {'object_name': 'TeamItem', 'db_table': "u'team_item'"},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'job_title': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'person_content': ('django.db.models.fields.TextField', [], {}),
            'person_digest': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'picture': ('django.db.models.fields.files.ImageField', [], {'max_length': '255'}),
            'pub_time': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'team': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['microsite.TeamApp']"})
        },
        u'microsite.trenditem': {
            'Meta': {'object_name': 'TrendItem', 'db_table': "u'trend_item'"},
            'content': ('django.db.models.fields.TextField', [], {}),
            'cover': ('django.db.models.fields.files.ImageField', [], {'max_length': '255', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'pub_time': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'summary': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'trend': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['microsite.TrendsApp']"})
        },
        u'microsite.trendsapp': {
            'Meta': {'object_name': 'TrendsApp', 'db_table': "u'trendsapp'", '_ormbases': ['microsite.App']},
            u'app_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['microsite.App']", 'unique': 'True', 'primary_key': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        u'microsite.weibopage': {
            'Meta': {'object_name': 'WeiboPage', 'db_table': "u'official_weibo'", '_ormbases': ['microsite.Page']},
            u'page_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['microsite.Page']", 'unique': 'True', 'primary_key': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'url': ('django.db.models.fields.URLField', [], {'max_length': '100'})
        }
    }

    complete_apps = ['microsite']