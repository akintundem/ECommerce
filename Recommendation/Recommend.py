import json
import random as random
class Recommendation:
    RECOMMENDATION = 5
    def __init__(self):
        pass

    def get_recommendations(self,cursor):
        initial_preferences = []
        try:
            with open("db/inventory.json") as f:
                data = json.load(f)
                items = data['categories']
                for _ in range(0, self.RECOMMENDATION):
                    initial_preferences.append(items[random.randint(0, len(items) - 1)])
        except Exception as e:
            return None
        response = get_products_by_categories(initial_preferences, cursor)
        return response
    
    def get_recommendation_by_user(self, user_id, cursor):
        return None

def get_products_by_categories(categories, cursor):
        query = '''
            SELECT p.product_id, p.product_name, p.discounted_price, p.actual_price, p.discount_percentage, p.rating, p.rating_count, p.about_product, p.number_of_inventory, p.img_link
            FROM Products p
            INNER JOIN ProductCategories pc ON p.product_id = pc.product_id
            INNER JOIN Categories c ON pc.category_id = c.category_id
            WHERE c.name IN ({})
        '''.format(','.join(['?'] * len(categories)))
        cursor.execute(query, categories)
        rows = cursor.fetchall()[:3]
        products = []
        for row in rows:
            product = {
                'product_id': row[0],
                'product_name': row[1],
                'discounted_price': float(row[2]),
                'actual_price': float(row[3]),
                'discount_percentage': float(row[4]),
                'rating': float(row[5]),
                'rating_count': int(row[6]),
                'about_product': row[7],
                'number_of_inventory': int(row[8]),
                'img_link': row[9]
            }
            products.append(product)
        return json.dumps(products)
