from django.db import models
from shapely.geometry import LineString
# Create your models here.
from django.db import models
import json
# Create your models here.
from django.db import models
from django.contrib.auth.models import BaseUserManager,AbstractBaseUser
from django.core.validators import RegexValidator, MinLengthValidator, MaxLengthValidator, EmailValidator
#  Custom User Manager
class UserManager(BaseUserManager):
  def create_user(self, email, username, password=None,password_confirmation=None, **extra_fields):
      """
      Creates and saves a User with the given email, name, tc and password.
      """
      if not email:
          raise ValueError('User must have an email address')
      
      email = self.normalize_email(email)

      user = self.model(
          email=self.normalize_email(email),
          username=username,
          # tc=tc,
          **extra_fields
      )

      user.set_password(password)
      user.save(using=self._db)
      return user

  def create_superuser(self, email, username, password=None):
      """
      Creates and saves a superuser with the given email, name, tc and password.
      """
      
      user = self.create_user(
          email,
          password=password,
          username=username,
          # tc=tc,
      )
      user.is_admin = True
      user.save(using=self._db)
      return user

#  Custom User Model
class User(AbstractBaseUser):
    # username = models.CharField(max_length=150, unique=True, validators=[MinLengthValidator(5), MaxLengthValidator(50)])
    # email = models.EmailField(unique=True, validators=[EmailValidator()])
    first_name = models.CharField(max_length=30, blank=True, null=True)
    last_name = models.CharField(max_length=30, blank=True, null=True)
    address = models.CharField(max_length=100, blank=True, null=True)
    phone_regex = RegexValidator(regex=r'^\d{8}$', message="Le numéro de téléphone doit être entré dans le format: '+999999999'. Jusqu'à 15 chiffres sont autorisés.")
    phone_number = models.CharField(validators=[phone_regex], max_length=8, blank=True, null=True)
    image = models.ImageField(upload_to='profile_pics/', blank=True, null=True)
    email = models.EmailField(
      verbose_name='Email',
      max_length=255,
      unique=True,
  )
    username = models.CharField(max_length=200)


  
    # tc = models.BooleanField()
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def __str__(self):
      return self.email

    def has_perm(self, perm, obj=None):
      "Does the user have a specific permission?"
      # Simplest possible answer: Yes, always
      return self.is_admin

    def has_module_perms(self, app_label):
      "Does the user have permissions to view the app `app_label`?"
      # Simplest possible answer: Yes, always
      return True

    @property
    def is_staff(self):
      "Is the user a member of staff?"
      # Simplest possible answer: All admins are staff
      return self.is_admin


import pyproj
from shapely.geometry import LineString as ShapelyLineString


class Point(models.Model):
    name = models.CharField(max_length=255)
    longitude = models.DecimalField(max_digits=20, decimal_places=16)
    latitude = models.DecimalField(max_digits=20, decimal_places=16)




class LineString(models.Model):
    name = models.CharField(max_length=255)
    path = models.TextField(null=False, blank=False)
    points = models.ForeignKey(Point ,  on_delete=models.CASCADE)


    def split_into_segments(self, num_segments):
        coordinates = self.path.split('],[')
        total_length = len(coordinates) - 1
        segment_length = total_length / num_segments

        line_coords = [
            (
                float(coord.split(',')[0].replace('[', '')),
                float(coord.split(',')[1][:-2])
            )
            for coord in coordinates
        ]
        linestring = ShapelyLineString(line_coords)

        # Define the projection for conversion
        proj_wgs84 = pyproj.Proj(init='EPSG:4326')
        proj_custom = pyproj.Proj(init='EPSG:4326')  # Replace YOUR_CUSTOM_EPSG_CODE with your custom CRS code

        points = []
        for i in range(num_segments):
            fraction_start = i * segment_length
            fraction_end = (i + 1) * segment_length

            start_point_on_linestring = linestring.interpolate(fraction_start, normalized=True)
            end_point_on_linestring = linestring.interpolate(fraction_end, normalized=True)

            # Convert coordinates to EPSG:4326
            start_point_on_linestring = pyproj.transform(proj_custom, proj_wgs84, start_point_on_linestring.x, start_point_on_linestring.y)
            end_point_on_linestring = pyproj.transform(proj_custom, proj_wgs84, end_point_on_linestring.x, end_point_on_linestring.y)

            start_longitude = start_point_on_linestring[0]
            start_latitude = start_point_on_linestring[1]

            points.append((start_longitude, start_latitude))

            if i == num_segments - 1:
                # Use the end point of the linestring as the end point of the last segment
                end_longitude = end_point_on_linestring[0]
                end_latitude = end_point_on_linestring[1]
            else:
                end_longitude = end_point_on_linestring[0]
                end_latitude = end_point_on_linestring[1]

            segment_name = f"zone{i + 1}"  # Generate a unique name for each segment
            segment = Segment.objects.create(
                linestring=self,
                start_longitude=start_longitude,
                start_latitude=start_latitude,
                end_longitude=end_longitude,
                end_latitude=end_latitude,
                name=segment_name  # Assign the generated name to the segment
            )

        return points

class Segment(models.Model):
    linestring = models.ForeignKey(LineString, on_delete=models.CASCADE)
    start_longitude = models.DecimalField(max_digits=20, decimal_places=16)
    start_latitude = models.DecimalField(max_digits=20, decimal_places=16)
    end_longitude = models.DecimalField(max_digits=20, decimal_places=16)
    end_latitude = models.DecimalField(max_digits=20, decimal_places=16)
    name = models.CharField(max_length=255)
    fuite = models.BooleanField(default=False)  # New boolean field
    def get_middle_point(self):
        middle_latitude = (self.start_latitude + self.end_latitude) / 2
        middle_longitude = (self.start_longitude + self.end_longitude) / 2
        return middle_latitude, middle_longitude

class WaterLevel(models.Model):
    level = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateTimeField()
    zone = models.ForeignKey(Segment, on_delete=models.CASCADE)

from django.utils import timezone

class Notification(models.Model):
    point = models.ForeignKey(Point, on_delete=models.CASCADE)
    zone = models.CharField(max_length=255)
    date = models.DateTimeField(default=timezone.now)
    is_read = models.BooleanField(default=False)
    
class History(models.Model):
    point = models.ForeignKey(Point, on_delete=models.CASCADE)
    segment = models.ForeignKey(Segment, on_delete=models.CASCADE)
    date = models.DateTimeField(default=timezone.now)







class Parametre(models.Model):
    capteur = models.ForeignKey(Point, on_delete=models.CASCADE)
    date = models.DateTimeField()
    Temprature=models.CharField(max_length=255,null=True, blank=True)
    pression = models.FloatField(null=True, blank=True)
    taux_humidite = models.FloatField(null=True, blank=True)
  