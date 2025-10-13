from django.shortcuts import render, redirect
from .models import StudentProfile, SchoolPost, StudentChat, School
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_exempt
from rest_framework import viewsets
from .serializers import SchoolSerializer, StudentProfileSerializer, SchoolPostSerializer, StudentChatSerializer

class SchoolViewSet(viewsets.ModelViewSet):
    queryset = School.objects.all()
    serializer_class = SchoolSerializer

class StudentProfileViewSet(viewsets.ModelViewSet):
    queryset = StudentProfile.objects.all()
    serializer_class = StudentProfileSerializer

class SchoolPostViewSet(viewsets.ModelViewSet):
    queryset = SchoolPost.objects.all()
    serializer_class = SchoolPostSerializer

class StudentChatViewSet(viewsets.ModelViewSet):
    queryset = StudentChat.objects.all()
    serializer_class = StudentChatSerializer

def landing_page(request):
    return render(request, 'Appowcus/landing_page.html')

@login_required
@csrf_exempt
def student_dashboard(request):
    student = StudentProfile.objects.get(user=request.user)
    posts = SchoolPost.objects.filter(school=student.school).order_by('-created_at')
    classmates = StudentProfile.objects.filter(school=student.school)
    chats = StudentChat.objects.filter(sender=student) | StudentChat.objects.filter(receiver=student)
    chats = chats.order_by('sent_at')[:30]

    if request.method == 'POST':
        if 'content' in request.POST:
            SchoolPost.objects.create(
                school=student.school,
                author=student,
                post_type=request.POST.get('post_type', 'text'),
                media_url=request.POST.get('media_url', ''),
                content=request.POST.get('content', '')
            )
            return redirect('student_dashboard')
        if 'message' in request.POST and 'receiver' in request.POST:
            receiver = StudentProfile.objects.get(id=request.POST['receiver'])
            StudentChat.objects.create(
                sender=student,
                receiver=receiver,
                message=request.POST['message']
            )
            return redirect('student_dashboard')
        if 'like' in request.POST:
            post = SchoolPost.objects.get(id=request.POST['like'])
            post.likes.add(student)
            return redirect('student_dashboard')
        if 'share' in request.POST:
            post = SchoolPost.objects.get(id=request.POST['share'])
            post.shares.add(student)
            return redirect('student_dashboard')

    return render(request, 'kidsedu/student_dashboard.html', {
        'student': student,
        'posts': posts,
        'classmates': classmates,
        'chats': chats,
    })

def login_view(request):
    error = ""
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return redirect('student_dashboard')
        else:
            error = "Invalid username or password."
    return render(request, 'Appowcus/login.html', {'error': error})

def signup_view(request):
    error = ""
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        roll_no = request.POST['roll_no']
        school_id = request.POST['school']
        bio = request.POST.get('bio', '')
        if User.objects.filter(username=username).exists():
            error = "Username already taken."
        else:
            user = User.objects.create_user(username=username, password=password)
            school = School.objects.get(id=school_id)
            StudentProfile.objects.create(user=user, roll_no=roll_no, school=school, bio=bio)
            login(request, user)
            return redirect('student_dashboard')
    schools = School.objects.all()
    return render(request, 'Appowcus/signup.html', {'error': error, 'schools': schools})

def logout_view(request):
    logout(request)
    return redirect('landing_page')