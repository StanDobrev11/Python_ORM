from datetime import date, timedelta

from django.core.exceptions import ValidationError
from django.core.validators import MaxLengthValidator
from django.db import models


# Create your models here.
class BaseCharacter(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()

    class Meta:
        abstract = True


class Mage(BaseCharacter):
    elemental_power = models.CharField(max_length=100)
    spellbook_type = models.CharField(max_length=100)


class Assassin(BaseCharacter):
    weapon_type = models.CharField(max_length=100)
    assassination_technique = models.CharField(max_length=100)


class DemonHunter(BaseCharacter):
    weapon_type = models.CharField(max_length=100)
    demon_slaying_ability = models.CharField(max_length=100)


class TimeMage(Mage):
    time_magic_mastery = models.CharField(max_length=100)
    temporal_shift_ability = models.CharField(max_length=100)


class Necromancer(Mage):
    raise_dead_ability = models.CharField(max_length=100)


class ViperAssassin(Assassin):
    venomous_strikes_mastery = models.CharField(max_length=100)
    venomous_bite_ability = models.CharField(max_length=100)


class ShadowbladeAssassin(Assassin):
    shadowstep_ability = models.CharField(max_length=100)


class VengeanceDemonHunter(DemonHunter):
    vengeance_mastery = models.CharField(max_length=100)
    retribution_ability = models.CharField(max_length=100)


class FelbladeDemonHunter(DemonHunter):
    felblade_ability = models.CharField(max_length=100)


class UserProfile(models.Model):
    username = models.CharField(max_length=70, unique=True)
    email = models.EmailField(unique=True)
    bio = models.TextField(blank=True, null=True)


class Message(models.Model):
    sender = models.ForeignKey(to=UserProfile, on_delete=models.CASCADE, related_name='sent_messages')
    receiver = models.ForeignKey(to=UserProfile, on_delete=models.CASCADE, related_name='received_messages')
    content = models.TextField()
    timestamp = models.DateField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

    def mark_as_read(self):
        self.is_read = True

    def mark_as_unread(self):
        self.is_read = False

    def reply_to_message(self, reply_content, receiver):
        self.mark_as_read()
        new_msg = Message.objects.create(sender=self.receiver, receiver=receiver, content=reply_content)
        new_msg.save()

        return new_msg

    def forward_message(self, sender, receiver):
        self.mark_as_read()
        new_msg = Message.objects.create(sender=sender, receiver=receiver, content=self.content)
        new_msg.save()

        return new_msg


class StudentIDField(models.PositiveIntegerField):
    from django.db import models

    class StudentIDField(models.PositiveIntegerField):
        def to_python(self, value):
            if value is None:
                return value
            # Convert the value to string and extract digits
            return int(''.join(filter(lambda x: isinstance(x, int), str(value))))


class Student(models.Model):
    name = models.CharField(max_length=100)
    student_id = StudentIDField()


class MaskedCreditCardField(models.CharField):
    def __init__(self, *args, **kwargs):
        kwargs['max_length'] = 20
        super().__init__(*args, **kwargs)

    def to_python(self, value):
        if not isinstance(value, str):
            raise ValidationError("The card number must be a string")

        for ch in value:
            try:
                int(ch)
            except ValueError:
                raise ValidationError("The card number must contain only digits")

        if len(value) != 16:
            raise ValidationError("The card number must be exactly 16 characters long")

        last_four_card_digits = value[-4:]

        return f"****-****-****-{last_four_card_digits}"


class CreditCard(models.Model):
    card_owner = models.CharField(max_length=100)
    card_number = MaskedCreditCardField()


class Hotel(models.Model):
    name = models.CharField(max_length=100)
    address = models.CharField(max_length=200)


class Room(models.Model):
    hotel = models.ForeignKey(to=Hotel, on_delete=models.CASCADE)
    number = models.CharField(max_length=100, unique=True)
    capacity = models.PositiveIntegerField()
    total_guests = models.PositiveIntegerField()
    price_per_night = models.DecimalField(max_digits=10, decimal_places=2)

    def save(self, *args, **kwargs):
        if self.total_guests > self.capacity:
            raise ValidationError("Total guests are more than the capacity of the room")

        super().save(*args, **kwargs)

        return f"Room {self.number} created successfully"


class BaseReservation(models.Model):
    class Meta:
        abstract = True

    room = models.ForeignKey(to=Room, on_delete=models.CASCADE)
    start_date = models.DateField()
    end_date = models.DateField()

    def reservation_period(self):
        return (self.end_date - self.start_date).days

    def calculate_total_cost(self):
        return self.reservation_period() * self.room.price_per_night

    def clean(self):
        if self.start_date >= self.end_date:
            raise ValidationError("Start date cannot be after or in the same end date")

        if self._is_reserved():
            raise ValidationError(f"Room {self.room.number} cannot be reserved")

    def _is_reserved(self, days=None):
        if days:
            end_date = self.end_date + timedelta(days=days)
        else:
            end_date = self.end_date
        # get all existing reservations for that room that are in conflict
        room_reservations = self.__class__.objects.filter(
            room=self.room,
            start_date__lte=end_date,
            end_date__gte=self.start_date
        )
        # if not any conflicts, then return True
        return room_reservations.exists()


class RegularReservation(BaseReservation):

    def save(self, *args, **kwargs):
        super().clean()

        super().save(*args, **kwargs)

        return f"Regular reservation for room {self.room.number}"


class SpecialReservation(BaseReservation):

    def save(self, *args, **kwargs):
        super().clean()

        super().save(*args, **kwargs)
        return f"Special reservation for room {self.room.number}"

    def extend_reservation(self, days: int):

        if self._is_reserved(days):
            raise ValidationError("Error during extending reservation")

        self.end_date += timedelta(days=days)
        self.save()

        return f"Extended reservation for room {self.room.number} with {days} days"
