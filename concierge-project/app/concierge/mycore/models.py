from django.core.exceptions import ValidationError
from django.db.models import Model, CharField, IntegerField, DateTimeField, OneToOneField, ForeignKey, CASCADE, \
    SET_NULL, DO_NOTHING, PROTECT, DateField, ImageField, Index, TextField, BigIntegerField

MAX_NAME_LENGTH = 80


class Tenant(Model):
    """
    Room's owner/tenant
    """
    first_name = CharField('First name', max_length=250)
    last_name = CharField('Last name', max_length=250)
    date_of_birth = DateField(blank=True, null=True, db_index=True)
    phone = CharField('Phone num', max_length=20, blank=True, null=True)
    photo = ImageField('Photo',
                       upload_to='tenant',
                       help_text='Photo of the tenant',
                       null=True,
                       blank=True,)
                       # width_field="width_field",
                       # height_field="height_field")
    # height_field = IntegerField(default=3456)
    # width_field = IntegerField(default=5184)
    notes = TextField(blank=True, null=True)

    @property
    def fullname(self):
        return f'{self.first_name} {self.last_name}'

    def __str__(self):
        return self.fullname

    class Meta:
        ordering = ['first_name', 'last_name']
        indexes = [
            Index(fields=['first_name', 'last_name']),
        ]


class Person(Model):
    name = CharField(max_length=MAX_NAME_LENGTH)

    # def __init__(self, name):
    #     name = self.name

    def __str__(self):
        return self.name


class Room(Model):
    number = IntegerField()
    max_tenants = IntegerField(null=True)
    owner = OneToOneField(Person, on_delete=SET_NULL, null=True, blank=True)

    def __str__(self):
        return f'{self.number}'


class Key(Model):
    room = OneToOneField(Room, on_delete=PROTECT, primary_key=False)

    def __str__(self):
        return f'{self.room.number}'


class KeyTransfer(Model):
    key_out_data = DateTimeField(null=True, blank=True)
    key_in_data = DateTimeField(null=True, blank=True)
    room_id = ForeignKey(Room, on_delete=DO_NOTHING, null=True)
    guests = IntegerField(blank=True, null=True)
    notes = CharField(max_length=256, blank=True)
    person_id = ForeignKey(Person, null=True, blank=True, on_delete=DO_NOTHING)

    def __str__(self):
        return f'{self.key_out_data}, {self.key_in_data}, {self.guests}, {self.notes}'

    def save(self, *args, **kwargs):
        room = self.room_id
        key_in = KeyTransfer.objects.filter(room_id=room.id).values("key_in_data").order_by('-id').first()
        key_out = KeyTransfer.objects.filter(room_id=room.id).values("key_out_data").order_by('-id').first()
        if self.guests and self.guests > room.max_tenants:
            raise ValidationError(f'Maximum available {room.max_tenants} guests')
        elif key_in or key_out:
            if self.key_out_data and self.key_in_data is None and key_in.get('key_in_data') is None:
                raise ValidationError(f'You can not turn in key because you did not take key')
            elif self.key_in_data and self.key_out_data is None and key_out.get('key_out_data') is None:
                raise ValidationError(f'You can not take key because you did not give them back.')
            elif self.key_out_data and key_in.get('key_in_data') and key_out.get('key_out_data'):
                raise ValidationError(f'You can not give back key, because you do not have key')
        super().save(*args, **kwargs)
