from django.shortcuts import render
from django.http import HttpResponse, request
from django.conf import settings
import datetime
from PbApp.models import rtv_cup, rtv_movil, rtv_nauta, trtv_cup, trtv_movil, trtv_nauta, t_anual, t_anual_nauta, t_anual_movil, facturaciones, t_facturaciones, t_anual_facturaciones, onat_etecsa, t_onat_etecsa
from PbApp.forms import form_insert_cup_movil, form_insert_nauta, form_rango_meses, form_insert_fact, form_insert_pago_onat, form_limpiar_registros
from django.contrib.admin import widgets
from PbApp.rtv.rtv_cup import sum_tcant_cup, sum_tvalor_facial, sum_tvalor_etecsa, sum_tingreso_ag, sum_t_anual
from PbApp.rtv.rtv_nauta import sum_tcant_nauta, sum_tvalor_facial_nauta, sum_tvalor_etecsa_nauta, sum_tingreso_ag_cup_nauta, sum_t_anual_nauta
from PbApp.rtv.rtv_movil import sum_tcant_movil, sum_tvalor_facial_movil, sum_tvalor_etecsa_movil, sum_tingreso_ag_cup_movil, sum_t_anual_movil
from PbApp.rtv.facturaciones import sum_tf, sum_tc, sum_t_anual_facturaciones
import json

global mes_numero_corto
mes_numero_corto=datetime.datetime.now()
mes_numero_corto=int(mes_numero_corto.month)

global meses_s
meses_s=['Enero', 'Febrero', 'Marzo', 'Abril', 'Mayo', 'Junio', 'Julio', 'Agosto', 'Septiembre', 'Octubre', 'Noviembre', 'Diciembre']

global datoday
datoday_full=datetime.datetime.now()
datoday=datetime.datetime.now()
datoday=str(datoday.date())

def home(request):
    year=datoday[:4]
    f = open('data.txt', 'r')
    d_o = str(f.readline())
    categories = f.readline()
    categories = json.dumps(categories)
    return render(request, "home.html", {'mes_c':mes_numero_corto, 'd_o':d_o, 'year':year, 'category':categories})

def menu_rtv_cup_2020(request):
    return render(request, 'menu_rtv_2020.html', {'mes_c':mes_numero_corto, 'tmpl': 'rel_trgtas_vendidas_cup'})

def menu_rtv_nauta_2020(request):
    return render(request, 'menu_rtv_2020.html', {'mes_c':mes_numero_corto, 'tmpl': 'rel_trgtas_vendidas_nauta'})

def menu_rtv_movil_2020(request):
    return render(request, 'menu_rtv_2020.html', {'mes_c':mes_numero_corto, 'tmpl': 'rel_trgtas_vendidas_movil'})

def menu_facturaciones(request):
    return render(request, 'menu_rtv_2020.html', {'mes_c':mes_numero_corto, 'tmpl': 'facturaciones'})

def menu_onat_2020(request):
    return render(request, 'menu_rtv_2020.html', {'mes_c':mes_numero_corto, 'tmpl': 'onat_etecsa'})

def total_anual(request):
    years=datoday[:4]
    years=datoday[:4]
    resultados=trtv_cup.objects.filter(fecha__icontains=years).order_by('fecha')
    tresultados=t_anual.objects.filter(fecha__icontains=years)
    date_total=[]
    date_total=t_anual.objects.all()
    coincidencia=False
    default=True
    res_filtrados=[]
    mes_1='Enero'
    mes_2=meses_s[(datoday_full.month)-1]
    erango=False

    #Variables de tresultados filtrados
    tc=td=tv=tvf=tve=tiag=0

    for x in date_total:
        z=str(x.fecha)
        z=z[:4]
        if z==years: coincidencia=True
    if not coincidencia: x=t_anual.objects.create(fecha=datoday, cant_c=0, cant_d=0, cant_v=0, valor_facial=0, valor_etecsa=0, ingreso_ag=0)


    if request.method=='POST':
        miF=form_rango_meses(request.POST)

        if miF.is_valid():
            infForm=miF.cleaned_data
            mes_1=infForm['mes_de_inicio']
            mes_1=mes_1.mes
            mes_2=infForm['mes_final']
            mes_2=mes_2.mes
            match=False

            #Evaluando un rango correcto
            meses_str=str(meses_s)
            m1=meses_str.find(mes_1)
            m2=meses_str.find(mes_2)

            if m1>m2:
                erango=True

            if not erango:
                #Filtrando los meses a mostrar
                default=False

                for x in resultados:
                    if not match:
                        if x.mes==mes_1:
                            res_filtrados.append(x)
                            match=True
                        continue
                    if match:
                        if x.mes!=mes_2:
                            res_filtrados.append(x)
                        else:
                            res_filtrados.append(x)
                            break

                #LLenando las tcant de los resultados filtrados
                for x in res_filtrados:
                    tc+=x.tcant_c
                    td+=x.tcant_d
                    tv+=x.tcant_v
                    tvf+=x.tvalor_facial
                    tve+=x.tvalor_etecsa
                    tiag+=x.tingreso_ag

    else:
        miF=form_rango_meses()
    return render(request, 't_anual.html', {
        'mes_c':mes_numero_corto, 'year':years, 'result':resultados,
        'tresultados':tresultados, 'res_filtrados':res_filtrados,
        'form':miF, 'rdefault':default,'tc':tc, 'td':td, 'tv':tv, 'tvf':tvf, 'tve':tve, 'tiag':tiag,
        'erango':erango
        })

def total_anual_nauta(request):
    years=datoday[:4]
    resultados=trtv_nauta.objects.filter(fecha__icontains=years).order_by('fecha')
    tresultados=t_anual_nauta.objects.filter(fecha__icontains=years)
    date_total=[]
    date_total=t_anual_nauta.objects.all()
    coincidencia=False
    res_filtrados=[]
    default=True
    mes_1='Enero'
    mes_2=meses_s[(datoday_full.month)-1]
    erango=False

    #Variables de tresultados filtrados
    tdos=tc=td=tvf=tve=tiagc=tiagp=0

    for x in date_total:
        z=str(x.fecha)
        z=z[:4]
        if z==years: coincidencia=True

    if not coincidencia: x=t_anual_nauta.objects.create(
        fecha=datoday, cant_dos=0, cant_c=0, cant_d=0, valor_facial=0,
        valor_etecsa=0, ingreso_ag_cup=0
        )
    if request.method=='POST':
        miF=form_rango_meses(request.POST)

        if miF.is_valid():
            infForm=miF.cleaned_data
            mes_1=infForm['mes_de_inicio']
            mes_1=mes_1.mes
            mes_2=infForm['mes_final']
            mes_2=mes_2.mes
            match=False
            #Evaluando un rango correcto
            meses_str=str(meses_s)
            m1=meses_str.find(mes_1)
            m2=meses_str.find(mes_2)

            if m1>m2:
                erango=True

            if not erango:
                #Filtrando los meses a mostrar
                default=False

                for x in resultados:
                    if not match:
                        if x.mes==mes_1:
                            res_filtrados.append(x)
                            match=True
                        continue
                    if match:
                        if x.mes!=mes_2:
                            res_filtrados.append(x)
                        else:
                            res_filtrados.append(x)
                            break

                #LLenando las tcant de los resultados filtrados
                for x in res_filtrados:
                    tdos+=x.tcant_dos
                    tc+=x.tcant_c
                    td+=x.tcant_d
                    tvf+=x.tvalor_facial
                    tve+=x.tvalor_etecsa
                    tiagp+=x.tingreso_ag_cup

    else:
        miF=form_rango_meses()
    return render(request, 't_anual_nauta.html', {
        'mes_c':mes_numero_corto, 'form':miF, 'year':years, 'result':resultados, 'tresultados':tresultados,
        'rdefault':default, 'tdos':tdos, 'tc':tc, 'td':td, 'tvf':tvf, 'tve':tve, 'tiagc':tiagc,'tiagp':tiagp,
        'res_filtrados':res_filtrados, 'erango':erango
        })

def total_anual_movil(request):
    years=datoday[:4]
    resultados=trtv_movil.objects.filter(fecha__icontains=years).order_by('fecha')
    tresultados=t_anual_movil.objects.filter(fecha__icontains=years)
    date_total=[]
    date_total=t_anual_movil.objects.all()
    coincidencia=False
    res_filtrados=[]
    default=True
    mes_1='Enero'
    mes_2=meses_s[(datoday_full.month)-1]
    erango=False

    #Variables de tresultados filtrados
    tc=td=tv=tvf=tve=tiagc=tiagp=0

    for x in date_total:
        z=str(x.fecha)
        z=z[:4]
        if z==years: coincidencia=True

    if not coincidencia: x=t_anual_movil.objects.create(
        fecha=datoday, cant_c=0, cant_d=0, cant_v=0, valor_facial=0,
        valor_etecsa=0, ingreso_ag_cup=0
        )

    if request.method=='POST':
        miF=form_rango_meses(request.POST)

        if miF.is_valid():
            infForm=miF.cleaned_data
            mes_1=infForm['mes_de_inicio']
            mes_1=mes_1.mes
            mes_2=infForm['mes_final']
            mes_2=mes_2.mes
            match=False
            #Evaluando un rango correcto
            meses_str=str(meses_s)
            m1=meses_str.find(mes_1)
            m2=meses_str.find(mes_2)

            if m1>m2:
                erango=True

            if not erango:
                #Filtrando los meses a mostrar
                default=False

                for x in resultados:
                    if not match:
                        if x.mes==mes_1:
                            res_filtrados.append(x)
                            match=True
                        continue
                    if match:
                        if x.mes!=mes_2:
                            res_filtrados.append(x)
                        else:
                            res_filtrados.append(x)
                            break

                #LLenando las tcant de los resultados filtrados
                for x in res_filtrados:
                    tc+=x.tcant_c
                    td+=x.tcant_d
                    tv+=x.tcant_v
                    tvf+=x.tvalor_facial
                    tve+=x.tvalor_etecsa
                    tiagp+=x.tingreso_ag_cup

    else:
        miF=form_rango_meses()

    return render(request, 't_anual_movil.html', {
        'mes_c':mes_numero_corto, 'form':miF, 'year':years, 'result':resultados, 'tresultados':tresultados,
        'rdefault':default, 'tc':tc, 'td':td, 'tv':tv, 'tvf':tvf, 'tve':tve, 'tiagc':tiagc,'tiagp':tiagp,
        'res_filtrados':res_filtrados, 'erango':erango
        })

def total_anual_fact(request):
    years=datoday[:4]
    resultados=t_facturaciones.objects.filter(fecha__icontains=years).order_by('fecha')
    tresultados=t_anual_facturaciones.objects.filter(fecha__icontains=years)
    date_total=[]
    date_total=t_anual_facturaciones.objects.all()
    coincidencia=False
    res_filtrados=[]
    default=True
    mes_1='Enero'
    mes_2=meses_s[(datoday_full.month)-1]
    erango=False

    #Variables de tresultados filtrados
    tf=tc=0

    for x in date_total:
        z=str(x.fecha)
        z=z[:4]
        if z==years: coincidencia=True

    if not coincidencia: x=t_anual_facturaciones.objects.create(
        fecha=datoday, factura=0, comision=0
        )

    if request.method=='POST':
        miF=form_rango_meses(request.POST)

        if miF.is_valid():
            infForm=miF.cleaned_data
            mes_1=infForm['mes_de_inicio']
            mes_1=mes_1.mes
            mes_2=infForm['mes_final']
            mes_2=mes_2.mes
            match=False
            #Evaluando un rango correcto
            meses_str=str(meses_s)
            m1=meses_str.find(mes_1)
            m2=meses_str.find(mes_2)

            if m1>m2:
                erango=True

            if not erango:
                #Filtrando los meses a mostrar
                default=False

                for x in resultados:
                    if not match:
                        if x.mes==mes_1:
                            res_filtrados.append(x)
                            match=True
                        continue
                    if match:
                        if x.mes!=mes_2:
                            res_filtrados.append(x)
                        else:
                            res_filtrados.append(x)
                            break

                #LLenando las tcant de los resultados filtrados
                for x in res_filtrados:
                    tf+=x.tfactura
                    tc+=x.tcomision

    else:
        miF=form_rango_meses()

    return render(request, 't_anual_fact.html', {
        'mes_c':mes_numero_corto, 'form':miF, 'year':years, 'result':resultados, 'tresultados':tresultados,
        'rdefault':default, 'tf':tf, 'tc':tc, 'res_filtrados':res_filtrados, 'erango':erango
        })

def total_anual_onat(request):
    erango = res = False
    rdf = True
    years = datoday[:4]
    tdatos_onat = datos_onat = {}
    d_o = []
    sin_r = True

    #Total de ingresos anual
    def results(tabla):
        return tabla.objects.filter(fecha__icontains=years).order_by('fecha')
    
    t_cup = results(trtv_cup)
    t_nauta = results(trtv_nauta)
    t_movil = results(trtv_movil)
    t_fact = results(t_facturaciones)

    t_i = 0

    for x in t_cup: t_i = x.tingreso_ag
    for x in t_nauta: t_i += x.tingreso_ag_cup
    for x in t_movil: t_i += x.tingreso_ag_cup
    for x in t_fact: t_i += x.tcomision

    #Total mensual
    def result(tabla, mts):
        return tabla.objects.filter(fecha__icontains=str(datoday_full.year), mes__icontains = mts)
    
    t_ingreso = []
    ti = 0

    lis_mes = meses_s[:datoday_full.month]
    p3, p5, p10, p15, p20 = 2501, 5000, 7000, 9000, 17000
    fza_trab = 87.5

    if request.method=='POST':
        miF=form_rango_meses(request.POST)

        if miF.is_valid():
            sin_r = False
            infForm=miF.cleaned_data
            mes_1=infForm['mes_de_inicio']
            mes_1=mes_1.mes
            mes_2=infForm['mes_final']
            mes_2=mes_2.mes
            match=False
            #Evaluando un rango correcto
            meses_str=str(meses_s)
            m1=meses_str.find(mes_1)
            m2=meses_str.find(mes_2)

            if m1>m2: erango=True

            if not erango:
                #Filtrando los meses a mostrar
                default=False

                lis_mes = meses_s[meses_s.index(mes_1):meses_s.index(mes_2) + 1]

    else: miF=form_rango_meses()

    total_ingreso = timp = tfzat_ssoc = tpo = 0

    for z in lis_mes:  
        ti = 0

        t_cup = result(trtv_cup, z)
        t_nauta = result(trtv_nauta, z)
        t_movil = result(trtv_movil, z)
        t_fact = result(t_facturaciones, z)

        for x in t_cup: ti = x.tingreso_ag
        for x in t_nauta: ti += x.tingreso_ag_cup
        for x in t_movil: ti += x.tingreso_ag_cup
        for x in t_fact: ti += x.tcomision

        total_ingreso += ti

        if ti < p3: imp = 0
        elif ti < p5: imp = 0.03
        elif ti < p10: imp = 0.05
        elif ti < p15: imp = 0.10
        elif ti < p20: imp = 0.15
        else: imp = 0.20

        imp = imp * ti
        
        timp += imp         #Total de impuestos

        tfzat_ssoc += fza_trab      #Total de fza de trabajo y seguridad social
        tpo += imp + fza_trab       #Total del pago a la Onat
    
        y = {'t_i':ti, 'imp':imp, 'fza_trab':fza_trab, 'pago_onat':imp + fza_trab}
        datos_onat.update({z:y})
        res = True

    pagado = 0

    if sin_r:
        q_pagado = onat_etecsa.objects.filter(fecha__icontains=str(datoday_full.year))
        for x in q_pagado: pagado += x.pagado_en_onat
        q_pagado.delete()
        x = onat_etecsa.objects.create(fecha=datoday_full.date(), pagar_en_onat = tpo, pagado_en_onat = pagado)

    tdatos_onat = {'t_i':total_ingreso, 'imp':timp, 'fza_trab':tfzat_ssoc, 'pago_onat':tpo}

    for x, y in datos_onat.items(): d_o.append(y['t_i'])

    f = open('data.txt','w')
    f.write(str(d_o)+'\n')
    l_m = str(lis_mes).replace("'",'').strip('[]')
    f.write(l_m)
    f.close()

    return render(request, 't_anual_onat.html', {
        'mes_c':mes_numero_corto, 'year':years, 'datos_onat':datos_onat, 'result':res,'form':miF, 'erango':erango,
        'rdf':rdf, 'tresultados':tdatos_onat
        })    
        
def insert_rtc(request):
    errorDeFecha=False
    #Comprobando año en trtv_cup y llenando el trtv del mes actual y anteriores
    mes_atras=mes_numero_corto
    date_ev=datoday[:7]
    t_trtv=trtv_cup.objects.all()
    pas_year=False

    try:
        pas_year=trtv_cup.objects.filter(fecha_icontains=date_ev)
    except:
        if not pas_year: comp_tcant.full_tcant_cup(date_ev,trtv_cup)

    #ingresando datos a la Db
    alert=False
    if request.method=='POST':
        miF=form_insert_cup_movil(request.POST)
        if miF.is_valid():

            infForm=miF.cleaned_data

            #Evaluando si es una fecha correcta
            fok=str(datoday)
            fok=fok.replace('-','')
            fok=int(fok)

            ff=str(infForm['fecha'])
            ff=ff.replace('-','')
            ff=int(ff)

            if fok >= ff:
                #Evaluando si el dato se encuentra en la Db
                coinc=rtv_cup.objects.filter(fecha__icontains=infForm['fecha'])
                borrar=coinc
                if coinc: borrar.delete()
                #numero de mes para q retroceda y salga en la tabla de ese mes
                mes_atras=str(infForm['fecha'])
                mes_atras=mes_atras[5:7]
                if mes_atras[0]=='0': mes_atras.strip('0')
                mes_atras=int(mes_atras)
                #Poniendo por defecto '0' si no es entrado algun valor
                c5=infForm['cant_5']
                c10=infForm['cant_10']
                c20=infForm['cant_20']
                if c5==None: c5=0
                if c10==None: c10=0
                if c20==None: c20=0
                val_facial=c5*5+c10*10+c20*20
                ing_ag=val_facial*0.10
                val_etecsa=val_facial-ing_ag
                x=rtv_cup.objects.create(fecha=infForm['fecha'], cant_c=c5, cant_d=c10, cant_v=c20, valor_facial=val_facial, valor_etecsa=val_etecsa, ingreso_ag=ing_ag)
                alert=True


        #Añadiendo valores a tcant
                sum_tcant_cup(infForm['fecha'])
        #Añadiendo valores a tvalor facial
                sum_tvalor_facial(infForm['fecha'])
        #Añadiendo valores a tvalor etecsa
                sum_tvalor_etecsa(infForm['fecha'])
        #Añadiendo valores a tingreso AG
                sum_tingreso_ag(infForm['fecha'])
        #Añadiendo valores a t_anual
                sum_t_anual(infForm['fecha'])
            else:
                errorDeFecha=True

    else:
        miF=form_insert_cup_movil()
    return render(request, 'insert_rtc.html', {'form':miF, 'alert':alert, 'mes_c':mes_numero_corto, 'mes_a':mes_atras,
    'err':errorDeFecha})

def insert_rtc_nauta(request):
    errorDeFecha=False
    #Comprobando año en trtv_nauta y llenando el trtv del mes actual y anteriores
    mes_atras=mes_numero_corto
    date_ev=datoday[:7]
    t_trtv=trtv_nauta.objects.all()
    pas_year=False

    try:
        pas_year=trtv_nauta.objects.filter(fecha_icontains=date_ev)
    except:
        if not pas_year: comp_tcant.full_tcant_nauta(date_ev,trtv_nauta)

    #ingresando datos a la Db
    alert=False
    if request.method=='POST':
        miF=form_insert_nauta(request.POST)
        if miF.is_valid():

            infForm=miF.cleaned_data

            #Evaluando si es una fecha correcta
            fok=str(datoday)
            fok=fok.replace('-','')
            fok=int(fok)

            ff=str(infForm['fecha'])
            ff=ff.replace('-','')
            ff=int(ff)

            if fok >= ff:
                #Evaluando si el dato se encuentra en la Db, si está se reemplaza
                coinc=rtv_nauta.objects.filter(fecha__icontains=infForm['fecha'])
                borrar=coinc
                if coinc: borrar.delete()
                #numero de mes para q retroceda y salga en la tabla de ese mes
                mes_atras=str(infForm['fecha'])
                mes_atras=mes_atras[5:7]
                if mes_atras[0]=='0': mes_atras.strip('0')
                mes_atras=int(mes_atras)
                #Poniendo por defecto '0' si no es entrado algun valor
                c2=infForm['cant_2']
                c5=infForm['cant_5']
                c10=infForm['cant_10']
                if c2==None: c2=0
                if c5==None: c5=0
                if c10==None: c10=0
                val_facial=c2*50+c5*125+c10*250
                ing_ag_cup=val_facial*0.10
                val_etecsa=val_facial-ing_ag_cup
                x=rtv_nauta.objects.create(fecha=infForm['fecha'], cant_dos=c2, cant_c=c5, cant_d=c10, valor_facial=val_facial, valor_etecsa=val_etecsa, ingreso_ag_cup=ing_ag_cup)
                alert=True

        #Añadiendo valores a tcant
                sum_tcant_nauta(infForm['fecha'])
        #Añadiendo valores a tvalor facial
                sum_tvalor_facial_nauta(infForm['fecha'])
        #Añadiendo valores a tvalor etecsa
                sum_tvalor_etecsa_nauta(infForm['fecha'])
        #Añadiendo valores a tingreso AG CUP
                sum_tingreso_ag_cup_nauta(infForm['fecha'])
        #Añadiendo valores a t_anual
                sum_t_anual_nauta(infForm['fecha'])
            else:
                errorDeFecha=True
    else:
        miF=form_insert_nauta()

    return render(request, 'insert_rtc_nauta.html', {'form':miF, 'alert':alert, 'mes_c':mes_numero_corto, 'mes_a':mes_atras, 'err':errorDeFecha})

def insert_rtc_movil(request):
    errorDeFecha=False
    #Comprobando año en trtv_movil y llenando el trtv del mes actual y anteriores
    mes_atras=mes_numero_corto
    date_ev=datoday[:7]
    t_trtv=trtv_movil.objects.all()
    pas_year=False
    
    try:
        pas_year=trtv_movil.objects.filter(fecha_icontains=date_ev)
    except:
        if not pas_year: comp_tcant.full_tcant_movil(date_ev,trtv_movil)

    #ingresando datos a la Db
    alert=False
    if request.method=='POST':
        miF=form_insert_cup_movil(request.POST)
        if miF.is_valid():

            infForm=miF.cleaned_data

            #Evaluando si es una fecha correcta
            fok=str(datoday)
            fok=fok.replace('-','')
            fok=int(fok)

            ff=str(infForm['fecha'])
            ff=ff.replace('-','')
            ff=int(ff)

            if fok >= ff:
                #Evaluando si el dato se encuentra en la Db, si está se reemplaza
                coinc=rtv_movil.objects.filter(fecha__icontains=infForm['fecha'])
                borrar=coinc
                if coinc: borrar.delete()
                #numero de mes para q retroceda y salga en la tabla de ese mes
                mes_atras=str(infForm['fecha'])
                mes_atras=mes_atras[5:7]
                if mes_atras[0]=='0': mes_atras.strip('0')
                mes_atras=int(mes_atras)
                #Poniendo por defecto '0' si no es entrado algun valor
                c5=infForm['cant_5']
                c10=infForm['cant_10']
                c20=infForm['cant_20']
                if c5==None: c5=0
                if c10==None: c10=0
                if c20==None: c20=0
                val_facial=c5*125+c10*250+c20*500
                ing_ag_cup=val_facial*0.10
                val_etecsa=val_facial-ing_ag_cup
                x=rtv_movil.objects.create(fecha=infForm['fecha'], cant_c=c5, cant_d=c10, cant_v=c20, valor_facial=val_facial, valor_etecsa=val_etecsa, ingreso_ag_cup=ing_ag_cup)
                alert=True

        #Añadiendo valores a tcant
                sum_tcant_movil(infForm['fecha'])
        #Añadiendo valores a tvalor facial
                sum_tvalor_facial_movil(infForm['fecha'])
        #Añadiendo valores a tvalor etecsa
                sum_tvalor_etecsa_movil(infForm['fecha'])
        #Añadiendo valores a tingreso AG CUP
                sum_tingreso_ag_cup_movil(infForm['fecha'])
        #Añadiendo valores a t_anual
                sum_t_anual_movil(infForm['fecha'])
            else:
                errorDeFecha=True

    else:
        miF=form_insert_cup_movil()

    return render(request, 'insert_rtc_movil.html', {'form':miF, 'alert':alert, 'mes_c':mes_numero_corto, 'mes_a':mes_atras, 'err':errorDeFecha})

def insert_fact(request):
    errorDeFecha=False
    #Comprobando año en t_facturaciones y llenando el total del mes actual y anteriores
    mes_atras=mes_numero_corto
    date_ev=datoday[:7]
    t_fact=t_facturaciones.objects.all()
    pas_year=False

    try:
        pas_year=t_facturaciones.objects.filter(fecha_icontains=date_ev)
    except:
        if not pas_year: comp_tcant.full_t_facturaciones(date_ev,t_facturaciones)

    #ingresando datos a la Db
    alert=False
    if request.method=='POST':
        miF=form_insert_fact(request.POST)
        if miF.is_valid():

            infForm=miF.cleaned_data

            #Evaluando si es una fecha correcta
            fok=str(datoday)
            fok=fok.replace('-','')
            fok=int(fok)

            ff=str(infForm['fecha'])
            ff=ff.replace('-','')
            ff=int(ff)

            if fok >= ff:
                #Evaluando si el dato se encuentra en la Db
                coinc=facturaciones.objects.filter(fecha__icontains=infForm['fecha'])
                borrar=coinc
                if coinc: borrar.delete()
                #numero de mes para q retroceda y salga en la tabla de ese mes
                mes_atras=str(infForm['fecha'])
                mes_atras=mes_atras[5:7]
                if mes_atras[0]=='0': mes_atras.strip('0')
                mes_atras=int(mes_atras)

                factura=infForm['factura']
                comision=factura*0.10
                x=facturaciones.objects.create(fecha=infForm['fecha'], factura=factura, comision=comision)
                alert=True

        #Añadiendo valores a tfactura
                sum_tf(infForm['fecha'])
        #Añadiendo valores a tcomision
                sum_tc(infForm['fecha'])
        #Añadiendo valores a t_anual_facturaciones
                sum_t_anual_facturaciones(infForm['fecha'])
            else:
                errorDeFecha=True

    else:
        miF=form_insert_fact()
    return render(request, 'insert_fact.html', {'form':miF, 'alert':alert, 'mes_c':mes_numero_corto, 'mes_a':mes_atras,
    'err':errorDeFecha})

def insert_pago_onat(request):
    errorDeFecha=False
    mes_atras=mes_numero_corto
    alert = False

    if request.method=='POST':
        miF=form_insert_pago_onat(request.POST)
        if miF.is_valid():
            infForm=miF.cleaned_data
            pagado=infForm['pagado']
                        
            #Evaluando si es una fecha correcta
            fok=str(datoday)
            fok=fok.replace('-','')
            fok=int(fok)

            ff=str(infForm['fecha'])
            ff=ff.replace('-','')
            ff=int(ff)

            if fok >= ff:
                alert = True
                pagado = 0
                q_pagado = onat_etecsa.objects.get(fecha__icontains = str(datoday_full.year))
                q_pagado.pagado_en_onat += infForm['pagado']
                q_pagado.save()
                # x = onat_etecsa.objects.create(fecha=str(datoday_full.date()[:5] + '-01-01'), pagar_en_onat = tpo, pagado_en_onat = pagado)

            else:
                errorDeFecha = True
    else:
        miF=form_insert_pago_onat()
    return render(request, 'insert_pago_onat.html', {'form':miF, 'mes_c':mes_numero_corto, 'mes_a':mes_atras, 
        'alert':alert, 'err':errorDeFecha})

def rel_trgtas_vendidas(request, mes_menu=None):
    r=retv.relacion_trgtas_vend_total(request, t_anual, t_anual_nauta, t_anual_movil, mes_menu, 'trgtas_total_anual.html')
    return HttpResponse(r)

def rel_trgtas_vendidas_cup(request, mes_menu=None):
    r=retv.relacion_trgtas_vend(request, rtv_cup, trtv_cup, mes_menu, 'rel_trgtas_vendidas_cup.html')
    return HttpResponse(r)

def rel_trgtas_vendidas_nauta(request, mes_menu=None):
    r=retv.relacion_trgtas_vend(request, rtv_nauta, trtv_nauta, mes_menu, 'rel_trgtas_vendidas_nauta.html')
    return HttpResponse(r)

def rel_trgtas_vendidas_movil(request, mes_menu=None):
    r=retv.relacion_trgtas_vend(request, rtv_movil, trtv_movil, mes_menu, 'rel_trgtas_vendidas_movil.html')
    return HttpResponse(r)

def fact(request, mes_menu=None):
    r=retv.relacion_trgtas_vend(request, facturaciones, t_facturaciones, mes_menu, 'facturaciones.html')
    return HttpResponse(r)

def ap(request):
    return render(request, 'ap.html', {'mes_c':mes_numero_corto})

def prestamistas(request):
    return render(request, 'prestamistas.html', {'mes_c':mes_numero_corto})

def recargas(request):
    return render(request, 'recargas.html', {'mes_c':mes_numero_corto})

def situacion_financiera(request):
    return render(request, 'situacion_financiera.html', {'mes_c':mes_numero_corto})

def onat_e(request, mes_menu=None, limp_reg=None):
    reloading = False
    mes_conv = mes_numero_corto
    if limp_reg == 2:
        x = onat_etecsa.objects.get(fecha__icontains = str(datoday_full.year))
        x.pagado_en_onat = 0
    #mes que se va a mostrar en la tabla
    try:
                
        if mes_menu < 10: mes_conv=str(datoday_full.year) + '-0' + str(mes_menu)
        else: mes_conv=str(datoday_full.year) + '-' + str(mes_menu)
    except:
        mes_menu = mes_numero_corto

    month_to_show = mes_conv

    mes=meses_s[mes_menu-1]

    #Total ingresos

    def results(tabla):
        return tabla.objects.filter(fecha__icontains=month_to_show)

    t_cup = results(trtv_cup)
    t_nauta = results(trtv_nauta)
    t_movil = results(trtv_movil)
    t_fact = results(t_facturaciones)
    
    t_i = 0

    for x in t_cup: t_i = x.tingreso_ag
    for x in t_nauta: t_i += x.tingreso_ag_cup
    for x in t_movil: t_i += x.tingreso_ag_cup
    for x in t_fact: t_i += x.tcomision
    
    #Impuesto segun ingresos

    p3, p5, p10, p15, p20 = 2501, 5000, 7000, 9000, 17000

    p = 0

    if t_i < p3:
        imp = 0
    elif t_i < p5:
        imp = 0.03
        p = 3
    elif t_i < p10:
        imp = 0.05
        p = 5
    elif t_i < p15:
        imp = 0.10
        p = 10
    elif t_i < p20:
        imp = 0.15
        p = 15
    else:
        imp = 0.20
        p = 20

    imp = imp * t_i
    fza_trab = 87.5

    query = onat_etecsa.objects.all()
    a_pagar = pagado = 0    
    for x in query:
        a_pagar = x.pagar_en_onat
        pagado = x.pagado_en_onat

    diferencia = a_pagar - pagado

    return render(request, 'onat_etecsa.html', {'month':mes, 't_i': t_i, 'imp':imp, 'p':p, 
        'pago_onat':a_pagar, 'mes_c':mes_numero_corto, 'mes_menu': mes_menu, 'fza_trab':fza_trab,
        'pagado': pagado, 'diferencia': diferencia})

def extras(request):
    return render(request, 'extras.html', {'mes_c':mes_numero_corto})

def extras_arqueo(request, mes_menu=None):
    return render(request, 'extras_arqueo.html', {'mes_c':mes_numero_corto})
    # r=retv.relacion_trgtas_vend(request, arqueo, t_arqueo, mes_menu, 'extras_arqueo.html')
    # return HttpResponse(r)

class retv():
        '''Renderiza las plantillas'''
        @classmethod
        def relacion_trgtas_vend(cls, reqq, tabla, ttabla, mes_menus, temp):
            #mes del encabezado
            mes=meses_s[mes_numero_corto-1]

            #mes que se va a mostrar en la tabla
            if mes_menus < 10: 
                mes_conv=str(datoday_full.year) + '-0' + str(mes_menus)
            else:
                mes_conv=str(datoday_full.year) + '-' + str(mes_menus)
            
            month_to_show=mes_conv

            mes=meses_s[mes_menus-1]
            resultados=tabla.objects.filter(fecha__icontains=month_to_show).order_by('fecha')
            tresultados=ttabla.objects.filter(fecha__icontains=month_to_show)
            return render(reqq, temp, {'month':mes, 'result':resultados, 'tresult':tresultados, 'mes_c':mes_numero_corto})

        @classmethod
        def relacion_trgtas_vend_total(cls, reqq, ttabla_cup, ttabla_nauta, ttabla_movil, mes_menus, temp):
            #año del encabezado
            year=datoday_full.year
            #año que se va a mostrar en la tabla
            year_to_show=year
            tresultados_cup=ttabla_cup.objects.filter(fecha__icontains=year)
            tresultados_nauta=ttabla_nauta.objects.filter(fecha__icontains=year)
            tresultados_movil=ttabla_movil.objects.filter(fecha__icontains=year)

            #Total
            pvf=nvf=mvf=pve=nve=mve=picup=nicup=micup=0

            for x in tresultados_cup:
                pvf=x.valor_facial
                pve=x.valor_etecsa
                picup=x.ingreso_ag

            for x in tresultados_nauta:
                nvf=x.valor_facial
                nve=x.valor_etecsa
                nicup=x.ingreso_ag_cup

            for x in tresultados_movil:
                mvf=x.valor_facial
                mve=x.valor_etecsa
                micup=x.ingreso_ag_cup

            t3_vf=pvf+nvf+mvf
            t3_ve=pve+nve+mve
            t3_icup=picup+nicup+micup

            return render(
                reqq, temp, {
                'year':year, 'tresult_cup':tresultados_cup, 'tresult_nauta':tresultados_nauta,
                'tresult_movil':tresultados_movil, 'mes_c':mes_numero_corto, 't3_vf':t3_vf, 't3_ve':t3_ve, 't3_icup':t3_icup
                }
            )

class comp_tcant():
    '''Crea el mes actual y anteriores de tcant'''

    @classmethod
    def full_tcant_cup(cls, date_e, ttabla):
        date_total=[]
        mes_total=[]
        date_total=ttabla.objects.all()
        coincidencia=False
        for x in date_total:
            z=str(x.fecha)
            z=z[:7]
            if z==date_e:
                i=int(date_e[5:7])-1
                if i<10: i='0'+str(i)
                date_e=date_e[:5]+str(i)
                if int(i)<1: break
                coincidencia=True
        else:
            if not coincidencia: x=ttabla.objects.create(fecha=date_e+'-01', tcant_c=0, tcant_d=0, tcant_v=0, tvalor_facial=0, tvalor_etecsa=0, tingreso_ag=0, mes=meses_s[int(date_e[5:7])-1])
            i=int(date_e[5:7])-1
            if i<10: i='0'+str(i)
            date_e=date_e[:5]+str(i)
        if date_e[5:]!='00': comp_tcant.full_tcant_cup(date_e,trtv_cup)

    @classmethod
    def full_tcant_nauta(cls, date_e, ttabla):
        date_total=[]
        date_total=ttabla.objects.all()
        coincidencia=False
        for x in date_total:
            z=str(x.fecha)
            z=z[:7]
            if z==date_e:
                i=int(date_e[5:7])-1
                if i<10: i='0'+str(i)
                date_e=date_e[:5]+str(i)
                if int(i)<1: break
                coincidencia=True
        else:
            if not coincidencia: x=ttabla.objects.create(fecha=date_e+'-01', tcant_dos=0, tcant_c=0, tcant_d=0, tvalor_facial=0, tvalor_etecsa=0, tingreso_ag_cup=0, mes=meses_s[int(date_e[5:7])-1])
            i=int(date_e[5:7])-1
            if i<10: i='0'+str(i)
            date_e=date_e[:5]+str(i)
        if date_e[5:]!='00': comp_tcant.full_tcant_nauta(date_e,trtv_nauta)

    @classmethod
    def full_tcant_movil(cls, date_e, ttabla):
        date_total=[]
        date_total=ttabla.objects.all()
        coincidencia=False
        for x in date_total:
            z=str(x.fecha)
            z=z[:7]
            if z==date_e:
                i=int(date_e[5:7])-1
                if i<10: i='0'+str(i)
                date_e=date_e[:5]+str(i)
                if int(i)<1: break
                coincidencia=True
        else:
            if not coincidencia: x=ttabla.objects.create(fecha=date_e+'-01', tcant_c=0, tcant_d=0, tcant_v=0, tvalor_facial=0, tvalor_etecsa=0, tingreso_ag_cup=0, mes=meses_s[int(date_e[5:7])-1])
            i=int(date_e[5:7])-1
            if i<10: i='0'+str(i)
            date_e=date_e[:5]+str(i)
        if date_e[5:]!='00': comp_tcant.full_tcant_movil(date_e,trtv_movil)

    @classmethod
    def full_t_facturaciones(cls, date_e, ttabla):
        date_total=[]
        date_total=ttabla.objects.all()
        coincidencia=False
        for x in date_total:
            z=str(x.fecha)
            z=z[:7]
            if z==date_e:
                i=int(date_e[5:7])-1
                if i<10: i='0'+str(i)
                date_e=date_e[:5]+str(i)
                if int(i)<1: break
                coincidencia=True
        else:
            if not coincidencia: x=ttabla.objects.create(fecha=date_e+'-01', tfactura=0, tcomision=0, mes=meses_s[int(date_e[5:7])-1])
            i=int(date_e[5:7])-1
            if i<10: i='0'+str(i)
            date_e=date_e[:5]+str(i)
        if date_e[5:]!='00': comp_tcant.full_t_facturaciones(date_e,t_facturaciones)
