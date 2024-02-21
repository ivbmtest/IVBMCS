from django.contrib import admin
from typing import Any
from django.contrib.auth.admin import UserAdmin

from django.utils.html import format_html
from django import forms
from .models import *
# Register your models here.
class UserModel(UserAdmin):
    ordering = ('email',)

admin.site.register(CustomUser,UserModel)
admin.site.register(Staff)
admin.site.register(Agent)
admin.site.register(Users)
admin.site.site_header = 'SuperAdmin Dashboard'
admin.site.site_title = 'Admin'



class CurrencyAdmin(admin.ModelAdmin):
    list_display = ('crname','crsymbol','crdescription','crstatus','usrid','dtupdatd','change_button', 'delete_button')
    list_per_page = 5
    search_fields = ('crname','crsymbol')
    list_editable = ['crstatus']
    list_filter = ('dtupdatd',)
    
    def display_name(self, obj):
        return obj.crname

    display_name.short_description = 'Name'
    
    def save_model(self, request, obj, form, change):
        if not obj.usrid_id:
            obj.usrid_id = request.user.id
        return super().save_model(request, obj, form, change)
    
    def change_button(self, obj):
        return format_html('<a class="btn" style="background-color:#3B71CA; padding:3px;color:white;border-radius:8px;" href="/admin/admin_panel/crnc/{}/change/">Update</a>', obj.crid)

    def delete_button(self, obj):
        return format_html('<a class="btn" style="background-color:#DC4C64; padding:3px;color:white;border-radius:8px;" href="/admin/admin_panel/crnc/{}/delete/">Delete</a>', obj.crid)



    

    
class CountryAdmin(admin.ModelAdmin):
    autocomplete_fields=['cncrid','cntxid']
    list_display = ('cnname','cndescription','cncrid','cntxid','cnstatus','usrid','dtupdatd','change_button', 'delete_button')
    list_per_page = 5
    search_fields = ('cnname',)
    list_editable = ['cnstatus']
    list_filter = ('dtupdatd',)
    
    def save_model(self, request, obj, form, change):
        if not obj.usrid_id:
            obj.usrid_id = request.user.id
        return super().save_model(request, obj, form, change)
    

    def change_button(self, obj):
        return format_html('<a class="btn" style="background-color:#3B71CA; padding:3px;color:white;border-radius:8px;" href="/admin/admin_panel/cntry/{}/change/">Update</a>', obj.cnid)

    def delete_button(self, obj):
        return format_html('<a class="btn" style="background-color:#DC4C64; padding:3px;color:white;border-radius:8px;" href="/admin/admin_panel/cntry/{}/delete/">Delete</a>', obj.cnid)

class CategoryAdmin(admin.ModelAdmin):
    list_display = ('ctname','ctcode','ctdescription','ctimg','ctstatus','usrid','dtupdatd','change_button', 'delete_button')
    list_per_page = 5
    search_fields = ('ctname',)
    list_editable = ['ctstatus']
    list_filter = ('dtupdatd',)
    def save_model(self, request, obj, form, change):
        if not obj.usrid_id:
            obj.usrid_id = request.user.id
        return super().save_model(request, obj, form, change)
    

    def change_button(self, obj):
        return format_html('<a class="btn" style="background-color:#3B71CA; padding:3px;color:white;border-radius:8px;" href="/admin/admin_panel/ctgry/{}/change/">Update</a>', obj.ctid)

    def delete_button(self, obj):
        return format_html('<a class="btn" style="background-color:#DC4C64; padding:3px;color:white;border-radius:8px;" href="/admin/admin_panel/ctgry/{}/delete/">Delete</a>', obj.ctid)


    
class ServiceAdmin(admin.ModelAdmin):
    autocomplete_fields=['svcategory','svcountry']
    search_fields = ('svname',)
    list_editable = ['svstatus']
    list_display = ('svcode','svname','svdescription','svcategory','svcountry',
                    'svrate','svratesplit','svsrvchg','discrt','discamt','disctxt',
                    'svagamt','svagrt','svtxid','svtxrt','svtxamt','svnetamt','svstatus','usrid','dtupdatd','change_button', 'delete_button')
    list_per_page = 5
    list_filter = ('dtupdatd','svcategory','svcountry')
    def save_model(self, request, obj, form, change):
        if not obj.usrid_id:
            obj.usrid_id = request.user.id
        return super().save_model(request, obj, form, change)
    
    def change_button(self, obj):
        return format_html('<a class="btn" style="background-color:#3B71CA; padding:3px;color:white;border-radius:8px;" href="/admin/admin_panel/srvc/{}/change/">Update</a>', obj.svid)

    def delete_button(self, obj):
        return format_html('<a class="btn" style="background-color:#DC4C64; padding:3px;color:white;border-radius:8px;" href="/admin/admin_panel/srvc/{}/delete/">Delete</a>', obj.svid)
    
# class DocumentRequiredAdmin(admin.ModelAdmin):
#     autocomplete_fields=['Service']
#     search_fields = ('DocumentName',)
#     list_editable = ['Status']
#     list_display = ('Service','DocumentName','Description','Format','MaxFileSize','Status',
#                     'CreatedBy','CreatedOn')
    
#     def save_model(self, request, obj, form, change):
#         # Set the created_by field to the currently logged-in admin user ID
#         if not obj.dtupdatd_id:
#             obj.dtupdatd_id = request.user.id

#         # Call the save_model method of the parent class
#         super().save_model(request, obj, form, change)
        
class DocumentRequiredAdmin(admin.ModelAdmin):
    autocomplete_fields=['Service']
    search_fields = ('DocumentName',)
    list_editable = ['Status']
    list_display = ('Service','DocumentName','Description','Format','MaxFileSize','Status',
                     'CreatedBy','CreatedOn','change_button', 'delete_button')
    list_per_page = 5       
    list_filter = ('CreatedOn',)

    def change_button(self, obj):
        return format_html('<a class="btn" style="background-color:#3B71CA; padding:3px;color:white;border-radius:8px;" href="/admin/admin_panel/DocumentsRequired/{}/change/">Update</a>', obj.tdid)

    def delete_button(self, obj):
        return format_html('<a class="btn" style="background-color:#DC4C64; padding:3px;color:white;border-radius:8px;" href="/admin/admin_panel/DocumentsRequired/{}/delete/">Delete</a>', obj.tdid)



class TaxMasterAdmin(admin.ModelAdmin):
    list_display = ('txname','txdescription','txisgst','txstatus','usrid','dtupdatd','change_button', 'delete_button')
    list_per_page = 5
    search_fields = ('txname',)
    list_editable = ['txstatus']
    list_filter = ('dtupdatd',)


    def save_model(self, request, obj, form, change):
        if not obj.usrid_id:
            obj.usrid_id = request.user.id
        return super().save_model(request, obj, form, change)
    

    def change_button(self, obj):
        return format_html('<a class="btn" style="background-color:#3B71CA; padding:3px;color:white;border-radius:8px;" href="/admin/admin_panel/txmst/{}/change/">Update</a>', obj.txid)

    def delete_button(self, obj):
        return format_html('<a class="btn" style="background-color:#DC4C64; padding:3px;color:white;border-radius:8px;" href="/admin/admin_panel/txmst/{}/delete/">Delete</a>', obj.txid)


class TaxDetailsAdmin(admin.ModelAdmin):
    list_display = ('tdtxid','tdname','tddescription','tdcgst','tdsgst','tdigst',
                    'tdvat','tdcess','tdstatus','usrid', 'dtupdatd','change_button', 'delete_button')
    list_per_page = 5
    search_fields = ('tdname',)
    list_editable = ['tdstatus']
    list_filter = ('dtupdatd',)


    def save_model(self, request, obj, form, change):
        if not obj.usrid_id:
            obj.usrid_id = request.user.id
        return super().save_model(request, obj, form, change)
    
    def change_button(self, obj):
        return format_html('<a class="btn" style="background-color:#3B71CA; padding:3px;color:white;border-radius:8px;" href="/admin/admin_panel/txdet/{}/change/">Update</a>', obj.tdid)

    def delete_button(self, obj):
        return format_html('<a class="btn" style="background-color:#DC4C64; padding:3px;color:white;border-radius:8px;" href="/admin/admin_panel/txdet/{}/delete/">Delete</a>', obj.tdid)
    
class FileFormatAdmin(admin.ModelAdmin):
    list_display = ('frname','frdescription','frfltr','frstatus','usrid','dtupdatd')
    list_per_page = 5
    search_fields = ('frname',)
    list_editable = ['frstatus']
    list_filter = ('dtupdatd',)

    def save_model(self, request, obj, form, change):
        if not obj.usrid_id:
            obj.usrid_id = request.user.id
        return super().save_model(request, obj, form, change)
       

class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('name','phone_number','email','service','document','image','payment','created_at')
    
    search_fields = ('name',)
    list_editable = ['payment']  



# admin.site.register(Document,DocumentAdmin)
admin.site.register(crnc,CurrencyAdmin)
admin.site.register(cntry,CountryAdmin)
admin.site.register(ctgry,CategoryAdmin)
admin.site.register(srvc,ServiceAdmin)
admin.site.register(DocumentsRequired,DocumentRequiredAdmin)
admin.site.register(txmst,TaxMasterAdmin)
admin.site.register(txdet,TaxDetailsAdmin)
admin.site.register(formt,FileFormatAdmin)
admin.site.register(UserProfile,UserProfileAdmin)
admin.site.register(clnt)
admin.site.register(states)
admin.site.register(clsubsdet)

# admin.site.register(admcat)
# admin.site.register(admroles)


class Media:
    css = {
        'all': ('admin_styles.css',),
    }