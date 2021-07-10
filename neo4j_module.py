from neo4j import GraphDatabase

driver = GraphDatabase.driver("neo4j://localhost:7687", auth=("neo4j", "0501cho"))

def create_patient(first_name, last_name, dob, email, phone_no):
    session = driver.session()
    session.run("create (n:Patient {name:'%s', first_name:'%s',last_name:'%s',dob:'%s',email:'%s',phone_no:'%s'})" % \
        (first_name +' '+last_name, first_name, last_name, dob, email, phone_no))
    session.close()

def patient_exists(first_name, last_name):
    session = driver.session()
    result =  len(list(session.run("match (n) where n.name = '%s' return n" % \
        (first_name +' '+last_name))))>0
    session.close()
    return result
def create_doctor(first_name, last_name, office, phone_no):
    session = driver.session()
    session.run("create (n:Doctor {name:'%s', first_name:'%s',last_name:'%s',office:'%s',phone_no:'%s'})" % \
        (first_name +' '+last_name, first_name, last_name, office, phone_no))
    session.close()

def appointment_available(doctor_name, appt_date, appt_time):
    session = driver.session()
    result =  len(list(session.run("match (a:Patient)-[r:Appointment]->(b:Doctor) where b.name = '%s' and r.appt_date='%s' and r.appt_time='%s' return r" % \
        (doctor_name, appt_date,appt_time))))==0
    session.close()
    return result

def create_appointment(patient_name, doctor_name, appt_date, appt_time):
    session = driver.session()
    session.run("""match (a:Patient), (b:Doctor)
    where a.name = '%s' and b.name = '%s'
    create (a)-[r:Appointment {appt_date:'%s', appt_time:'%s'}]->(b)
    """ % (patient_name, doctor_name, appt_date, appt_time))
    session.close()

if __name__=="__main__":
    create_patient('Yeon Sik','Cho','1989-11-27','yeonsikcho@gmail.com','3106061709')
    patient_exists("Yeon Sik", "Cho")
    create_doctor('Eric','Cho','Arlington','123-456-7890')
    create_doctor('Ben','Smith','Fairfax','111-222-3333')
    create_doctor('John','Doe','Falls Church','444-111-2222')
    create_appointment('Yeon Sik Cho','Eric Cho','2021-07-10','09:15')
    appointment_available('Eric Cho','2021-07-10','09:15')