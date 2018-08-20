import json

from flask import request, render_template


def model_crud(session, model, fields, params, item_id):
    if item_id is not None:
        item = model.query.get(item_id)
    else:
        item = model()
    cleaned_data = []
    for field in fields:
        if (not field) | (field is None):
            field = None
        cleaned_data.append(field)
    if all(f is None for f in cleaned_data):
        pass
    else:
        for p, param in enumerate(params):
            set_foo(item, param, cleaned_data[p])

        if item_id is not None:
            session.commit()
        else:
            session.add(item)
            session.commit()


def render_table(session, model, template_location='main/email.html', argument_name='project_id', model_name='email',
                 page_name="Budget Data Collection"):
    params = ['first_name', 'last_name', 'email', 'token']
    if request.method == 'POST':  # this block is only entered when the form is submitted
        print('post request')
        fields = []
        for param in params[:-1]:
            field = request.form.get(param, None)
            print(field)
            fields.append(field)
        item_id = request.args.get(argument_name, None, int)
        model_crud(session, model, fields, params[:-1], item_id)
    fields = params[:]
    fields.insert(0, 'id')
    # fields.append('token')
    print(params)
    params_jso = json.dumps(params[:-1])
    return render_template(template_location, headers=fields, name=page_name, model=model_name, params=params_jso)


def set_foo(some_object, foo_string, value):
    return setattr(some_object, foo_string, value)


def get_foo(some_object, foo_string):
    return getattr(some_object, foo_string)
