from django.core.management.base import BaseCommand
from mainbdd.models import User, RealEstateAdd, Offer
from mainbdd.factories import UserFactory, RealEstateAddFactory, OfferFactory
import random


def offersGen():
    reas = RealEstateAdd.objects.all()
    for rea in reas:
        users = User.objects.exclude(pk=rea.owner.id)
        nboffers = random.choice([0,1,2,3,4,5])
        for i in range(nboffers):
            OfferFactory(offerer=random.choice(users), real_estate=rea)
            


class Command(BaseCommand):
    def handle(self, **options):
        offersGen()
