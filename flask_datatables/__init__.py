from flask import Blueprint
from flask import render_template, Markup, g
from json import dumps


class Datatable(object):

    def __init__(self, *args, **kwargs):
        pass
    
    def render(self, *args, **kwargs):
        print('RENDERING')
        print(*args)
        print(*kwargs)
        return render_template(*args, **kwargs)

    @property
    def js(self):
        pa = 'datatables/datatables.html'
        print('render js')
        js = Markup(self.render(pa))
        print(js)
        return Markup(self.render(pa))

    @property
    def html(self):
        pa = 'datatables/datatables.html'

        print('render html')
        html = Markup(self.render(pa))
        print(html)
        return Markup(self.render(pa))


def googlemap_obj(*args, **kwargs):
    print('LOADING DATATABLE OBJECT')
    datatable = Datatable(*args, **kwargs)
    return datatable


def googlemap(*args, **kwargs):
    print('GOOGLE MAP?')
    datatable = googlemap_obj(*args, **kwargs)
    js = datatable.js
    html = datatable.html
    print(html)
    print(js)

    return Markup("".join((js, html)))


def googlemap_html(*args, **kwargs):
    print('HTML?')
    return googlemap_obj(*args, **kwargs).html


def googlemap_js(*args, **kwargs):
    print('JS?')
    return googlemap_obj(*args, **kwargs).js


def set_datatables_loaded():
    print("LOADED?")
    g.datatables_loaded = True
    return ''


def is_datatables_loaded():
    print("IS LOADED?")
    return getattr(g, 'datatables', False)


class FlaskDatatable(object):

    def __init__(self, app=None):
        print("INITIALIZING DATATABLES")
        if app is not None:
            self.init_app(app)

    def init_app(self, app):
        print('RESISTERING DATATABLES')
        self.register_blueprint(app)
        app.add_template_filter(googlemap_html)
        app.add_template_filter(googlemap_js)
        app.add_template_global(googlemap_obj)
        app.add_template_filter(googlemap)
        app.add_template_global(googlemap)
        # app.add_template_global(
        # app.config.get('GOOGLEMAPS_KEY'), name='GOOGLEMAPS_KEY')
        app.add_template_global(set_datatables_loaded)
        app.add_template_global(is_datatables_loaded)

    def register_blueprint(self, app):
        module = Blueprint("datatables", __name__, template_folder="templates")
        app.register_blueprint(module)
        print('REGISTERED DATATABLES')
        print(module)
        return module


