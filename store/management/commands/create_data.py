from random import random, choice, randint, uniform

import faker.providers
from faker import Faker

from django.core.management.base import BaseCommand
from store.models import Product, Collection


COLLECTIONS = [
    "Shoes",
    "Boots",
    "Trainers",
    "Clothes",
    "Dress",
    "T-shirt",
    "Jeans",
    "Shirts",
    "PrintedShirts",
    "TankTops",
    "PoloShirt",
    "Beauty",
    "DIYTools",
    "GardenOutdoors",
    "Grocery",
    "HealthPersonalCare",
    "Lighting",
]


class Provider(faker.providers.BaseProvider):
    def collection(self):
        return self.random_element(COLLECTIONS)


class Command(BaseCommand):
    help = "Command Information"

    def handle(self, *args, **kwargs):
        fake = Faker()
        fake.add_provider(Provider)

        for _ in range(15):
            title = fake.unique.collection()
            Collection.objects.create(title=title)

        for _ in range(15):
            title = fake.text(max_nb_chars=30)
            description = fake.text(max_nb_chars=100)
            collections = Collection.objects.values_list("pk", flat=True)
            collection_id = choice(collections)
            inventory = randint(0, 100)
            price = round(uniform(50.99, 99.99), 2)
            Product.objects.create(
                title=title,
                description=description,
                price=price,
                inventory=inventory,
                collection_id=collection_id,
            )
