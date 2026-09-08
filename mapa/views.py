import requests
import json

from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from .spatial import buscar_manzana
from django.conf import settings

@login_required
def consulta_view(request):
   

    resultado = None

    

    if request.method == "POST":
        direccion = request.POST.get("direccion")

        print("DIRECCION RECIBIDA:", direccion)

        url = "https://nominatim.openstreetmap.org/search"

        params = {
            "q": direccion,
            "format": "json",
            "limit": 1,
            "addressdetails": 1,
        }

        headers = {
            "User-Agent": "mapa_chile_app/1.0"
        }

        response = requests.get(
            url,
            params=params,
            headers=headers,
            timeout=10
        )

        datos = response.json()

        print("RESPUESTA NOMINATIM:", datos)

        if datos:

            lat = datos[0]["lat"]
            lon = datos[0]["lon"]

            codigo_postal = datos[0].get(
                "address", {}
                ).get(
                    "postcode",
                    "No disponible"
                )

            manzana = buscar_manzana(lat, lon)
            datos_manzana = None

            if manzana:

                props = manzana["props"]

                datos_manzana = {
                    "ubicacion": {
                        "Región": props.get("REGION"),
                        "Provincia": props.get("PROVINCIA"),
                        "Comuna": props.get("COMUNA"),
                        "Distrito": props.get("DISTRITO"),
                        "Localidad": props.get("LOCALIDAD"),
                        "Entidad": props.get("ENTIDAD"),
                        "Área": props.get("AREA_C"),
                        "Categoría": props.get("CATEGORIA"),
                        "Código de manzana": props.get("COD_MANZANA"),
                        "Tipo de manzana": props.get("TIPO_MZ"),
                    },

                    "poblacion": {
                        "Personas": props.get("n_per"),
                        "Hombres": props.get("n_hombres"),
                        "Mujeres": props.get("n_mujeres"),
                        "Edad promedio": props.get("prom_edad"),
                        "0 a 5 años": props.get("n_edad_0_5"),
                        "6 a 13 años": props.get("n_edad_6_13"),
                        "14 a 17 años": props.get("n_edad_14_17"),
                        "18 a 24 años": props.get("n_edad_18_24"),
                        "25 a 44 años": props.get("n_edad_25_44"),
                        "45 a 59 años": props.get("n_edad_45_59"),
                        "60 años o más": props.get("n_edad_60_mas"),
                    },

                    "educacion": {
                        "Escolaridad promedio (18 años o más)": props.get("prom_escolaridad18"),
                        "Asistencia a educación parvularia": props.get("n_asistencia_parv"),
                        "Asistencia a educación básica": props.get("n_asistencia_basica"),
                        "Asistencia a educación media": props.get("n_asistencia_media"),
                        "Asistencia a educación superior": props.get("n_asistencia_superior"),
                        "Nunca cursó / primera infancia": props.get(
                            "n_cine_nunca_curso_primera_infancia"
                        ),
                        "Nivel educacional primario": props.get("n_cine_primaria"),
                        "Nivel educacional secundario": props.get("n_cine_secundaria"),

                        "Educación terciaria, maestría o doctorado": props.get(
                            "n_cine_terciaria_maestria_doctorado"
                        ),
                        "Educación especial o diferencial": props.get(
                            "n_cine_especial_diferencial"
                        ),
                        "Personas analfabetas": props.get("n_analfabet"),
                    }, 

                    "trabajo": {
                        "Personas ocupadas": props.get("n_ocupado"),
                        "Personas desocupadas": props.get("n_desocupado"),
                        "Fuera de la fuerza de trabajo": props.get(
                            "n_fuera_fuerza_trabajo"
                        ),
                        "Trabajadores independientes": props.get(
                            "n_cise_rec_independientes"
                        ),
                        "Trabajadores dependientes": props.get(
                            "n_cise_rec_dependientes"
                        ),
                        "Trabajadores no remunerados": props.get(
                            "n_cise_rec_trabajador_no_remunerado"
                        ),
                    },

                    "transporte": {
                        "Automóvil": props.get("n_transporte_auto"),
                        "Transporte público": props.get("n_transporte_publico"),
                        "Caminata": props.get("n_transporte_camina"),
                        "Bicicleta": props.get("n_transporte_bicicleta"),
                        "Motocicleta": props.get("n_transporte_motocicleta"),
                        "Caballo, lancha o bote": props.get(
                            "n_transporte_cab_lan_bote"
                        ),
                        "Otros medios de transporte": props.get(
                            "n_transporte_otros"
                        ),
                    },

                    "hogares": {
                        "Total de hogares": props.get("n_hog"),
                        "Promedio de personas por hogar": props.get("prom_per_hog"),
                        "Hogares unipersonales": props.get("n_hog_unipersonales"),
                        "Hogares con personas de 60 años o más": props.get("n_hog_60"),
                        "Hogares con menores": props.get("n_hog_menores"),
                        "Hogares con jefatura femenina": props.get("n_jefatura_mujer"),
                    },

                    "vivienda": {
                        "Total de viviendas particulares": props.get("n_vp"),
                        "Viviendas ocupadas": props.get("n_vp_ocupada"),
                        "Viviendas desocupadas": props.get("n_vp_desocupada"),
                        "Casas": props.get("n_tipo_viv_casa"),
                        "Departamentos": props.get("n_tipo_viv_depto"),
                        "Viviendas indígenas": props.get("n_tipo_viv_indigena"),
                        "Piezas": props.get("n_tipo_viv_pieza"),
                        "Mediaguas": props.get("n_tipo_viv_mediagua"),
                        "Viviendas móviles": props.get("n_tipo_viv_movil"),
                        "Otros tipos de vivienda": props.get("n_tipo_viv_otro"),
                        "Viviendas hacinadas": props.get("n_viv_hacinadas"),
                        "Viviendas irrecuperables": props.get("n_viv_irrecuperables"),
                        "Hogares allegados": props.get("n_hog_allegados"),
                        "Núcleos hacinados allegados": props.get(
                            "n_nucleos_hacinados_allegados"
                        ),
                        "Viviendas no ampliables": props.get("n_viv_no_ampliables"),
                        "Déficit cuantitativo": props.get("n_deficit_cuantitativo"),
                    },

                    "tenencia": {
                        "Vivienda propia pagada": props.get("n_tenencia_propia_pagada"),
                        "Vivienda propia pagándose": props.get("n_tenencia_propia_pagandose"),
                        "Arrendada con contrato": props.get(
                            "n_tenencia_arrendada_contrato"
                        ),
                        "Arrendada sin contrato": props.get(
                            "n_tenencia_arrendada_sin_contrato"
                        ),
                        "Cedida por trabajo": props.get("n_tenencia_cedida_trabajo"),
                        "Cedida por familiar": props.get("n_tenencia_cedida_familiar"),
                        "Otra forma de tenencia": props.get("n_tenencia_otro"),
                    },

                    "dormitorios": {
                        "Viviendas con 1 dormitorio": props.get("n_dormitorios_1"),
                        "Viviendas con 2 dormitorios": props.get("n_dormitorios_2"),
                        "Viviendas con 3 dormitorios": props.get("n_dormitorios_3"),
                        "Viviendas con 4 dormitorios": props.get("n_dormitorios_4"),
                        "Viviendas con 5 dormitorios": props.get("n_dormitorios_5"),
                        "Viviendas con 6 dormitorios o más": props.get(
                            "n_dormitorios_6_o_mas"
                        ),
                    },

                    "tecnologia": {
                        "Hogares con teléfono móvil": props.get("n_serv_tel_movil"),
                        "Hogares con computador": props.get("n_serv_compu"),
                        "Hogares con tablet": props.get("n_serv_tablet"),
                        "Hogares con internet fijo": props.get("n_serv_internet_fija"),
                        "Hogares con internet móvil": props.get("n_serv_internet_movil"),
                        "Hogares con internet satelital": props.get(
                            "n_serv_internet_satelital"
                        ),
                        "Hogares con acceso a internet": props.get("n_internet"),
                    },

                    "servicios_basicos": {
                        "Agua de red pública": props.get("n_fuente_agua_publica"),
                        "Agua de pozo": props.get("n_fuente_agua_pozo"),
                        "Agua mediante camión": props.get("n_fuente_agua_camion"),
                        "Agua de río": props.get("n_fuente_agua_rio"),

                        "Agua por llave dentro de la vivienda": props.get(
                            "n_distrib_agua_llave"
                        ),
                        "Agua por llave fuera de la vivienda": props.get(
                            "n_distrib_agua_llave_fuera"
                        ),
                        "Agua por acarreo": props.get("n_distrib_agua_acarreo"),

                        "Alcantarillado dentro de la vivienda": props.get(
                            "n_serv_hig_alc_dentro"
                        ),
                        "Alcantarillado fuera de la vivienda": props.get(
                            "n_serv_hig_alc_fuera"
                        ),
                        "Fosa séptica": props.get("n_serv_hig_fosa"),
                        "Pozo negro": props.get("n_serv_hig_pozo"),
                        "Acequia o canal": props.get("n_serv_hig_acequia_canal"),
                        "Baño químico": props.get("n_serv_hig_bano_quimico"),
                        "Baño seco": props.get("n_serv_hig_bano_seco"),
                        "Sin servicio higiénico": props.get("n_serv_hig_no_tiene"),

                        "Electricidad de red pública": props.get(
                            "n_fuente_elect_publica"
                        ),
                        "Electricidad mediante diésel": props.get(
                            "n_fuente_elect_diesel"
                        ),
                        "Electricidad solar": props.get("n_fuente_elect_solar"),
                        "Electricidad eólica": props.get("n_fuente_elect_eolica"),
                        "Otra fuente de electricidad": props.get(
                            "n_fuente_elect_otro"
                        ),
                        "Sin electricidad": props.get("n_fuente_elect_no_tiene"),

                        "Recolección de basura por servicios": props.get(
                            "n_basura_servicios"
                        ),
                        "Basura enterrada": props.get("n_basura_entierra"),
                        "Basura en sitio eriazo": props.get("n_basura_eriazo"),
                        "Basura en río": props.get("n_basura_rio"),
                        "Otra eliminación de basura": props.get("n_basura_otro"),
                        "Cajón u otro servicio higiénico": props.get(
                            "n_serv_hig_cajon_otro"
                        ),
                    },

                    "materialidad": {
                        # Paredes
                        "Paredes de hormigón": props.get("n_mat_paredes_hormigon"),
                        "Paredes de albañilería": props.get("n_mat_paredes_albanileria"),
                        "Tabique forrado": props.get("n_mat_paredes_tabique_forrado"),
                        "Tabique sin forro": props.get("n_mat_paredes_tabique_sin_forro"),
                        "Paredes artesanales": props.get("n_mat_paredes_artesanal"),
                        "Paredes de material precario": props.get(
                            "n_mat_paredes_precarios"
                        ),

                        # Techos
                        "Techo de tejas": props.get("n_mat_techo_tejas"),
                        "Techo de hormigón": props.get("n_mat_techo_hormigon"),
                        "Techo de zinc": props.get("n_mat_techo_zinc"),
                        "Techo de fibrocemento": props.get("n_mat_techo_fibrocemento"),
                        "Techo de fonolita": props.get("n_mat_techo_fonolita"),
                        "Techo de paja": props.get("n_mat_techo_paja"),
                        "Techo de material precario": props.get(
                            "n_mat_techo_precarios"
                        ),
                        "Sin cubierta de techo": props.get(
                            "n_mat_techo_sin_cubierta"
                        ),

                        # Pisos
                        "Radier con revestimiento": props.get(
                            "n_mat_piso_radier_con_revestimiento"
                        ),
                        "Radier sin revestimiento": props.get(
                            "n_mat_piso_radier_sin_revestimiento"
                        ),
                        "Piso de baldosa de cemento": props.get(
                            "n_mat_piso_baldosa_cemento"
                        ),
                        "Piso de capa de cemento": props.get(
                            "n_mat_piso_capa_cemento"
                        ),
                        "Piso de tierra": props.get("n_mat_piso_tierra"),
                    },

                    "energia": {
                        # Combustible para cocinar
                        "Cocina con gas": props.get("n_comb_cocina_gas"),
                        "Cocina con parafina": props.get("n_comb_cocina_parafina"),
                        "Cocina con leña": props.get("n_comb_cocina_lena"),
                        "Cocina con pellet": props.get("n_comb_cocina_pellet"),
                        "Cocina con carbón": props.get("n_comb_cocina_carbon"),
                        "Cocina con electricidad": props.get(
                            "n_comb_cocina_electricidad"
                        ),
                        "Cocina con energía solar": props.get("n_comb_cocina_solar"),
                        "No utiliza combustible para cocinar": props.get(
                            "n_comb_cocina_no_utiliza"
                        ),

                        # Combustible para calefacción
                        "Calefacción con gas": props.get("n_comb_calefaccion_gas"),
                        "Calefacción con parafina": props.get(
                            "n_comb_calefaccion_parafina"
                        ),
                        "Calefacción con leña": props.get("n_comb_calefaccion_lena"),
                        "Calefacción con pellet": props.get(
                            "n_comb_calefaccion_pellet"
                        ),
                        "Calefacción con carbón": props.get(
                            "n_comb_calefaccion_carbon"
                        ),
                        "Calefacción eléctrica": props.get(
                            "n_comb_calefaccion_electricidad"
                        ),
                        "Otra fuente de calefacción": props.get(
                            "n_comb_calefaccion_otra"
                        ),
                        "No utiliza calefacción": props.get(
                            "n_comb_calefaccion_no_utiliza"
                        ),
                    },

                    "caracteristicas_poblacion": {
                        "Personas inmigrantes": props.get("n_inmigrantes"),
                        "Nacionalidad": props.get("n_nacionalidad"),
                        "Pertenencia a pueblos originarios": props.get("n_pueblos_orig"),
                        "Afrodescendencia": props.get("n_afrodescendencia"),
                        "Lengua indígena": props.get("n_lengua_indigena"),
                        "Religión": props.get("n_religion"),

                        # Discapacidad y dificultades
                        "Dificultad para ver": props.get("n_dificultad_ver"),
                        "Dificultad para oír": props.get("n_dificultad_oir"),
                        "Dificultad para moverse": props.get("n_dificultad_mover"),
                        "Dificultad cognitiva": props.get("n_dificultad_cogni"),
                        "Dificultad para el cuidado personal": props.get(
                            "n_dificultad_cuidado"
                        ),
                        "Dificultad para comunicarse": props.get(
                            "n_dificultad_comunic"
                        ),
                        "Personas con discapacidad": props.get("n_discapacidad"),

                        # Estado civil o conyugal
                        "Casadas": props.get("n_estcivcon_casado"),
                        "Convivientes": props.get("n_estcivcon_conviviente"),
                        "Con acuerdo de unión civil": props.get(
                            "n_estcivcon_conv_civil"
                        ),
                        "Anuladas, separadas o divorciadas": props.get(
                            "n_estcivcon_anul_sep_div"
                        ),
                        "Viudas": props.get("n_estcivcon_viudo"),
                        "Solteras": props.get("n_estcivcon_soltero"),
                    }, 

                    "ocupaciones": {
                        "Grupo de ocupación 1": props.get("n_ciuo_1"),
                        "Grupo de ocupación 2": props.get("n_ciuo_2"),
                        "Grupo de ocupación 3": props.get("n_ciuo_3"),
                        "Grupo de ocupación 4": props.get("n_ciuo_4"),
                        "Grupo de ocupación 5": props.get("n_ciuo_5"),
                        "Grupo de ocupación 6": props.get("n_ciuo_6"),
                        "Grupo de ocupación 7": props.get("n_ciuo_7"),
                        "Grupo de ocupación 8": props.get("n_ciuo_8"),
                        "Grupo de ocupación 9": props.get("n_ciuo_9"),
                        "Grupo de ocupación 0": props.get("n_ciuo_0"),
                    },

                    "actividad_economica": {
                        "Actividad económica A": props.get("n_caenes_A"),
                        "Actividad económica B": props.get("n_caenes_B"),
                        "Actividad económica C": props.get("n_caenes_C"),
                        "Actividad económica D": props.get("n_caenes_D"),
                        "Actividad económica E": props.get("n_caenes_E"),
                        "Actividad económica F": props.get("n_caenes_F"),
                        "Actividad económica G": props.get("n_caenes_G"),
                        "Actividad económica H": props.get("n_caenes_H"),
                        "Actividad económica I": props.get("n_caenes_I"),
                        "Actividad económica J": props.get("n_caenes_J"),
                        "Actividad económica K": props.get("n_caenes_K"),
                        "Actividad económica L": props.get("n_caenes_L"),
                        "Actividad económica M": props.get("n_caenes_M"),
                        "Actividad económica N": props.get("n_caenes_N"),
                        "Actividad económica O": props.get("n_caenes_O"),
                        "Actividad económica P": props.get("n_caenes_P"),
                        "Actividad económica Q": props.get("n_caenes_Q"),
                        "Actividad económica R": props.get("n_caenes_R"),
                        "Actividad económica S": props.get("n_caenes_S"),
                        "Actividad económica T": props.get("n_caenes_T"),
                        "Actividad económica U": props.get("n_caenes_U"),
                    },                                               
                }

                print("DATOS MANZANA:")
                print(datos_manzana)
            
            resultado = {
                "direccion": datos[0]["display_name"],
                "lat": lat,
                "lon": lon,
                "codigo_postal": codigo_postal,
                "manzana": manzana,
                "manzana_json": json.dumps(manzana["feature"]) if manzana else None,
                "datos_manzana": datos_manzana,
            }

    return render(
        request,
        "mapa/consulta.html",
        {
            "resultado": resultado
        }
    )

def obtener_coordenadas(direccion):

    url = "https://nominatim.openstreetmap.org/search"

    params = {
        "q": direccion,
        "format": "json",
        "limit": 1,
    }

    headers = {
        "User-Agent": "mapa_chile_app/1.0"
    }

    response = requests.get(
        url,
        params=params,
        headers=headers,
        timeout=10
    )

    datos = response.json()

    if datos:
        return {
            "lat": datos[0]["lat"],
            "lon": datos[0]["lon"],
        }

    return None


@login_required
def ruta_view(request):

    resultado = None
    error = None

    if request.method == "POST":

        origen = request.POST.get("origen")
        destino = request.POST.get("destino")

        url = "https://maps.googleapis.com/maps/api/distancematrix/json"

        modos = {
            "auto": "driving",
            "caminando": "walking",
            "bicicleta": "bicycling",
        }

        tiempos = {}
        distancia = None
        origen_google = None
        destino_google = None

        for nombre, modo in modos.items():

            params = {
                "origins": origen,
                "destinations": destino,
                "mode": modo,
                "language": "es",
                "key": settings.GOOGLE_MAPS_API_KEY,
            }

            response = requests.get(
                url,
                params=params,
                timeout=10
            )

            datos = response.json()

            print(f"RESPUESTA GOOGLE {nombre}:", datos)

            if datos.get("status") == "OK":

                elemento = datos["rows"][0]["elements"][0]

                if elemento.get("status") == "OK":

                    tiempos[nombre] = elemento["duration"]["text"]

                    if distancia is None:
                        distancia = elemento["distance"]["text"]

                    if origen_google is None:
                        origen_google = datos["origin_addresses"][0]

                    if destino_google is None:
                        destino_google = datos["destination_addresses"][0]

                else:
                    tiempos[nombre] = "No disponible"

            else:
                tiempos[nombre] = "No disponible"

        if origen_google and destino_google:

            

            coordenadas_origen = obtener_coordenadas(origen_google)
            coordenadas_destino = obtener_coordenadas(destino_google)

            resultado = {
                "origen": origen_google,
                "destino": destino_google,
                "distancia": distancia,
                "auto": tiempos.get("auto"),
                "caminando": tiempos.get("caminando"),
                "bicicleta": tiempos.get("bicicleta"),

                "origen_lat": coordenadas_origen["lat"] if coordenadas_origen else None,
                "origen_lon": coordenadas_origen["lon"] if coordenadas_origen else None,

                "destino_lat": coordenadas_destino["lat"] if coordenadas_destino else None,
                "destino_lon": coordenadas_destino["lon"] if coordenadas_destino else None,
            }
            
        else:
            error = "No fue posible calcular la ruta."

    return render(
        request,
        "mapa/ruta.html",
        {
            "resultado": resultado,
            "error": error,
        }
    )  