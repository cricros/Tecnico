from itertools import product
import string
from flask_marshmallow import fields

from werkzeug.formparser import default_stream_factory
from utils.db import db, ma
from datetime import datetime, date, timedelta

#primera tabla
class unitModel(db.Model):
    __tablename__ = 'unitModel'
    #columnas 
    #id = db.Column(db.Integer, primary_key=True)
    unitMesuareid = db.Column(db.String(20), primary_key=True)
    name = db.Column(db.String(50))
    #prodt = db.relationship('Products', back_populates='umodelid', uselist=False)

    
    #lo que mando 
    def __init__(self, unitMesuareid, name):
        self.unitMesuareid = unitMesuareid
        self.name = name

#segunda tabla
class Products(db.Model):
    __tablename__ = 'products'
    #columnas
    nameProduct = db.Column(db.String(50), primary_key=True)
    priceProduct = db.Column(db.String())
    unitmeidProduct = db.Column(db.String(20))
    #se hace la llave foranea para traer el unitMesuareid
    #unitmodelid = db.Column(db.String(20), db.ForeignKey('unitModel.unitMesuareid'))
    #umodelid = db.relationship('unitModel', back_populates='prodt')

    
    def __init__(self, nameProduct, priceProduct, unitmeidProduct):
        self.nameProduct = nameProduct
        self.priceProduct = priceProduct
        self.unitmeidProduct = unitmeidProduct

class Sales(db.Model):
    __tablename__ = 'sales'
    #columnas
    idSales = db.Column(db.Integer, primary_key=True)
    date1 = db.Column(db.String(10))
    quantity = db.Column(db.String())
    product = db.Column(db.String(30))

    def __init__(self, date, quantity, product):
        self.date1 = date
        self.quantity = quantity
        self.product = product

#creando los modelos para POSTMAN mediante Marshmellow
class eachProductSchema(ma.Schema):
    class Meta:
        fields = ('date', 'quantity', 'product', 'priceProduct')


class allProductsSchema(ma.Schema): 
    class Meta:
        fields = ('quantity', 'product', 'priceProduct')


