from django.shortcuts import render, redirect
from administration_app.models import Admin
from carchive_app.models import *
from django.contrib import messages
import bcrypt

# Create your views here.
def is_logged_in(request):
    if 'id' in request.session:
        return True
    else:
        return False

def admins_login(request):
    if is_logged_in(request):
        return redirect('/admin/dashboard/')
    return render(request,'admins_login.html')

def login(request):
    if request.method == 'POST':
        email=request.POST['email']
        password=request.POST['password']
        print(email)
        try:
            admin=Admin.objects.get(email=email)
        except:
            messages.error(request,'Account Does Not Exist')
            print("user does not exist")
            return redirect('/admin/')
        else:
            if bcrypt.checkpw(str(password).encode(), str(admin.password).encode()):
                request.session['id'] = admin.id
                return redirect('/admin/dashboard/')
            else:
                return redirect('/admin/dashboard/')
    
    
def logout(request):
    if 'id' in request.session:
        del request.session['id']
    return redirect('/admin/')



def admin_dashboard(request):
    if not is_logged_in(request):
        return redirect('/admin/')
    context={
        'showrooms':Showroom.objects.all()
    }
    return render(request,'admin_dashboard.html',context)


def add_showroom(request):
    if not is_logged_in(request):
        return redirect('/admin/')
    return render(request,'add_showroom.html')

def create_showroom(request):
    if not is_logged_in(request):
        return redirect('/admin/')
    if request.method == 'POST':
        admin=Admin.objects.get(id=request.session['id'])
        name=request.POST['name']
        email=request.POST['email']
        password=str(request.POST['password'])
        license_number=request.POST['license_number']
        payment=request.POST['payment']
        pw_hash=bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()
        # pw_hash=bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()
        Showroom.objects.create(name=name,email=email,password=pw_hash
                                ,license_number=license_number,payment=payment,created_by=admin)
        return redirect('/admin/dashboard/')
    return redirect('/admin/')


def edit_showroom(request,id):
    if not is_logged_in(request):
        return redirect('/admin/')
    context={
        "this_showroom":Showroom.objects.get(id=id),
    }
    return render(request,'edit_showroom.html', context)


def update_showroom(request, id):
    if not is_logged_in(request):
        return redirect('/admin/')
    this_showroom= Showroom.objects.get(id=id)
    this_showroom.license_number=request.POST['license_number']
    this_showroom.name=request.POST['name']
    this_showroom.email=request.POST['email']
    if len(request.POST['password'])>5:
        password=request.POST['password']
        pw_hash = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()
        this_showroom.password=pw_hash
    
    this_showroom.save()
    return redirect('/admin/edit_showroom/' + str(this_showroom.id)+'/')



def add_items(request):
    if not is_logged_in(request):
        return redirect('/admin/')
    context={
        'brands':Brand.objects.all()
    }
    return render(request,'add_items.html',context)

def process_items(request):
    if not is_logged_in(request):
        return redirect('/admin/')
    if request.method == 'POST':
        if request.POST['source']=='brand':
            brand_name=request.POST['brand']
            Brand.objects.create(name=brand_name)
        elif request.POST['source']=='model':
            brand=Brand.objects.get(id=request.POST['brand'])
            new_model=request.POST['model']
            BrandModel.objects.create(brand=brand,name=new_model)
        elif request.POST['source']=='doc_type':
            doc_type=request.POST['doc_type']
            DocumentType.objects.create(type=doc_type)
        return redirect('/admin/add_items/')

    else:
        return redirect('/admin/')


def display_showroom(request, id):
    if not is_logged_in(request):
        return redirect('/admin/')
    context={
        "this_showroom":Showroom.objects.get(id=id),
    }
    return render(request,"display_showroom.html", context)

def delete_showroom(request, id):
    if not is_logged_in(request):
        return redirect('/admin/')
    this_showroom = Showroom.objects.get(id=id)
    this_showroom.delete()
    return redirect('/admin/dashboard/')
