from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.db import IntegrityError
from django.shortcuts import render, redirect
from rest_framework import status
from rest_framework.generics import ListCreateAPIView, ListAPIView, CreateAPIView
from rest_framework.response import Response

from master.filters import SkillsFilter, DetailSkillFilter
from master.models import Master, Service
from master.serializers import MasterSkillsSerializer, DetailSkillSerializer, \
    AddServiceSerializer


# Registration and authentication code zone
def signup_user(request):
    if request.method == "GET":
        return render(request, 'master/signupuser.html', {'form': UserCreationForm()})
    else:
        if request.POST['password1'] == request.POST['password2']:
            try:
                user = User.objects.create_user(username=request.POST['username'], password=request.POST['password1'], email=request.POST['email'])
                user.save()
                login(request, user) # there should be redirect to master's cabinet
                return redirect('loginuser')
            except IntegrityError:
                return render(request, 'master/signupuser.html', {'form': UserCreationForm(), 'error': 'That username has already been taken'})
        else:
            return render(request, 'master/signupuser.html', {'form': UserCreationForm(), 'error': 'Passwords did not match'})


def login_user(request):
    if request.method == "GET":
        return render(request, 'master/loginuser.html', {'form': AuthenticationForm()})
    else:
        user = authenticate(request, username=request.POST['username'], password=request.POST['password'])
        if not user:
            return render(request, 'master/loginuser.html', {'form': AuthenticationForm(), 'error': 'Username and password did not match'})
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
    model = Service
    queryset = Service.objects.all()
    serializer_class = MasterSkillsSerializer
    filterset_class = SkillsFilter


# Show detail skill information
class DetailSkillView(ListAPIView):
    model = Service
    queryset = Service.objects.all()
    serializer_class = DetailSkillSerializer
    filterset_class = DetailSkillFilter


# Add new service
class AddServiceView(CreateAPIView):
    model = Service
    serializer_class = AddServiceSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def perform_create(self, serializer):
        user = self.request.user.id
        master = Master.objects.get(user=user)
        serializer.save(master=master)


master_skills_list_view = MasterSkillsListView.as_view()
detail_skill_list_view = DetailSkillView.as_view()
add_service_view = AddServiceView.as_view()