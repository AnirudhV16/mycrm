from django.shortcuts import render,redirect
from django.contrib.auth import login,logout,authenticate
from django.contrib import messages
from .forms import SignUpForm,AddCustomer
from .models import customer
# Create your views here.
def home(request):
    customers=customer.objects.all()
    if request.method=='POST':
        print(request.POST)
        username=request.POST.get('username')
        password=request.POST.get('password')
        user=authenticate(request,username=username,password=password)
        if user is not None:
            login(request,user)
            messages.success(request,'you have loggged in successfully.')
            return redirect('home')
        else:
            messages.success(request,'invalid login details....')
            return redirect('home')
    else:       
        return render(request,'home.html',{'records':customers})
def logout_user(request):
    logout(request)
    messages.success(request,'you have successfully logged out....')
    return render(request,'home.html',{})
def register_user(request):
    if request.method=="POST":
        form=SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username=form.cleaned_data['username']
            password=form.cleaned_data['password1']
            print(username)
            print(password)
            user=authenticate(request,username=username,password=password)
            if user is not None:
                login(request,user)
                messages.success(request,'you have successfully registered....')
                return redirect(home)
            else:
                messages.success(request,'something wrong with the authentication of your details....')
                return redirect(register_user)
    else:
        print('dfghj')
        form=SignUpForm()
        return render(request,'register.html',{'form':form})
    return render(request,'register.html',{'form':form})

def add_customer(request):
    form = AddCustomer(request.POST or None)
    if request.user.is_authenticated:
        if request.method=="POST":
            if form.is_valid():
                add_record=form.save()
                messages.success(request,'customer successfully added....')
                return redirect(home)
        return render(request,'add_customer.html',{'form':form})
    else:
        messages.success(request,"you must be logged in....")
        return redirect(home)
def show_customer(request,id):
    if request.user.is_authenticated:
        data=customer.objects.get(id=id)
        return render(request,'show_record.html',{'record':data})
    else:
        messages.success(request,"you must be logged in....")
        return redirect(home)
def update_customer(request,id):
    if request.user.is_authenticated:
        data=customer.objects.get(id=id)
        if request.method=="POST":
            form=AddCustomer(request.POST , instance=data)
            if form.is_valid():
                form.save()
                messages.success(request,"customer Successfully updated....")
                return redirect(home)
        else:
            form=AddCustomer(instance=data)
            return render(request,'update_customer.html',{'form':form})
    else:
        messages.success(request,"you must be logged in....")
        return redirect(home)
def delete_customer(request,id):
    if request.user.is_authenticated:
        data=customer.objects.get(id=id)
        data.delete()
        messages.success(request,"Record Successfully Deleted....")
        return redirect(home)
    else:
        messages.success(request,"you must be logged in....")
        return redirect(home)