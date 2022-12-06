from django.conf import settings
from django.db import transaction
from django.utils import timezone
from rest_framework.exceptions import NotFound, ParseError, PermissionDenied
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from rest_framework.status import HTTP_204_NO_CONTENT
from rest_framework.views import APIView

from bookings.models import Booking
from bookings.serializers import PublicBookingSerializer
from categories.models import Category
from experiences.models import Perk, Experience
from experiences.serializers import PerkSerializer, ExperienceSerializer, ExperienceDetailSerializer, \
    CreateExperienceBookingSerializer


class Experiences(APIView):
    permission_classes = [IsAuthenticatedOrReadOnly]

    # pass

    def get(self, request):
        all_experiences = Experience.objects.all()
        serializer = ExperienceSerializer(all_experiences, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = ExperienceDetailSerializer(data=request.data)
        # print("serializer : ", serializer)
        if serializer.is_valid():
            category_pk = request.data.get('category')
            if not category_pk:
                raise ParseError("Category is required")
            try:
                category = Category.objects.get(pk=category_pk)
                print("category: %s", category)
                if category.kind == Category.CategoryKindChoices.ROOMS:
                    raise ParseError("The category kind should be experience")
            except Category.DoesNotExist:
                raise ParseError("Category Not Found")
            try:
                with transaction.atomic():
                    experience = serializer.save(host=request.user, category=category)
                    perks = request.data.get('perks')
                    for perks_pk in perks:
                        perk = Perk.objects.get(pk=perks_pk)
                        experience.perks.add(perk)
                        serializer = ExperienceDetailSerializer(experience)
                    return Response(serializer.data)
            except:
                raise ParseError("Perk Not Found")
        else:
            return Response(serializer.errors)


class ExperienceDetail(APIView):
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_object(self, pk):
        try:
            return Experience.objects.get(pk=pk)
        except Experience.DoesNotExist:
            raise NotFound

    def get(self, request, pk):
        experience = self.get_object(pk)
        print("experience2", experience)
        serializer = ExperienceDetailSerializer(experience, context={"request": request}, )
        return Response(serializer.data)

    def put(self, request, pk):
        experience = self.get_object(pk)
        serializer = ExperienceDetailSerializer(experience, data=request.data, partial=True)
        if serializer.is_valid():
            category_pk = request.data.get('category')
            if category_pk:
                try:
                    category = Category.objects.get(pk=category_pk)
                    if category.kind == Category.CategoryKindChoices.ROOMS:
                        raise ParseError("the category kind should be experience")
                except Category.DoesNotExist:
                    raise ParseError("Category does not exists")
            try:
                with transaction.atomic():
                    if category_pk:
                        experience = serializer.save(category=category)
                    else:
                        experience = serializer.save()
                    perks = request.data.get('perk')
                    for perk_pk in perks:
                        perk = Perk.objects.get(pk=perk_pk)
                        experience.perks.add(perk)
                        serializer = ExperienceDetailSerializer(experience)
                    return Response(serializer.data)
            except Exception:
                raise ParseError("perk not found")

        else:
            return Response(serializer.errors)

    def delete(self, request, pk):
        experience = self.get_object(pk)
        print("experience=owner", experience.name, request.user)
        if experience.host != request.user:
            raise PermissionDenied
        experience.delete()
        return Response(status=HTTP_204_NO_CONTENT)


class ExperienceBookings(APIView):
    def get_object(self, pk):
        try:
            return Experience.objects.get(pk=pk)
        except Experience.DoesNotExist:
            raise NotFound

    def get(self, request, pk):
        try:
            page = int(request.query_params.get("page", 1))
        except ValueError:
            page = 1
        page_size = settings.PAGE_SIZE
        start = (page - 1) * page_size
        end = start + page_size
        experience = self.get_object(pk)
        now = timezone.localtime(timezone.now())
        print("now: ", now, "type: ", type(now))
        bookings = Booking.objects.filter(
            experience=experience,
            kind=Booking.BookingKindChoices.EXPERIENCE,
            experience_time__gt=now,
        )[start:end]
        serializer = PublicBookingSerializer(
            bookings,
            many=True,
        )
        return Response(serializer.data)

    def post(self, request, pk):
        experience = self.get_object(pk)
        serializer = CreateExperienceBookingSerializer(data=request.data, )
        if serializer.is_valid():
            booking = serializer.save(
                experience=experience,
                user=request.user,
                kind=Booking.BookingKindChoices.EXPERIENCE, )
            serializer = PublicBookingSerializer(booking)
            return Response(serializer.data)
        else:
            return Response(serializer.errors)


class ExperienceBookingsDetail(APIView):
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_experience(self, pk):
        try:
            return Experience.objects.get(pk=pk)
        except Experience.DoesNotExist:
            raise NotFound

    def get_booking(self, pk):
        try:
            return Booking.objects.get(pk=pk)
        except Booking.DoesNotExist:
            raise NotFound

    def get(self, request, pk, booking_pk):
        booking = self.get_booking(booking_pk)
        return Response(PublicBookingSerializer(booking).data)

    def put(self, request, pk, booking_pk):
        booking = self.get_booking(booking_pk)
        if booking.user.pk != request.user.pk:
            raise PermissionDenied
        serializer = CreateExperienceBookingSerializer(booking, data=request.data, partial=True)

        if serializer.is_valid():
            booking = serializer.save()
            serializer = PublicBookingSerializer(booking)
            return Response(serializer.data)
        else:
            return Response(serializer.errors)

    def delete(self, request, pk, booking_pk):
        booking = self.get_booking(booking_pk)
        if booking.user.pk != request.user.pk:
            raise PermissionDenied
        booking.delete()
        return Response(status=HTTP_204_NO_CONTENT)


class Perks(APIView):

    def get(self, request):
        all_perks = Perk.objects.all()
        serializer = PerkSerializer(all_perks, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = PerkSerializer(data=request.data)
        if serializer.is_valid():
            perk = serializer.save()
            return Response(PerkSerializer(perk).data)
        else:
            return Response(serializer.errors)


class PerkDetail(APIView):

    def get_object(self, pk):
        try:
            return Perk.objects.get(pk=pk)
        except Perk.DoesNotExist:
            raise NotFound

    def get(self, request, pk):
        perk = self.get_object(pk)
        serializer = PerkSerializer(perk)
        return Response(serializer.data)

    def put(self, request, pk):
        perk = self.get_object(pk)
        serializer = PerkSerializer(perk, data=request.data, partial=True)
        if serializer.is_valid():
            updated_perk = serializer.save()
            return Response(PerkSerializer(updated_perk).data)
        else:
            return Response(serializer.errors)

    def delete(self, request, pk):
        perk = self.get_object(pk)
        perk.delete()
        return Response(status=HTTP_204_NO_CONTENT)
