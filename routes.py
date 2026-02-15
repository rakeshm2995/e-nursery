from flask import render_template, request, redirect, url_for, flash, jsonify, send_from_directory
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.utils import secure_filename
from models import db, User, Plant, Ingredient, Cart, Order, OrderItem, Wishlist, Review
from datetime import datetime, timedelta
from sqlalchemy import or_, func
import os

UPLOAD_FOLDER = 'static/uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'webp'}


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def init_routes(app):
    # ==================== HOME & GENERAL ====================

    @app.route('/')
    def index():
        plants = Plant.query.filter(Plant.stock > 0).limit(8).all()
        ingredients = Ingredient.query.filter(Ingredient.stock > 0).limit(4).all()
        categories = db.session.query(Plant.category, func.count(Plant.id)).group_by(Plant.category).all()
        return render_template('index.html', plants=plants, ingredients=ingredients, categories=categories)

    @app.route('/about')
    def about():
        return render_template('about.html')

    @app.route('/contact')
    def contact():
        return render_template('contact.html')

    # ==================== AUTHENTICATION ====================

    @app.route('/register', methods=['GET', 'POST'])
    def register():
        if current_user.is_authenticated:
            return redirect(url_for('index'))

        if request.method == 'POST':
            username = request.form.get('username')
            email = request.form.get('email')
            password = request.form.get('password')
            full_name = request.form.get('full_name')
            phone = request.form.get('phone')

            if User.query.filter_by(username=username).first():
                flash('Username already exists', 'danger')
                return redirect(url_for('register'))

            if User.query.filter_by(email=email).first():
                flash('Email already registered', 'danger')
                return redirect(url_for('register'))

            user = User(username=username, email=email, full_name=full_name, phone=phone)
            user.set_password(password)
            db.session.add(user)
            db.session.commit()

            flash('Registration successful! Please login.', 'success')
            return redirect(url_for('login'))

        return render_template('register.html')

    @app.route('/login', methods=['GET', 'POST'])
    def login():
        if current_user.is_authenticated:
            return redirect(url_for('index'))

        if request.method == 'POST':
            username = request.form.get('username')
            password = request.form.get('password')

            user = User.query.filter_by(username=username).first()

            if user and user.check_password(password):
                login_user(user)
                flash(f'Welcome back, {user.full_name or user.username}!', 'success')
                next_page = request.args.get('next')
                return redirect(next_page) if next_page else redirect(url_for('index'))
            else:
                flash('Invalid username or password', 'danger')

        return render_template('login.html')

    @app.route('/logout')
    @login_required
    def logout():
        logout_user()
        flash('You have been logged out successfully', 'info')
        return redirect(url_for('index'))

    @app.route('/profile')
    @login_required
    def profile():
        return render_template('profile.html')

    @app.route('/profile/update', methods=['POST'])
    @login_required
    def update_profile():
        current_user.full_name = request.form.get('full_name')
        current_user.phone = request.form.get('phone')
        current_user.address = request.form.get('address')
        current_user.city = request.form.get('city')
        current_user.state = request.form.get('state')
        current_user.pincode = request.form.get('pincode')

        db.session.commit()
        flash('Profile updated successfully', 'success')
        return redirect(url_for('profile'))

    # ==================== PLANTS ====================

    @app.route('/plants')
    def plants():
        category = request.args.get('category')
        search = request.args.get('search')
        min_price = request.args.get('min_price', type=float)
        max_price = request.args.get('max_price', type=float)
        in_stock = request.args.get('in_stock')

        query = Plant.query

        if category:
            query = query.filter_by(category=category)

        if search:
            query = query.filter(or_(
                Plant.name.ilike(f'%{search}%'),
                Plant.description.ilike(f'%{search}%')
            ))

        if min_price is not None:
            query = query.filter(Plant.price >= min_price)

        if max_price is not None:
            query = query.filter(Plant.price <= max_price)

        if in_stock == 'true':
            query = query.filter(Plant.stock > 0)

        plants = query.all()
        categories = db.session.query(Plant.category).distinct().all()

        return render_template('plants.html', plants=plants, categories=[c[0] for c in categories])

    @app.route('/plant/<int:id>')
    def plant_detail(id):
        plant = Plant.query.get_or_404(id)
        reviews = Review.query.filter_by(plant_id=id).order_by(Review.created_at.desc()).all()
        related_plants = Plant.query.filter(Plant.category == plant.category, Plant.id != id, Plant.stock > 0).limit(
            4).all()

        user_wishlist = None
        if current_user.is_authenticated:
            user_wishlist = Wishlist.query.filter_by(user_id=current_user.id, plant_id=id).first()

        return render_template('plant_detail.html', plant=plant, reviews=reviews, related_plants=related_plants,
                               user_wishlist=user_wishlist)

    # ==================== INGREDIENTS ====================

    @app.route('/ingredients')
    def ingredients():
        type_filter = request.args.get('type')
        search = request.args.get('search')
        min_price = request.args.get('min_price', type=float)
        max_price = request.args.get('max_price', type=float)
        in_stock = request.args.get('in_stock')

        query = Ingredient.query

        if type_filter:
            query = query.filter_by(type=type_filter)

        if search:
            query = query.filter(or_(
                Ingredient.name.ilike(f'%{search}%'),
                Ingredient.description.ilike(f'%{search}%')
            ))

        if min_price is not None:
            query = query.filter(Ingredient.price >= min_price)

        if max_price is not None:
            query = query.filter(Ingredient.price <= max_price)

        if in_stock == 'true':
            query = query.filter(Ingredient.stock > 0)

        ingredients = query.all()
        types = db.session.query(Ingredient.type).distinct().all()

        return render_template('ingredients.html', ingredients=ingredients, types=[t[0] for t in types])

    @app.route('/ingredient/<int:id>')
    def ingredient_detail(id):
        ingredient = Ingredient.query.get_or_404(id)
        related_ingredients = Ingredient.query.filter(Ingredient.type == ingredient.type, Ingredient.id != id,
                                                      Ingredient.stock > 0).limit(4).all()
        return render_template('ingredient_detail.html', ingredient=ingredient, related_ingredients=related_ingredients)

    # ==================== CART ====================

    @app.route('/cart')
    @login_required
    def cart():
        cart_items = Cart.query.filter_by(user_id=current_user.id).all()

        subtotal = sum(item.subtotal for item in cart_items)
        gst = subtotal * 0.18
        total = subtotal + gst

        return render_template('cart.html', cart_items=cart_items, subtotal=subtotal, gst=gst, total=total)

    @app.route('/cart/add', methods=['POST'])
    @login_required
    def add_to_cart():
        item_type = request.form.get('item_type')
        item_id = int(request.form.get('item_id'))
        quantity = int(request.form.get('quantity', 1))

        # Check stock
        if item_type == 'plant':
            item = Plant.query.get(item_id)
        else:
            item = Ingredient.query.get(item_id)

        if not item or item.stock < quantity:
            flash('Insufficient stock', 'danger')
            return redirect(request.referrer)

        # Check if already in cart
        cart_item = Cart.query.filter_by(user_id=current_user.id, item_type=item_type, item_id=item_id).first()

        if cart_item:
            new_quantity = cart_item.quantity + quantity
            if item.stock < new_quantity:
                flash('Cannot add more. Insufficient stock', 'danger')
                return redirect(request.referrer)
            cart_item.quantity = new_quantity
        else:
            cart_item = Cart(user_id=current_user.id, item_type=item_type, item_id=item_id, quantity=quantity)
            db.session.add(cart_item)

        db.session.commit()
        flash('Item added to cart', 'success')
        return redirect(request.referrer or url_for('cart'))

    @app.route('/cart/update/<int:id>', methods=['POST'])
    @login_required
    def update_cart(id):
        cart_item = Cart.query.get_or_404(id)

        if cart_item.user_id != current_user.id:
            flash('Unauthorized', 'danger')
            return redirect(url_for('cart'))

        quantity = int(request.form.get('quantity', 1))
        item = cart_item.get_item()

        if item.stock < quantity:
            flash('Insufficient stock', 'danger')
            return redirect(url_for('cart'))

        cart_item.quantity = quantity
        db.session.commit()
        flash('Cart updated', 'success')
        return redirect(url_for('cart'))

    @app.route('/cart/remove/<int:id>')
    @login_required
    def remove_from_cart(id):
        cart_item = Cart.query.get_or_404(id)

        if cart_item.user_id != current_user.id:
            flash('Unauthorized', 'danger')
            return redirect(url_for('cart'))

        db.session.delete(cart_item)
        db.session.commit()
        flash('Item removed from cart', 'success')
        return redirect(url_for('cart'))

    # ==================== CHECKOUT & ORDERS ====================

    @app.route('/checkout')
    @login_required
    def checkout():
        cart_items = Cart.query.filter_by(user_id=current_user.id).all()

        if not cart_items:
            flash('Your cart is empty', 'warning')
            return redirect(url_for('cart'))

        # Validate stock
        for item in cart_items:
            product = item.get_item()
            if product.stock < item.quantity:
                flash(f'Insufficient stock for {product.name}', 'danger')
                return redirect(url_for('cart'))

        subtotal = sum(item.subtotal for item in cart_items)
        gst = subtotal * 0.18
        total = subtotal + gst

        return render_template('checkout.html', cart_items=cart_items, subtotal=subtotal, gst=gst, total=total)

    @app.route('/place-order', methods=['POST'])
    @login_required
    def place_order():
        cart_items = Cart.query.filter_by(user_id=current_user.id).all()

        if not cart_items:
            flash('Your cart is empty', 'warning')
            return redirect(url_for('cart'))

        # Validate stock again
        for item in cart_items:
            product = item.get_item()
            if product.stock < item.quantity:
                flash(f'Insufficient stock for {product.name}', 'danger')
                return redirect(url_for('cart'))

        # Calculate total
        subtotal = sum(item.subtotal for item in cart_items)
        gst = subtotal * 0.18
        total = subtotal + gst

        # Get shipping details
        shipping_address = f"{request.form.get('address')}, {request.form.get('city')}, {request.form.get('state')} - {request.form.get('pincode')}"
        payment_method = request.form.get('payment_method')

        # Create order
        order = Order(
            user_id=current_user.id,
            total_amount=total,
            payment_method=payment_method,
            shipping_address=shipping_address,
            estimated_delivery=datetime.utcnow() + timedelta(days=7)
        )
        order.generate_tracking_number()

        if payment_method == 'cod':
            order.payment_status = 'Pending'
        else:
            order.payment_status = 'Completed'

        db.session.add(order)
        db.session.flush()

        # Create order items and reduce stock
        for item in cart_items:
            product = item.get_item()

            order_item = OrderItem(
                order_id=order.id,
                item_type=item.item_type,
                item_id=item.item_id,
                item_name=product.name,
                quantity=item.quantity,
                price=product.price,
                subtotal=item.subtotal
            )
            db.session.add(order_item)

            # Reduce stock
            product.stock -= item.quantity

        # Clear cart
        for item in cart_items:
            db.session.delete(item)

        db.session.commit()

        flash('Order placed successfully!', 'success')
        return redirect(url_for('order_confirmation', order_id=order.id))

    @app.route('/order-confirmation/<int:order_id>')
    @login_required
    def order_confirmation(order_id):
        order = Order.query.get_or_404(order_id)

        if order.user_id != current_user.id:
            flash('Unauthorized', 'danger')
            return redirect(url_for('index'))

        return render_template('order_confirmation.html', order=order)

    @app.route('/orders')
    @login_required
    def my_orders():
        orders = Order.query.filter_by(user_id=current_user.id).order_by(Order.created_at.desc()).all()
        return render_template('my_orders.html', orders=orders)

    @app.route('/order/<int:id>')
    @login_required
    def order_detail(id):
        order = Order.query.get_or_404(id)

        if order.user_id != current_user.id and current_user.role != 'admin':
            flash('Unauthorized', 'danger')
            return redirect(url_for('index'))

        return render_template('order_detail.html', order=order)

    @app.route('/track-order', methods=['GET', 'POST'])
    def track_order():
        if request.method == 'POST':
            tracking_number = request.form.get('tracking_number')
            order = Order.query.filter_by(tracking_number=tracking_number).first()

            if not order:
                flash('Invalid tracking number', 'danger')
                return redirect(url_for('track_order'))

            return render_template('track_order.html', order=order)

        return render_template('track_order.html', order=None)

    @app.route('/order/cancel/<int:id>')
    @login_required
    def cancel_order(id):
        order = Order.query.get_or_404(id)

        if order.user_id != current_user.id:
            flash('Unauthorized', 'danger')
            return redirect(url_for('my_orders'))

        if order.order_status in ['Shipped', 'Out for Delivery', 'Delivered']:
            flash('Cannot cancel order at this stage', 'danger')
            return redirect(url_for('order_detail', id=id))

        # Restore stock
        for item in order.order_items:
            if item.item_type == 'plant':
                product = Plant.query.get(item.item_id)
            else:
                product = Ingredient.query.get(item.item_id)

            if product:
                product.stock += item.quantity

        order.order_status = 'Cancelled'
        db.session.commit()

        flash('Order cancelled successfully', 'success')
        return redirect(url_for('order_detail', id=id))

    # ==================== WISHLIST ====================

    @app.route('/wishlist')
    @login_required
    def wishlist():
        wishlist_items = Wishlist.query.filter_by(user_id=current_user.id).all()
        return render_template('wishlist.html', wishlist_items=wishlist_items)

    @app.route('/wishlist/add/<int:plant_id>')
    @login_required
    def add_to_wishlist(plant_id):
        plant = Plant.query.get_or_404(plant_id)

        existing = Wishlist.query.filter_by(user_id=current_user.id, plant_id=plant_id).first()

        if existing:
            flash('Already in wishlist', 'info')
        else:
            wishlist_item = Wishlist(user_id=current_user.id, plant_id=plant_id)
            db.session.add(wishlist_item)
            db.session.commit()
            flash('Added to wishlist', 'success')

        return redirect(request.referrer or url_for('plants'))

    @app.route('/wishlist/remove/<int:id>')
    @login_required
    def remove_from_wishlist(id):
        wishlist_item = Wishlist.query.get_or_404(id)

        if wishlist_item.user_id != current_user.id:
            flash('Unauthorized', 'danger')
            return redirect(url_for('wishlist'))

        db.session.delete(wishlist_item)
        db.session.commit()
        flash('Removed from wishlist', 'success')
        return redirect(url_for('wishlist'))

    @app.route('/wishlist/move-to-cart/<int:id>')
    @login_required
    def move_to_cart(id):
        wishlist_item = Wishlist.query.get_or_404(id)

        if wishlist_item.user_id != current_user.id:
            flash('Unauthorized', 'danger')
            return redirect(url_for('wishlist'))

        plant = wishlist_item.plant

        if plant.stock < 1:
            flash('Product out of stock', 'danger')
            return redirect(url_for('wishlist'))

        # Add to cart
        cart_item = Cart.query.filter_by(user_id=current_user.id, item_type='plant', item_id=plant.id).first()

        if cart_item:
            if plant.stock >= cart_item.quantity + 1:
                cart_item.quantity += 1
            else:
                flash('Insufficient stock', 'danger')
                return redirect(url_for('wishlist'))
        else:
            cart_item = Cart(user_id=current_user.id, item_type='plant', item_id=plant.id, quantity=1)
            db.session.add(cart_item)

        # Remove from wishlist
        db.session.delete(wishlist_item)
        db.session.commit()

        flash('Moved to cart', 'success')
        return redirect(url_for('wishlist'))

    # ==================== REVIEWS ====================

    @app.route('/review/add/<int:plant_id>', methods=['POST'])
    @login_required
    def add_review(plant_id):
        plant = Plant.query.get_or_404(plant_id)

        # Check if user has purchased this plant
        has_purchased = db.session.query(OrderItem).join(Order).filter(
            Order.user_id == current_user.id,
            OrderItem.item_type == 'plant',
            OrderItem.item_id == plant_id,
            Order.order_status == 'Delivered'
        ).first()

        if not has_purchased:
            flash('You can only review products you have purchased and received', 'danger')
            return redirect(url_for('plant_detail', id=plant_id))

        # Check if already reviewed
        existing_review = Review.query.filter_by(user_id=current_user.id, plant_id=plant_id).first()

        if existing_review:
            flash('You have already reviewed this product', 'info')
            return redirect(url_for('plant_detail', id=plant_id))

        rating = int(request.form.get('rating'))
        comment = request.form.get('comment')

        review = Review(
            user_id=current_user.id,
            plant_id=plant_id,
            rating=rating,
            comment=comment
        )

        db.session.add(review)
        db.session.commit()

        flash('Review submitted successfully', 'success')
        return redirect(url_for('plant_detail', id=plant_id))

    # ==================== ADMIN ROUTES ====================

    @app.route('/admin')
    @login_required
    def admin_dashboard():
        if current_user.role != 'admin':
            flash('Unauthorized access', 'danger')
            return redirect(url_for('index'))

        # Analytics
        total_users = User.query.filter_by(role='user').count()
        total_plants = Plant.query.count()
        total_ingredients = Ingredient.query.count()
        total_orders = Order.query.count()
        total_revenue = db.session.query(func.sum(Order.total_amount)).filter(
            Order.order_status != 'Cancelled').scalar() or 0

        # Low stock items
        low_stock_plants = Plant.query.filter(Plant.stock > 0, Plant.stock <= 5).all()
        low_stock_ingredients = Ingredient.query.filter(Ingredient.stock > 0, Ingredient.stock <= 5).all()

        # Most sold items
        most_sold_plant = db.session.query(
            OrderItem.item_id,
            Plant.name,
            func.sum(OrderItem.quantity).label('total_sold')
        ).join(Plant, OrderItem.item_id == Plant.id).filter(
            OrderItem.item_type == 'plant'
        ).group_by(OrderItem.item_id, Plant.name).order_by(func.sum(OrderItem.quantity).desc()).first()

        most_sold_ingredient = db.session.query(
            OrderItem.item_id,
            Ingredient.name,
            func.sum(OrderItem.quantity).label('total_sold')
        ).join(Ingredient, OrderItem.item_id == Ingredient.id).filter(
            OrderItem.item_type == 'ingredient'
        ).group_by(OrderItem.item_id, Ingredient.name).order_by(func.sum(OrderItem.quantity).desc()).first()

        recent_orders = Order.query.order_by(Order.created_at.desc()).limit(10).all()

        return render_template('admin/dashboard.html',
                               total_users=total_users,
                               total_plants=total_plants,
                               total_ingredients=total_ingredients,
                               total_orders=total_orders,
                               total_revenue=total_revenue,
                               low_stock_plants=low_stock_plants,
                               low_stock_ingredients=low_stock_ingredients,
                               most_sold_plant=most_sold_plant,
                               most_sold_ingredient=most_sold_ingredient,
                               recent_orders=recent_orders)

    # ==================== ADMIN - PLANTS ====================

    @app.route('/admin/plants')
    @login_required
    def admin_plants():
        if current_user.role != 'admin':
            flash('Unauthorized access', 'danger')
            return redirect(url_for('index'))

        plants = Plant.query.order_by(Plant.created_at.desc()).all()
        return render_template('admin/plants.html', plants=plants)

    @app.route('/admin/plant/add', methods=['GET', 'POST'])
    @login_required
    def admin_add_plant():
        if current_user.role != 'admin':
            flash('Unauthorized access', 'danger')
            return redirect(url_for('index'))

        if request.method == 'POST':
            name = request.form.get('name')
            category = request.form.get('category')
            price = float(request.form.get('price'))
            description = request.form.get('description')
            sunlight = request.form.get('sunlight')
            water = request.form.get('water')
            care_instructions = request.form.get('care_instructions')
            stock = int(request.form.get('stock'))

            # Handle file upload
            image_filename = 'default_plant.jpg'
            if 'image' in request.files:
                file = request.files['image']
                if file and file.filename and allowed_file(file.filename):
                    filename = secure_filename(file.filename)
                    filename = f"{datetime.utcnow().strftime('%Y%m%d%H%M%S')}_{filename}"
                    file.save(os.path.join(UPLOAD_FOLDER, filename))
                    image_filename = filename

            plant = Plant(
                name=name,
                category=category,
                price=price,
                description=description,
                sunlight=sunlight,
                water=water,
                care_instructions=care_instructions,
                stock=stock,
                image=image_filename
            )

            db.session.add(plant)
            db.session.commit()

            flash('Plant added successfully', 'success')
            return redirect(url_for('admin_plants'))

        return render_template('admin/add_plant.html')

    @app.route('/admin/plant/edit/<int:id>', methods=['GET', 'POST'])
    @login_required
    def admin_edit_plant(id):
        if current_user.role != 'admin':
            flash('Unauthorized access', 'danger')
            return redirect(url_for('index'))

        plant = Plant.query.get_or_404(id)

        if request.method == 'POST':
            plant.name = request.form.get('name')
            plant.category = request.form.get('category')
            plant.price = float(request.form.get('price'))
            plant.description = request.form.get('description')
            plant.sunlight = request.form.get('sunlight')
            plant.water = request.form.get('water')
            plant.care_instructions = request.form.get('care_instructions')
            plant.stock = int(request.form.get('stock'))

            # Handle file upload
            if 'image' in request.files:
                file = request.files['image']
                if file and file.filename and allowed_file(file.filename):
                    filename = secure_filename(file.filename)
                    filename = f"{datetime.utcnow().strftime('%Y%m%d%H%M%S')}_{filename}"
                    file.save(os.path.join(UPLOAD_FOLDER, filename))
                    plant.image = filename

            plant.updated_at = datetime.utcnow()
            db.session.commit()

            flash('Plant updated successfully', 'success')
            return redirect(url_for('admin_plants'))

        return render_template('admin/edit_plant.html', plant=plant)

    @app.route('/admin/plant/delete/<int:id>')
    @login_required
    def admin_delete_plant(id):
        if current_user.role != 'admin':
            flash('Unauthorized access', 'danger')
            return redirect(url_for('index'))

        plant = Plant.query.get_or_404(id)
        db.session.delete(plant)
        db.session.commit()

        flash('Plant deleted successfully', 'success')
        return redirect(url_for('admin_plants'))

    # ==================== ADMIN - INGREDIENTS ====================

    @app.route('/admin/ingredients')
    @login_required
    def admin_ingredients():
        if current_user.role != 'admin':
            flash('Unauthorized access', 'danger')
            return redirect(url_for('index'))

        ingredients = Ingredient.query.order_by(Ingredient.created_at.desc()).all()
        return render_template('admin/ingredients.html', ingredients=ingredients)

    @app.route('/admin/ingredient/add', methods=['GET', 'POST'])
    @login_required
    def admin_add_ingredient():
        if current_user.role != 'admin':
            flash('Unauthorized access', 'danger')
            return redirect(url_for('index'))

        if request.method == 'POST':
            name = request.form.get('name')
            type_ = request.form.get('type')
            price = float(request.form.get('price'))
            description = request.form.get('description')
            usage_instructions = request.form.get('usage_instructions')
            stock = int(request.form.get('stock'))

            # Handle file upload
            image_filename = 'default_ingredient.jpg'
            if 'image' in request.files:
                file = request.files['image']
                if file and file.filename and allowed_file(file.filename):
                    filename = secure_filename(file.filename)
                    filename = f"{datetime.utcnow().strftime('%Y%m%d%H%M%S')}_{filename}"
                    file.save(os.path.join(UPLOAD_FOLDER, filename))
                    image_filename = filename

            ingredient = Ingredient(
                name=name,
                type=type_,
                price=price,
                description=description,
                usage_instructions=usage_instructions,
                stock=stock,
                image=image_filename
            )

            db.session.add(ingredient)
            db.session.commit()

            flash('Ingredient added successfully', 'success')
            return redirect(url_for('admin_ingredients'))

        return render_template('admin/add_ingredient.html')

    @app.route('/admin/ingredient/edit/<int:id>', methods=['GET', 'POST'])
    @login_required
    def admin_edit_ingredient(id):
        if current_user.role != 'admin':
            flash('Unauthorized access', 'danger')
            return redirect(url_for('index'))

        ingredient = Ingredient.query.get_or_404(id)

        if request.method == 'POST':
            ingredient.name = request.form.get('name')
            ingredient.type = request.form.get('type')
            ingredient.price = float(request.form.get('price'))
            ingredient.description = request.form.get('description')
            ingredient.usage_instructions = request.form.get('usage_instructions')
            ingredient.stock = int(request.form.get('stock'))

            # Handle file upload
            if 'image' in request.files:
                file = request.files['image']
                if file and file.filename and allowed_file(file.filename):
                    filename = secure_filename(file.filename)
                    filename = f"{datetime.utcnow().strftime('%Y%m%d%H%M%S')}_{filename}"
                    file.save(os.path.join(UPLOAD_FOLDER, filename))
                    ingredient.image = filename

            db.session.commit()

            flash('Ingredient updated successfully', 'success')
            return redirect(url_for('admin_ingredients'))

        return render_template('admin/edit_ingredient.html', ingredient=ingredient)

    @app.route('/admin/ingredient/delete/<int:id>')
    @login_required
    def admin_delete_ingredient(id):
        if current_user.role != 'admin':
            flash('Unauthorized access', 'danger')
            return redirect(url_for('index'))

        ingredient = Ingredient.query.get_or_404(id)
        db.session.delete(ingredient)
        db.session.commit()

        flash('Ingredient deleted successfully', 'success')
        return redirect(url_for('admin_ingredients'))

    # ==================== ADMIN - ORDERS ====================

    @app.route('/admin/orders')
    @login_required
    def admin_orders():
        if current_user.role != 'admin':
            flash('Unauthorized access', 'danger')
            return redirect(url_for('index'))

        orders = Order.query.order_by(Order.created_at.desc()).all()
        return render_template('admin/orders.html', orders=orders)

    @app.route('/admin/order/<int:id>/update-status', methods=['POST'])
    @login_required
    def admin_update_order_status(id):
        if current_user.role != 'admin':
            flash('Unauthorized access', 'danger')
            return redirect(url_for('index'))

        order = Order.query.get_or_404(id)
        order.order_status = request.form.get('order_status')

        db.session.commit()

        flash('Order status updated successfully', 'success')
        return redirect(url_for('admin_orders'))

    # ==================== ADMIN - USERS ====================

    @app.route('/admin/users')
    @login_required
    def admin_users():
        if current_user.role != 'admin':
            flash('Unauthorized access', 'danger')
            return redirect(url_for('index'))

        users = User.query.filter_by(role='user').order_by(User.created_at.desc()).all()
        return render_template('admin/users.html', users=users)

    # ==================== UTILITY ====================

    @app.route('/uploads/<filename>')
    def uploaded_file(filename):
        return send_from_directory(UPLOAD_FOLDER, filename)

    @app.context_processor
    def utility_processor():
        def format_currency(amount):
            return f"₹ {amount:,.2f}"

        def cart_count():
            if current_user.is_authenticated:
                return Cart.query.filter_by(user_id=current_user.id).count()
            return 0

        return dict(format_currency=format_currency, cart_count=cart_count)