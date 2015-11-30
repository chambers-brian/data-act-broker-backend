import sys
import os

from flask import Flask, request, make_response, session, g, redirect, url_for, \
     abort, render_template, flash ,session, Response
import json
import flask


from handlers.aws.session import DynamoInterface, SessionTable, LoginSession

from handlers.loginHandler import LoginHandler
from handlers.fileHandler import FileHandler
from handlers.aws.s3UrlHandler import s3UrlHandler
from fileRoutes import add_file_routes
from loginRoutes import add_login_routes

# Set parameters
debugFlag = True # Should be false for prod

# Create application
app = Flask(__name__)
app.config.from_object(__name__)

#Enable AWS Sessions
app.session_interface = DynamoInterface()

# Root will point to index.html
@app.route("/")
def root():
    content = open(os.getcwd()+"/index.html").read()
    return Response(content, mimetype="text/html")

#Add routes for modules here
add_file_routes(app)
add_login_routes(app)

if __name__ == '__main__':
    SessionTable.setup(app,True,False)
    app.run(debug=debugFlag)
