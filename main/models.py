from django.db import models
from django.contrib.auth.models import User


class City(models.Model):
    name = models.CharField(max_length=255)
    possibilities = models.CharField(max_length=255, blank=True, null=True)
    is_blocked = models.BooleanField(default=True)

    def __str__(self):
        return self.name


class CityGroups(models.Model):
    name = models.CharField(max_length=255)
    cities = models.ManyToManyField(City)

    def __str__(self):
        return self.name


class BasicUser(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    city = models.ForeignKey(City, on_delete=models.CASCADE)
    phone_number = models.CharField(max_length=90)
    profile_img = models.ImageField(
        upload_to="profile_pictures/", null=True, blank=True
    )
    location = models.ForeignKey(
        "Location", on_delete=models.SET_NULL, null=True, blank=True
    )
    comments = models.ManyToManyField("Comment")
    top_attempts = models.IntegerField(default=1)

    def __str__(self):
        return self.user.first_name


class Category(models.Model):
    icon = models.FileField(upload_to="svg_icon/", blank=True, null=True)
    name = models.CharField(max_length=40, unique=True)

    def __str__(self):
        return self.name


class Image(models.Model):
    image = models.ImageField(upload_to="post_images/")


class Location(models.Model):
    latitude = models.CharField(max_length=20)
    longitude = models.CharField(max_length=20)


class Comment(models.Model):
    user = models.ForeignKey(BasicUser, on_delete=models.CASCADE)
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]


class AD(models.Model):
    title = models.CharField(max_length=255)
    link = models.URLField(max_length=255)
    active = models.BooleanField(default=True)
    image_size_1 = models.ImageField(
        upload_to="ads_images/size_1", null=True, blank=True
    )
    image_size_2 = models.ImageField(
        upload_to="ads_images/size_2", null=True, blank=True
    )


class Post(models.Model):
    CURRENCY_CHOICES = (("uzs", "uzs"), ("usd", "usd"))
    title = models.CharField(max_length=40)
    post_type = models.ForeignKey(Category, on_delete=models.CASCADE)
    images = models.ManyToManyField(Image)
    phone_number = models.CharField(max_length=30)
    more_info = models.TextField(blank=True, null=True)
    price = models.CharField(max_length=20)
    user = models.ForeignKey(BasicUser, on_delete=models.CASCADE)
    city = models.ForeignKey(City, on_delete=models.CASCADE)
    views = models.ManyToManyField(BasicUser, related_name="views", blank=True)
    liked = models.ManyToManyField(BasicUser, related_name="liked", blank=True)
    top = models.BooleanField(default=False)
    currency = models.CharField(max_length=10, choices=CURRENCY_CHOICES, default="uzs")
    location = models.ForeignKey(
        Location, on_delete=models.PROTECT, null=True, blank=True
    )
    sold = models.BooleanField(default=False)
    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def increase_views(self, user):
        self.views.add(user)
        self.save()

    def increase_likes(self, user):
        self.liked.add(user)
        self.save()

    def has_user_viewed(self, user):
        return self.views.filter(id=user.id).exists()

    def has_user_liked(self, user):
        return self.liked.filter(id=user.id).exists()

    def remove_like(self, user):
        self.liked.remove(user)
        self.save()


class TestData(models.Model):
    region = models.CharField(max_length=255)
    district = models.CharField(max_length=255)
