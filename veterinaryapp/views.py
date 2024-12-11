from datetime import date

from django.contrib import messages


from django.contrib.auth import authenticate, login

from django.shortcuts import render, redirect

from veterinaryapp import models
from veterinaryapp.forms import LoginRegister, DoctorForm, PatientsForm, DoctorScheduleForm, \
    BillForm
from veterinaryapp.models import Patients, Doctor, DoctorSchedule, Bill, Prescript, Joinnsreqst


# Create your views here.
def home(request):
    return render(request,"home.html")

def index(request):
    return render(request,"index.html")
def Admin_temp(request):
    return render(request,"admintemp/base.html")


def doctor(request):
    data=Doctor.objects.get(user_1_id=request.user)
    return render(request,"doctor/base.html",{"data":data})

def patients(request):
    data=Patients.objects.get(user_2_id=request.user)
    return render(request,"patients/base.html",{"data":data})
def doctor_login(request):
    Login_form=LoginRegister()
    Doctor_form=DoctorForm()
    if request.method == 'POST':
        Login_form=LoginRegister(request.POST)
        Doctor_form=DoctorForm(request.POST,request.FILES)

        if Login_form.is_valid() and Doctor_form.is_valid():
            user2=Login_form.save(commit=False)
            user2.is_doctor=True
            user2.save()
            user1=Doctor_form.save(commit=False)
            user1.user_1=user2
            user1.save()
            return redirect("logview")
    return render(request,'doctor.html',{"Login_form":Login_form,"Doctor_form":Doctor_form})


def patient_login(request):
    Login_form=LoginRegister()
    patient_form=PatientsForm()
    if request.method == 'POST':
        Login_form=LoginRegister(request.POST)
        patient_form=PatientsForm(request.POST)

        if Login_form.is_valid() and patient_form.is_valid():
            user2=Login_form.save(commit=False)
            user2.is_patients=True
            user2.save()
            user1=patient_form.save(commit=False)
            user1.user_2=user2
            user1.save()
            return  redirect("logview")
    return render(request,'patients.html',{"Login_form":Login_form,"patient_form":patient_form})


def login_view(request):
    if request.method == 'POST':
        username=request.POST.get('uname')
        password=request.POST.get('pass')
        user=authenticate(request,username=username,password=password)
        if user is not None:
            login(request,user)
            if user.is_staff:
                return redirect("admintemp")
            if user.is_doctor:
                return redirect("doct")
            if user.is_patients:
                return redirect("patients")
            else:
                messages.info(request,'Invalid credentials')

    return render(request,'login.html')



def patients_view(request):
    data=Patients.objects.all()
    return render(request,"admintemp/patientsview.html",{"data":data})

def patients_update(request,id):
    data=Patients.objects.get(id=id)
    form=PatientsForm(instance=data)
    if request.method == 'POST':
        form=PatientsForm(request.POST,instance=data)
        if form.is_valid():
            form.save()
            return redirect("admpatientsview")
    return render(request,"admintemp/patientsupdate.html",{"form":form})



def patients_delt(request,id):
    data=Patients.objects.get(id=id)
    data.delete()
    return redirect("admpatientsview")
def doct_view(request):
    data=Doctor.objects.all()
    return render(request,"admintemp/doctview.html",{"data":data})

def doct_update(request,id):
    data=Doctor.objects.get(id=id)
    form=DoctorForm(instance=data)
    if request.method=='POST':
        form=DoctorForm(request.POST,request.FILES,instance=data)
        if form.is_valid():
            form.save()
            return redirect("admdoctview")
    return render(request,"admintemp/doctupdate.html",{"form":form})


def doct_delt(request,id):
    data=Doctor.objects.get(id=id)
    data.delete()
    return redirect("admdoctview")

def patient_doct_view(request):
    data=Doctor.objects.all()
    return render(request,"patients/doctview.html",{"data":data})


def add_doct_schedule(request):
    schedule=DoctorScheduleForm()

    if request.method == 'POST':
        schedule=DoctorScheduleForm(request.POST)
        if schedule.is_valid():
            schedule.save()
            return redirect("doct")
    return  render(request,"doctor/addschedule.html",{"schedule":schedule})

def doct_schedule_view(request):
    data=DoctorSchedule.objects.all()
    return render(request,"doctor/scheduleview.html",{"data":data})

def doct_schedule_update(request,id):
    data=DoctorSchedule.objects.get(id=id)
    form=DoctorScheduleForm(instance=data)
    if request.method == 'POST':
        form=DoctorScheduleForm(request.POST,instance=data)
        if form.is_valid():
            form.save()
            return redirect("doctscheduleview")
    return render(request,"doctor/scheduleupdate.html",{"form":form})

def doct_schedule_delt(request,id):
    data=DoctorSchedule.objects.get(id=id)
    data.delete()
    return redirect("admndoctscheduleview")

def adm_doct_schedule_view(request):
    data = DoctorSchedule.objects.all()
    return render(request, "admintemp/doctscheduleview.html", {"data": data})

def adm_doct_shchedule_update(request,id):
    data = DoctorSchedule.objects.get(id=id)
    form = DoctorScheduleForm(instance=data)
    if request.method == 'POST':
        form = DoctorScheduleForm(request.POST, instance=data)
        if form.is_valid():
            form.save()
            return redirect("doctscheduleview")
    return render(request, "admintemp/scheduleupdate.html", {"form": form})


def patient_doct_schedule_view(request,id):
    u=Doctor.objects.get(id=id)
    data = DoctorSchedule.objects.filter(Name_id=u)

    return render(request, "patients/doctscheduleview.html", {"data":data})



def appoint(request,id):
    schedule=DoctorSchedule.objects.get(id=id)
    patient=request.user
    u=Patients.objects.get(user_2=patient)
    print(u)
    j=Joinnsreqst.objects.filter(Name_id=u,approve=schedule)
    print(j)
    dob = request.POST.get("dob")
    categories=request.POST.get("categories")
    gender=request.POST.get("gender")
    disease=request.POST.get("disease")

    if j.exists():
        messages.info(request, "you are already exist")
    else:
        if request.method=='POST':
            obj=Joinnsreqst()
            obj.dob= dob
            obj.categories = categories
            obj.gender = gender
            obj.Disease = disease
            obj.Name=u
            obj.approve=schedule

            obj.save()

            schedule.status = 1
            schedule.save()


            messages.info(request,'appointment request send successfully')

    return render(request,"patients/appoint.html",{"schedule":schedule,"u":u})

def adm_patient_rqst_view(request):
    join=Joinnsreqst.objects.all()


    return render(request,"admintemp/patients_appoint_rqst_view.html",{"join":join})


def approve(request,id):
    data=Joinnsreqst.objects.get(id=id)
    print(data)

    # data.status= 2
    dat = data.approve
    print(dat)
    dat.status = 2
    dat.save()
    return redirect("admnpatientrqstview")


def reject(request,id):
    data = Joinnsreqst.objects.get(id=id)
    # if request.method == 'POST':
    dats = data.approve
    print(dats)
    dats.status =0
    dats.save()
    return redirect("admnpatientrqstview")


def patients_appoint_view(request):
    data=Joinnsreqst.objects.all()

    return render(request,"patients/appointview.html",{"data":data})


def patients_appoint_delt(requset,id):
    data=Joinnsreqst.objects.get(id=id)

    data.delete()
    return redirect("patientsappointview")


def doct_patients_appoint_view(request):
    data=Joinnsreqst.objects.all()


    return render(request,"doctor/patientappointview.html",{"data":data})



def generate_bill(request,id):
    patient = Patients.objects.get(id=id)
    appoint = Joinnsreqst.objects.get(id=id)
    a = request.user
    doctor = Doctor.objects.get(user_1_id=a)



    patientDict={
        'patientId':id,
        'patient_name':patient.Pet_name,
        'mobile':patient.phone_number,
        'disease':appoint.Disease,
        'doctorname':doctor,

    }
    if request.method == 'POST':
        feeDict={
            'roomCharge':int(request.POST['roomCharge']),
            'syringeCost':int(request.POST['syringeCost']),
            'injectionMedicine':int(request.POST['injectionMedicine']),
            'doctorFee':int(request.POST['doctorFee']),
            # 'otherFee':int(request.POST['otherFee']),
            'total':int(request.POST['roomCharge'])+int(request.POST['syringeCost'])+int(request.POST['injectionMedicine'])+int(request.POST['doctorFee'])
        }
        patientDict.update(feeDict)
        pB=models.Bill()
        pB.patientId=id
        pB.patient_name=patient.Pet_name
        pB.doctorName=doctor
        pB.mobile=patient.phone_number
        pB.disease=appoint.Disease
        pB.roomCharge=int(request.POST['roomCharge'])
        pB.syringeCost=int(request.POST['syringeCost'])
        pB.injectionMedicine= int(request.POST['injectionMedicine'])
        pB.doctorFee=int(request.POST['doctorFee'])
        # pB.otherFee = int(request.POST['otherFee'])
        pB.total=int(request.POST['roomCharge'])+int(request.POST['syringeCost'])+int(request.POST['injectionMedicine'])+int(request.POST['doctorFee'])
        pB.save()
        return render(request,'doctor/patient_final_bill.html',context=patientDict)
    return render(request,'doctor/patient_generate_bill.html',context=patientDict)

def doct_bill_view(request):
    bill=Bill.objects.all()

    doct=DoctorSchedule.objects.all()

    combine=zip(bill,doct)
    return render(request,"doctor/bill_view.html",{"combine":combine})

def doct_bill_delt(request,id):
    bill=Bill.objects.get(id=id)
    bill.delete()
    return redirect("doctbillview")
def patients_bill_view(request):
    bill=Bill.objects.all()
    join=Joinnsreqst.objects.all()
    combine=zip(bill,join)
    return render(request,"patients/bill_view.html",{"combine":combine})

def prescription(request,id):
    patient=models.Patients.objects.get(id=id)
    appoint=Joinnsreqst.objects.get(id=id)
    a=request.user
    doctor=Doctor.objects.get(user_1_id=a)
    d=date.today()

    year=d.year
    age=year-appoint.dob.year
    patientDict={
        "patientId":id,
        "patient_name":patient.Pet_name,
        "mobile":patient.phone_number,
        "age":age,
        "dis":appoint.Disease,
        "email":doctor.Email,
        "doctorname":doctor,
        "date":d,
    }
    if request.method =='POST':
        prscriptionDict={
            "disease":request.POST['disease'],
            "test":request.POST['tests'],
            "med":request.POST['medicine'],

        }
        patientDict.update(prscriptionDict)
        pR=models.Prescript()
        pR.patientId=id
        pR.patient_name=patient.Pet_name
        pR.doctor_name=doctor
        pR.doct_email=doctor.Email
        pR.date=d
        pR.age=age
        pR.symptoms=appoint.Disease
        pR.disease=request.POST['disease'],
        pR.tests=request.POST['tests'],
        pR.medicine=request.POST['medicine']
        pR.save()
        return render(request,"doctor/prescription.html",context=patientDict)
    return render(request,"doctor/prescription_generate.html",context=patientDict)

def doct_presc_view(request):
    presc=Prescript.objects.all()
    doct=DoctorSchedule.objects.all()
    comb=zip(presc,doct)
    return render(request,"doctor/prescription_view.html",{'comb':comb})


def doct_presc_delt(request,id):
    data=Prescript.objects.get(id=id)
    data.delete()
    return redirect("doctprescview")

def patients_presc_view(request):

    presc=Prescript.objects.all()
    join=Joinnsreqst.objects.all()

    comb=zip(presc,join)
    return render(request,"patients/prescriptionview.html",{"comb":comb})

def patients_bill_precs_view(request):
    data = Joinnsreqst.objects.all()

    return render(request, "patients/bill_presc_view.html", {"data":data})
