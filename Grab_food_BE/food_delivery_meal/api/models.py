from django.db import models
from django.contrib.auth.models import AbstractUser, Group, Permission
from django.utils import timezone


# Role Model
class Role(models.Model):
    role_name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.role_name


# Food Type Model
class FoodType(models.Model):
    type_name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.type_name


# UserProfile to extend User with a role
class User(AbstractUser):
    role = models.ForeignKey(Role, on_delete=models.CASCADE, null=True, blank=True)
    groups = models.ManyToManyField(Group, related_name='customuser_set', blank=True)
    user_permissions = models.ManyToManyField(Permission, related_name='customuser_permissions_set', blank=True)

    def __str__(self):
        return self.username

# Customer Model
class Customer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    age = models.IntegerField(null=True, blank=True)
    phone = models.CharField(max_length=15, null=True, blank=True)
    address = models.CharField(max_length=255, null=True, blank=True)

    def __str__(self):
        return self.user.username


# Admin Model
class Admin(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    age = models.IntegerField(null=True, blank=True)
    phone = models.CharField(max_length=15, null=True, blank=True)

    def __str__(self):
        return self.user.username


# Restaurant Model
class Restaurant(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    restaurant_name = models.CharField(max_length=100)
    phone = models.CharField(max_length=15, null=True, blank=True)
    address = models.CharField(max_length=255, null=True, blank=True)

    def __str__(self):
        return self.restaurant_name


# Shipper Model
class Shipper(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    age = models.IntegerField(null=True, blank=True)
    cccd = models.CharField(max_length=12, null=True, blank=True)
    license_plate = models.CharField(max_length=20, null=True, blank=True)
    address = models.CharField(max_length=255, null=True, blank=True)
    phone = models.CharField(max_length=15, null=True, blank=True)
    vehicle = models.CharField(max_length=50, null=True, blank=True)

    def __str__(self):
        return self.user.username


# Menu Model
class Menu(models.Model):
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE)
    food_name = models.CharField(max_length=100, unique=True)
    food_type = models.ForeignKey(FoodType, on_delete=models.SET_NULL, null=True)
    price = models.PositiveIntegerField()

    def __str__(self):
        return self.food_name


# Order History Model
class History(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    menu = models.ForeignKey(Menu, on_delete=models.CASCADE)
    count = models.PositiveIntegerField()
    delivery_date = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.customer.user.username} - {self.menu.food_name}"


# Menu Review Model
class ReviewMenu(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    menu = models.ForeignKey(Menu, on_delete=models.CASCADE)
    rating = models.PositiveIntegerField()
    created_at = models.DateTimeField(auto_now_add=True)  # Thay đổi ở đây

    def __str__(self):
        return f"Review {self.rating} for {self.menu.food_name}"


# User Review Model
class Review(models.Model):
    reviewer = models.ForeignKey(User, on_delete=models.CASCADE, related_name="reviews_given")
    reviewee = models.ForeignKey(User, on_delete=models.CASCADE, related_name="reviews_received")
    rating = models.PositiveIntegerField()
    comment = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)  # Thay đổi ở đây

    def __str__(self):
        return f"{self.reviewer.username} -> {self.reviewee.username}"


# Message Model
class Message(models.Model):
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name="sent_messages")
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name="received_messages")
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)  # Thay đổi ở đây

    def __str__(self):
        return f"Message from {self.sender.username} to {self.receiver.username}"


# Voucher Model
class Voucher(models.Model):
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE)
    value = models.PositiveIntegerField()
    minimum_order_value = models.PositiveIntegerField()
    expiration_date = models.DateTimeField()  # Thay đổi ở đây để không có giá trị mặc định

    def __str__(self):
        return f"Voucher {self.value}% for {self.restaurant.restaurant_name}"


# Favorite Restaurant Model
class FavoriteRestaurant(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='favorite_restaurants')
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.customer.user.username} -> {self.restaurant.restaurant_name}"


# Favorite Menu Model
class FavoriteMenu(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='favorite_menus')
    menu = models.ForeignKey(Menu, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.customer.user.username} -> {self.menu.food_name}"


# Shopping Cart Model
class Cart(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='cart_items')
    menu = models.ForeignKey(Menu, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    added_at = models.DateTimeField(auto_now_add=True)  # Thay đổi ở đây

    def __str__(self):
        return f"Cart: {self.customer.user.username} - {self.menu.food_name}"