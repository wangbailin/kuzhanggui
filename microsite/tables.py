from models import HomePage

class HomePageTable(tables.Table):
    class Meta:
        model = HomePage
        attrs = {'class' : 'table table-striped'}
        orderable = False
