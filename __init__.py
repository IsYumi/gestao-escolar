from flask import Flask, jsonify
from main.views import init_views

global app
app = Flask('app')
init_views(app)
