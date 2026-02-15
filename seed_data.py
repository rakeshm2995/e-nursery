from app import app, db
from models import User, Plant, Ingredient, Order, OrderItem
from datetime import datetime, timedelta
import random


def seed_database():
    with app.app_context():
        # Clear existing data
        db.drop_all()
        db.create_all()

        print("🌱 Seeding database...")

        # Create Admin User
        admin = User(
            username='admin',
            email='admin@enursery.com',
            full_name='Admin User',
            phone='9876543210',
            address='123 Admin Street',
            city='Bangalore',
            state='Karnataka',
            pincode='560001',
            role='admin'
        )
        admin.set_password('admin123')
        db.session.add(admin)

        # Create Sample Users
        users_data = [
            {'username': 'rajesh_kumar', 'email': 'rajesh@gmail.com', 'full_name': 'Rajesh Kumar',
             'phone': '9876543211', 'city': 'Mumbai', 'state': 'Maharashtra', 'pincode': '400001'},
            {'username': 'priya_sharma', 'email': 'priya@gmail.com', 'full_name': 'Priya Sharma', 'phone': '9876543212',
             'city': 'Delhi', 'state': 'Delhi', 'pincode': '110001'},
            {'username': 'amit_patel', 'email': 'amit@gmail.com', 'full_name': 'Amit Patel', 'phone': '9876543213',
             'city': 'Ahmedabad', 'state': 'Gujarat', 'pincode': '380001'},
            {'username': 'sneha_reddy', 'email': 'sneha@gmail.com', 'full_name': 'Sneha Reddy', 'phone': '9876543214',
             'city': 'Hyderabad', 'state': 'Telangana', 'pincode': '500001'},
            {'username': 'vikram_singh', 'email': 'vikram@gmail.com', 'full_name': 'Vikram Singh',
             'phone': '9876543215', 'city': 'Jaipur', 'state': 'Rajasthan', 'pincode': '302001'},
        ]

        users = []
        for user_data in users_data:
            user = User(**user_data, address=f"{random.randint(1, 999)} Garden Road", role='user')
            user.set_password('password123')
            users.append(user)
            db.session.add(user)

        print("✓ Users created")

        # Create Medicinal Plants
        medicinal_plants = [
            {
                'name': 'Tulsi (Holy Basil)',
                'category': 'Medicinal',
                'price': 150.00,
                'description': 'Sacred plant known for its medicinal properties. Excellent for respiratory health, immunity booster, and stress relief.',
                'sunlight': 'Full Sun (6-8 hours)',
                'water': 'Moderate - Keep soil moist',
                'care_instructions': 'Tulsi thrives in warm climate. Water regularly but avoid waterlogging. Pinch off flowers to promote leaf growth. Can be grown in pots or ground.',
                'stock': 45,
                'image': 'default_plant.jpg'
            },
            {
                'name': 'Aloe Vera',
                'category': 'Medicinal',
                'price': 120.00,
                'description': 'Succulent plant with gel-filled leaves. Great for skin care, burns, digestion, and air purification.',
                'sunlight': 'Bright Indirect Light',
                'water': 'Low - Water once a week',
                'care_instructions': 'Aloe vera prefers well-draining soil. Water deeply but infrequently. Perfect for beginners. Can tolerate some neglect.',
                'stock': 60,
                'image': 'default_plant.jpg'
            },
            {
                'name': 'Neem Tree',
                'category': 'Medicinal',
                'price': 250.00,
                'description': 'Powerful medicinal tree. Known for antibacterial, antifungal properties. Every part is useful - leaves, bark, seeds.',
                'sunlight': 'Full Sun',
                'water': 'Moderate',
                'care_instructions': 'Neem is hardy and drought-resistant once established. Requires minimal care. Can be grown in large pots or ground.',
                'stock': 30,
                'image': 'default_plant.jpg'
            },
            {
                'name': 'Mint (Pudina)',
                'category': 'Medicinal',
                'price': 80.00,
                'description': 'Aromatic herb perfect for teas, chutneys, and medicinal use. Helps in digestion and fresh breath.',
                'sunlight': 'Partial Shade to Full Sun',
                'water': 'High - Keep soil consistently moist',
                'care_instructions': 'Mint grows vigorously and spreads quickly. Best grown in containers to control spread. Harvest regularly for bushy growth.',
                'stock': 3,
                'image': 'default_plant.jpg'
            },
            {
                'name': 'Ashwagandha',
                'category': 'Medicinal',
                'price': 180.00,
                'description': 'Ancient medicinal herb known as Indian ginseng. Helps reduce stress, anxiety, and boosts immunity.',
                'sunlight': 'Full Sun',
                'water': 'Low to Moderate',
                'care_instructions': 'Ashwagandha prefers dry climate and well-drained soil. Roots are harvested after 6-7 months for medicinal use.',
                'stock': 25,
                'image': 'default_plant.jpg'
            },
        ]

        # Create Flower Plants
        flower_plants = [
            {
                'name': 'Rose Plant (Desi Gulab)',
                'category': 'Flower',
                'price': 200.00,
                'description': 'Classic fragrant rose plant. Produces beautiful blooms. Perfect for Indian gardens and balconies.',
                'sunlight': 'Full Sun (6+ hours)',
                'water': 'Moderate - Water daily in summer',
                'care_instructions': 'Roses need regular feeding and pruning. Remove dead flowers to encourage new blooms. Protect from pests.',
                'stock': 40,
                'image': 'default_plant.jpg'
            },
            {
                'name': 'Marigold (Genda)',
                'category': 'Flower',
                'price': 60.00,
                'description': 'Vibrant orange and yellow flowers. Auspicious plant for Indian festivals. Easy to grow and maintain.',
                'sunlight': 'Full Sun',
                'water': 'Moderate',
                'care_instructions': 'Marigold is very easy to grow. Deadhead regularly for continuous flowering. Can be grown from seeds.',
                'stock': 80,
                'image': 'default_plant.jpg'
            },
            {
                'name': 'Jasmine (Mogra)',
                'category': 'Flower',
                'price': 175.00,
                'description': 'Highly fragrant white flowers. Used in worship and perfumes. Night-blooming variety available.',
                'sunlight': 'Full Sun to Partial Shade',
                'water': 'Moderate to High',
                'care_instructions': 'Jasmine needs support for climbing. Water regularly during flowering season. Prune after flowering.',
                'stock': 35,
                'image': 'default_plant.jpg'
            },
            {
                'name': 'Bougainvillea',
                'category': 'Flower',
                'price': 220.00,
                'description': 'Stunning colorful bracts in pink, purple, orange. Drought-tolerant and long-flowering climber.',
                'sunlight': 'Full Sun',
                'water': 'Low to Moderate',
                'care_instructions': 'Bougainvillea loves heat and sun. Reduce water in winter. Prune to maintain shape. Thorny plant.',
                'stock': 28,
                'image': 'default_plant.jpg'
            },
            {
                'name': 'Hibiscus (Gudhal)',
                'category': 'Flower',
                'price': 140.00,
                'description': 'Large showy flowers in various colors. Used in worship. Attracts butterflies and hummingbirds.',
                'sunlight': 'Full Sun',
                'water': 'Moderate to High',
                'care_instructions': 'Hibiscus needs regular watering and feeding. Flowers bloom for one day. Prune to encourage bushiness.',
                'stock': 4,
                'image': 'default_plant.jpg'
            },
        ]

        # Create Vegetable Plants
        vegetable_plants = [
            {
                'name': 'Tomato Plant',
                'category': 'Vegetable',
                'price': 90.00,
                'description': 'Fresh homegrown tomatoes. Hybrid variety suitable for Indian climate. High yielding.',
                'sunlight': 'Full Sun (6-8 hours)',
                'water': 'Regular - Keep soil evenly moist',
                'care_instructions': 'Provide support with stakes. Feed with organic fertilizer. Pinch off suckers for better yield.',
                'stock': 50,
                'image': 'default_plant.jpg'
            },
            {
                'name': 'Chilli Plant (Mirchi)',
                'category': 'Vegetable',
                'price': 70.00,
                'description': 'Spicy green chillies. Compact plant suitable for pots. Produces chillies throughout the year.',
                'sunlight': 'Full Sun',
                'water': 'Moderate',
                'care_instructions': 'Chilli plants love heat. Water regularly but avoid overwatering. Harvest when green or red.',
                'stock': 65,
                'image': 'default_plant.jpg'
            },
            {
                'name': 'Brinjal Plant (Baingan)',
                'category': 'Vegetable',
                'price': 85.00,
                'description': 'Purple eggplant variety. Perfect for curries and bharta. Produces 15-20 fruits per plant.',
                'sunlight': 'Full Sun',
                'water': 'Regular watering',
                'care_instructions': 'Brinjal needs warm weather. Support may be needed for heavy fruits. Watch for pests.',
                'stock': 42,
                'image': 'default_plant.jpg'
            },
            {
                'name': 'Coriander (Dhania)',
                'category': 'Vegetable',
                'price': 50.00,
                'description': 'Fresh coriander leaves for garnishing. Fast-growing herb. Can be grown year-round.',
                'sunlight': 'Partial Shade to Full Sun',
                'water': 'Keep soil moist',
                'care_instructions': 'Coriander prefers cool weather. Harvest leaves regularly. Sow seeds every 2-3 weeks for continuous supply.',
                'stock': 2,
                'image': 'default_plant.jpg'
            },
            {
                'name': 'Lady Finger (Bhindi)',
                'category': 'Vegetable',
                'price': 75.00,
                'description': 'Okra plant perfect for Indian cooking. High yielding and easy to grow in summer.',
                'sunlight': 'Full Sun',
                'water': 'Regular but not excessive',
                'care_instructions': 'Lady finger loves hot weather. Harvest young tender pods regularly. Add organic compost.',
                'stock': 38,
                'image': 'default_plant.jpg'
            },
        ]

        # Create Fruit Plants
        fruit_plants = [
            {
                'name': 'Lemon Plant (Nimbu)',
                'category': 'Fruit',
                'price': 350.00,
                'description': 'Dwarf lemon variety perfect for pots. Produces juicy lemons. Fragrant flowers.',
                'sunlight': 'Full Sun (8+ hours)',
                'water': 'Regular, keep soil moist',
                'care_instructions': 'Lemon plants need regular feeding. Protect from extreme cold. Produces fruit in 2-3 years.',
                'stock': 25,
                'image': 'default_plant.jpg'
            },
            {
                'name': 'Pomegranate (Anar)',
                'category': 'Fruit',
                'price': 400.00,
                'description': 'Ruby-red fruit loaded with antioxidants. Ornamental flowers. Can be grown in large pots.',
                'sunlight': 'Full Sun',
                'water': 'Moderate - drought tolerant',
                'care_instructions': 'Pomegranate is hardy and low-maintenance. Prune to control shape. Bears fruit in 2-3 years.',
                'stock': 18,
                'image': 'default_plant.jpg'
            },
            {
                'name': 'Guava Plant (Amrud)',
                'category': 'Fruit',
                'price': 300.00,
                'description': 'Tropical fruit tree. Sweet and aromatic fruits. High in Vitamin C. Grows well in Indian climate.',
                'sunlight': 'Full Sun',
                'water': 'Regular watering',
                'care_instructions': 'Guava is easy to grow and fast-growing. Produces fruit in 2-3 years. Prune annually.',
                'stock': 22,
                'image': 'default_plant.jpg'
            },
            {
                'name': 'Papaya Plant',
                'category': 'Fruit',
                'price': 150.00,
                'description': 'Fast-growing fruit plant. Produces nutritious fruits in 8-10 months. Great for small gardens.',
                'sunlight': 'Full Sun',
                'water': 'Regular, well-drained soil',
                'care_instructions': 'Papaya grows very fast. Needs support when fruiting. Sensitive to frost and cold.',
                'stock': 5,
                'image': 'default_plant.jpg'
            },
            {
                'name': 'Curry Leaf Plant',
                'category': 'Fruit',
                'price': 180.00,
                'description': 'Essential for Indian cooking. Aromatic leaves used in tempering. Easy to grow and maintain.',
                'sunlight': 'Partial Shade to Full Sun',
                'water': 'Regular watering',
                'care_instructions': 'Curry leaf plant grows slowly initially. Harvest leaves regularly. Protect from extreme cold.',
                'stock': 32,
                'image': 'default_plant.jpg'
            },
        ]

        # Add all plants to database
        all_plants = medicinal_plants + flower_plants + vegetable_plants + fruit_plants
        for plant_data in all_plants:
            plant = Plant(**plant_data)
            db.session.add(plant)

        print("✓ Plants created")

        # Create Gardening Ingredients
        ingredients_data = [
            {
                'name': 'Organic Vermicompost (5kg)',
                'type': 'Fertilizer',
                'price': 250.00,
                'description': 'Premium quality vermicompost made from earthworm castings. Rich in nutrients and beneficial microorganisms.',
                'usage_instructions': 'Mix 1 part vermicompost with 3 parts soil. Apply as top dressing every 30 days. Excellent for all plants.',
                'stock': 100,
                'image': 'default_ingredient.jpg'
            },
            {
                'name': 'NPK Fertilizer 19:19:19 (1kg)',
                'type': 'Fertilizer',
                'price': 180.00,
                'description': 'Balanced NPK fertilizer for healthy plant growth. Water-soluble for quick absorption.',
                'usage_instructions': 'Mix 5-10 grams per liter of water. Apply every 15 days during growing season. Avoid over-application.',
                'stock': 75,
                'image': 'default_ingredient.jpg'
            },
            {
                'name': 'Neem Oil Organic Pesticide (500ml)',
                'type': 'Fertilizer',
                'price': 320.00,
                'description': 'Natural pesticide and fungicide. Safe for organic gardening. Controls pests and diseases.',
                'usage_instructions': 'Mix 5ml neem oil per liter water. Spray on plants in evening. Apply weekly for pest control.',
                'stock': 55,
                'image': 'default_ingredient.jpg'
            },
            {
                'name': 'Bone Meal Fertilizer (2kg)',
                'type': 'Fertilizer',
                'price': 200.00,
                'description': 'Rich in phosphorus for root development and flowering. Slow-release organic fertilizer.',
                'usage_instructions': 'Mix 100g per medium-sized pot. Apply during planting and flowering season. Good for flowering plants.',
                'stock': 4,
                'image': 'default_ingredient.jpg'
            },
            {
                'name': 'Cocopeat Block (5kg)',
                'type': 'Soil',
                'price': 150.00,
                'description': 'Compressed coconut coir. Excellent soil conditioner. Retains moisture and improves drainage.',
                'usage_instructions': 'Soak in water to expand. Mix with soil in 1:1 ratio. Ideal for seed starting and potting mix.',
                'stock': 90,
                'image': 'default_ingredient.jpg'
            },
            {
                'name': 'Garden Soil Mix (10kg)',
                'type': 'Soil',
                'price': 120.00,
                'description': 'Ready-to-use potting mix. Blend of soil, compost, and organic matter. pH balanced.',
                'usage_instructions': 'Use directly for potting plants. Suitable for most indoor and outdoor plants. No mixing required.',
                'stock': 110,
                'image': 'default_ingredient.jpg'
            },
            {
                'name': 'Perlite (1kg)',
                'type': 'Soil',
                'price': 180.00,
                'description': 'Volcanic glass for improved aeration and drainage. Prevents soil compaction.',
                'usage_instructions': 'Mix 10-20% perlite with potting soil. Essential for succulents and cacti. Lightweight and sterile.',
                'stock': 45,
                'image': 'default_ingredient.jpg'
            },
            {
                'name': 'Ceramic Pot with Drainage (10 inch)',
                'type': 'Pot',
                'price': 350.00,
                'description': 'Beautiful ceramic planter with drainage hole. Durable and decorative. Multiple colors available.',
                'usage_instructions': 'Place broken pieces at bottom for drainage. Fill with potting mix. Suitable for medium-sized plants.',
                'stock': 35,
                'image': 'default_ingredient.jpg'
            },
            {
                'name': 'Plastic Grow Bag Set (5 pieces)',
                'type': 'Pot',
                'price': 150.00,
                'description': 'UV-stabilized grow bags. Breathable fabric pots. Set of 5 bags (12 inch size).',
                'usage_instructions': 'Excellent drainage and air pruning. Reusable and easy to store. Perfect for vegetables and herbs.',
                'stock': 2,
                'image': 'default_ingredient.jpg'
            },
            {
                'name': 'Terracotta Pot (8 inch)',
                'type': 'Pot',
                'price': 120.00,
                'description': 'Traditional clay pot. Porous and allows roots to breathe. Natural earthy look.',
                'usage_instructions': 'Soak in water before first use. Water plants more frequently. Perfect for succulents and herbs.',
                'stock': 60,
                'image': 'default_ingredient.jpg'
            },
            {
                'name': 'Garden Tool Set (5 pieces)',
                'type': 'Tools',
                'price': 450.00,
                'description': 'Essential gardening tools set. Includes trowel, fork, pruner, rake, and cultivator. Rust-resistant.',
                'usage_instructions': 'Clean tools after use. Store in dry place. Sharpen pruner regularly for clean cuts.',
                'stock': 30,
                'image': 'default_ingredient.jpg'
            },
            {
                'name': 'Watering Can (5 Liter)',
                'type': 'Tools',
                'price': 280.00,
                'description': 'Durable plastic watering can with long spout. Detachable rose for gentle watering.',
                'usage_instructions': 'Fill with water and gently pour. Use rose attachment for seedlings. Clean regularly.',
                'stock': 42,
                'image': 'default_ingredient.jpg'
            },
            {
                'name': 'Garden Sprayer (1.5 Liter)',
                'type': 'Tools',
                'price': 320.00,
                'description': 'Pressure sprayer for pesticides and fertilizers. Adjustable nozzle. Ergonomic design.',
                'usage_instructions': 'Fill liquid, pump to pressurize, and spray. Clean thoroughly after use. Wear protective gear.',
                'stock': 25,
                'image': 'default_ingredient.jpg'
            },
            {
                'name': 'Gardening Gloves (1 Pair)',
                'type': 'Tools',
                'price': 150.00,
                'description': 'Heavy-duty gardening gloves. Protects hands from thorns and dirt. Breathable and comfortable.',
                'usage_instructions': 'Wear while handling plants and soil. Wash with soap and dry after use. Choose correct size.',
                'stock': 3,
                'image': 'default_ingredient.jpg'
            },
            {
                'name': 'Tomato Seeds (Hybrid)',
                'type': 'Seeds',
                'price': 60.00,
                'description': 'High-yielding tomato seeds. Disease-resistant variety. Suitable for Indian climate.',
                'usage_instructions': 'Sow in seedling tray. Transplant after 3-4 weeks. Germination in 7-10 days. Optimal temperature 20-30°C.',
                'stock': 150,
                'image': 'default_ingredient.jpg'
            },
            {
                'name': 'Chilli Seeds (Green)',
                'type': 'Seeds',
                'price': 50.00,
                'description': 'Hot chilli pepper seeds. Long and slender variety. Continuous harvesting possible.',
                'usage_instructions': 'Sow directly or in seedling tray. Keep soil moist. Germination in 10-15 days. Harvest in 60-80 days.',
                'stock': 120,
                'image': 'default_ingredient.jpg'
            },
            {
                'name': 'Marigold Seeds Mix',
                'type': 'Seeds',
                'price': 40.00,
                'description': 'Colorful marigold flower seeds. Mix of orange and yellow varieties. Easy to grow.',
                'usage_instructions': 'Sow directly in soil. Water lightly. Germination in 5-7 days. Flowers appear in 45-50 days.',
                'stock': 180,
                'image': 'default_ingredient.jpg'
            },
            {
                'name': 'Coriander Seeds (Dhania)',
                'type': 'Seeds',
                'price': 35.00,
                'description': 'Fresh coriander herb seeds. Fast-growing. Suitable for year-round cultivation.',
                'usage_instructions': 'Sow thickly in rows. Keep soil moist. Germination in 7-10 days. Start harvesting in 3-4 weeks.',
                'stock': 200,
                'image': 'default_ingredient.jpg'
            },
            {
                'name': 'Sunflower Seeds (Giant)',
                'type': 'Seeds',
                'price': 80.00,
                'description': 'Giant sunflower variety. Grows up to 6-8 feet tall. Produces large flower heads.',
                'usage_instructions': 'Sow directly in ground. Space 1-2 feet apart. Germination in 7-10 days. Requires full sun.',
                'stock': 95,
                'image': 'default_ingredient.jpg'
            },
            {
                'name': 'Mixed Vegetable Seeds Pack',
                'type': 'Seeds',
                'price': 120.00,
                'description': 'Variety pack with 10 different vegetable seeds. Perfect for kitchen garden beginners.',
                'usage_instructions': 'Follow individual seed instructions. Sow according to season. Water regularly and provide adequate sunlight.',
                'stock': 65,
                'image': 'default_ingredient.jpg'
            },
        ]

        for ingredient_data in ingredients_data:
            ingredient = Ingredient(**ingredient_data)
            db.session.add(ingredient)

        print("✓ Ingredients created")

        # Create Sample Orders
        db.session.commit()  # Commit to get IDs

        plants_list = Plant.query.all()
        ingredients_list = Ingredient.query.all()

        order_statuses = ['Delivered', 'Delivered', 'Delivered', 'Delivered', 'Shipped', 'Packed', 'Confirmed',
                          'Pending', 'Cancelled', 'Delivered']

        for i in range(10):
            user = random.choice(users)
            num_items = random.randint(1, 4)

            order = Order(
                user_id=user.id,
                total_amount=0,
                order_status=order_statuses[i],
                payment_status='Completed' if order_statuses[i] != 'Cancelled' else 'Failed',
                payment_method=random.choice(['cod', 'upi', 'card']),
                shipping_address=f"{user.address}, {user.city}, {user.state} - {user.pincode}",
                estimated_delivery=datetime.utcnow() + timedelta(days=random.randint(1, 10)),
                created_at=datetime.utcnow() - timedelta(days=random.randint(1, 30))
            )
            order.generate_tracking_number()
            db.session.add(order)
            db.session.flush()

            order_total = 0

            for _ in range(num_items):
                item_type = random.choice(['plant', 'ingredient'])

                if item_type == 'plant':
                    item = random.choice(plants_list)
                else:
                    item = random.choice(ingredients_list)

                quantity = random.randint(1, 3)
                subtotal = item.price * quantity
                order_total += subtotal

                order_item = OrderItem(
                    order_id=order.id,
                    item_type=item_type,
                    item_id=item.id,
                    item_name=item.name,
                    quantity=quantity,
                    price=item.price,
                    subtotal=subtotal
                )
                db.session.add(order_item)

            # Add GST
            order_total_with_gst = order_total * 1.18
            order.total_amount = order_total_with_gst

        db.session.commit()
        print("✓ Orders created")

        print("✅ Database seeded successfully!")
        print("\n" + "=" * 50)
        print("LOGIN CREDENTIALS:")
        print("=" * 50)
        print("\n🔐 Admin Account:")
        print("   Username: admin")
        print("   Password: admin123")
        print("\n👤 User Accounts:")
        print("   Username: rajesh_kumar, priya_sharma, amit_patel, etc.")
        print("   Password: password123 (for all users)")
        print("\n" + "=" * 50)


if __name__ == '__main__':
    seed_database()