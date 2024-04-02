# from app import *
# from backend.settings.settings import *
# from flask_socketio import emit
#
#
# @app.route("/http-call")
# def http_call():
#     """return JSON with string data as the value"""
#     data = {'data': 'This text was fetched using an HTTP call to server on render'}
#     return jsonify(data)
#
#
# @socketio.on("connect")
# def connected():
#     """event listener when client connects to the server"""
#     print("client has connected", request.sid)
#     emit("connect", {"data": f"id: {request.sid} is connected"})
#
#
# @socketio.on("message")
# def handle_message(data):
#     """event listener when client types a message"""
#     print("data from the front end: ", data)
#     emit("data", {'data': data, 'id': request.sid}, broadcast=True)
#
#
# @socketio.on("disconnect")
# def disconnected():
#     """event listener when client disconnects to the server"""
#     print("user disconnected", request.sid)
#     emit("disconnect", f"user {request.sid} disconnected", broadcast=True)
