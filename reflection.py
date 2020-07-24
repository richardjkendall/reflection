import json
import os
import uuid

from flask import Flask, make_response, request, jsonify

def return_success_response(payload):
  resp = make_response(jsonify(payload), 200)
  resp.headers["Content-type"] = "application/json"
  return resp

def return_404_response():
  payload = {
    "error": "404"
  }
  resp = make_response(jsonify(payload), 404)
  resp.headers["Content-type"] = "application/json"
  return resp

def return_400_response():
  payload = {
    "error": "400"
  }
  resp = make_response(jsonify(payload), 400)
  resp.headers["Content-type"] = "application/json"
  return resp

def read_obj(dir, obj, id):
  path = "{dir}/{obj}/{id}".format(dir = dir, obj = obj, id = id)
  if os.path.isfile(path):
    with open(path, "r") as f:
      data = json.load(f)
      f.close()
      return data
  else:
    return False

def update_obj(dir, obj, id, new):
  path = "{dir}/{obj}/{id}".format(dir = dir, obj = obj, id = id)
  data = {}
  with open(path, "r") as f:
    data = json.load(f)
    f.close()
  data.update(new)
  with open(path, "w") as f:
    json.dump(data, f)
    f.close()
  return {
    "id": id,
    "type": obj,
    "data": data
  }

def scan_dir(dir, obj, get_attrs=False):
  data = []
  path = "{dir}/{obj}".format(dir = dir, obj = obj)
  if not os.path.isdir(path):
    return return_404_response()
  else:
    for f in os.listdir("{dir}/{obj}".format(dir = dir, obj = obj)):
      if not get_attrs:
        # don't need to read the files
        data.append({
          "type": obj,
          "id": f
        })
      else:
        data.append({
          "type": obj,
          "id": f,
          "data": read_obj(dir, obj, f)
        })
    return return_success_response(data)

def make_obj(dir, obj, payload, new_id = None):
  path = "{dir}/{obj}".format(dir = dir, obj = obj)
  if new_id == None:
    new_id = str(uuid.uuid4())
  data = {
    "id": new_id,
    "type": obj,
    "data": payload
  }
  if not os.path.isdir(path):
    os.mkdir(path)
  with open("{path}/{new_id}".format(path = path, new_id = new_id), "w") as f:
    json.dump(payload, f)
    f.close()
  return return_success_response(data)

def rem_obj(dir, obj, id):
  path = "{dir}/{obj}/{id}".format(dir = dir, obj = obj, id = id)
  os.remove(path)
  
def create_app(test_config=None):
  app = Flask(__name__)
  path = ""
  # check if the store directory exists
  if "DATA_STORE" in os.environ:
    # we've been told the directory to use
    path = os.environ["DATA_STORE"]
    if not os.path.isdir(os.environ["DATA_STORE"]):
      os.mkdir(os.environ["DATA_STORE"])
  else:
    # we've not been told the directory to use
    path = "_data_"
    if not os.path.isdir("_data_"):
      os.mkdir("_data_")

  @app.route("/<string:obj>", methods=["GET"])
  def lst(obj):
    return_attributes = request.args.get("return_attributes", default = False, type = bool)
    data = scan_dir(
      dir = path,
      obj = obj,
      get_attrs = return_attributes
    )
    return data
  
  @app.route("/<string:obj>/<string:id>", methods=["GET"])
  def get(obj, id):
    data = read_obj(
      dir = path,
      obj = obj,
      id = id
    )
    if not data:
      return return_404_response()
    payload = {
      "type": obj,
      "id": id,
      "data": data
    }
    return return_success_response(payload)
  
  @app.route("/<string:obj>", methods=["PUT"])
  def add(obj):
    if not request.json:
      return return_400_response()
    return make_obj(
      dir = path,
      obj = obj,
      payload = request.json
    )
  
  @app.route("/<string:obj>/<string:id>", methods=["POST", "PATCH"])
  def update(obj, id):
    if not request.json:
      return return_400_response()
    data = read_obj(
      dir = path,
      obj = obj,
      id = id
    )
    if not data:
      return return_404_response()
    new = update_obj(
      dir = path,
      obj = obj,
      id = id,
      new = request.json
    )
    return return_success_response(new)

  @app.route("/<string:obj>/<string:id>", methods=["DELETE"])
  def remove(obj, id):
    data = read_obj(
      dir = path,
      obj = obj,
      id = id
    )
    if not data:
      return return_404_response()
    rem_obj(
      dir = path,
      obj = obj,
      id = id
    )
    return return_success_response({
      "status": "deleted"
    })

  @app.route("/<string:obj>/<string:id>", methods=["PUT"])
  def replace(obj, id):
    if not request.json:
      return return_400_response()
    return make_obj(
      dir = path,
      obj = obj,
      payload = request.json,
      new_id = id
    )
    
  return app
