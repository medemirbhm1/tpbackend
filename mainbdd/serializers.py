from rest_framework import serializers
from .models import User, RealEstateAdd, Offer, Photo


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        #We'll start with the none relational fields... i don't think we need
        #_the relational ones ...
        fields = ['first_name','last_name','username','email','phone_num' , 'picture']


class PhotoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Photo
        fields = ['id','rea','photo']

class ReaSerializer(serializers.ModelSerializer):
    photos = PhotoSerializer(many=True)
    class Meta:
        model = RealEstateAdd
        fields = ['id','title','description','category','type','surface',
        'price','pub_date','localisation','wilaya','commune','owner','photos','longitude',
        'latitude']


class OfferSerializer(serializers.ModelSerializer):
    class Meta:
        model = Offer
        fields = ['id','description','proposal','offerer','real_estate']































#class ProfileSerializer(serializers.ModelSerializer):    
#     class Meta:
#         model = Profile
#         fields = ['name','age']


# class PhotoSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Photo
#         fields = ['photo','rea']
