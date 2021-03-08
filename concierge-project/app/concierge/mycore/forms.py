from django import forms
from django.forms import ModelForm
from mycore.models import Person, Key, Room, Tenant, KeyTransfer


class PersonForm(forms.Form):
    person_name = forms.CharField(label='Person name', max_length=80)

    def save_form(self):
        data = self.cleaned_data
        person_object = Person(name=data.get('person_name'))
        person_object.save()


class KeyForm(forms.Form):
    key_id = forms.IntegerField(label='Key from room', max_value=100)

    def save_form(self):
        data = self.cleaned_data
        key_object = Key(room_id=data.get('key_id'))
        key_object.save()


class RoomForm(forms.Form):
    number = forms.IntegerField(label='Room number', max_value=100)
    max_tenants = forms.IntegerField(label='Maximum tenants')
    owner_id = forms.IntegerField(label='Owner id', required=False)

    def save_form(self):
        data = self.cleaned_data
        room = Room(number=data.get('number'),
                    max_tenants=data.get('max_tenants'),
                    owner_id=data.get('owner_id'))
        room.save()


class TenantForm(forms.Form):
    first_name = forms.CharField(label='First name', max_length=250)
    last_name = forms.CharField(label='Last name', max_length=250)
    date_of_birth = forms.DateField(label='Date of birth')
    phone = forms.IntegerField(label='Phone')
    photo = forms.ImageField(label=u'Photo', required=False)
    text = forms.TimeField(label='Comments', required=False)

    def save_form(self):
        data = self.cleaned_data
        tenant = Tenant(first_name=data.get('first_name'),
                        last_name=data.get('last_name'),
                        date_of_birth=data.get('date_of_birth'),
                        phone=data.get('phone'),
                        photo=data.get('photo'),
                        notes=data.get('notes'))
        tenant.save()


class KeyTransferForm(ModelForm):
    class Meta:
        model = KeyTransfer
        fields = '__all__'

    def save_form(self):
        data = self.cleaned_data
        key_transfer = KeyTransfer(**data)
        key_transfer.save()
