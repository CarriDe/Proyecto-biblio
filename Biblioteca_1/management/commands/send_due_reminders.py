from datetime import timedelta

from django.core.mail import send_mail
from django.core.management.base import BaseCommand
from django.utils import timezone

from Biblioteca_1.models import Prestamo
from django.conf import settings


class Command(BaseCommand):
    help = 'Envía recordatorios por email para préstamos próximos a vencer'

    def handle(self, *args, **options):
        ahora = timezone.now()
        manana = ahora + timedelta(days=1)
        proximos = Prestamo.objects.filter(
            estado__in=['RESERVADO', 'EN_PRESTAMO'],
            fecha_fin__date__in=[ahora.date(), manana.date()],
        ).select_related('usuario', 'libro')

        if not proximos:
            self.stdout.write('No hay recordatorios para enviar.')
            return

        for prestamo in proximos:
            if not prestamo.usuario.email:
                continue

            fecha_fin = prestamo.fecha_fin.strftime('%d/%m/%Y') if prestamo.fecha_fin else 'sin fecha'
            subject = f'Recordatorio devolución: {prestamo.libro.titulo}'
            message = (
                f'Hola {prestamo.usuario.first_name or prestamo.usuario.username},\n\n'
                f'Recordamos que el libro "{prestamo.libro.titulo}" tiene fecha de devolución programada para el {fecha_fin}.\n'
                'Por favor devuelve el libro puntualmente para evitar demoras.\n\n'
                'Gracias por usar la Biblioteca.'
            )

            send_mail(
                subject,
                message,
                settings.DEFAULT_FROM_EMAIL,
                [prestamo.usuario.email],
                fail_silently=True,
            )
            self.stdout.write(f'Recordatorio enviado a {prestamo.usuario.email} para {prestamo.libro.titulo}.')
