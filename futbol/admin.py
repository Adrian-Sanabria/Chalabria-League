from django.contrib import admin
from .models import Equipo, Grupo, GrupoEquipo, Partido

admin.site.register(Equipo)
admin.site.register(Grupo)
admin.site.register(GrupoEquipo)
admin.site.register(Partido)