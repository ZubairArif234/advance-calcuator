from flask import Blueprint , jsonify,request,session
from config.database import db
from modals.product import Product
from decorators.isAuth import isAuth
from werkzeug.utils import secure_filename

import os

product = Blueprint("product" , __name__)
myCollection = db['products']

@product.route('/create',methods=['POST'])
@isAuth
def createProduct ():
   
    userDetail = session.get('user')
    print(userDetail)
    print(request.files)
    try:
        if 'image' not in request.files:
            return jsonify({"error": "Upload Image "}), 400
        
        file = request.files["image"]
        
        if file :
            filename = secure_filename(file.filename)
            filepath=os.path.join('uploads/' , filename)
            file.save(filepath)
            thumbnailImg=filepath
           
        product = Product(
        name = request.form.get('name'),
        desc =request.form.get('desc'),
        price = request.form.get('price'),
        shades = request.form.getlist('shades[]'),
        sizes = request.form.getlist('sizes[]'),
        thumbnailImg=thumbnailImg
        )
        product.save()
        return jsonify({"message": "Product created successfully"}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
@product.route('/update/<product_id>', methods=['PUT'])
@isAuth
def updateProduct(product_id):
    try:
        product = Product.objects.get(id=product_id)
        
        if not product :
            return jsonify({"error": "Product not found"}), 404
        
        if 'name' in request.form:
            product.name = request.form.get('name')
        if 'desc' in request.form:
            product.desc = request.form.get('desc')
        if 'price' in request.form:
            product.price = request.form.get('price')
        if 'shades[]' in request.form:
            product.shades = request.form.getlist('shades[]')
        if 'sizes[]' in request.form:
            product.sizes = request.form.getlist('sizes[]')

        # Handle file upload if provided
        if 'image' in request.files:
            file = request.files['image']
            if file.filename != '':
               
                filename = secure_filename(file.filename)
                file_path = os.path.join('uploads/', filename)
                file.save(file_path)
                product.thumbnailImg = file_path

        # Save the updated product
        product.save()
        return jsonify({"message": "Product updated successfully"}), 200

    
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
@product.route('/delete/<product_id>', methods=["delete"]) 
@isAuth
def deleteProduct (product_id):
    try:
        product = Product.objects.get(id = product_id)
        
        if not product:
            return jsonify({"error": "Product not found"}), 500
            
        product.delete()
        return jsonify({"message": "Product deleted successfully"}), 201
    except Exception as e:
         return jsonify({"error": str(e)}), 500
    
@product.route('/single/<product_id>', methods=["get"]) 
@isAuth
def getSingleProduct (product_id):
    try:
        product = Product.objects.get(id = product_id)
        
        if not product:
            return jsonify({"error": "Product not found"}), 500
        
        product_data = {
            "id": str(product.id), 
            "name": product.name,
            "desc": product.desc,
            "price": product.price,
            "shades": product.shades,
            "sizes": product.sizes,
            "thumbnailImg": product.thumbnailImg  
        }
        
        return jsonify({"message": "Product fetched successfully", "product": product_data}), 200  
    except Exception as e:
         return jsonify({"error": str(e)}), 500
    
    
    