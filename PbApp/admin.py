from django.contrib import admin
from PbApp.models import rtv_cup, rtv_nauta, rtv_movil, trtv_cup, trtv_nauta, trtv_movil, costo_utilidad

# Register your models here.

class rtv_cupAdmin(admin.ModelAdmin):
    list_display=('fecha', 'cant', 'valor_facial', 'valor_etecsa', 'ingreso_ag')
    search_fields=('fecha',)
    list_filter=('fecha',)

class rtv_nautaAdmin(admin.ModelAdmin):
    list_display=('fecha', 'cant', 'valor_facial', 'valor_etecsa', 'ingreso_ag_cuc', 'ingreso_ag_cup')
    search_fields=('fecha',)

class rtv_movilAdmin(admin.ModelAdmin):
    list_display=('fecha', 'cant', 'valor_facial', 'valor_etecsa', 'ingreso_ag_cuc', 'ingreso_ag_cup')
    search_fields=('fecha',)

class trtv_cupAdmin(admin.ModelAdmin):
    list_display=('fecha', 'tcant', 'tvalor_facial', 'tvalor_etecsa', 'tingreso_ag')
    search_fields=('fecha',)

class trtv_nautaAdmin(admin.ModelAdmin):
    list_display=('fecha', 'tcant', 'tvalor_facial', 'tvalor_etecsa', 'tingreso_ag_cuc', 'tingreso_ag_cup')
    search_fields=('fecha',)

class trtv_movilAdmin(admin.ModelAdmin):
    list_display=('fecha', 'tcant', 'tvalor_facial', 'tvalor_etecsa', 'tingreso_ag_cuc', 'tingreso_ag_cup')
    search_fields=('fecha',)

class costo_utilidadAdmin(admin.ModelAdmin):
    list_display=('fecha', 'costo_etecsa', 'utilidad_diaria')
    search_fields=('fecha',)

admin.site.register(rtv_cup, rtv_cupAdmin)
admin.site.register(rtv_nauta, rtv_nautaAdmin)
admin.site.register(rtv_movil, rtv_movilAdmin)
admin.site.register(trtv_cup, trtv_cupAdmin)
admin.site.register(trtv_nauta, trtv_nautaAdmin)
admin.site.register(trtv_movil, trtv_movilAdmin)
admin.site.register(costo_utilidad, costo_utilidadAdmin)
