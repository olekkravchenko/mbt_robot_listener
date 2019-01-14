import time


class DUT(object):
    ROBOT_LIBRARY_SCOPE = 'TEST SUITE'

    def __init__(self):
        self.available_products = []
        self.selected_products = []
        self.selected_product_name = ''
        self.remove_product_name = ''
        self.checkout = False
        self.initialize()

    def initialize(self):
        self.available_products = list(map(lambda x, y: str(x) + str(y), ["product"]*10, xrange(10)))
        self.selected_products = []
        self.selected_product_name = ''
        self.remove_product_name = ''
        self.checkout = False

    def get_available_products(self):
        return self.available_products

    def get_selected_products(self):
        return self.selected_products

    def select_product_to_add(self, product):
        self.selected_product_name = product

    def select_product_to_remove(self, product):
        self.remove_product_name = product

    def get_selected_product_number(self):
        return len(self.selected_products)

    def press_add_product(self):
        self.selected_products.append(self.selected_product_name)
        time.sleep(2)

    def press_remove_product(self):
        self.selected_products = [product for product in self.selected_products if product != self.remove_product_name]
        time.sleep(2)

    def press_empty_cart(self):
        self.selected_products = []
        self.checkout = False
        time.sleep(2)

    def press_checkout(self):
        self.checkout = True
        time.sleep(2)

    def press_finish_checkout(self):
        self.checkout = False
        # Next line is commented on purpose, it triggers a test failure when transition from Checkout state to Empty Cart state is made
        # Uncomment to fix the failure
        # self.selected_products = []
        time.sleep(2)

    def empty_cart_button_is_visible(self):
        return bool(self.selected_products)

    def add_product_button_is_visible(self):
        return not self.checkout

    def remove_product_button_is_visible(self):
        return not self.checkout and bool(self.selected_products)

    def checkout_button_is_visible(self):
        return not self.checkout and bool(self.selected_products)
