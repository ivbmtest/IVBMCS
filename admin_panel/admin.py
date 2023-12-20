from django.contrib import admin
from typing import Any
from django.contrib import admin
from django.utils.html import format_html
from django import forms
from .models import *
# Register your models here.
# class DocumentAdmin(admin.ModelAdmin):
#     list_display = ('title', 'file')  # Fields to display in the list view
#     search_fields = ('title',)  # Add a search box for the specified fields
#     # list_filter = ('created_at',)  # Add filters based on the specified fields

#     def display_file_link(self, obj):
#         return format_html('<a href="{}" target="_blank">{}</a>', obj.file.url, obj.file.name)

#     display_file_link.short_description = 'file'
    
class CurrencyAdmin(admin.ModelAdmin):
    list_display = ('crname','crsymbol','crdescription','crstatus','usrid','dtupdatd')
    search_fields = ('crname','crsymbol')
    list_editable = ['crstatus']
    
    def display_name(self, obj):
        return obj.crname

    display_name.short_description = 'Name'
    
    def save_model(self, request, obj, form, change):
        if not obj.usrid_id:
            obj.usrid_id = request.user.id
        return super().save_model(request, obj, form, change)
    
class CountryAdmin(admin.ModelAdmin):
    autocomplete_fields=['cncrid','cntxid']
    list_display = ('cnname','cndescription','cncrid','cntxid','cnstatus','usrid','dtupdatd')
    search_fields = ('cnname',)
    list_editable = ['cnstatus']
    
    def save_model(self, request, obj, form, change):
        if not obj.usrid_id:
            obj.usrid_id = request.user.id
        return super().save_model(request, obj, form, change)

class CategoryAdmin(admin.ModelAdmin):
    list_display = ('ctname','ctcode','ctdescription','ctimg','ctstatus','usrid','dtupdatd')
    search_fields = ('ctname',)
    list_editable = ['ctstatus']
    
    def save_model(self, request, obj, form, change):
        if not obj.usrid_id:
            obj.usrid_id = request.user.id
        return super().save_model(request, obj, form, change)
    
class ServiceAdmin(admin.ModelAdmin):
    autocomplete_fields=['svcategory','svcountry']
    search_fields = ('svname',)
    list_editable = ['svstatus']
    list_display = ('svcode','svname','svdescription','svcategory','svcountry',
                    'svrate','svratesplit','svsrvchg','discrt','discamt','disctxt',
                    'svagamt','svagrt','svtxid','svtxrt','svtxamt','svnetamt','svstatus','usrid','dtupdatd')
    
    def save_model(self, request, obj, form, change):
        if not obj.usrid_id:
            obj.usrid_id = request.user.id
        return super().save_model(request, obj, form, change)
    
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
        
        
        
class TaxMasterAdmin(admin.ModelAdmin):
    list_display = ('txname','txdescription','txisgst','txstatus','usrid','dtupdatd')
    search_fields = ('txname',)
    list_editable = ['txstatus']
    
    def save_model(self, request, obj, form, change):
        if not obj.usrid_id:
            obj.usrid_id = request.user.id
        return super().save_model(request, obj, form, change)

class TaxDetailsAdmin(admin.ModelAdmin):
    list_display = ('tdtxid','tdname','tddescription','tdcgst','tdsgst','tdigst',
                    'tdvat','tdcess','tdstatus','usrid', 'dtupdatd')
    search_fields = ('tdname',)
    list_editable = ['tdstatus']
    
    def save_model(self, request, obj, form, change):
        if not obj.usrid_id:
            obj.usrid_id = request.user.id
        return super().save_model(request, obj, form, change)
    
    
class FileFormatAdmin(admin.ModelAdmin):
    list_display = ('frname','frdescription','frfltr','frstatus','usrid','dtupdatd')
    search_fields = ('frname',)
    list_editable = ['frstatus']
    
    def save_model(self, request, obj, form, change):
        if not obj.usrid_id:
            obj.usrid_id = request.user.id
        return super().save_model(request, obj, form, change)
       
    

# admin.site.register(Document,DocumentAdmin)
admin.site.register(crnc,CurrencyAdmin)
admin.site.register(cntry,CountryAdmin)
admin.site.register(ctgry,CategoryAdmin)
admin.site.register(srvc,ServiceAdmin)
# admin.site.register(DocumentsRequired,DocumentRequiredAdmin)
admin.site.register(txmst,TaxMasterAdmin)
admin.site.register(txdet,TaxDetailsAdmin)
admin.site.register(formt,FileFormatAdmin)

