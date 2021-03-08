from datetime import datetime
import time
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import (
    login_required,
    permission_required,
)
from django.conf import settings
from django.core.cache import cache
from django.shortcuts import render
from django.views.generic.list import ListView

from django.views.decorators.cache import cache_page
from .models import Tenant
from http import HTTPStatus
from django.core import serializers
from django.core.serializers import SerializerDoesNotExist
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render
from django.urls import reverse_lazy, reverse
from django.views.generic import View, ListView, DetailView
from mycore.forms import PersonForm, KeyForm, RoomForm, TenantForm, KeyTransferForm
from mycore.models import Person, Key, Room, Tenant, KeyTransfer
import mycore.models


def get_users():
    ukey = 'users_all'
    users = cache.get(ukey)
    if not users:
        users = get_user_model().objects.all()
        cache.set(ukey, users, settings.CACHE_TTL)
    return users


@login_required()
def simple_view(request):
    context = dict(
        title='simple view title',
        text='Lorem ipsum for you honor',
        months='Jan Feb Mar Apr May Jun Jul Aug Sep Oct Nov Dec'.split(),
        users=get_users(),
    )
    return render(request, 'mycore/simple_view.html', context=context)


@cache_page(settings.CACHE_TTL)
@permission_required('mycore.view_tenant')
def tenant_view(request):
    context = dict(
        title='Tenant list',
        object_list=Tenant.objects.all()
    )
    return render(request, 'mycore/tenant_list.html', context=context)


class TenantListView(ListView):
    model = Tenant
    # paginate_by = 100

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['current_date'] = datetime.utcnow()
        time.sleep(1)
        return context

def index(request):
    return render(request, 'index.html', {'title': "concierge",
                                          "room": "Room",
                                          "rooms": "List of rooms",
                                          "key": "Key",
                                          "keys": "List of keys",
                                          "tenant": "Tenant",
                                          "tenants": "List of tenants",
                                          "person": "Person",
                                          "people": "List of people",
                                          "key_transfer": "Key_transfer",
                                          "key_transfers": "Key_transfers",
                                          })


class PersonView(View):
    form_class = PersonForm
    model = Person
    template_name = 'person.html'

    def get(self, request):
        form = self.form_class
        all_people = Person.objects.all()
        data = {"all_people": all_people, 'form': form}
        return render(request, self.template_name, data)

    def post(self, request):
        form = self.form_class(request.POST)
        context = {'form': form}
        if form.is_valid():
            form.save_form()
            return HttpResponseRedirect(reverse('person'), context)
        else:
            return render(request, self.template_name, {'form': form})


class PersonList(ListView):
    model = Person
    template_name = 'people.html'

    def get_context_data(self, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_expired'] = True
        return context


class KeyView(View):
    form_class = KeyForm
    model = Key
    template_name = 'key.html'

    def get(self, request):
        form = self.form_class
        keys = Key.objects.all()
        data = {"keys": keys, 'form': form}
        return render(request, self.template_name, data)

    def post(self, request):
        form = self.form_class(request.POST)
        context = {'form': form}
        if form.is_valid():
            form.save_form()
            return HttpResponseRedirect(reverse('key'), context)
        else:
            return render(request, self.template_name, {'form': form})


class KeyList(ListView):
    model = Key
    template_name = 'keys.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_expired'] = True
        return context


class RoomView(View):
    form_class = RoomForm
    model = Room
    template_name = 'room.html'

    def get(self, request):
        form = self.form_class
        rooms = Room.objects.all()
        owner = Person.objects.all()
        data = {"rooms": rooms, 'form': form, 'owner': owner}
        return render(request, self.template_name, data)

    def post(self, request):
        form = self.form_class(request.POST)
        file = self.form_class(request.FILES)
        context = {'form': form}
        if form.is_valid():
            form.save_form()
            return HttpResponseRedirect(reverse('room'), context)
        else:
            return render(request, self.template_name, {'form': form})


class RoomList(ListView):
    model = Room
    template_name = 'rooms.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_expired'] = True
        return context


class TenantView(View):
    form_class = TenantForm
    model = Tenant
    template_name = 'tenant.html'

    def get(self, request):
        form = self.form_class
        tenants = Tenant.objects.all()
        data = {"tenants": tenants, "form": form}
        return render(request, self.template_name, data)

    def post(self, request):
        form = self.form_class(request.POST or None, request.FILES or None)
        context = {'form': form}
        if form.is_valid():
            form.save_form()
            return HttpResponseRedirect(reverse('tenant'), context)
        return render(request, self.template_name, {'form': form})


class TenantList(ListView):
    model = Tenant
    template_name = 'tenants.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_expired'] = True
        return context


class TenantDetail(DetailView):
    model = Tenant
    template_name = 'tenant-detail.html'
    context_object_name = 'tenant'


class KeyTransferView(View):
    form_class = KeyTransferForm
    model = KeyTransfer
    template_name = 'key_transfer.html'

    def get(self, request):
        form = self.form_class
        key_transfer = KeyTransfer.objects.all()
        data = {"key_transfer": key_transfer, "form": form}
        return render(request, self.template_name, data)

    def post(self, request):
        form = self.form_class(request.POST)
        context = {'form': form}
        if form.is_valid():
            form.save_form()
            return HttpResponseRedirect(reverse('keytransfer'), context)
        return render(request, self.template_name, {'form': form})


class KetTransferList(ListView):
    model = KeyTransfer
    template_name = 'key_transfers.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_expired'] = True
        return context


def api_serializer(request, object_type, object_id):
    try:
        if object_type == 'keytransfer':
            model = getattr(mycore.models, "KeyTransfer")
        else:
            model = getattr(mycore.models, object_type.capitalize())
        return HttpResponse(
            serializers.serialize(
                request.GET['format'],
                [model.objects.get(id=object_id)]
            )
        )
    except (AttributeError,
            SerializerDoesNotExist,
            mycore.models.Key.DoesNotExist,
            mycore.models.Room.DoesNotExist,
            mycore.models.Person.DoesNotExist,
            mycore.models.Tenant.DoesNotExist,
            mycore.models.KeyTransfer.DoesNotExist):
        return HttpResponse(status=HTTPStatus.NOT_FOUND)
