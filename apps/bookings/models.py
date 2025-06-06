from django.db import models
from django.utils.translation import gettext_lazy as _
from django.core.exceptions import ValidationError
from django.db.models import Q

class BookingStatus(models.TextChoices):
    PENDING = 'PENDING', _('Ожидает подтверждения')
    CONFIRMED = 'CONFIRMED', _('Подтверждено')
    REJECTED = 'REJECTED', _('Отклонено')
    CANCELLED = 'CANCELLED', _('Отменено')
    CANCELLED_BY_OWNER = 'cancelled_by_owner', _('Отменено арендодателем')


class Booking(models.Model):
    offer = models.ForeignKey(
        'rent.Offer',
        on_delete=models.CASCADE,
        related_name='bookings'
    )
    renter = models.ForeignKey(
        'user.User',
        on_delete=models.CASCADE,
        related_name='bookings'
    )
    start_date = models.DateField()
    end_date = models.DateField()
    status = models.CharField(
        max_length=20,
        choices=BookingStatus.choices,
        default=BookingStatus.PENDING
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def clean(self):
        if self.end_date <= self.start_date:
            raise ValidationError(_("Дата окончания должна быть позже даты начала."))
        overlapping_bookings = Booking.objects.filter(
            Q(offer=self.offer) &
            Q(status=BookingStatus.CONFIRMED) &
            Q(start_date__lte=self.end_date) &
            Q(end_date__gte=self.start_date)
        ).exclude(id=self.id)
        if overlapping_bookings.exists():
            raise ValidationError(_("Выбранные даты пересекаются с другим подтверждённым бронированием."))

        duplicate_pending = Booking.objects.filter(
            offer=self.offer,
            renter=self.renter,
            start_date=self.start_date,
            end_date=self.end_date,
            status=BookingStatus.PENDING
        ).exclude(id=self.id)

        if duplicate_pending.exists():
            raise ValidationError(_("Вы уже создали заявку на эти даты. Ожидайте подтверждения."))

    def save(self, *args, **kwargs):
        if self.status in [BookingStatus.PENDING, BookingStatus.CONFIRMED]:
            self.full_clean()
        super().save(*args, **kwargs)

    class Meta:
        indexes = [
            models.Index(fields=['offer', 'start_date', 'end_date']),
            models.Index(fields=['renter']),
            models.Index(fields=['status']),
        ]

    def __str__(self):
        return f"Бронирование {self.offer.title} от {self.renter.username}"