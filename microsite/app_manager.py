#coding:utf8
from models import ContactApp, JoinApp, TrendsApp, TeamApp, CaseApp, ContactItem, JoinItem, TrendItem, TeamItem, CaseItem, CaseClass, ProductApp, ProductClass, ProductItem, ContactPeople
from django.contrib.contenttypes.models import ContentType
from tables import ContactTable, ContactPeopleTable, JoinTable, TrendsTable, TeamTable, CaseItemTable, CaseClassTable, ProductItemTable, ProductClassTable

class AppMgr(object):
    @classmethod
    def get_app_info(cls, app):
        if app.real_type == ContentType.objects.get_for_model(ContactApp):
            items = ContactItem.objects.filter(contact=app)
            peoples = []
            for item in items:
                peoples.extend(ContactPeople.objects.filter(contact_item=item))
            return (ContactTable(items, prefix='ct-'), ContactPeopleTable(peoples, prefix='cp-'))
        elif app.real_type == ContentType.objects.get_for_model(TrendsApp):
            return TrendsTable(TrendItem.objects.filter(trend=app), prefix='ti-')
        elif app.real_type == ContentType.objects.get_for_model(JoinApp):
            return JoinTable(JoinItem.objects.filter(join=app), prefix='ji-')
        elif app.real_type == ContentType.objects.get_for_model(TeamApp):
            return TeamTable(TeamItem.objects.filter(team=app), prefix='tt-')
        elif app.real_type == ContentType.objects.get_for_model(CaseApp):
            return (CaseItemTable(CaseItem.objects.filter(case_app=app), prefix='ci-'),
                CaseClassTable(CaseClass.objects.filter(case_app=app)))
        elif app.real_type == ContentType.objects.get_for_model(ProductApp):
            return (ProductItemTable(ProductItem.objects.filter(product_app=app),prefix='pi-'),
                ProductClassTable(ProductClass.objects.filter(product_app=app)))
    @classmethod
    def get_app_enable(cls, app):
        if app.real_type == ContentType.objects.get_for_model(ContactApp):
            return ContactApp.objects.filter(app_ptr_id=app.pk)[0]
        elif app.real_type == ContentType.objects.get_for_model(TrendsApp):
            return TrendsApp.objects.filter(app_ptr_id=app.pk)[0]
        elif app.real_type == ContentType.objects.get_for_model(JoinApp):
            return JoinApp.objects.filter(app_ptr_id=app.pk)[0]
        elif app.real_type == ContentType.objects.get_for_model(CaseApp):
            return CaseApp.objects.filter(app_ptr_id=app.pk)[0]
        elif app.real_type == ContentType.objects.get_for_model(ProductApp):
            return ProductApp.objects.filter(app_ptr_id=app.pk)[0]
        elif app.real_type == ContentType.objects.get_for_model(TeamApp):
            return TeamApp.objects.filter(app_ptr_id=app.pk)[0]

