from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.db import IntegrityError
from django.shortcuts import render, redirect
from rest_framework import status
from rest_framework.generics import ListAPIView, CreateAPIView, UpdateAPIView
from rest_framework.response import Response

from master import handlers
from master.filters import SkillsFilter, DetailSkillFilter
from master.handlers import get_user_id_if_approve
from master.models import Master, Service
from master.serializers import MasterSkillsSerializer, DetailSkillSerializer, \
    AddServiceSerializer, CreateMasterSerializer, AddMasterTelegramInfoSerializer


# Registration and authentication code zone
def signup_user(request):
    if request.method == "GET":
        return render(request, 'master/signupuser.html', {'form': UserCreationForm()})
    else:
        if request.POST['password1'] == request.POST['password2']:
            try:
                user = User.objects.create_user(username=request.POST['username'], password=request.POST['password1'],
                                                email=request.POST['email'])
                user.save()
                login(request, user) # there should be redirect to master's cabinet # TODO delete this comment in future
                return redirect('loginuser')
            except IntegrityError:
                return render(request, 'master/signupuser.html', {'form': UserCreationForm(),
                                                                  'error': 'That username has already been taken'})
        else:
            return render(request, 'master/signupuser.html', {'form': UserCreationForm(),
                                                              'error': 'Passwords did not match'})


def login_user(request):
    if request.method == "GET":
        return render(request, 'master/loginuser.html', {'form': AuthenticationForm()})
    else:
        user = authenticate(request, username=request.POST['username'], password=request.POST['password'])
        if not user:
            return render(request, 'master/loginuser.html', {'form': AuthenticationForm(),
                                                             'error': 'Username and password did not match'})
        else:
            login(request, user)
            # return redirect('currenttodos') # there should be redirect to master's cabinet


def logoutuser(request):
    if request.method == "POST":
        logout(request)
        return redirect('loginuser')
# The end of registration and authentication code zone


# Show master skills
class MasterSkillsListView(ListAPIView):
    """Returns a list of masters' services.
    Implemented for debug purposes only and isn't used by any clients."""
    model = Service
    queryset = Service.objects.all()
    serializer_class = MasterSkillsSerializer
    filterset_class = SkillsFilter


# Show detail skill information
class DetailedSkillView(ListAPIView):
    """Returns a list of detailed information of masters' services."""
    model = Service
    queryset = Service.objects.all()
    serializer_class = DetailSkillSerializer
    filterset_class = DetailSkillFilter


# Add new service
class AddServiceView(CreateAPIView):
    """Creates a new service."""
    model = Service
    serializer_class = AddServiceSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def perform_create(self, serializer):
        user_id = self.request.user.id
        master = Master.objects.get(user=user_id)
        serializer.save(master=master)


class CreateMasterView(CreateAPIView):
    """Creates a Master instance and links it to a User instance implicitly."""
    model = Master
    serializer_class = CreateMasterSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        user_id = self.request.user.id
        master = Master.objects.get(user=user_id)
        handlers.generate_code(master)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def perform_create(self, serializer):
        user = self.request.user
        serializer.save(user=user)


class AddMasterTelegramInfoView(UpdateAPIView):
    """Links Master instance with Telegram account information."""
    model = Master
    serializer_class = AddMasterTelegramInfoSerializer

    def update(self, request, *args, **kwargs):
        # TODO: describe what's going on on the next line, just in case
        partial = kwargs.pop('partial', False)
        master_id = get_user_id_if_approve(request.data)
        instance = Master.objects.get(id=master_id)
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data)

    def perform_update(self, serializer):
        serializer.save()

    def partial_update(self, request, *args, **kwargs):
        kwargs['partial'] = True
        return self.update(request, *args, **kwargs)


# TODO: remove this and use ViewName.as_view() in urls.py?
# master_skills_list_view = MasterSkillsListView.as_view()
# detail_skill_list_view = DetailSkillView.as_view()
# add_service_view = AddServiceView.as_view()
# create_master_view = CreateMasterView.as_view()
# add_master_telegram_info_view = AddMasterTelegramInfoView.as_view()
