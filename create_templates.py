#!/usr/bin/env python3
"""
Script to generate all remaining HTML templates for e-Nursery
"""

templates = {
    'plants.html': '''{% extends 'base.html' %}
{% block title %}Plants{% endblock %}
{% block content %}
<div class="container">
    <h2 class="mb-4">Browse Plants</h2>

    <div class="row mb-4">
        <div class="col-md-12">
            <form method="GET" class="row g-3">
                <div class="col-md-3">
                    <input type="text" name="search" class="form-control" placeholder="Search plants..." value="{{ request.args.get('search', '') }}">
                </div>
                <div class="col-md-2">
                    <select name="category" class="form-select">
                        <option value="">All Categories</option>
                        {% for cat in categories %}
                        <option value="{{ cat }}" {% if request.args.get('category') == cat %}selected{% endif %}>{{ cat }}</option>
                        {% endfor %}
                    </select>
                </div>
                <div class="col-md-2">
                    <input type="number" name="min_price" class="form-control" placeholder="Min ₹" value="{{ request.args.get('min_price', '') }}">
                </div>
                <div class="col-md-2">
                    <input type="number" name="max_price" class="form-control" placeholder="Max ₹" value="{{ request.args.get('max_price', '') }}">
                </div>
                <div class="col-md-2">
                    <div class="form-check mt-2">
                        <input type="checkbox" name="in_stock" value="true" class="form-check-input" {% if request.args.get('in_stock') %}checked{% endif %}>
                        <label class="form-check-label">In Stock Only</label>
                    </div>
                </div>
                <div class="col-md-1">
                    <button type="submit" class="btn btn-primary w-100">Filter</button>
                </div>
            </form>
        </div>
    </div>

    <div class="row g-4">
        {% for plant in plants %}
        <div class="col-md-3">
            <div class="card h-100">
                <div class="position-relative">
                    <img src="{{ url_for('static', filename='uploads/' + plant.image) }}" class="card-img-top" alt="{{ plant.name }}" style="height: 200px; object-fit: cover;">
                    {% if plant.is_low_stock %}
                    <span class="badge badge-low-stock position-absolute top-0 end-0 m-2">Low Stock</span>
                    {% elif plant.is_out_of_stock %}
                    <span class="badge badge-out-stock position-absolute top-0 end-0 m-2">Out of Stock</span>
                    {% endif %}
                </div>
                <div class="card-body">
                    <span class="badge bg-success mb-2">{{ plant.category }}</span>
                    <h5 class="card-title">{{ plant.name }}</h5>
                    <p class="card-text text-muted small">{{ plant.description[:80] }}...</p>
                    <div class="d-flex justify-content-between align-items-center">
                        <span class="price-tag">{{ format_currency(plant.price) }}</span>
                        {% if plant.average_rating > 0 %}
                        <span class="text-warning"><i class="bi bi-star-fill"></i> {{ "%.1f"|format(plant.average_rating) }}</span>
                        {% endif %}
                    </div>
                </div>
                <div class="card-footer bg-white border-0">
                    <a href="{{ url_for('plant_detail', id=plant.id) }}" class="btn btn-outline-primary w-100">View Details</a>
                </div>
            </div>
        </div>
        {% endfor %}
    </div>

    {% if plants|length == 0 %}
    <div class="alert alert-info text-center">No plants found matching your criteria.</div>
    {% endif %}
</div>
{% endblock %}''',

    'plant_detail.html': '''{% extends 'base.html' %}
{% block title %}{{ plant.name }}{% endblock %}
{% block content %}
<div class="container">
    <div class="row">
        <div class="col-md-5">
            <img src="{{ url_for('static', filename='uploads/' + plant.image) }}" class="img-fluid rounded shadow" alt="{{ plant.name }}">
        </div>
        <div class="col-md-7">
            <nav aria-label="breadcrumb">
                <ol class="breadcrumb">
                    <li class="breadcrumb-item"><a href="{{ url_for('index') }}">Home</a></li>
                    <li class="breadcrumb-item"><a href="{{ url_for('plants') }}">Plants</a></li>
                    <li class="breadcrumb-item active">{{ plant.name }}</li>
                </ol>
            </nav>

            <h2>{{ plant.name }}</h2>
            <span class="badge bg-success mb-3">{{ plant.category }}</span>

            {% if plant.average_rating > 0 %}
            <div class="mb-3">
                <span class="text-warning fs-5">
                    {% for i in range(plant.average_rating|int) %}★{% endfor %}
                    {% if plant.average_rating % 1 >= 0.5 %}☆{% endif %}
                </span>
                <span class="text-muted">({{ plant.reviews|length }} reviews)</span>
            </div>
            {% endif %}

            <h3 class="price-tag mb-4">{{ format_currency(plant.price) }}</h3>

            <p class="lead">{{ plant.description }}</p>

            <div class="card mb-4">
                <div class="card-body">
                    <h5>Care Instructions</h5>
                    <p><strong><i class="bi bi-sun"></i> Sunlight:</strong> {{ plant.sunlight }}</p>
                    <p><strong><i class="bi bi-droplet"></i> Water:</strong> {{ plant.water }}</p>
                    <p><strong><i class="bi bi-info-circle"></i> Care:</strong> {{ plant.care_instructions }}</p>
                </div>
            </div>

            <div class="mb-3">
                <strong>Stock:</strong> 
                {% if plant.is_out_of_stock %}
                <span class="badge bg-danger">Out of Stock</span>
                {% elif plant.is_low_stock %}
                <span class="badge bg-warning">{{ plant.stock }} left</span>
                {% else %}
                <span class="badge bg-success">In Stock ({{ plant.stock }})</span>
                {% endif %}
            </div>

            {% if current_user.is_authenticated %}
            <form method="POST" action="{{ url_for('add_to_cart') }}" class="mb-3">
                <input type="hidden" name="item_type" value="plant">
                <input type="hidden" name="item_id" value="{{ plant.id }}">
                <div class="row g-2">
                    <div class="col-auto">
                        <input type="number" name="quantity" class="form-control" value="1" min="1" max="{{ plant.stock }}" style="width: 80px;" {% if plant.is_out_of_stock %}disabled{% endif %}>
                    </div>
                    <div class="col-auto">
                        <button type="submit" class="btn btn-primary" {% if plant.is_out_of_stock %}disabled{% endif %}>
                            <i class="bi bi-cart-plus"></i> Add to Cart
                        </button>
                    </div>
                    <div class="col-auto">
                        {% if user_wishlist %}
                        <a href="{{ url_for('remove_from_wishlist', id=user_wishlist.id) }}" class="btn btn-danger">
                            <i class="bi bi-heart-fill"></i> Remove from Wishlist
                        </a>
                        {% else %}
                        <a href="{{ url_for('add_to_wishlist', plant_id=plant.id) }}" class="btn btn-outline-danger">
                            <i class="bi bi-heart"></i> Add to Wishlist
                        </a>
                        {% endif %}
                    </div>
                </div>
            </form>
            {% else %}
            <a href="{{ url_for('login') }}" class="btn btn-primary">Login to Purchase</a>
            {% endif %}
        </div>
    </div>

    <hr class="my-5">

    <h3>Customer Reviews</h3>
    {% if current_user.is_authenticated %}
    <form method="POST" action="{{ url_for('add_review', plant_id=plant.id) }}" class="mb-4">
        <div class="card">
            <div class="card-body">
                <h5>Write a Review</h5>
                <div class="mb-3">
                    <label class="form-label">Rating</label>
                    <select name="rating" class="form-select" required>
                        <option value="5">5 Stars - Excellent</option>
                        <option value="4">4 Stars - Good</option>
                        <option value="3">3 Stars - Average</option>
                        <option value="2">2 Stars - Below Average</option>
                        <option value="1">1 Star - Poor</option>
                    </select>
                </div>
                <div class="mb-3">
                    <label class="form-label">Comment</label>
                    <textarea name="comment" class="form-control" rows="3" required></textarea>
                </div>
                <button type="submit" class="btn btn-primary">Submit Review</button>
            </div>
        </div>
    </form>
    {% endif %}

    {% for review in reviews %}
    <div class="card mb-3">
        <div class="card-body">
            <div class="d-flex justify-content-between">
                <h6>{{ review.user.full_name or review.user.username }}</h6>
                <span class="text-warning">
                    {% for i in range(review.rating) %}★{% endfor %}
                </span>
            </div>
            <p class="mb-1">{{ review.comment }}</p>
            <small class="text-muted">{{ review.created_at.strftime('%d-%m-%Y') }}</small>
        </div>
    </div>
    {% endfor %}

    {% if related_plants %}
    <hr class="my-5">
    <h3>Related Plants</h3>
    <div class="row g-4">
        {% for p in related_plants %}
        <div class="col-md-3">
            <div class="card">
                <img src="{{ url_for('static', filename='uploads/' + p.image) }}" class="card-img-top" alt="{{ p.name }}" style="height: 150px; object-fit: cover;">
                <div class="card-body">
                    <h6 class="card-title">{{ p.name }}</h6>
                    <p class="price-tag mb-2">{{ format_currency(p.price) }}</p>
                    <a href="{{ url_for('plant_detail', id=p.id) }}" class="btn btn-sm btn-outline-primary">View</a>
                </div>
            </div>
        </div>
        {% endfor %}
    </div>
    {% endif %}
</div>
{% endblock %}''',

    'ingredients.html': '''{% extends 'base.html' %}
{% block title %}Garden Supplies{% endblock %}
{% block content %}
<div class="container">
    <h2 class="mb-4">Garden Supplies</h2>

    <div class="row mb-4">
        <div class="col-md-12">
            <form method="GET" class="row g-3">
                <div class="col-md-4">
                    <input type="text" name="search" class="form-control" placeholder="Search supplies..." value="{{ request.args.get('search', '') }}">
                </div>
                <div class="col-md-2">
                    <select name="type" class="form-select">
                        <option value="">All Types</option>
                        {% for t in types %}
                        <option value="{{ t }}" {% if request.args.get('type') == t %}selected{% endif %}>{{ t }}</option>
                        {% endfor %}
                    </select>
                </div>
                <div class="col-md-2">
                    <input type="number" name="min_price" class="form-control" placeholder="Min ₹" value="{{ request.args.get('min_price', '') }}">
                </div>
                <div class="col-md-2">
                    <input type="number" name="max_price" class="form-control" placeholder="Max ₹" value="{{ request.args.get('max_price', '') }}">
                </div>
                <div class="col-md-1">
                    <button type="submit" class="btn btn-primary w-100">Filter</button>
                </div>
            </form>
        </div>
    </div>

    <div class="row g-4">
        {% for ingredient in ingredients %}
        <div class="col-md-3">
            <div class="card h-100">
                <div class="position-relative">
                    <img src="{{ url_for('static', filename='uploads/' + ingredient.image) }}" class="card-img-top" alt="{{ ingredient.name }}" style="height: 200px; object-fit: cover;">
                    {% if ingredient.is_out_of_stock %}
                    <span class="badge badge-out-stock position-absolute top-0 end-0 m-2">Out of Stock</span>
                    {% elif ingredient.is_low_stock %}
                    <span class="badge badge-low-stock position-absolute top-0 end-0 m-2">Low Stock</span>
                    {% endif %}
                </div>
                <div class="card-body">
                    <span class="badge bg-info mb-2">{{ ingredient.type }}</span>
                    <h5 class="card-title">{{ ingredient.name }}</h5>
                    <p class="card-text text-muted small">{{ ingredient.description[:80] }}...</p>
                    <span class="price-tag">{{ format_currency(ingredient.price) }}</span>
                </div>
                <div class="card-footer bg-white border-0">
                    <a href="{{ url_for('ingredient_detail', id=ingredient.id) }}" class="btn btn-outline-info w-100">View Details</a>
                </div>
            </div>
        </div>
        {% endfor %}
    </div>

    {% if ingredients|length == 0 %}
    <div class="alert alert-info text-center">No supplies found matching your criteria.</div>
    {% endif %}
</div>
{% endblock %}''',

    'ingredient_detail.html': '''{% extends 'base.html' %}
{% block title %}{{ ingredient.name }}{% endblock %}
{% block content %}
<div class="container">
    <div class="row">
        <div class="col-md-5">
            <img src="{{ url_for('static', filename='uploads/' + ingredient.image) }}" class="img-fluid rounded shadow" alt="{{ ingredient.name }}">
        </div>
        <div class="col-md-7">
            <nav aria-label="breadcrumb">
                <ol class="breadcrumb">
                    <li class="breadcrumb-item"><a href="{{ url_for('index') }}">Home</a></li>
                    <li class="breadcrumb-item"><a href="{{ url_for('ingredients') }}">Garden Supplies</a></li>
                    <li class="breadcrumb-item active">{{ ingredient.name }}</li>
                </ol>
            </nav>

            <h2>{{ ingredient.name }}</h2>
            <span class="badge bg-info mb-3">{{ ingredient.type }}</span>

            <h3 class="price-tag mb-4">{{ format_currency(ingredient.price) }}</h3>

            <p class="lead">{{ ingredient.description }}</p>

            <div class="card mb-4">
                <div class="card-body">
                    <h5>Usage Instructions</h5>
                    <p>{{ ingredient.usage_instructions }}</p>
                </div>
            </div>

            <div class="mb-3">
                <strong>Stock:</strong> 
                {% if ingredient.is_out_of_stock %}
                <span class="badge bg-danger">Out of Stock</span>
                {% elif ingredient.is_low_stock %}
                <span class="badge bg-warning">{{ ingredient.stock }} left</span>
                {% else %}
                <span class="badge bg-success">In Stock ({{ ingredient.stock }})</span>
                {% endif %}
            </div>

            {% if current_user.is_authenticated %}
            <form method="POST" action="{{ url_for('add_to_cart') }}" class="mb-3">
                <input type="hidden" name="item_type" value="ingredient">
                <input type="hidden" name="item_id" value="{{ ingredient.id }}">
                <div class="row g-2">
                    <div class="col-auto">
                        <input type="number" name="quantity" class="form-control" value="1" min="1" max="{{ ingredient.stock }}" style="width: 80px;" {% if ingredient.is_out_of_stock %}disabled{% endif %}>
                    </div>
                    <div class="col-auto">
                        <button type="submit" class="btn btn-info text-white" {% if ingredient.is_out_of_stock %}disabled{% endif %}>
                            <i class="bi bi-cart-plus"></i> Add to Cart
                        </button>
                    </div>
                </div>
            </form>
            {% else %}
            <a href="{{ url_for('login') }}" class="btn btn-info text-white">Login to Purchase</a>
            {% endif %}
        </div>
    </div>

    {% if related_ingredients %}
    <hr class="my-5">
    <h3>Related Products</h3>
    <div class="row g-4">
        {% for ing in related_ingredients %}
        <div class="col-md-3">
            <div class="card">
                <img src="{{ url_for('static', filename='uploads/' + ing.image) }}" class="card-img-top" alt="{{ ing.name }}" style="height: 150px; object-fit: cover;">
                <div class="card-body">
                    <h6 class="card-title">{{ ing.name }}</h6>
                    <p class="price-tag mb-2">{{ format_currency(ing.price) }}</p>
                    <a href="{{ url_for('ingredient_detail', id=ing.id) }}" class="btn btn-sm btn-outline-info">View</a>
                </div>
            </div>
        </div>
        {% endfor %}
    </div>
    {% endif %}
</div>
{% endblock %}''',

    'cart.html': '''{% extends 'base.html' %}
{% block title %}Shopping Cart{% endblock %}
{% block content %}
<div class="container">
    <h2 class="mb-4">Shopping Cart</h2>

    {% if cart_items|length == 0 %}
    <div class="alert alert-info text-center">
        <i class="bi bi-cart-x fs-1"></i>
        <p class="mt-3">Your cart is empty</p>
        <a href="{{ url_for('plants') }}" class="btn btn-primary">Start Shopping</a>
    </div>
    {% else %}
    <div class="row">
        <div class="col-md-8">
            {% for item in cart_items %}
            {% set product = item.get_item() %}
            <div class="card mb-3">
                <div class="card-body">
                    <div class="row align-items-center">
                        <div class="col-md-2">
                            <img src="{{ url_for('static', filename='uploads/' + product.image) }}" class="img-fluid rounded" alt="{{ product.name }}">
                        </div>
                        <div class="col-md-4">
                            <h5>{{ product.name }}</h5>
                            <span class="badge bg-secondary">{{ item.item_type.title() }}</span>
                        </div>
                        <div class="col-md-2">
                            <p class="mb-0 fw-bold">{{ format_currency(product.price) }}</p>
                        </div>
                        <div class="col-md-2">
                            <form method="POST" action="{{ url_for('update_cart', id=item.id) }}" class="d-inline">
                                <input type="number" name="quantity" value="{{ item.quantity }}" min="1" max="{{ product.stock }}" class="form-control form-control-sm" onchange="this.form.submit()">
                            </form>
                        </div>
                        <div class="col-md-2 text-end">
                            <p class="mb-0 fw-bold">{{ format_currency(item.subtotal) }}</p>
                            <a href="{{ url_for('remove_from_cart', id=item.id) }}" class="btn btn-sm btn-danger mt-2">
                                <i class="bi bi-trash"></i> Remove
                            </a>
                        </div>
                    </div>
                </div>
            </div>
            {% endfor %}
        </div>

        <div class="col-md-4">
            <div class="card">
                <div class="card-body">
                    <h5 class="card-title">Order Summary</h5>
                    <hr>
                    <div class="d-flex justify-content-between mb-2">
                        <span>Subtotal:</span>
                        <span>{{ format_currency(subtotal) }}</span>
                    </div>
                    <div class="d-flex justify-content-between mb-2">
                        <span>GST (18%):</span>
                        <span>{{ format_currency(gst) }}</span>
                    </div>
                    <hr>
                    <div class="d-flex justify-content-between mb-3">
                        <strong>Total:</strong>
                        <strong class="price-tag">{{ format_currency(total) }}</strong>
                    </div>
                    <a href="{{ url_for('checkout') }}" class="btn btn-primary w-100">
                        Proceed to Checkout
                    </a>
                    <a href="{{ url_for('plants') }}" class="btn btn-outline-primary w-100 mt-2">
                        Continue Shopping
                    </a>
                </div>
            </div>
        </div>
    </div>
    {% endif %}
</div>
{% endblock %}''',

    'checkout.html': '''{% extends 'base.html' %}
{% block title %}Checkout{% endblock %}
{% block content %}
<div class="container">
    <h2 class="mb-4">Checkout</h2>

    <div class="row">
        <div class="col-md-8">
            <div class="card mb-4">
                <div class="card-body">
                    <h5 class="card-title">Shipping Address</h5>
                    <form method="POST" action="{{ url_for('place_order') }}" id="checkoutForm">
                        <div class="mb-3">
                            <label class="form-label">Full Name</label>
                            <input type="text" name="full_name" class="form-control" value="{{ current_user.full_name }}" required>
                        </div>
                        <div class="mb-3">
                            <label class="form-label">Phone</label>
                            <input type="tel" name="phone" class="form-control" value="{{ current_user.phone }}" required>
                        </div>
                        <div class="mb-3">
                            <label class="form-label">Address</label>
                            <textarea name="address" class="form-control" rows="2" required>{{ current_user.address }}</textarea>
                        </div>
                        <div class="row">
                            <div class="col-md-6 mb-3">
                                <label class="form-label">City</label>
                                <input type="text" name="city" class="form-control" value="{{ current_user.city }}" required>
                            </div>
                            <div class="col-md-6 mb-3">
                                <label class="form-label">State</label>
                                <input type="text" name="state" class="form-control" value="{{ current_user.state }}" required>
                            </div>
                        </div>
                        <div class="mb-3">
                            <label class="form-label">Pincode</label>
                            <input type="text" name="pincode" class="form-control" value="{{ current_user.pincode }}" required>
                        </div>

                        <h5 class="mt-4">Payment Method</h5>
                        <div class="mb-3">
                            <div class="form-check">
                                <input class="form-check-input" type="radio" name="payment_method" value="cod" id="cod" checked>
                                <label class="form-check-label" for="cod">
                                    Cash on Delivery (COD)
                                </label>
                            </div>
                            <div class="form-check">
                                <input class="form-check-input" type="radio" name="payment_method" value="upi" id="upi">
                                <label class="form-check-label" for="upi">
                                    UPI (Simulated)
                                </label>
                            </div>
                            <div class="form-check">
                                <input class="form-check-input" type="radio" name="payment_method" value="card" id="card">
                                <label class="form-check-label" for="card">
                                    Credit/Debit Card (Simulated)
                                </label>
                            </div>
                        </div>

                        <button type="submit" class="btn btn-success btn-lg w-100">
                            <i class="bi bi-check-circle"></i> Place Order
                        </button>
                    </form>
                </div>
            </div>
        </div>

        <div class="col-md-4">
            <div class="card">
                <div class="card-body">
                    <h5 class="card-title">Order Summary</h5>
                    <hr>

                    {% for item in cart_items %}
                    {% set product = item.get_item() %}
                    <div class="d-flex justify-content-between mb-2">
                        <span class="small">{{ product.name }} x {{ item.quantity }}</span>
                        <span class="small">{{ format_currency(item.subtotal) }}</span>
                    </div>
                    {% endfor %}

                    <hr>
                    <div class="d-flex justify-content-between mb-2">
                        <span>Subtotal:</span>
                        <span>{{ format_currency(subtotal) }}</span>
                    </div>
                    <div class="d-flex justify-content-between mb-2">
                        <span>GST (18%):</span>
                        <span>{{ format_currency(gst) }}</span>
                    </div>
                    <hr>
                    <div class="d-flex justify-content-between">
                        <strong>Total:</strong>
                        <strong class="price-tag">{{ format_currency(total) }}</strong>
                    </div>
                </div>
            </div>
        </div>
    </div>
</div>
{% endblock %}''',

    'order_confirmation.html': '''{% extends 'base.html' %}
{% block title %}Order Confirmed{% endblock %}
{% block content %}
<div class="container">
    <div class="text-center mb-5">
        <i class="bi bi-check-circle-fill text-success" style="font-size: 5rem;"></i>
        <h2 class="mt-3">Order Placed Successfully!</h2>
        <p class="lead">Thank you for your order. Your order has been placed successfully.</p>
    </div>

    <div class="row justify-content-center">
        <div class="col-md-8">
            <div class="card">
                <div class="card-body">
                    <h5 class="card-title">Order Details</h5>
                    <hr>
                    <div class="row mb-3">
                        <div class="col-md-6">
                            <p><strong>Order ID:</strong> #{{ order.id }}</p>
                            <p><strong>Tracking Number:</strong> {{ order.tracking_number }}</p>
                            <p><strong>Order Date:</strong> {{ order.created_at.strftime('%d-%m-%Y %H:%M') }}</p>
                        </div>
                        <div class="col-md-6">
                            <p><strong>Payment Method:</strong> {{ order.payment_method.upper() }}</p>
                            <p><strong>Payment Status:</strong> <span class="badge bg-info">{{ order.payment_status }}</span></p>
                            <p><strong>Order Status:</strong> <span class="badge bg-success">{{ order.order_status }}</span></p>
                        </div>
                    </div>

                    <h6>Shipping Address:</h6>
                    <p>{{ order.shipping_address }}</p>

                    <h6 class="mt-4">Order Items:</h6>
                    <table class="table">
                        <thead>
                            <tr>
                                <th>Item</th>
                                <th>Price</th>
                                <th>Quantity</th>
                                <th>Subtotal</th>
                            </tr>
                        </thead>
                        <tbody>
                            {% for item in order.order_items %}
                            <tr>
                                <td>{{ item.item_name }}</td>
                                <td>{{ format_currency(item.price) }}</td>
                                <td>{{ item.quantity }}</td>
                                <td>{{ format_currency(item.subtotal) }}</td>
                            </tr>
                            {% endfor %}
                        </tbody>
                        <tfoot>
                            <tr>
                                <th colspan="3" class="text-end">Total Amount:</th>
                                <th class="price-tag">{{ format_currency(order.total_amount) }}</th>
                            </tr>
                        </tfoot>
                    </table>

                    <div class="text-center mt-4">
                        <a href="{{ url_for('my_orders') }}" class="btn btn-primary">View My Orders</a>
                        <a href="{{ url_for('index') }}" class="btn btn-outline-primary">Continue Shopping</a>
                    </div>
                </div>
            </div>
        </div>
    </div>
</div>
{% endblock %}''',
}

# Write all templates
import os

template_dir = '/home/claude/e-nursery/templates'

for filename, content in templates.items():
    filepath = os.path.join(template_dir, filename)
    with open(filepath, 'w') as f:
        f.write(content)
    print(f"Created: {filename}")

print(f"\nCreated {len(templates)} templates successfully!")