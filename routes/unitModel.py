#se importan librerias necesarias para flask
from flask import Blueprint, jsonify, render_template, request, redirect, session, url_for, flash
from flask_marshmallow.fields import re
from sqlalchemy.engine import result, url
#se importan las clases de las tablas
from models.unitmodel import unitModel, Products, Sales, allProductsSchema
# se importa la bd para poder hacer el commit con sql
from utils.db import db, ma
from sqlalchemy import func



uModel = Blueprint('unitModel', __name__)

#home
@uModel.route("/")
def home():
    return render_template("index.html")

"""CRUD API Endpoints for a UnitMeasure model.
With fields: unit measure id and name."""
# se general los apartados para los siguientes metodos: POST, GET, PUT, DELETE
# create
@uModel.route("/unitModel/create", methods=['GET', 'POST'])
def postUnit():
    """Endpoint generado para procesar solicitudes POST"""
    if request.method == 'POST':
        unitMesuareid = request.form['unitMesuareid']
        name = request.form['name']
        new_uModel = unitModel(unitMesuareid, name)
        db.session.add(new_uModel)
        db.session.commit()
        #mensajes flash
        flash("Se agrego correctamente")
        return redirect(url_for('unitModel.postUnit'))

    return render_template("unitMesuare.html")

# read
@uModel.route("/unitModel/read", methods=['GET'])
def getUnit():
    """Endpoint generado para procesar solicitudes GET"""
    modelRead = unitModel.query.all()
    return render_template("unitMesuareget.html", modelRead=modelRead)


# update
@uModel.route("/unitModel/actualizar/<unitMesuareid>", methods=['POST', 'GET'])
def putUnit(unitMesuareid):
    """Endpoint generado para procesar solicitudes de actualización de datos mediante GET y POST"""
    model = unitModel.query.get(unitMesuareid)
    if request.method == "POST":
        model.unitMesuareid = request.form['unitMesuareid']
        model.name = request.form['name']
        db.session.commit()
        #mensajes flash
        flash("Se actualizo correctamente")
        return redirect(url_for('unitModel.getUnit'))
    
    return render_template("Mesuareupdate.html", model=model)

# delete
@uModel.route("/unitModel/delete/<unitMesuareid>")
def delUnit(unitMesuareid):
    """Endpoint generado para procesar solicitudes de eliminado"""
    model = unitModel.query.get(unitMesuareid)
    db.session.delete(model)
    db.session.commit()
    #mensajes flash
    flash("Se elimino correctamente")
    return redirect(url_for('unitModel.getUnit'))


"""CRUD API Endpoints for a Products model.
With fields: name, price, and unit measure id.
Only can receive unit measure id’s created."""
#create

@uModel.route('/product/create', methods=['GET','POST'])
def productPost():
    """Endpoint generado para procesar solicitudes POST"""
    if request.method == 'POST':
        nameProduct = request.form['nameProduct']
        priceProduct = request.form['priceProduct']
        unitmeidProduct = request.form['unitmeidProduct']
        idunitproduct = unitModel.query.filter(unitModel.unitMesuareid == f"{unitmeidProduct}").first()
        if idunitproduct:
            newProduct = Products(nameProduct, priceProduct, unitmeidProduct)
            db.session.add(newProduct)
            db.session.commit()
            #mensajes flash
            flash("Se agrego correctamente")
            return redirect(url_for('unitModel.productPost'))
        
    return render_template("products.html")

#read
@uModel.route('/product/read', methods=['GET'])
def productGet():
    """Endpoint generado para procesar solicitudes GET"""
    productread = Products.query.all()
    return render_template("productsget.html", productread=productread)

#update
@uModel.route('/product/update/<nameProduct>', methods=['POST','GET'])
def productUpdate(nameProduct):
    """Endpoint generado para procesar solicitudes de actualización de datos mediante GET y POST"""
    prod =  Products.query.get(nameProduct)
    if request.method == 'POST':
        prod.nameProduct = request.form['nameProduct']
        prod.priceProduct = request.form['priceProduct']
        prod.unitmeidProduct = request.form['unitmeidProduct']
        unitmeidProduct = prod.unitmeidProduct = request.form['unitmeidProduct']
        idunitproduct = unitModel.query.filter(unitModel.unitMesuareid == f"{unitmeidProduct}").first()
        if idunitproduct:
            db.session.commit()
            #mensajes flash
            flash("Se actualizo correctamente")
            return redirect(url_for('unitModel.productGet'))
    return render_template("productsupdate.html", prod=prod)


#delete
@uModel.route('/product/delete/<nameProduct>')
def productDelete(nameProduct):
    """Endpoint generado para procesar solicitudes de eliminado"""
    prod = Products.query.get(nameProduct)
    db.session.delete(prod)
    db.session.commit()
    flash("Se elimino correctamente")
    return redirect(url_for('unitModel.productGet'))

"""API Endpoint to generate sales. post
With fields: date, quantity, and product."""
#post
@uModel.route('/sales/create', methods=['GET', 'POST'])
def salesPost():
    """Endpoint generado para procesar solicitudes POST"""
    if request.method == 'POST':
        date = request.form['date']
        quantity = request.form['quantity']
        product = request.form['product']
        productExist = Products.query.filter(Products.nameProduct == f"{product}").first()
        #validacion de que solo agregue productos que ya existen
        if productExist:
            newSale = Sales(date, quantity, product)
            db.session.add(newSale)
            db.session.commit()
            flash("Se agrego correctamente")
            return redirect(url_for('unitModel.salesPost'))
    return render_template('sales.html')


"""4. API Request example of getting the sales of each product (Quantity and
amount) get
#get RESTAPI - POSTMAN
"""
@uModel.route('/eachproduct/<product>', methods=['GET'])
def eachProduct(product):
    productName = Products.query.get(product)

    productQty = Sales.query.filter(Sales.quantity == f"{product}").first()
    productPrice = Products.query.filter(Products.priceProduct == f"{product}").first()
    
    print(productName)
    print(productQty)
    print(productPrice)
    return "ola"


"""API Request example of getting the sales of all products (Quantity and
amount) get 
#get RESTAPI - POSTMAN
"""

@uModel.route('/allProducts', methods=['GET'])
def allProductsGet():
    """Endpoint generado para procesar solicitudes GET"""
    #iniciando el schema
    productSchema= allProductsSchema(many=True)
    #se hace la consulta
    allProduts = Sales.query.all()
    resultProducts = productSchema.dump(allProduts)
    return jsonify(resultProducts) and jsonify (resultProducts)
