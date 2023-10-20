from django.contrib import admin
from Auth.models import User,Point,LineString , Segment , WaterLevel , History , Notification,Parametre
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
admin.site.register(LineString)
admin.site.register(Segment)
admin.site.register(Point)
admin.site.register(WaterLevel)
admin.site.register(Notification)
admin.site.register(History)
admin.site.register(Parametre)
class UserModelAdmin(BaseUserAdmin):
  # The fields to be used in displaying the User model.
  # These override the definitions on the base UserModelAdmin
  # that reference specific fields on auth.User.
  list_display = ('id', 'email', 'username', 'is_admin','image','first_name','last_name','phone_number','address')
  list_filter = ('is_admin',)
  fieldsets = (
      ('User Credentials', {'fields': ('email', 'password')}),
      ('Personal info', {'fields': ('username','first_name')}),
      ('Permissions', {'fields': ('is_admin',)}),
  )
  # add_fieldsets is not a standard ModelAdmin attribute. UserModelAdmin
  # overrides get_fieldsets to use this attribute when creating a user.
  add_fieldsets = (
      (None, {
          'classes': ('wide',),
          'fields': ('email', 'username', 'password1', 'password2','image','address','phone_number','first_name','last_name'),
      }),
  )
  search_fields = ('email',)
  ordering = ('email', 'id')
  filter_horizontal = ()


# Now register the new UserModelAdmin...
admin.site.register(User, UserModelAdmin)