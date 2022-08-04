import json
from flask import Flask, request, jsonify, Blueprint
import sys
sys.path.append("..")
from apps import model
from Control.Model import Model


book_bp = Blueprint('book_bp', __name__)


@book_bp.route('/user=<user>/book=<book>/main')
def c_book(user, book):
    return jsonify(model.detail_show(user, book))

@book_bp.route('/user=<user>/book=<book>/praise')
def c_praise(user, book):
    model.praise(model.de_ctry(user), model.index_to_book(book))


@book_bp.route('/user=<user>/book=<book>/start')
def c_collect(user, book):
    model.collect(model.de_ctry(user), model.index_to_book(book))


@book_bp.route('/user=<user>/book=<book>/review', methods=["GET", "POST"])
def c_review(user, book):
    dic = json.loads(request.get_data(as_text=True))
    model.review(model.de_ctry(user), model.index_to_book(book), dic.get("user_url"), dic.get("review"))
