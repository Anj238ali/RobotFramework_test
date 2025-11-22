"""
Test Data Generator
"""

from faker import Faker
import random
import logging


class TestDataGenerator:

    def __init__(self, locale='en_US'):

        self.faker = Faker(locale)
        self.logger = logging.getLogger(__name__)
    
    def generate_person_data(self):

        return {
            'first_name': self.faker.first_name(),
            'last_name': self.faker.last_name(),
            'full_name': self.faker.name(),
            'email': self.faker.email(),
            'phone': self.faker.phone_number(),
            'username': self.faker.user_name(),
            'password': self.faker.password(length=12, special_chars=True),
        }
    
    def generate_address_data(self):

        return {
            'street_address': self.faker.street_address(),
            'city': self.faker.city(),
            'state': self.faker.state(),
            'postal_code': self.faker.postcode(),
            'country': self.faker.country(),
            'latitude': self.faker.latitude(),
            'longitude': self.faker.longitude(),
        }
    
    def generate_company_data(self):

        return {
            'company_name': self.faker.company(),
            'job_title': self.faker.job(),
            'department': self.faker.bs(),
            'company_email': self.faker.company_email(),
        }
    
    def generate_checkout_data(self):

        return {
            'first_name': self.faker.first_name(),
            'last_name': self.faker.last_name(),
            'postal_code': self.faker.postcode(),
        }
    
    def generate_credit_card_data(self):

        return {
            'card_number': self.faker.credit_card_number(),
            'card_provider': self.faker.credit_card_provider(),
            'card_expire': self.faker.credit_card_expire(),
            'card_security_code': self.faker.credit_card_security_code(),
        }
    
    def generate_internet_data(self):

        return {
            'email': self.faker.email(),
            'username': self.faker.user_name(),
            'password': self.faker.password(),
            'url': self.faker.url(),
            'domain': self.faker.domain_name(),
            'ipv4': self.faker.ipv4(),
            'mac_address': self.faker.mac_address(),
        }
    
    def generate_text_data(self):

        return {
            'sentence': self.faker.sentence(),
            'paragraph': self.faker.paragraph(),
            'text': self.faker.text(),
            'word': self.faker.word(),
            'words': self.faker.words(nb=5),
        }
    
    def generate_random_number(self, min_value=1, max_value=100):

        return random.randint(min_value, max_value)
    
    def generate_random_choice(self, choices):

        return random.choice(choices)
    
    def generate_date_data(self):

        return {
            'date': self.faker.date(),
            'date_time': self.faker.date_time(),
            'future_date': self.faker.future_date(),
            'past_date': self.faker.past_date(),
            'time': self.faker.time(),
        }
    
    def generate_file_data(self):

        return {
            'file_name': self.faker.file_name(),
            'file_extension': self.faker.file_extension(),
            'file_path': self.faker.file_path(),
            'mime_type': self.faker.mime_type(),
        }
    
    def generate_product_data(self):

        return {
            'product_name': self.faker.catch_phrase(),
            'description': self.faker.text(max_nb_chars=200),
            'price': round(random.uniform(10.0, 1000.0), 2),
            'quantity': random.randint(1, 10),
            'sku': self.faker.ean13(),
            'barcode': self.faker.ean8(),
        }
    
    def generate_bulk_data(self, data_type='person', count=10):

        data_generators = {
            'person': self.generate_person_data,
            'address': self.generate_address_data,
            'company': self.generate_company_data,
            'checkout': self.generate_checkout_data,
            'product': self.generate_product_data,
        }
        
        generator = data_generators.get(data_type, self.generate_person_data)
        
        return [generator() for _ in range(count)]
    
    def get_random_user_credentials(self):

        return {
            'username': self.faker.user_name(),
            'password': self.faker.password(length=12, special_chars=True, digits=True, upper_case=True, lower_case=True)
        }
