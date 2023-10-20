from django.shortcuts import render
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from rest_framework.authentication import TokenAuthentication
# Create your views here.
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from Auth.serializers import SendPasswordResetEmailSerializer ,UserChangePasswordSerializer, UserLoginSerializer, UserPasswordResetSerializer, UserProfileSerializer, UserRegistrationSerializer,UserSerializer,LineStringSerializer , SegmentSerializer , PointSerializer , WaterLevelSerializer , NotificationSerializer , HistorySerializer
from django.contrib.auth import authenticate
from Auth.renderers import UserRenderer
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAuthenticated
from .models import User,Point,LineString , Segment , WaterLevel , Notification , History,Parametre
from django.core.mail import send_mail
from django.core.mail import EmailMessage
# Generate Token Manually
import requests 

def getweather():
        api_key = 'acb4de2147565bd1be3296938681cc5c'
        url = f'https://api.openweathermap.org/data/2.5/weather?q=Sfax&appid={api_key}&units=metric'
        # url = "https://api.openweathermap.org/data/2.5/weather?q=Sfax&appid=<votre_api_key>&units=metric"
        response = requests.get(url)
        data = response.json()
        temperature = data['weather'][0]['main']
        print(temperature)
        return (temperature)
    
def get_tokens_for_user(user):
  refresh = RefreshToken.for_user(user)
  return {
      'refresh': str(refresh),
      'access': str(refresh.access_token),
  }

class UserRegistrationView(APIView):
  renderer_classes = [UserRenderer]
  def post(self, request, format=None):
    serializer = UserRegistrationSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    user = serializer.save()
            # send email to user
    # subject = "Welcome to MySite"
    # from_email = "MySite <noreply@mysite.com>"
    # to_email = user.email
    # context = {'username': user.username, 'email': user.email, 'password': request.data['password']}
    # html_content = render_to_string('email_template.html', context)
    # text_content = strip_tags(html_content)
    # email = EmailMultiAlternatives(subject, text_content, from_email, [to_email])
    # email.attach_alternative(html_content, "text/html")
    # email.send()

      # Send email to user
    # send_mail(
    #         'Registration Successful',
    #         f"Dear {user.username},\n\nThank you for registering. Here are your registration details:\n\nUsername: {user.username}\nEmail: {user.email}\nPassword: {request.data['password']}\n\nBest regards,\nYour Company",
    #         'noreply@yourcompany.com',
    #         [user.email],z
    #         fail_silently=False,
    #     )

      # Send email to user
    subject = 'Welcome to our website!'
    message = f'Hi {user.username},\n\nThank you for registering with us. Your account details are:\n\nUsername: {user.username}\nEmail: {user.email}\nPassword: {serializer.validated_data["password"]}\n\nBest regards,\nOur website team'
    from_email = 'tibou'
    recipient_list = [user.email]
    send_mail(subject, message, from_email, recipient_list, fail_silently=False)
    return Response({ 'msg':'Registration Successful'}, status=status.HTTP_201_CREATED)

class UserLoginView(APIView):
  renderer_classes = [UserRenderer]
  def post(self, request, format=None):
    serializer = UserLoginSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    email = serializer.data.get('email')
    password = serializer.data.get('password')
    user = authenticate(email=email, password=password)
    if user is not None:
      token = get_tokens_for_user(user)
      return Response({'token':token, 'msg':'Login Success'}, status=status.HTTP_200_OK)
    else:
      return Response({'errors':{'non_field_errors':['Email or Password is not Valid']}}, status=status.HTTP_404_NOT_FOUND)
from rest_framework import generics
class UserProfileView(APIView):
  renderer_classes = [UserRenderer]
  permission_classes = [IsAuthenticated]
  def get(self, request, format=None):
    serializer = UserProfileSerializer(request.user)
    return Response(serializer.data, status=status.HTTP_200_OK)
    
  def put(self, request, format=None):
        serializer = UserProfileSerializer(request.user, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'msg':'Profile Updated'}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class UserChangePasswordView(APIView):
  renderer_classes = [UserRenderer]
  # permission_classes = [IsAuthenticated]
  def post(self, request, format=None):
    serializer = UserChangePasswordSerializer(data=request.data, context={'user':request.user})
    serializer.is_valid(raise_exception=True)
    return Response({'msg':'Password Changed Successfully'}, status=status.HTTP_200_OK)

class SendPasswordResetEmailView(APIView):
  renderer_classes = [UserRenderer]
  def post(self, request, format=None):
    serializer = SendPasswordResetEmailSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    return Response({'msg':'Password Reset link send. Please check your Email'}, status=status.HTTP_200_OK)

class UserPasswordResetView(APIView):
  renderer_classes = [UserRenderer]
  def post(self, request, uid, token, format=None):
    serializer = UserPasswordResetSerializer(data=request.data, context={'uid':uid, 'token':token})
    serializer.is_valid(raise_exception=True)
    return Response({'msg':'Password Reset Successfully'}, status=status.HTTP_200_OK)


class  UserGetView(APIView):
    def get(self, request):
        users = User.objects.all()
        serializer = UserSerializer(users, many = True)
        return Response(serializer.data) 

class DeleteUserView(APIView):
    # permission_classes = [IsAdminUser]
    def delete(self, request, id):
        try:
            user = User.objects.get(id=id)
            user.delete()
            return Response({'msg':'user delete Successfully'} ,status=status.HTTP_204_NO_CONTENT)
        except User.DoesNotExist:
            return Response({'msg':'user don_t exist'} ,status=status.HTTP_404_NOT_FOUND) 
        



    
class UpdateUserView(APIView):
    renderer_classes = [UserRenderer]
    def put(self, request, pk):
        user = User.objects.get(pk=pk)
        serializer = UserProfileSerializer(user ,data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



# class UserView(APIView):
#     authentication_classes = [TokenAuthentication]
#     permission_classes = [IsAuthenticated]

#     def get(self, request):
#         user = request.user
#         data = {
#             'username': user.username,
#             'email': user.email,
#             'isAdmin': user.is_staff,
#             # Ajoutez d'autres champs utilisateur ici si nécessaire
#         }
#         return Response(data)        
    
class PointListView(APIView):
  
    def get(self, request, format=None):
        points = Point.objects.all()
        serializer = PointSerializer(points, many=True)
        return Response(serializer.data)
    
    def post(self, request, format=None):
        serializer = PointSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def put(self, request, pk, format=None):
        point = Point.objects.get(pk=pk)
        serializer = PointSerializer(point, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    def delete(self, request, pk, format=None):
        point = Point.objects.get(pk=pk)
        point.delete()
        return Response({'msg':'user delete Successfully'} ,status=status.HTTP_204_NO_CONTENT)

class LineStringList(APIView):
     def get(self, request, format=None):
        line = LineString.objects.all()
        serializer = LineStringSerializer(line, many=True)
        return Response(serializer.data)
     
     def post(self, request, format=None):
        serializer = LineStringSerializer(data=request.data)
        if serializer.is_valid():
            print(request.data)
            line_string = serializer.save()
            print(int(request.data['zone']))
            if int(request.data['zone'])!=0 :          
               line_string.split_into_segments(num_segments=int(request.data['zone']))
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
     


     
     def delete(self, request, pk, format=None):
        point = LineString.objects.get(pk=pk)
        point.delete()
        return Response({'msg':'line delete Successfully'} ,status=status.HTTP_204_NO_CONTENT)
     
class SegmentList(APIView):
    def get(self, request, format=None):
        segments = Segment.objects.all()
        serializer = SegmentSerializer(segments, many=True)
        return Response(serializer.data)

    def delete(self, request, pk, format=None):
        if pk is None:
            return Response({'message': 'Segment ID is required.'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            segment = Segment.objects.get(pk=pk)
            line_string = segment.linestring
            segment.delete()  # Delete the segment
            line_string.delete()  # Delete the associated line string
            return Response({'message': 'Segment and associated line deleted successfully.'}, status=status.HTTP_204_NO_CONTENT)
        except Segment.DoesNotExist:
            return Response({'message': 'Segment not found.'}, status=status.HTTP_404_NOT_FOUND)
        
from django.utils import timezone
from django.db.models import Avg
from django.utils.datetime_safe import datetime
from django.utils.dateparse import parse_date

class WaterLevelAPIView(APIView):
  def get(self, request, pk, format=None):
    linestring = LineString.objects.get(pk=pk)
    selected_date = datetime.combine(parse_date(request.GET.get('selectedDate')), datetime.min.time())
    timezone.activate('Africa/Tunis')
    start_time = timezone.make_aware(datetime(selected_date.year, selected_date.month, selected_date.day, 0, 0, 0))
    end_time = start_time + timezone.timedelta(hours=23)
    water_level_data = WaterLevel.objects.filter(
        date__range=(start_time, end_time),
        zone__linestring=linestring
    ).extra(select={'hour': "strftime('%%Y-%%m-%%dT%%H:00:00', date)"}).values('zone', 'hour').annotate(
        avg_level=Avg('level')).order_by('zone', 'hour')
    serialized_data = {}
    for datum in water_level_data:
        zone = datum['zone']
        hour = datum['hour']
        avg_level = datum['avg_level']
        if zone not in serialized_data:
            serialized_data[zone] = []
        serialized_data[zone].append({'date': hour, 'level': avg_level})
    return Response(serialized_data)

    # def get(self, request, pk):
        
    #     linestring = LineString.objects.get(pk=pk)
    #     segments = Segment.objects.filter(linestring=linestring)
    #     print(segments)
    #     water_levels = WaterLevel.objects.filter(zone__in=segments).order_by('date')
    #     serializer = WaterLevelSerializer(water_levels, many=True)
    #     return Response(serializer.data)


class NotificationList(APIView):
    def get(self, request, format=None):
        notifications = Notification.objects.all()
        serializer = NotificationSerializer(notifications, many=True)
        notification_data = serializer.data
        serialized_data = []

        for notification in notification_data:
            points = Point.objects.filter(id=notification['point'])
            point_serializer = PointSerializer(points, many=True)
            point_data = point_serializer.data

            for point in point_data:
                line = LineString.objects.filter(points=point['id'])
                line_serializer = LineStringSerializer(line, many=True)
                segment = Segment.objects.filter(linestring=int(line_serializer.data[0]['id']), name=notification['zone'])
                segment_serializer = SegmentSerializer(segment, many=True)
                # water_levels = WaterLevel.objects.filter(zone=segment_serializer.data[0]['id'])
                # water_level_serializer = WaterLevelSerializer(water_levels, many=True)
                # water_level_data = water_level_serializer.data
                # weather = getweather()
                weather = 'Rain'
                if weather == 'Rain':
                        # Check if the notification is read
                        if not notification['is_read']:
                            # Create a new history only if the notification is not read
                            existing_history = History.objects.filter(
                                point_id=point['id'],
                                segment_id=segment_serializer.data[0]['id'],
                                date=notification['date']
                            ).first()

                            if existing_history is None:
                                # Create a new history if it doesn't already exist
                                hist = History.objects.create(
                                    point_id=point['id'],
                                    segment_id=segment_serializer.data[0]['id'],
                                    date=notification['date']
                                )
                                users = User.objects.all()
                                subject = 'alert!'
                                message = f"il-y-a une fuite dans la nœud {point['name']},\n\n dans la zone: {segment_serializer.data[0]['name']}\n"
                                from_email = 'tibou'
                                for user in users:
                                  recipient_list = [user.email]
                                  send_mail(subject, message, from_email, recipient_list, fail_silently=False)
                                segment_instance = segment[0]  # Assuming there's only one matching segment
                                segment_instance.fuite = True
                                segment_instance.save()

                serialized_data.append({ 'point': point, 'zone': segment_serializer.data, 'date': notification['date'], 'notif': notification})
 
        return Response(serialized_data)
# class NotificationList(APIView):
#     def get(self, request, format=None):
#         notifications = Notification.objects.all()
#         serializer = NotificationSerializer(notifications, many=True)
#         notification_data = serializer.data
#         serialized_data = []

#         for notification in notification_data:
#             points = Point.objects.filter(id=notification['point'])
#             point_serializer = PointSerializer(points, many=True)
#             point_data = point_serializer.data

#             for point in point_data:
#                 line = LineString.objects.filter(points=point['id'])
#                 line_serializer = LineStringSerializer(line, many=True)
#                 segment = Segment.objects.filter(linestring=int(line_serializer.data[0]['id']), name=notification['zone'])
#                 segment_serializer = SegmentSerializer(segment, many=True)
#                 water_levels = WaterLevel.objects.filter(zone=segment_serializer.data[0]['id'])
#                 water_level_serializer = WaterLevelSerializer(water_levels, many=True)
#                 water_level_data = water_level_serializer.data
#                 # weather = getweather()
#                 weather = 'Rain'

#                 for water_level in water_level_data:
#                     if float(water_level['level']) > 30 and weather == 'Rain':
#                         hist = History.objects.create(
#                             point_id=point['id'],
#                             segment_id=segment_serializer.data[0]['id'],
#                             date=water_level['date']
#                         )

#                         serialized_data.append({'water_level': water_level, 'point': point, 'zone': segment_serializer.data , 'date':water_level['date'], 'line':line_serializer.data})

#         return Response(serialized_data)
class HistoryList(APIView):
    def get(self, request, format=None):
        serialized_data = []
        history = History.objects.all()
        serializer = HistorySerializer(history, many=True)
        history_data = serializer.data
        for hist in history_data:
            line = LineString.objects.filter(points=hist['point'])
            line_serializer = LineStringSerializer(line, many=True)     
            points = Point.objects.filter(id=hist['point'])
            point_serializer = PointSerializer(points, many=True)
            segment = Segment.objects.filter(id=hist['segment'],)
            segment_serializer = SegmentSerializer(segment, many=True)
            water_levels = WaterLevel.objects.filter(zone=segment_serializer.data[0]['id'])
            water_level_serializer = WaterLevelSerializer(water_levels, many=True)
            hist = History.objects.filter(point=point_serializer.data[0]['id'] , segment=segment_serializer.data[0]['id'])
            hist_serializer = HistorySerializer(hist, many=True)
            serialized_data.append({'line': line_serializer.data, 'point': point_serializer.data, 'zone': segment_serializer.data , 'water_level': water_level_serializer.data , 'history':hist_serializer.data })
        return Response(serialized_data)

    def delete(self, request, id):
        try:
            history = History.objects.get(id=id)
            history.delete()
            return Response({'msg':'history delete Successfully'} ,status=status.HTTP_204_NO_CONTENT)
        except User.DoesNotExist:
            return Response({'msg':'history don_t exist'} ,status=status.HTTP_404_NOT_FOUND) 
        

class NotificationDetail(APIView):
    def patch(self, request, notification_id, format=None):
        try:
            notification = Notification.objects.get(id=notification_id)
            notification.is_read = True
            notification.save()
            return Response(status=status.HTTP_200_OK)
        except Notification.DoesNotExist:
            return Response({'error': 'Notification not found'}, status=status.HTTP_404_NOT_FOUND)
    def delete(self, request, id):
        try:
            notification = Notification.objects.get(id=id)
            notification.delete()
            return Response({'msg':'notification delete Successfully'} ,status=status.HTTP_204_NO_CONTENT)
        except User.DoesNotExist:
            return Response({'msg':'notification don_t exist'} ,status=status.HTTP_404_NOT_FOUND)
      
class SfaxWeatherView(APIView):
    def get(self, request):
        api_key = 'acb4de2147565bd1be3296938681cc5c'
        url = f'https://api.openweathermap.org/data/2.5/weather?q=Sfax&appid={api_key}&units=metric'
        # url = "https://api.openweathermap.org/data/2.5/weather?q=Sfax&appid=<votre_api_key>&units=metric"
        response = requests.get(url)
        data = response.json()
        temperature = data['main']['temp']
        humidity= data['main']['humidity']
        weather=data['weather'][0]['main']
        pressure=data['main']['pressure']

        return Response({'temperature': temperature,'humidity':humidity,'weather':weather,'pressure':pressure})
    

class ParametreWeatherAPIView(APIView):
  def get(self, request, pk, format=None):
    segmant = Segment.objects.get(pk=pk)
    middle_latitude, middle_longitude = segmant.get_middle_point()
    api_key = 'acb4de2147565bd1be3296938681cc5c'
    url = f'https://api.openweathermap.org/data/2.5/weather?lat={middle_latitude}&lon={middle_longitude}&appid={api_key}&units=metric'
    response = requests.get(url)
    data = response.json()
    temperature = data['main']['temp']
    humidity= data['main']['humidity']
    weather=data['weather'][0]['main']
    pressure=data['main']['pressure']
    return Response({'temperature': temperature,'humidity':humidity,'weather':weather,'pressure':pressure})


class ParametrAPIView(APIView):
        def get(self, request, pk, format=None):
          segment = Segment.objects.filter(linestring=pk)
          segment_serializer = SegmentSerializer(segment, many=True)
          return Response(segment_serializer.data)
        

class ParametresAPIView(APIView):
    def get(self, request, format=None):
        zones = Segment.objects.all()
        parameters = ['temperature', 'pressure', 'humidity']
        selected_zone = request.GET.get('selectedZone')
        selected_parameter = request.GET.get('selectedParameter')
        selected_date = request.GET.get('selectedDate')

        if not selected_zone or not selected_parameter or not selected_date:
            return Response({'error': 'Please select a zone, parameter, and date.'}, status=status.HTTP_400_BAD_REQUEST)

        # Convert selected date to datetime object
        try:
            selected_date = datetime.strptime(selected_date, '%Y-%m-%d')
        except ValueError:
            return Response({'error': 'Invalid date format. Please select a valid date.'}, status=status.HTTP_400_BAD_REQUEST)

        parametre_data = Parametre.objects.filter(
            capteur=selected_zone,
            date__date=selected_date.date(),
            date__isnull=False
        ).values('date', selected_parameter).order_by('date')

        serialized_data = {
            'zone': selected_zone,
            'parameter': selected_parameter,
            'data': []
        }

        for datum in parametre_data:
            date = datum['date']
            value = datum[selected_parameter]
            serialized_data['data'].append({'date': date, 'value': value})

        return Response(serialized_data)        
    


class ZoneView(APIView):
    def patch(self, request, pk, format=None):
        try:
            notification = Segment.objects.get(id=pk)
            notification.fuite = False
            notification.save()
            return Response(status=status.HTTP_200_OK)
        except Notification.DoesNotExist:
            return Response({'error': 'Notification not found'}, status=status.HTTP_404_NOT_FOUND)
        
from collections import Counter

from django.db.models.functions import TruncMonth
from datetime import datetime

from django.db.models.functions import TruncMonth
from datetime import datetime

class SegmentListCreateView(APIView):
    def get(self, request, pk):
        date = request.GET.get('date', None)  # Set default value to None if date is not provided

        if not date:
            return Response({'error': 'Please provide a date parameter.'}, status=400)

        try:
            date_obj = datetime.strptime(date, '%Y-%m-%d')
            year = date_obj.year
            month = date_obj.month
        except ValueError:
            return Response({'error': 'Invalid date format. Please provide date in the format "YYYY-MM-DD".'}, status=400)

        start_date = datetime(year, month, 1)
        end_date = start_date.replace(day=1, hour=0, minute=0, second=0, microsecond=0)

        history = History.objects.filter(point=pk, date__gte=end_date, date__lt=end_date.replace(month=end_date.month+1))
        serializerHistory = HistorySerializer(history, many=True)

        all_segments = Segment.objects.filter(linestring__points=pk)
        all_segment_serializer = SegmentSerializer(all_segments, many=True)

        all_segment_names = [segment['name'] for segment in all_segment_serializer.data]

        segment_values = Counter()
        for segment_data in all_segment_serializer.data:
            segment_name = segment_data['name']
            segment_values[segment_name] = 0

        for entry in serializerHistory.data:
            segment_id = entry['segment']
            for segment_data in all_segment_serializer.data:
                if segment_data['id'] == segment_id:
                    segment_name = segment_data['name']
                    segment_values[segment_name] += 1

        data = {
            'labels': list(all_segment_names),
            'values': [segment_values[segment_name] for segment_name in all_segment_names]
        }

        return Response(data)