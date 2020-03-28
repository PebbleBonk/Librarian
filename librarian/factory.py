from flask import Flask, jsonify, request, render_template
from flask import abort, redirect, send_from_directory
from flask_cors import CORS
from werkzeug.datastructures import FileStorage
from librarian.validators.exceptions import ValidationError
import json
import os
from io import BytesIO
import base64
from bson.objectid import ObjectId


def create_librarian(datatype, datatag,
                     label_validator, label_actor,
                     data_validator, data_actor,
                     cross_validator):
    app = Flask(__name__)
    CORS(app)

    @app.route('/')
    def index():
        return redirect('http://github.com/oikone', code=302)


    @app.route('/put', methods=['POST'])
    def putter():
        # Put-put golf:
        labels = parse_url_args(request.args)

        if datatype=="file" and request.files is not None:
            data = request.files.get(datatag, 0)
        elif datatype=='base64' and request.form:
            raw64 = request.form[datatag]
            # Make sure we don't have any nasty tags:
            raw64 = raw64.split(',')[-1]
            data = FileStorage(
                stream=BytesIO(base64.b64decode(raw64)),
                filename=labels.get('filename', 'input')
            )
        elif datatype=="json" and request.json is not None:
            # default value of no data tag: get full json from request:
            data = request.json.get(datatag, 0) if datatag else request.json
        else:
            abort(406, "Invalid data type")

        if not data:
            abort(406, "Data tag not found")

        try:
            # 1. Run label validator on label(s)
            label_validator(labels)
            # 2. Run data validator for data
            data_validator(data)
            # 3. Run cross validator for label(s) and data
            cross_validator(labels, data)
        except ValidationError as e:
            abort(415, str(e))

        # if everything is ok, create a unique ID:
        uid = str(ObjectId())

        # 5. Run label action
        try:
            label_actor_response = label_actor.act(labels, uid)
            # 6. Run data action
        except Exception as e:
            abort(415, "Error occurred during LABEL actor: "+str(e))
        try:
            data_actor_response = data_actor.act(data, uid)
        except Exception as e:
            abort(415, "Error occurred during DATA actor: "+str(e))
        # 7. Return success
        return jsonify(
            'Lables and data processed successfully:\n' +
            f'\tLabel response: {label_actor_response}\n' +
            f'\tData response: {data_actor_response}'
        ), 200


    @app.route('/get', methods=['GET'])
    def getter():
        # Yo momma such a go-getter that ...
        abort(501, 'API call not implemented')

    print("\n\n~ Created a Librarian instance. ~")
    print("[LABEL VALIDATOR]:", str(label_validator))
    print("[DATA VALIDATOR]:", str(data_validator))
    print("[CROSS VALIDATOR]:", str(cross_validator))
    print("[LABEL ACTOR]:", str(label_actor))
    print("[DATA ACTOR]:", str(data_actor))

    return app



def parse_url_args(args):
    """ All the parameters are passed as strings. try to convert them
        back to their original types """
    parsed = {}
    for k, v in args.items():
        # First, try converting to float and int:
        try:
            parsed[k] = int(v)
            continue
        except ValueError:
            pass
        try:
            parsed[k] = float(v)
        except ValueError:
            pass
        # Then try explicit bool conversion:
        if v.lower() in ['true', 'false']:
            parsed[k] = v.lower() == "true"
        # Finally, just accept it as a string:
        else:
            parsed[k] = v
    return parsed