from django import forms
from django.contrib.auth.forms import UserCreationForm

from veterinaryapp.models import Login, Doctor, Patients, DoctorSchedule, Bill, Joinnsreqst


class LoginRegister(UserCreationForm):
    username=forms.CharField()
    password1 = forms.CharField(label="password",widget=forms.PasswordInput)
    password2 = forms.CharField(label="confirm password",widget=forms.PasswordInput)

    class Meta:
        model=Login
        fields=("username","password1","password2")



class DoctorForm(forms.ModelForm):
    class Meta:
        model=Doctor
        fields="__all__"
        exclude=("user_1",)


class DateInput(forms.DateInput):
    input_type = 'date'
class TimeInput(forms.TimeInput):
    input_type = 'time'


class PatientsForm(forms.ModelForm):

    class Meta:
        model=Patients
        fields="__all__"

        exclude=("user_2",)


class DoctorScheduleForm(forms.ModelForm):
    Day=forms.DateField(widget=DateInput)
    Time=forms.TimeField(widget=TimeInput)

    class Meta:
        model=DoctorSchedule
        fields=("Name","Day","Time")






class JoinForm(forms.ModelForm):
    dob = forms.DateField(widget=DateInput)
    class Meta:
        model= Joinnsreqst
        fields='__all__'
        widgets = {
            'gender': forms.RadioSelect()
        }
        exclude = ("user_2",)


class BillForm(forms.ModelForm):
    class Meta:
        model=Bill
        fields=("roomCharge","syringeCost","injectionMedicine","doctorFee","total")