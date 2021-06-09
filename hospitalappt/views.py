from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
import datetime
import json


def loadmain(request):
    return render(request, 'apptpage.html')


def make_appointments(request):
    data = json.loads(request.GET.get('data'))
    patient_id = patients.get_id_by_name(data['first_name'], data['last_name'])
    if patient_id is None:
        patient_id = patients.add_new_patient(
            data['first_name'], data['last_name'], data['dob'], data['email'], data['phone_no'])
    _, msg = doctors[data['doctor_selection']].make_appointment(
        data['appt_date'], data['appt_time'], patient_id)
    return JsonResponse({'msg': msg})
# Data for Appt Availabilities and Patient Information are stored in class format
# (normally I would store it in databases, but since this is objected oriented programming class, class structure is used)


class Person():
    """Base class for Person"""

    def __init__(self, first_name, last_name):
        self.first_name = first_name
        self.last_name = last_name

    def get_name(self):
        return self.first_name + ' ' + self.last_name


class Patient(Person):
    """Object that stores patient information"""

    def __init__(self, patient_id, first_name, last_name, dob, email, phone_no):
        super().__init__(first_name, last_name)
        self.patient_id = patient_id
        self.dob = dob
        self.email = email
        self.phone_no = phone_no


class Patients():
    """Group of patients"""

    def __init__(self):
        self.patients = []
        self.next_available_id = -1

    def add_new_patient(self, first_name, last_name, dob, email, phone_no):
        self.next_available_id += 1
        self.patients.append(
            Patient(self.next_available_id, first_name, last_name, dob, email, phone_no))
        return self.next_available_id

    def get_id_by_name(self, first_name, last_name):
        print(self.patients)
        for patient in self.patients:
            if patient.first_name == first_name and patient.last_name == last_name:
                return patient.patient_id
        return None


class Doctor(Person):
    """Object that stores doctors' appointment availability"""

    def __init__(self, first_name, last_name, location, phone_no):
        super().__init__(first_name, last_name)
        self.location = location
        self.phone_no = phone_no
        self.appointments = {}

    def check_appt_availabiltiy(self, appt_date, appt_time):
        # Convert string appt_date, appt_time to date and integer formats
        appt_dt = datetime.datetime.strptime(appt_date, "%Y-%m-%d").date()
        hour = int(appt_time.split(":")[0])
        # First check whether appt_date is M-F
        if appt_dt.weekday() > 4:
            return False
        # Next check whether time is between 9AM - 6PM
        if not 9 <= hour < 18:
            return False
        # Next check whether the slot is not already taken
        if appt_date not in self.appointments:
            self.appointments[appt_date] = {}
        return appt_time not in self.appointments[appt_date]

    def make_appointment(self, appt_date, appt_time, patient_id):
        if not self.check_appt_availabiltiy(appt_date, appt_time):
            return False, "Requested Date/Time is not available for Dr. "+self.get_name()
        self.appointments[appt_date][appt_time] = patient_id
        patient = patients.patients[patient_id]
        return True, f"""Appointment Booked Successfully for Dr. {self.get_name()}
Patient Name:{patient.first_name} {patient.last_name}
Doctor Phone No:{self.phone_no}
Appointment Time: {appt_date} {appt_time}
        """


patients = Patients()

doctors = {
    '1': Doctor('Eric', 'Cho', 'Arlington', '123-456-7890'),
    '2': Doctor('Ben', 'Smith', 'Fairfax', '111-222-3333'),
    '3': Doctor('John', 'Doe', 'Falls Church', '444-111-2222')
}
