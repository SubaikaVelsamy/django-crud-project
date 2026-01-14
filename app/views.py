from django.shortcuts import render, redirect
from django.core.paginator import Paginator
from django.db.models import Q
from .models import Student
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
import re

@login_required(login_url='login')
def student_list(request):
    query = request.GET.get('q')

    if query:
        student = Student.objects.filter(
            Q(full_name__icontains=query) |
            Q(mobile__icontains=query) |
            Q(email__icontains=query)
        )
    else:
        student = Student.objects.all()
    paginator = Paginator(student,5)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    return render(request,"student_list.html",{"page_obj": page_obj,
        "query": query})

@login_required(login_url='login')
def student_create(request):
    if request.method == "POST":
        full_name = request.POST['full_name']
        mobile = request.POST['mobile']
        email = request.POST['email']
        student = Student (full_name,mobile,email)

        # Email format validation
        email_regex = r'^[\w\.-]+@[\w\.-]+\.\w+$'
        if not re.match(email_regex, email):
            messages.error(request,"Invalid Email Format")
            return render(request, "student_form.html")

        # Mobile validation
        if not mobile.isdigit() or len(mobile) != 10:
            messages.error(request,"Mobile must be 10 digits")
            return render(request, "student_form.html")

        # Duplicate email check
        if Student.objects.filter(email=email).exists():
            messages.error(request,"Email already exists")
            return render(request, "student_form.html")

        # Duplicate mobile check
        if Student.objects.filter(mobile=mobile).exists():
            messages.error(request,"Mobile already exists")
            return render(request, "student_form.html")
        student = Student(
            full_name=full_name,
            mobile=mobile,
            email=email
        )
        student.save()
        return redirect(student_list)
    return render(request,"student_form.html")

@login_required(login_url='login')
def student_delete(request,id):
    student = Student.objects.get(id=id)
    student.delete()
    return redirect(student_list)

@login_required(login_url='login')
def student_update(request,id):
    student = Student.objects.get(id=id)
    if request.method == "POST":
        full_name = request.POST['full_name']
        mobile = request.POST['mobile']
        email = request.POST['email']

        # Email format validation
        email_regex = r'^[\w\.-]+@[\w\.-]+\.\w+$'
        if not re.match(email_regex, email):
            messages.error(request,"Invalid email format")
            return render(request, "student_form.html", {
                "student": student,
                 })

        # Mobile validation
        if not mobile.isdigit() or len(mobile) != 10:
            messages.error(request,"Mobile must be 10 digits")
            return render(request, "student_form.html", {
                "student": student
            })

        # Duplicate email check (exclude self)
        if Student.objects.filter(email=email).exclude(id=id).exists():
            messages.error(request,"Email already exists")
            return render(request, "student_form.html", {
                "student": student
            })

        # Duplicate mobile check (exclude self)
        if Student.objects.filter(mobile=mobile).exclude(id=id).exists():
            messages.error(request,"Mobile already exists")
            return render(request, "student_form.html", {
                "student": student})
        
        student.full_name = full_name
        student.mobile = mobile
        student.email = email
        student.save()
        return redirect(student_list)
    return render(request,"student_form.html", {"student": student})

# Create your views here.

@login_required(login_url='login')
def student_update_status(request,id):
    student = Student.objects.get(id=id)
    current_status = student.status
    if current_status == "Y":
        update_status = "N"
    else:
        update_status = "Y"
    student.status = update_status
    student.save()
    return redirect(student_list)

def user_login(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect("student_list")
        else:
            messages.error(request, "Invalid username or password")

    return render(request, "login.html")

def user_logout(request):
    logout(request)
    return redirect("login")

def register(request):
    if request.method == "POST":
        username = request.POST.get('email')
        email = request.POST.get('email')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')

        # 1. Password match check
        if password != confirm_password:
            messages.error(request, "Passwords do not match")
            return redirect('register')

        # 2. Username exists check
        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists")
            return redirect('register')

        # 3. Email exists check
        if User.objects.filter(email=email).exists():
            messages.error(request, "Email already exists")
            return redirect('register')

        # 4. Create user
        user = User.objects.create_user(
            username=username,
            email=email,
            password=password
        )
        user.save()

        messages.success(request, "Registration successful. Please login.")
        return redirect('login')

    return render(request, 'register.html')

