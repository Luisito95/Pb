from django.db import models

class rtv_cup(models.Model):
    fecha=models.DateField()
    cant=models.IntegerField(verbose_name='Cantidad')
    valor_facial=models.FloatField(verbose_name='Valor Facial')
    valor_etecsa=models.FloatField(verbose_name='Valor Etecsa')
    ingreso_ag=models.FloatField(verbose_name='Ingreso A.G')

class trtv_cup(models.Model):
    fecha=models.DateField()
    tcant=models.IntegerField(verbose_name='Total: Cantidad')
    tvalor_facial=models.FloatField(verbose_name='Total: Valor Facial')
    tvalor_etecsa=models.FloatField(verbose_name='Total: Valor Etecsa')
    tingreso_ag=models.FloatField(verbose_name='Total: Ingreso')

class rtv_nauta(models.Model):
    fecha=models.DateField()
    cant=models.IntegerField(verbose_name='Cantidad')
    valor_facial=models.FloatField(verbose_name='Valor Facial')
    valor_etecsa=models.FloatField(verbose_name='Valor Etecsa')
    ingreso_ag_cuc=models.FloatField(verbose_name='Ingreso A.G-CUC')
    ingreso_ag_cup=models.FloatField(verbose_name='Ingreso A.G-CUP')    

class trtv_nauta(models.Model):
    fecha=models.DateField()
    tcant=models.IntegerField(verbose_name='Total: Cantidad')
    tvalor_facial=models.FloatField(verbose_name='Total: Valor Facial')
    tvalor_etecsa=models.FloatField(verbose_name='Total: Valor Etecsa')
    tingreso_ag_cuc=models.FloatField(verbose_name='Total: Ingreso A.G-CUC')
    tingreso_ag_cup=models.FloatField(verbose_name='Total: Ingreso A.G-CUP')    

class rtv_movil(models.Model):
    fecha=models.DateField()
    cant=models.IntegerField(verbose_name='Cantidad')
    valor_facial=models.FloatField(verbose_name='Valor Facial')
    valor_etecsa=models.FloatField(verbose_name='Valor Etecsa')
    ingreso_ag_cuc=models.FloatField(verbose_name='Ingreso A.G-CUC')
    ingreso_ag_cup=models.FloatField(verbose_name='Ingreso A.G-CUP')

class trtv_movil(models.Model):
    fecha=models.DateField()
    tcant=models.IntegerField(verbose_name='Total: Cantidad')
    tvalor_facial=models.FloatField(verbose_name='Total: Valor Facial')
    tvalor_etecsa=models.FloatField(verbose_name='Total: Valor Etecsa')
    tingreso_ag_cuc=models.FloatField(verbose_name='Total: Ingreso A.G-CUC')
    tingreso_ag_cup=models.FloatField(verbose_name='Total: Ingreso A.G-CUP')

class costo_utilidad(models.Model):
    fecha=models.DateField()
    costo_etecsa=models.FloatField(verbose_name='Costo Etecsa')
    utilidad_diaria=models.FloatField(verbose_name='Utilidad Diaria')
