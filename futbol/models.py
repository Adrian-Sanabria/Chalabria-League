from django.db import models

class Equipo(models.Model):
    nombre = models.CharField(max_length=100)

    def __str__(self):
        return self.nombre
    logo = models.ImageField(upload_to='logos/', null=True, blank=True)


class Grupo(models.Model):
    nombre = models.CharField(max_length=1)  # A, B, C, D

    def __str__(self):
        return f"Grupo {self.nombre}"


class GrupoEquipo(models.Model):
    equipo = models.ForeignKey(Equipo, on_delete=models.CASCADE)
    grupo = models.ForeignKey(Grupo, on_delete=models.CASCADE)

    pj = models.IntegerField(default=0)
    g = models.IntegerField(default=0)
    e = models.IntegerField(default=0)
    p = models.IntegerField(default=0)
    gf = models.IntegerField(default=0)
    gc = models.IntegerField(default=0)
    puntos = models.IntegerField(default=0)


class Partido(models.Model):
    FASES = [
        ('grupos', 'Grupos'),
        ('cuartos', 'Cuartos'),
        ('semis', 'Semifinal'),
        ('final', 'Final'),
    ]

    equipo_local = models.ForeignKey(Equipo, on_delete=models.CASCADE, related_name='local')
    equipo_visitante = models.ForeignKey(Equipo, on_delete=models.CASCADE, related_name='visitante')

    goles_local = models.IntegerField(null=True, blank=True)
    goles_visitante = models.IntegerField(null=True, blank=True)

    fase = models.CharField(max_length=20, choices=FASES)
    grupo = models.ForeignKey(Grupo, on_delete=models.CASCADE, null=True, blank=True)

    fecha = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"{self.equipo_local} vs {self.equipo_visitante}"
    
def actualizar_tabla(partido):
    if partido.fase != 'grupos':
        return

    local = GrupoEquipo.objects.get(equipo=partido.equipo_local, grupo=partido.grupo)
    visitante = GrupoEquipo.objects.get(equipo=partido.equipo_visitante, grupo=partido.grupo)

    gl = partido.goles_local
    gv = partido.goles_visitante

    local.pj += 1
    visitante.pj += 1

    local.gf += gl
    local.gc += gv

    visitante.gf += gv
    visitante.gc += gl

    if gl > gv:
        local.g += 1
        local.puntos += 3
        visitante.p += 1
    elif gv > gl:
        visitante.g += 1
        visitante.puntos += 3
        local.p += 1
    else:
        local.e += 1
        visitante.e += 1
        local.puntos += 1
        visitante.puntos += 1

    local.save()
    visitante.save()

from django.db.models.signals import post_save
from django.dispatch import receiver

@receiver(post_save, sender=Partido)
def actualizar_despues_guardar(sender, instance, created, **kwargs):
    if instance.goles_local is not None and instance.goles_visitante is not None:
        actualizar_tabla(instance)