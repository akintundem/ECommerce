class Cart:
    def __init__(self):
        pass

    def add_product(self, product):
        self.storage.save(product)

    def remove_product(self, product):
        self.storage.delete(product)

    def get_user_products(self):
        return self.storage.get_all()