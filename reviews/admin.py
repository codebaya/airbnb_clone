from django.contrib import admin

from .models import Review


class BadOrGood(admin.SimpleListFilter):
    title = 'Bad or good'
    parameter_name = "badorgood"

    def lookups(self, request, models_admin, ):
        return [
            ("bad", "Bad"),
            ("good", "Good"),
        ]

    def queryset(self, request, reviews):
        word = self.value()
        print(word)
        if word == "bad":
            return reviews.filter(rating__lt=4)
        elif word == "good":
            return reviews.filter(rating__gt=3)
        else:
            return reviews


class WordFilter(admin.SimpleListFilter):
    title = "Filter by Word"
    parameter_name = "word"

    def lookups(self, request, models_admin, ):
        return [
            ("good", "Good"),
            ("great", "Great"),
            ("awesome", "Awesome"),
        ]

    def queryset(self, request, reviews):
        word = self.value()
        if word != None:
            return reviews.filter(payload__contains=word)


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = (
        "__str__",
        "room",
        "payload",
        "rating",
    )
    list_filter = (
        WordFilter,
        BadOrGood,
        "room", "payload", "rating",
        "room__category", "user__is_host",
    )
