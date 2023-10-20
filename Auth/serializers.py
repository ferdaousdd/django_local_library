from rest_framework import serializers
from Auth.models import User,Point , LineString , Segment, WaterLevel  , Notification , History 
from django.utils.encoding import smart_str, force_bytes, DjangoUnicodeDecodeError
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from Auth.utils import Util
class UserRegistrationSerializer(serializers.ModelSerializer):
  # We are writing this becoz we need confirm password field in our Registratin Request
  password_confirmation = serializers.CharField(write_only=True, required=True, style={'input_type': 'password'})
  # password2 = serializers.CharField(style={'input_type':'password'}, write_only=True, required=True)
  class Meta:
    model = User
    fields=['username','email','last_name','address', 'first_name', 'password', 'password_confirmation', 'phone_number','image']
    extra_kwargs={
      'password':{'write_only':True}
    }

  # Validating Password and Confirm Password while Registration
  def validate(self, attrs):
    password = attrs.get('password')
    password_confirmation = attrs.get('password_confirmation')
    if password != password_confirmation:
      raise serializers.ValidationError("Password and Confirm Password doesn't match")
    return attrs


  def create(self, validate_data):
    return User.objects.create_user(**validate_data)


class UserProfileSerializer(serializers.ModelSerializer):
  class Meta:
    model = User
    fields = ['id', 'email', 'username','last_name','address', 'first_name','phone_number','image','is_admin']

class UserSerializer(serializers.ModelSerializer):
  class Meta:
    model = User
    fields = ['id', 'email', 'username','last_name','address', 'first_name','phone_number','image']


class UserLoginSerializer(serializers.ModelSerializer):
  email = serializers.EmailField(max_length=255)
  class Meta:
    model = User
    fields = ['email', 'password']

class UserupdateSerializer(serializers.ModelSerializer):
     class Meta:
      model = User
      fields = ['id', 'email', 'username','last_name','address', 'first_name','phone_number']


class UserChangePasswordSerializer(serializers.Serializer):
  password_confirmation = serializers.CharField(max_length=255, style={'input_type':'password'}, write_only=True)
  password = serializers.CharField(max_length=255, style={'input_type':'password'}, write_only=True)
  old_password=serializers.CharField(max_length=255, style={'input_type':'password'}, write_only=True)
  class Meta:
    fields = ['password', 'password_confirmation','old_password']

  def validate(self, attrs):
    password = attrs.get('password')
    password_confirmation = attrs.get('password_confirmation')
    old_password=attrs.get('old_password')
    user = self.context.get('user')
    if not user.check_password(old_password):
       raise serializers.ValidationError("Invalid old password")


    if password != password_confirmation:
      raise serializers.ValidationError("Password and Confirm Password doesn't match ")
    user.set_password(password)
    user.save()
    return attrs

class SendPasswordResetEmailSerializer(serializers.Serializer):
  email = serializers.EmailField(max_length=255)
  class Meta:
    model = User
    fields = ['email']


  def validate(self, attrs):
    email = attrs.get('email')
    if User.objects.filter(email=email).exists():
      user = User.objects.get(email = email)
      uid = urlsafe_base64_encode(force_bytes(user.id))
      print('Encoded UID', uid)
      token = PasswordResetTokenGenerator().make_token(user)
      print('Password Reset Token', token)
      link = 'http://localhost:3000/api/user/reset/'+uid+'/'+token
      print('Password Reset Link', link)
      # Send EMail
      body = 'Click Following Link to Reset Your Password '+link
      data = {
        'subject':'Reset Your Password',
        'body':body,
        'to_email':user.email
      }
      Util.send_email(data)
      return attrs
    else:
      raise serializers.ValidationError('You are not a Registered User')
    


class UserPasswordResetSerializer(serializers.Serializer):
  password = serializers.CharField(max_length=255, style={'input_type':'password'}, write_only=True)
  password_confirmation = serializers.CharField(max_length=255, style={'input_type':'password'}, write_only=True)
  class Meta:
    fields = ['password', 'password_confirmation']

  def validate(self, attrs):
    try:
      password = attrs.get('password')
      password_confirmation = attrs.get('password_confirmation')
      uid = self.context.get('uid')
      token = self.context.get('token')
      if password != password_confirmation:
        raise serializers.ValidationError("Password and Confirm Password doesn't match")
      id = smart_str(urlsafe_base64_decode(uid))
      user = User.objects.get(id=id)
      if not PasswordResetTokenGenerator().check_token(user, token):
        raise serializers.ValidationError('Token is not Valid or Expired')
      user.set_password(password)
      user.save()
      return attrs
    except DjangoUnicodeDecodeError as identifier:
      PasswordResetTokenGenerator().check_token(user, token)
      raise serializers.ValidationError('Token is not Valid or Expired')
  

class LineStringSerializer(serializers.ModelSerializer):
    class Meta:
        model = LineString
        fields = ('id', 'name', 'path' , 'points')

class PointSerializer(serializers.ModelSerializer):
    class Meta:
        model = Point
        fields = ('id', 'name', 'longitude', 'latitude')    


class SegmentSerializer(serializers.ModelSerializer):

    class Meta:
        model = Segment
        fields = '__all__'


class WaterLevelSerializer(serializers.ModelSerializer):
    class Meta:
        model = WaterLevel
        fields = ['level', 'date', 'zone']


class NotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notification
        fields = '__all__'


class HistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = History
        fields = '__all__'


