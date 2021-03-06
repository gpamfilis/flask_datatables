import json

from flask import render_template
from flask import request, jsonify
from flask.views import MethodView


def row2dict(row, column_names=None):
    """Given a row, it returns a dict."""
    if column_names is None:
        d = {}
        for column in row.__table__.columns:
            d[column.name] = getattr(row, column.name)
        return d
    else:
        d = {}
        for column in row.__table__.columns:
            if column.name in column_names:
                d[column.name] = getattr(row, column.name)
        return d


def model_crud(session, model, form_values, form_keys, primary_key=None, primary_key_val=None, item_id=None):
    """
    This method handles the insertion of data into the database model.

    TODO add fields example and params
        model_crud(db.session, MenuItem, fields, params, item_id)

    """
    print(primary_key, primary_key_val)
    print('model crude')
    # if the item_id is not None that means that we are about to update an entry in the database.

    if item_id is not None:
        print('Item Exists Therefore PUT')
        item = model.query.get(item_id)
    # We are about to create an entry in the database.
    else:
        print('New ITem')
        item = model()
    formated_form_values = []
    for form_value in form_values:
        if (not form_value) | (form_value is None):
            form_value = None
        formated_form_values.append(form_value)
    # check and see if all the fields are None in the processed fields.
    if all(cd is None for cd in formated_form_values):
        pass
    else:
        # set the param value equal to the values of the cleaned data.
        for p, key in enumerate(form_keys):
            set_foo(item, key, formated_form_values[p])
        if primary_key is not None:
            set_foo(item, primary_key, primary_key_val)
        # todo try except for a rollback.
        # since the item_id is not None we commit the update
        if item_id is not None:
            session.commit()
        # since the item_id is None we will add a new item to the database.
        else:
            session.add(item)
            session.commit()


def render_table(session, model, template_location='main/email.html', argument_name='item_id', model_name='email',
                 model_name2=None,
                 page_name="Budget Data Collection", params=['first_name', 'last_name', 'email', 'token'],
                 exclude=['token'], modal_info=None, item_id=None, primary_key=None, primary_key_val=None,
                 datatables_fields=None):
    print('RENDER TABLE')
    form_params = [p for p in params if p not in exclude]
    da = model.modal_info()
    primary_key = da['primary_key']
    primary_key_val = da['primary_key_val']
    if request.method == 'POST':  # this block is only entered when the form is submitted
        print('post request')
        fields = []
        for param in form_params:
            field = request.form.get(param, None)
            print(field)
            fields.append(field)
        print('item_id', item_id)
        model_crud(session, model, fields, form_params, item_id=item_id, primary_key=primary_key,
                   primary_key_val=primary_key_val)
    fields = params[:]
    fields.insert(0, 'id')
    print(params)
    params_jso = json.dumps(form_params)
    return render_template(template_location, headers=fields, name=page_name, model=model_name, model_name2=model_name2,
                           params=params_jso, **model.modal_info())  # json.dumps(datatables_fields))


def set_foo(some_object, foo_string, value):
    return setattr(some_object, foo_string, value)


def get_foo(some_object, foo_string):
    return getattr(some_object, foo_string)


class ModelCrudAPI(MethodView):
    """
    class MenuItemCategoryEditor(ModelCrudAPI):
        def __init__(self):
            ModelCrudAPI.__init__(self, MenuItemCategory, db)


    api.add_url_rule("/menu-item-category",
                    view_func=MenuItemCategoryEditor.as_view("menu-item-category"),
                    methods=['GET', 'POST', 'PUT', 'DELETE'])
    """

    def __init__(self, model, db):
        self.model = model
        self.db = db

    def get(self, iid):
        # store_id = request.args.get("store_id", None, int)
        # TODO change the store_id to some string value
        query_items = self.model.query.filter_by(store_id=iid).all()
        if query_items is None or iid is None:
            return jsonify({'items': [], 'store_id': iid}), 204
        else:
            items = []
            for item in query_items:
                print(item.id)
                items.append(row2dict(item))
            return jsonify({"items": items, "columns": [

                {"data": "id"},
                {"data": "first_name"},
                {"data": "last_name"},
                {"data": "username"},
                {"data": "email"},
                {"data": "position"}

            ], 'store_id': iid})

    def post(self, iid):
        # store_i/d = request.args.get("store_id", None, int)
        if iid is None:
            return jsonify({'error': 'No store id'}), 400
        else:
            try:
                data = request.json["items"]
                if len(data) == 0:
                    return jsonify({'error': 'no body'}), 400
                else:
                    data["store_id"] = iid
                    item = self.model(**dict(data))
                    self.db.session.add(item)
                    self.db.session.commit()
                    return jsonify({"status": "added"}), 201
            except KeyError as e:
                return jsonify({'error': str(e)}), 400

    def put(self, iid):
        # item_id = request.args.get("item_id", None, int)
        if iid is None:
            return jsonify({'error': 'No store id'}), 400
        else:
            try:
                data = request.json["items"]
                if len(data) == 0:
                    return jsonify({'error': 'no body'}), 400
                else:
                    data["id"] = iid
                    self.model.query.filter_by(id=iid).update(dict(data))
                    self.db.session.commit()
                    return jsonify({"status": "updated"})
            except KeyError as e:
                return jsonify({'error': str(e)}), 400

    def delete(self, iid):
        # item_id = request.args.get("item_id", None, type=int)
        item = self.model.query.filter_by(id=iid).first()
        if item is None:
            return jsonify({"error": "not found!"}), 404
        else:
            self.db.session.delete(item)
            self.db.session.commit()
            return jsonify({"status": "deleted"}), 200
        self.db.session.delete(item)
        self.db.session.commit()
        return jsonify({"status": "OK"})
