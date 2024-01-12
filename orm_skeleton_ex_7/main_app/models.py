from django.core.exceptions import ValidationError
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
