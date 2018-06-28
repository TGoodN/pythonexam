from django.shortcuts import render,redirect,HttpResponse
from . models import *
from django.contrib import messages
import bcrypt
# Create your views here.

def index(request):
    return render(request,'jobs/index.html')

def home(request):
    if 'ID' in request.session:
        user=Users.objects.get(id=request.session['ID'])
        context={
            'user':user,
            'jobs':Jobs.objects.all(),
            'my_jobs':user.added_job.all()
        }
        return render(request,'jobs/home.html',context)
    else:
        return redirect('/')

def register(request):
    if request.method=='POST':
        errors=Users.objects.registration_validator(request.POST)
        if len(Users.objects.filter(email_address=request.POST['valEmail']))>0:
            errors['dupEmail']="duplicate email detected."
        if len(errors):
            for key,value in errors.items():
                messages.error(request,value)
                print(key)
            return redirect('/')
        else:
            password=request.POST['txtPWord']
            pwHash=bcrypt.hashpw(password.encode(),bcrypt.gensalt())
            print(pwHash)
            Users.objects.create(first_name=request.POST['firstName'],last_name=request.POST['lastName'],email_address=request.POST['valEmail'],password=pwHash)
            user=Users.objects.get(email_address=request.POST['valEmail'])
            request.session['ID']=user.id
    return redirect('/home')

def login(request):
    validator=Users.objects.login_validator(request.POST)
    if 'ID' not in validator:
        for key,value in validator.items():
            messages.error(request,value)
            print(key)
        return redirect('/')
    else:    
        request.session['ID']=validator['ID']
        return redirect('/home')

def logout(request):
    request.session.clear()
    return redirect('/')

def newJob(request):
    if 'ID' in request.session:
        context={
            'user':Users.objects.get(id=request.session['ID'])
        }
        return render(request,'jobs/add.html',context)
    else:
        return redirect('/')

def saveNewJob(request):
    errors=Jobs.objects.job_validator(request.POST)
    if len(errors)>0:
        for key,value in errors.items():
            messages.error(request,value)
            print(key)
        return redirect('/add')
    else:
        user=Users.objects.get(id=request.session['ID'])
        Jobs.objects.create(title=request.POST['vTitle'],description=request.POST['vDesc'],location=request.POST['vLoc'],job_by=user)
        return redirect('/home')

def edit(request,id):
    if 'ID' in request.session:
        context={
            'user':Users.objects.get(id=request.session['ID']),
            'job':Jobs.objects.get(id=id)
        }
        return render(request,'jobs/edit.html',context)
    else:
        return redirect('/')

def saveJob(request,id):
    errors=Jobs.objects.job_validator(request.POST)
    if len(errors)>0:
        for key,value in errors.items():
            messages.error(request,value)
            print(key)
        return redirect('/add')
    else:
        job=Jobs.objects.get(id=id)
        job.title=request.POST['vTitle']
        job.description=request.POST['vDesc']
        job.location=request.POST['vLoc']
        job.save()
        return redirect('/home')

def view(request,id):
    if 'ID' in request.session:
        context={
            'user':Users.objects.get(id=request.session['ID']),
            'job':Jobs.objects.get(id=id)
        }
        return render(request,'jobs/viewJob.html',context)
    else:
        return redirect('/')

def cancel(request,id):
    if 'ID' in request.session:
        job=Jobs.objects.get(id=id)
        job.delete()
        return redirect('/home')
    else:
        return ('/')

def add(request,id):
    if 'ID' in request.session:
        job=Jobs.objects.get(id=id)
        user=Users.objects.get(id=request.session['ID'])
        user.added_job.add(job)
        return redirect('/home')
    else:
        return ('/')

def doneJob(request,id):
    if 'ID' in request.session:
        job=Jobs.objects.get(id=id)
        user=Users.objects.get(id=request.session['ID'])
        user.added_job.remove(job)
        return redirect('/home')
    else:
        return ('/')