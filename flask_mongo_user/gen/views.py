from flask import Flask, Blueprint, render_template, request
from flask_mongo_user import um
from flask_mongo_user.gen import gen

@gen.route('/')
def home():
    return render_template(
        '_base.html',
        um=um
    )
