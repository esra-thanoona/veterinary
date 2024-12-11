from django.contrib.auth.models import AbstractUser
from django.db import models

# Create your models here.

class Login(AbstractUser):
    is_doctor = models.BooleanField(default=False)
    is_patients = models.BooleanField(default=False)


class Doctor(models.Model):
    user_1=models.ForeignKey(Login,on_delete=models.CASCADE)
    Name=models.CharField(max_length=50)
    Email=models.EmailField()
    Address=models.CharField(max_length=90)
    Description=models.CharField(max_length=100)
    Image=models.FileField(upload_to='images/')
    fee=models.IntegerField()

    def __str__(self):
        return self.Name


class Patients(models.Model):
    user_2=models.ForeignKey(Login,on_delete=models.CASCADE)
    Owner_name=models.CharField(max_length=50)
    Pet_name=models.CharField(max_length=50)
    phone_number=models.CharField(max_length=10)

    def __str__(self):
        return self.Pet_name


class DoctorSchedule(models.Model):
    Name=models.ForeignKey(Doctor,on_delete=models.CASCADE)
    Day=models.DateField()
    Time=models.TimeField()
    status = models.IntegerField(default=0)




class Joinnsreqst(models.Model):

    approve=models.ForeignKey(DoctorSchedule,on_delete=models.CASCADE)
    Name = models.ForeignKey(Patients, on_delete=models.CASCADE)
    dob = models.DateField()
    CATEGORIES = (
        ('DOG', 'DOG'),
        ('CAT', 'CAT'),
        ('RABBIT', 'RABBIT'),
        ('BIRDS', 'BIRDS'),
        ('FISH', 'FISH'),
        ('RODENTS', 'RODENTS'),
    )
    CHOICES = (
        ('M', 'MALE'),
        ('F', 'FEMALE'),
    )
    gender = models.CharField(max_length=6, choices=CHOICES)
    categories = models.CharField(max_length=50, choices=CATEGORIES)
    Disease = models.TextField()


class Bill(models.Model):
    patientId=models.PositiveIntegerField(null=True)
    patient_name=models.CharField(max_length=40)
    doctorName=models.CharField(max_length=40)
    mobile=models.CharField(max_length=10)
    disease=models.CharField(max_length=40,null=True)

    roomCharge=models.PositiveIntegerField(null=False)
    syringeCost=models.PositiveIntegerField(null=False)
    injectionMedicine=models.PositiveIntegerField(null=False)
    doctorFee=models.PositiveIntegerField(null=False)

    total=models.PositiveIntegerField(null=False)

class Prescript(models.Model):
    patientId=models.PositiveIntegerField(null=True)
    patient_name=models.CharField(max_length=40)
    doctor_name=models.CharField(max_length=40)
    doct_email=models.CharField(max_length=50)
    date=models.DateField(null=False)
    age=models.PositiveIntegerField(null=True)
    symptoms=models.CharField(max_length=100,null=True)

    disease=models.TextField()
    medicine=models.TextField()
    tests=models.TextField()





