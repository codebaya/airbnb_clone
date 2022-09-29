from django.shortcuts import render

from .models import Room


def see_all_rooms(request):
	rooms = Room.objects.all()
	return render(
			request, "all_rooms.html",
			{ "rooms":rooms,
			  "title":"Hello! this title comes from django!!",
			  }
	)


def see_one_room(request, room_pk):
	try:
		room = Room.objects.get(pk=room_pk)
		return render(
				request, "room_details.html",
				{
					"room":room,
				}
		)
	except Room.DoesNotExist:
		return render(
				request, "room_details.html",
				{
					"not_found":True,
				},
		)

# def see_one_room(request, room_name):
# 	return HttpResponse(f"see_one_room_name : {room_name}")