#coding:utf8
from models import ContactApp, TrendsApp, CaseApp, ContactItem, TrendItem, CaseItem, CaseClass, ProductApp, ProductClass, ProductItem
from django.contrib.contenttypes.models import ContentType
from tables import ContactTable, TrendsTable, CaseItemTable, CaseClassTable, ProductItemTable, ProductClassTable

class AppMgr(object):
    @classmethod
    def get_app_info(cls, app):
        if app.real_type == ContentType.objects.get_for_model(ContactApp):
            return ContactTable(ContactItem.objects.filter(contact=app))
        elif app.real_type == ContentType.objects.get_for_model(TrendsApp):
            return TrendsTable(TrendItem.objects.filter(trend=app))
        elif app.real_type == ContentType.objects.get_for_model(CaseApp):
            return (CaseItemTable(CaseItem.objects.filter(case_app=app)),
                CaseClassTable(CaseClass.objects.filter(case_app=app)))
        elif app.real_type == ContentType.objects.get_for_model(ProductApp):
            return (ProductItemTable(ProductItem.objects.filter(product_app=app)),
                ProductClassTable(ProductClass.objects.filter(product_app=app)))
    @classmethod
    def get_app_enable(cls, app):
        if app.real_type == ContentType.objects.get_for_model(ContactApp):
            return ContactApp.objects.filter(app_ptr_id=app.pk)[0].enable
        elif app.real_type == ContentType.objects.get_for_model(TrendsApp):
            return TrendsApp.objects.filter(app_ptr_id=app.pk)[0].enable
        elif app.real_type == ContentType.objects.get_for_model(CaseApp):
            return CaseApp.objects.filter(app_ptr_id=app.pk)[0].enable
        elif app.real_type == ContentType.objects.get_for_model(ProductApp):
            return ProductApp.objects.filter(app_ptr_id=app.pk)[0].enable
        
