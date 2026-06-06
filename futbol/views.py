from django.shortcuts import render
from .models import Grupo, Partido
from django.db.models import Q

def inicio(request):
    grupos = Grupo.objects.all().order_by('nombre')

    clasificados_por_grupo = {}

    for grupo in grupos:
        tabla = []

        for ge in grupo.grupoequipo_set.all():
            equipo = ge.equipo

            partidos = Partido.objects.filter(
                Q(equipo_local=equipo) | Q(equipo_visitante=equipo),
                grupo=grupo
            )

            pj = partidos.count()
            g = e = p = gf = gc = 0

            for partido in partidos:
                if partido.goles_local is None:
                    continue

                if partido.equipo_local == equipo:
                    gf += partido.goles_local
                    gc += partido.goles_visitante

                    if partido.goles_local > partido.goles_visitante:
                        g += 1
                    elif partido.goles_local == partido.goles_visitante:
                        e += 1
                    else:
                        p += 1
                else:
                    gf += partido.goles_visitante
                    gc += partido.goles_local

                    if partido.goles_visitante > partido.goles_local:
                        g += 1
                    elif partido.goles_visitante == partido.goles_local:
                        e += 1
                    else:
                        p += 1

            puntos = g * 3 + e
            dg = gf - gc

            tabla.append({
                'equipo': equipo,
                'pj': pj,
                'g': g,
                'e': e,
                'p': p,
                'gf': gf,
                'gc': gc,
                'dg': dg,
                'puntos': puntos
            })

        # ORDENAR
        tabla.sort(key=lambda x: (x['puntos'], x['dg']), reverse=True)
        grupo.tabla = tabla

        # GUARDAR TOP 2 POR GRUPO
        if len(tabla) >= 2:
            clasificados_por_grupo[grupo.nombre] = [
                tabla[0]['equipo'],
                tabla[1]['equipo']
            ]

    # 🏆 ARMAR CUARTOS (TIPO CHAMPIONS)
    cuartos_auto = []

    try:
        A1, A2 = clasificados_por_grupo['A']
        B1, B2 = clasificados_por_grupo['B']
        C1, C2 = clasificados_por_grupo['C']
        D1, D2 = clasificados_por_grupo['D']

        cuartos_auto = [
            (A1, B2),
            (B1, A2),
            (C1, D2),
            (D1, C2),
        ]

    except KeyError:
        # Por si aún no tienes todos los grupos completos
        cuartos_auto = []

    return render(request, "index.html", {
        "grupos": grupos,
        "cuartos_auto": cuartos_auto
    })