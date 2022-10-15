import os
from datetime import datetime
import bcrypt
from django.contrib import messages
from django.core.files.storage import FileSystemStorage
from django.http import JsonResponse
from django.shortcuts import HttpResponse, redirect, render
from django.core import serializers
from carchive_app.models import *


# Create your views here.
#renders the login page
def showroom_login(request):
    if 'showroom_id' in request.session:
        return redirect('/dashboard/')
    return render(request,'showroom_login.html')

#processes the logout and deletes session key
def showroom_logout(request):
    if 'showroom_id' in request.session:
        del request.session['showroom_id']
    return redirect('/')

#checks if the user is logged in
def showroom_logged_in(request):
    if not 'showroom_id' in request.session:
        return False
    else:
        return True

#processes the login post request and identifies the user
def logging(request):
    if request.method == 'POST':
        email=request.POST['email']
        password=request.POST['password']
        try:
            showroom=Showroom.objects.get(email=email)
        except:
            messages.error(request,'Account Does Not Exist')
            print("user does not exist")
            return redirect('/')
        else:
            if bcrypt.checkpw(str(password).encode(), str(showroom.password).encode()):
                request.session['showroom_id'] = showroom.id
                return redirect('/dashboard/')
            else:
                return redirect('/')
    else:
        return ('/')


#renders the user's change password template
def change_password(request):
    if not showroom_logged_in(request):
        return redirect('/')
    context={
        'showroom':Showroom.objects.get(id=request.session['showroom_id']),
    }
    return render(request,'change_password.html',context)


#processes the input coming from change password template
def update_password(request):
    if not showroom_logged_in(request):
        return redirect('/')
    if request.method == 'POST':
        logged_showroom=Showroom.objects.get(id=request.session['showroom_id'])
        old_password=str(request.POST['old_password'])
        new_password=str(request.POST['new_password'])
        conf_new_password=request.POST['conf_new_password']
        if bcrypt.checkpw(old_password.encode(),str(logged_showroom.password).encode()):
            if new_password == conf_new_password:
                logged_showroom.password=bcrypt.hashpw(new_password.encode(),bcrypt.gensalt()).decode()
                logged_showroom.save()
                print('password updated')
                return redirect ('/dashboard/')
            else:
                print('password confirmation does not match')
                messages.error(request,'password confirmation does not match')
                return redirect('/change_password/')
    else:
        print('Wrong old password')
        messages.error(request,'Wrong old password')
        return redirect('/change_password/')


#renders the homepage(dashboard) of the user
def cars_dashboard(request):
    if not showroom_logged_in(request):
        return redirect('/')
    context={
        "cars":Showroom.objects.get(id=request.session['showroom_id']).cars.all(),
        'showroom':Showroom.objects.get(id=request.session['showroom_id']),
    }
    return render(request,'cars_dashboard.html',context)


#uses AJAX to search for 
def find_by_vin(request):
    if request.method == 'GET':
        key=request.GET['key']
        print(key)
        showroom_cars=Showroom.objects.get(id=request.session['showroom_id']).cars.all().filter(vin__startswith=key)
        print(showroom_cars)
        results=[]
        for car in showroom_cars:
            temp={
                'id':car.id,
                'vin':car.vin,
                'model':car.model.brand.name+' '+car.model.name,
            }
            results.append(temp)
        print(results)
        # results=Showroom.objects.get(id=request.session['showroom_id']).cars.all().filter(vin__startswith=key)
        # data=[]
        # for car in results:
        #     item={
        #         'id':car.id,
        #         'vin':car.vin,
        #         'model':car.model.brand.name+' '+car.model.name,
        #     }
        #     data.append(item)
        #     res=data
        return JsonResponse({'results':results})


#renders adding a new car template
def add_new_car(request):
    if not showroom_logged_in(request):
        return redirect('/')
    context={
        'brands':Brand.objects.all(),
        'showroom':Showroom.objects.get(id=request.session['showroom_id']),
    }
    return render(request,'add_new_car.html',context)

#creates a new car object
def create_car(request):
    if not showroom_logged_in(request):
        return redirect('/')
    if request.method == 'POST':
        model=BrandModel.objects.get(id=request.POST['model'])
        showroom=Showroom.objects.get(id=request.session['showroom_id'])
        prod_date=request.POST['prod_date']
        color=request.POST['color']
        vin=request.POST['vin']
        Car.objects.create(model=model,showroom=showroom,prod_date=prod_date,color=color,vin=vin)
        return redirect('/dashboard/')
    return redirect('/dashboard/')

#gets models of brands using AJAX request response
def get_models(request):
    if request.method == 'GET':
        selected_brand=Brand.objects.get(id=request.GET['id'])
        selected_brand_models=selected_brand.models.all()
        models_list=[]
        for model in selected_brand_models:
            models_list.append([model.id,model.name])
        print(models_list)
        return JsonResponse({"data": models_list}, status=200)

#renders edit car
def edit_car(request,id):
    if not showroom_logged_in(request):
        return redirect('/')
    car=Car.objects.get(id=id)
    car_prod_date=datetime.strftime(car.prod_date,'%Y-%m-%d')
    if not car in Showroom.objects.get(id=request.session['showroom_id']).cars.all():
        return redirect('/')
    context={
        'car':car,
        'brands':Brand.objects.all(),
        'models':BrandModel.objects.all(),
        'car_prod_date':car_prod_date,
        'showroom':Showroom.objects.get(id=request.session['showroom_id']),
    }

    return render(request,'edit_car.html',context)

#updates the car table with the posted data
def update_car(request,id):
    if not showroom_logged_in(request):
        return redirect('/')
    if request.method == 'POST':
        try:
            car=Car.objects.get(id=id)
        except:
            return redirect('/')
        else:
            model=BrandModel.objects.get(id=request.POST['model'])
            prod_date=request.POST['prod_date']
            color=request.POST['color']
            vin=request.POST['vin']
            car.model=model
            car.prod_date=prod_date
            car.color=color
            car.vin=vin
            car.save()
            return redirect('/show_car/'+str(car.id)+'/')
    return ('/')

#deletes a car object
def delete_car(request,id):
    tb_deleted_car=Car.objects.get(id=id)
    tb_deleted_car.delete()
    return redirect('/dashboard/')
    

#renders the showcar template with the documents list
def show_car(request,id):
    if not showroom_logged_in(request):
        return redirect('/')
    car=Car.objects.get(id=id)
    if not car in Showroom.objects.get(id=request.session['showroom_id']).cars.all():
        return redirect('/')
    context={
        'car':car,
        'doc_types':DocumentType.objects.all(),
        'showroom':Showroom.objects.get(id=request.session['showroom_id']),
    }
    return render(request,'show_car.html',context)

#uploading car's documents process
def upload_doc(request,id):
    if request.method == 'POST':
        uploaded_file=request.FILES['document']
        doc_type_id = request.POST['doc_type']
        doc_type=DocumentType.objects.get(id = doc_type_id)
        car=Car.objects.get(id=id)
        # print(uploaded_file.name)
        # print(uploaded_file.size)
        # fs=FileSystemStorage()
        # fs.save(uploaded_file.name,uploaded_file)
        Document.objects.create(car=car,type=doc_type,doc=uploaded_file)



    return redirect('/show_car/'+str(id)+'/')

#deletes document from db and filesystem
def delete_document(request,id):
    tb_deleted_doc=Document.objects.get(id=id)
    car_id=tb_deleted_doc.car.id
    tb_deleted_doc.delete()
    print('deleted file'+'/media/'+str(tb_deleted_doc.doc))
    return redirect('/show_car/'+str(car_id)+'/')


# """ Deletes file from filesystem. """
def _delete_file(path):
    if os.path.isfile(path):
        print('inside the function deleted file '+path)
        os.remove(path)
    else:
        print ('file '+path+' not fount ')
