from django.shortcuts import render
from rest_framework.response import Response
from django.views.decorators.csrf import csrf_exempt
from .models import User, RealEstateAdd, Photo, Offer
from .serializers import UserSerializer, ReaSerializer, OfferSerializer, PhotoSerializer
from rest_framework.decorators import api_view
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.parsers import MultiPartParser,FormParser
from .custom_renderers import PNGRenderer
from rest_framework.renderers import JSONRenderer
import jwt
import requests
from google.oauth2.credentials import Credentials 
from google.auth.transport.requests import Request
from google.auth import jwt as gjwt 





class UserDetail(APIView):
    def get(self, request, format=None):

        id_token  = request.headers.get('Authorization')
        
        try:
            user = getUser(id_token)
        except jwt.InvalidSignatureError:
            return Response({'detail':'User of user_id not found'},status=status.HTTP_400_BAD_REQUEST)
        
        
        serializer = UserSerializer(user)
        return Response(serializer.data, status=status.HTTP_302_FOUND)



"""...........RealEsateAdd(s) -Rea(s) for short- Management..........."""



"""--->>> View for the post_rea endpoint"""
class PostRea(APIView):
    
    #Class Configuration
    parser_classes=[MultiPartParser,FormParser]
    
    """->Posts a rea for the user defined by the user_id url agrument"""
    """->Body contains: uploaded_photos, title, description, ... RealEstateAdd Model fields"""
    def post(self, request, format=None):
        files = request.FILES.getlist('uploaded_photos')
        if files:
            request.data.pop('uploaded_photos')


        id_token  = request.headers.get('Authorization')
        try:
            user = getUser(id_token)
        except jwt.InvalidSignatureError:
            return Response({'detail':'User of user_id not found'},status=status.HTTP_400_BAD_REQUEST)
        
        

        request.data['owner'] = user.id
        serializer = ReaSerializer(data=request.data, partial=True)
        if serializer.is_valid():
            rea = serializer.save()
            for file in files:
                Photo(rea=rea, photo=file).save()
            serializer = ReaSerializer(rea)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(status=status.HTTP_400_BAD_REQUEST)


"""--->>> View for reas_of_user endpoint"""
class ReasOfUser(APIView):
    
   
    """->Gets all the reas of user defined by user_id url argument"""
    def get(self, request, format=None):
        id_token  = request.headers.get('Authorization')
        try:
            user = getUser(id_token)
        except jwt.InvalidSignatureError:
            return Response({'detail':'User of user_id not found'},status=status.HTTP_400_BAD_REQUEST)
        
        
        reasOfUser = user.ownedReas.all()
        serializer = ReaSerializer(reasOfUser, many=True)
        return Response(serializer.data, status=status.HTTP_302_FOUND)
    
    """->Delete a rea from the owned reas of user defined by user_id url argument"""
    """->Body contains: rea_to_delete_id"""
    def delete(self, request, format=None):
        id_token  = request.headers.get('Authorization')
        try:
            user = getUser(id_token)
        except jwt.InvalidSignatureError:
            return Response({'detail':'User of user_id not found'},status=status.HTTP_400_BAD_REQUEST)
        
        
        
        if 'rea_to_delete_id' not in request.data:
            return Response({'detail':'Missing rea_to_delete_id field'},status=status.HTTP_400_BAD_REQUEST)
        try:
            rea = RealEstateAdd.objects.get(pk=request.data['rea_to_delete_id'])
        except RealEstateAdd.DoesNotExist:
            return Response({'detail':'Rea does not exit'},status=status.HTTP_404_NOT_FOUND)
        
        if rea.owner.id != user.id:
            return Response({'detail':'Rea is not owned by user'},status=status.HTTP_400_BAD_REQUEST)
        
        rea.delete()
        return Response(status=status.HTTP_200_OK)
      
"""--->>>View for the search_for_reas endpoint"""          
class SearchForReas(APIView):

    """->Gets all the reas corresponding to the search criteria"""
    """->Body contains: search_field, type, wilaya, commune, start_date, end_date"""
    """->start/end_date must be formated YYYY-MM-DD"""
    def post(self, request, format=None):

        id_token  = request.headers.get('Authorization')
        try:
            user = getUser(id_token)
        except jwt.InvalidSignatureError:
            return Response({'detail':'User of user_id not found'},status=status.HTTP_400_BAD_REQUEST)
        
        
        
        
        if 'search_field' not in request.data:
            return Response({'detail':'Missing search_field JSON field'},status=status.HTTP_400_BAD_REQUEST)
            
        if request.data['search_field'] == '':
            q= RealEstateAdd.objects.all()
        else:
            key_words = request.data['search_field'].split()
            q = RealEstateAdd.objects.none()
            for key_word in key_words:
                q = q | RealEstateAdd.objects.filter(title__icontains=key_word) | RealEstateAdd.objects.filter(description__icontains=key_word)
                
        if request.data['type'] !='':
            q = q.filter(type=request.data['type'])
        if request.data['wilaya'] !='':
            q = q.filter(wilaya=request.data['wilaya'])
        if request.data['commune'] !='':
            q = q.filter(commune=request.data['commune'])
        if request.data['start_date'] != '':
            q = q.filter(pub_date__gte=request.data['start_date'])
        if request.data['end_date'] != '':
            q = q.filter(pub_date__lte=request.data['end_date'])
                    
        serializer = ReaSerializer(q, many=True)
        return Response(serializer.data, status=status.HTTP_302_FOUND)
        

"""--->>> View for rea_of_id endpoint"""
class ReaOfId(APIView):
    
    def get(self, request, rea_id, format=None):
        try:
            rea = RealEstateAdd.objects.get(pk=rea_id)
        except RealEstateAdd.DoesNotExist:
            return Response({'detail':'Rea does not exist'},status=status.HTTP_400_BAD_REQUEST)
        serializer = ReaSerializer(rea)
        return Response(serializer.data, status=status.HTTP_200_OK)



"""...........Favorit(s) -Fav(s) for short- Management..........."""



"""--->>> View for favs_of_user endpoint"""   
class FavsOfUser(APIView):
    """->Gets all the favorits of the user defined by user_id url argument"""
    def get(self, request, format=None):

        id_token  = request.headers.get('Authorization')

        try:
            user = getUser(id_token)
        except jwt.InvalidSignatureError:
            return Response({'detail':'User of user_id not found'},status=status.HTTP_400_BAD_REQUEST)
        
        
        favsOfUser = user.favorits.all()
        serializer = ReaSerializer(favsOfUser, many=True)
        return Response(serializer.data, status=status.HTTP_302_FOUND)
    
    """->Registers a new favorit for the user defined by user_id url argument"""
    """->Body contains: rea_id"""
    def post(self, request, format=None):

        id_token  = request.headers.get('Authorization')
        user = getUser(id_token)
        
        if 'rea_id' not in request.data:
            return Response({'detail':'rea_id missing in request body'},status=status.HTTP_400_BAD_REQUEST)
        
        try:
            rea = RealEstateAdd.objects.get(pk=request.data['rea_id'])
        except RealEstateAdd.DoesNotExist:
            return Response({'detail':'rea of rea_id was not found'}, status=status.HTTP_400_BAD_REQUEST)
        
        if rea.owner != user:
            user.favorits.add(rea)
            return Response(status=status.HTTP_200_OK)
        return Response({'detail':'Cannot add owned rea to favs'}, status=status.HTTP_400_BAD_REQUEST)
    
    """->Removes a rea from favorits of user defined by user_id url argument"""
    """->Body contains: rea_id"""
    def delete(self, request, format=None):
        id_token  = request.headers.get('Authorization')
        try:
            user = getUser(id_token)
        except jwt.InvalidSignatureError:
            return Response({'detail':'User of user_id not found'},status=status.HTTP_400_BAD_REQUEST)
        
        if 'rea_id' not in request.data:
            return Response({'detail':'rea_id missing in body'}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            rea = RealEstateAdd.objects.get(pk=request.data['rea_id'])
        except RealEstateAdd.DoesNotExist:
            return Response({'detail':'Rea of rea_id not found'}, status=status.HTTP_400_BAD_REQUEST)

        user.favorits.remove(rea)
        return Response(status=status.HTTP_200_OK)
        


"""...........Offers Managing..........."""



"""--->>> View for offers_made_by_user endpoint"""
class OffersMadeByUser(APIView):
    """->Gets all the offers made by the user defined by user_id"""
    def get(self, request, format=None):
        id_token  = request.headers.get('Authorization')
        try:
            user = getUser(id_token)
        except jwt.InvalidSignatureError:
            return Response({'detail':'User of user_id not found'},status=status.HTTP_400_BAD_REQUEST)
        
        
        offers = Offer.objects.filter(offerer=user)
        serializer = OfferSerializer(offers, many=True)
        return Response(serializer.data, status=status.HTTP_302_FOUND)


"""--->>> View for posting_offer endpoint"""
class PostingOffer(APIView):
    
    """->Posts a new offers for the rea definde by rea_id url terminal"""
    """->Body contains : description, proposal"""
    def post(self, request, rea_id, format=None):

        id_token  = request.headers.get('Authorization')
        try:
            user = getUser(id_token)
        except jwt.InvalidSignatureError:
            return Response({'detail':'User of user_id not found'},status=status.HTTP_400_BAD_REQUEST)
        
        
        
        try:
            rea = RealEstateAdd.objects.get(pk=rea_id)
        except RealEstateAdd.DoesNotExist:
            return Response({'detail':'Rea of rea_id not found'},status=status.HTTP_404_NOT_FOUND)
        
        if  'description' not in request.data or 'proposal' not in request.data:
            return Response({'detail':'fields missing in request body'}, status=status.HTTP_400_BAD_REQUEST)
        offer = Offer(
                description=request.data['description'],
                proposal=request.data['proposal'],
                offerer=user,
                real_estate=rea).save()
        serializer = OfferSerializer(offer)      
        return Response(serializer.data, status=status.HTTP_201_CREATED)


"""--->>> View for offers_of_rea endpoint"""
class OffersOfRea(APIView):
    
    """->Gets the offers related to the rea defined by rea_id"""
    def get(self, request, rea_id, format=None):

        id_token  = request.headers.get('Authorization')
        try:
            user = getUser(id_token)
        except jwt.InvalidSignatureError:
            return Response({'detail':'User of user_id not found'},status=status.HTTP_400_BAD_REQUEST)
        
        try:
            rea = RealEstateAdd.objects.get(pk=rea_id)
        except RealEstateAdd.DoesNotExist:
            return Response({'detail':'Rea of rea_id not found'},status=status.HTTP_404_NOT_FOUND)

        offersOfRea = rea.offers.all()
        serializer = OfferSerializer(offersOfRea, many=True)
        return Response(serializer.data, status=status.HTTP_302_FOUND)
    
   

        






#LOGIN PART

def getUser(token): 
    id_token = token.rsplit("Bearer ")[1]   
    user_json = jwt.decode(id_token,"secret", algorithms=["HS256"])
    try :
        user = User.objects.filter(email= user_json['email']).first()
    except User.DoesNotExist:
        raise User.DoesNotExist

    return user





@api_view(['POST'])
def login(request):
    token  = request.headers.get('Authorization')
    id_token = token.rsplit("Bearer ")[1]

    try:
        claims = gjwt.decode(id_token, verify=False) 
        token_valide = True
        user_data = {
        "first_name": claims["given_name"] ,
        "last_name":claims["family_name"] ,
        "email":claims["email"],
        "picture":claims["picture"],
        'username':claims["name"]
        }
    except RealEstateAdd.DoesNotExist:
        token_valide = False
        return Response({'detail':'token not valid'},status=status.HTTP_404_NOT_FOUND)
    

    

    user = UserSerializer(data =user_data)
    test = User.objects.filter(email= user_data["email"]).first()

    if token_valide:
        if not test :
            if user.is_valid():
                user.save()
                return Response({
                'token': jwt.encode(user_data ,"secret", algorithm="HS256"),
                'status' : "200_signup",
                } )
            else : return Response(
             'email and username are not identical'
        )
        else :
            return Response({
            'token': jwt.encode(user_data, "secret", algorithm="HS256"),
            'status' : "200_login"
            } )
    else :
        return Response(
        status=status.HTTP_404_NOT_FOUND
        )         
























# def sepu():
#     print('---------------------------')
#     print(' ')
# def sepd():
#     print(' ')
#     print('---------------------------')

# class ProfileUpload(APIView):
#     parser_classes=[MultiPartParser,FormParser]
    
#     def post(self, request, format=None):
#         files = request.FILES.getlist('uploaded_files')
#         if files:
#             request.data.pop('uploaded_files')
#         serializer = ProfileSerializer(data=request.data)
#         if serializer.is_valid():
#             pro = serializer.save()
#             pro_id = pro.id
#             for file in files:
#                 Photo(rea=pro, photo=file).save()
#             photos = pro.photos.all()
#             serializer = PhotoSerializer(photos, many=True)
#         return Response(serializer.data, status=status.HTTP_200_OK)

# class ProfileLoad(APIView):
#     #renderer_classes=[PNGRenderer]
#     def get(self, request,profile_id, format=None):
        
#         try:
#             profile = Profile.objects.get(pk=profile_id)
#         except Profile.DoesNotExist:
#             return Response(status=status.HTTP_404_NOT_FOUND)
        
#         serializer = ProfileSerializer(profile)
#         return Response(serializer.data, status=status.HTTP_200_OK)

# class ProfileImagesLoad(APIView):
#     renderer_classes=[PNGRenderer]
#     def get(self, request,profile_id, format=None):
        
#         try:
#             profile = Profile.objects.get(pk=profile_id)
#         except Profile.DoesNotExist:
#             return Response(status=status.HTTP_404_NOT_FOUND)
#         photos = []
#         for photo in profile.photos.all():
#             photos.append(photo.photo)
#         return Response({'loaded_photos':photos}, status=status.HTTP_200_OK)
    
            





# class ProfileUpload(APIView):
#     parser_classes=[MultiPartParser, FormParser]
#     renderer_classes=[PNGRenderer]
#     def post(self, request, format=None):
#         request.data['ufiles']
#         return Response(request.data['ufiles'], status=status.HTTP_200_OK)


#---------------------------------------------------------------------------#
#---------------------------------------------------------------------------#
#---------------------------------------------------------------------------#


# @api_view(['GET','POST'])
# def user_lc(request):
#     if request.method == 'GET':
#         users = User.objects.all()
#         serializer = UserSerializer(users, many=True)
#         return Response(serializer.data, status=status.HTTP_302_FOUND)
    
#     elif request.method =='POST':
#         serializer = UserSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# @api_view(['GET','DELETE','PUT'])
# def user_gdu(request,pk):
#     try:
#         user = User.objects.get(pk=pk)
#     except User.DoesNotExist:
#         return Response(status=status.HTTP_404_NOT_FOUND)

#     if request.method == 'GET':
#         serializer = UserSerializer(user)
#         return Response(serializer.data, status=status.HTTP_302_FOUND)
#     elif request.method == 'DELETE':
#         user.delete()
#         return Response(UserSerializer(User.objects.all(), many=True).data, status=status.HTTP_410_GONE)
#     elif request.method =='PUT':
#         serializer = UserSerializer(user, data=request.data, partial=True)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_200_OK)
#         return Response(status=status.HTTP_400_BAD_REQUEST)

# Create your views here.
