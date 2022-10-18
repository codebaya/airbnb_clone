from django.core.exceptions import PermissionDenied
from django.db import transaction
from rest_framework.exceptions import NotAuthenticated, NotFound, ParseError
from rest_framework.response import Response
from rest_framework.status import HTTP_204_NO_CONTENT
from rest_framework.views import APIView

from categories.models import Category
from rooms.models import Amenity, Room
from rooms.serializers import AmenitySerializer, RoomDetailSerializer, RoomListSerializer


# /api/v1/rooms/Amenities
# /api/v1/rooms/Amenities/1

class Amenities(APIView):
	
	def get(self, request):
		all_amenities = Amenity.objects.all()
		serializer = AmenitySerializer(all_amenities, many=True)
		return Response(serializer.data)
	
	def post(self, request, ):
		serializer = AmenitySerializer(data=request.data)
		if serializer.is_valid():
			amenity = serializer.save()
			return Response(
					AmenitySerializer(amenity).data,
			)
		else:
			return Response(serializer.errors)


class AmenityDetail(APIView):
	
	def get_object(self, pk):
		try:
			return Amenity.objects.get(pk=pk)
		except Amenity.DoesNotExist:
			raise NotFound
	
	def get(self, request, pk):
		amenity = self.get_object(pk)
		serializer = AmenitySerializer(amenity)
		return Response(serializer.data)
	
	def put(self, request, pk):
		amenity = self.get_object(pk)
		serializer = AmenitySerializer(amenity, data=request.data, partial=True)
		if serializer.is_valid():
			updated_amenity = serializer.save()
			return Response(AmenitySerializer(updated_amenity).data)
		else:
			return Response(serializer.errors)
	
	def delete(self, request, pk):
		amenity = self.get_object(pk)
		amenity.delete()
		return Response(status=HTTP_204_NO_CONTENT)


class Rooms(APIView):
	
	def get(self, request):
		all_rooms = Room.objects.all()
		serializer = RoomListSerializer(all_rooms, many=True)
		return Response(serializer.data)
	
	def post(self, request):
		if request.user.is_authenticated:
			serializer = RoomDetailSerializer(data=request.data)
			if serializer.is_valid():
				category_pk = request.data.get("category")
				print(f"category_pk : {category_pk}")
				if not category_pk:
					raise ParseError("Category is required")
				try:
					category = Category.objects.get(pk=category_pk)
					print(f"category : {category}")
					if category.kind == Category.CategoryKindChoices.EXPERIENCE:
						raise ParseError("The category kind should be 'room'")
				
				except Category.DoesNotExist:
					raise ParseError("Category Not Found")
				try:
					with transaction.atomic():
						room = serializer.save(owner=request.user, category=category)
						amenities = request.data.get('amenities')
						for amenity_pk in amenities:
							amenity = Amenity.objects.get(pk=amenity_pk)
							room.amenities.add(amenity)
						serializer = RoomDetailSerializer(room)
						return Response(serializer.data)
				except:
					raise ParseError("Amenity not found")
			else:
				return Response(serializer.errors)
		else:
			raise NotAuthenticated


class RoomDetail(APIView):
	
	def get_object(self, pk):
		try:
			return Room.objects.get(pk=pk)
		except Room.DoesNotExist:
			raise NotFound
	
	def get(self, request, pk):
		room = self.get_object(pk)
		serializer = RoomDetailSerializer(room)
		return Response(serializer.data)
	
	def put(self, request, pk):
		room = self.get_object(pk)
		serializer = RoomDetailSerializer(room, data=request.data, partial=True)
		if serializer.is_valid():
			updated_room = serializer.save()
			return Response(RoomDetailSerializer(updated_room).data)
		else:
			return Response(serializer.errors)
	
	def delete(self, request, pk):
		room = self.get_object(pk)
		if not request.user.is_authenticated:
			raise NotAuthenticated
		if room.owner != request.user:
			raise PermissionDenied
		room.delete()
		return Response(status=HTTP_204_NO_CONTENT)

# from django.shortcuts import render
#
# from .models import Room
#
#
# def see_all_rooms(request):
# 	rooms = Room.objects.all()
# 	return render(
# 			request, "all_rooms.html",
# 			{ "rooms":rooms,
# 			  "title":"Hello! this title comes from django!!",
# 			  }
# 	)
#
#
# def see_one_room(request, room_pk):
# 	try:
# 		room = Room.objects.get(pk=room_pk)
# 		return render(
# 				request, "room_details.html",
# 				{
# 					"room":room,
# 				}
# 		)
# 	except Room.DoesNotExist:
# 		return render(
# 				request, "room_details.html",
# 				{
# 					"not_found":True,
# 				},
# 		)
#
# # def see_one_room(request, room_name):
# # 	return HttpResponse(f"see_one_room_name : {room_name}")