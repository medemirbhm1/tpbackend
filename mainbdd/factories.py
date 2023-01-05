import factory
from factory.django import DjangoModelFactory

from .models import User, RealEstateAdd, Offer

class UserFactory(DjangoModelFactory):
    class Meta:
        model = User
    
    first_name = factory.Faker('first_name')
    last_name = factory.Faker('last_name')
    email = factory.Faker('free_email')
    phone_num = factory.Faker('phone_number')


class RealEstateAddFactory(DjangoModelFactory):
    class Meta:
        model = RealEstateAdd

    title = factory.Faker('sentence')
    description = factory.Faker('text',max_nb_chars=30)
    category = factory.Faker('word', ext_word_list=['Vente','Echange','Location','LocationPourVacances'])
    type = factory.Faker('word', ext_word_list=['Terrain','Maison','Appartement','TerrainAgricole'])
    surface = factory.Faker('random_int',max=100)
    price = factory.Faker('random_int',max=100)
    pub_date = factory.Faker('date')#watch out
    localisation = factory.Faker('sentence')#to improve
    wilaya = factory.Faker('word', ext_word_list=['Alger','Oran','Blida','Constantine'])
    commune = factory.Faker('word', ext_word_list=['DarElBeida','Kouba','HusseinDey'])
    #owner = factory.SubFactory(UserFactory)


class OfferFactory(DjangoModelFactory):
    class Meta:
        model=Offer

    description = factory.Faker('text', max_nb_chars=30)
    proposal = factory.Faker('random_int', max=100)
    #offerer = factory.SubFactory(UserFactory)
    #real_estate = factory.SubFactory(RealEstateAddFactory)


    