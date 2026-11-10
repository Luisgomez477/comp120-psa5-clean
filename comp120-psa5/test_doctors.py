"""
Module: test_doctors

PyTest Unit Test cases for COMP120 PSA5 (Doctors Without Orders)
"""

import pytest

# the following is the module(s) we are testing
import doctors
from doctors import Doctor, Patient

def test_no_patients():
    """Test for the base case of when there is a doctor but are no patients to be seen."""

    d = Doctor("D1", 100)
    schedule = {d: set()} # schedule has doctor with no patients

    result = doctors.can_schedule_all([d], [], schedule)
    assert result == True


def test_no_doctors():
    """Test for the base case of when there isn't a doctor but there are patients."""

    p = Patient("P1", 1)
    result = doctors.can_schedule_all([], [p], {})

    assert result == False


def test_one_doctor_and_patient_ok():
    """Test for when there is one doctor and one patient and the doctor has
    enough hours to meet the patient."""

    d = Doctor("D1", 10)
    p = Patient("P1", 1)

    actual_schedule = {d: set()} # initial schedule is empty

    result = doctors.can_schedule_all([d], [p], actual_schedule)

    # create a set with the patient
    expected_patients_for_d = set()
    expected_patients_for_d.add(p)

    # need to check that we returned the right value and that the actual
    # schedule for the doctor matches what we expected
    assert result == True
    assert actual_schedule[d] == expected_patients_for_d


# TODO: Complete all of the test functions below.
# DO NOT modify any of the test functions above here.


def test_one_doctor_and_patient_bad():
    """Test for when there is one doctor and one patient and the doctor does
    NOT have enough hours to meet the patient."""
    d = Doctor("D1", 1)
    p = Patient("P1", 10)

    actual_schedule = {d: set()}  
    # initial schedule is empty

    result = doctors.can_schedule_all([d], [p], actual_schedule)

    assert result == False
    assert actual_schedule[d] == set()  
    # No patients should be assigned


def test_one_doctor_multiple_patient_ok():
    """Test for when there is one doctor and multiple patients, and that the
    doctor has enough time to meet with all patients."""
    d = Doctor("D1", 10)
    p1 = Patient("P1", 2)
    p2 = Patient("P2", 3)
    p3 = Patient("P3", 5)

    actual_schedule = {d: set()}  
    # initial schedule is empty

    result = doctors.can_schedule_all([d], [p1, p2, p3], actual_schedule)

    expected_patients_for_d = {p1, p2, p3}

    assert result == True
    assert actual_schedule[d] == expected_patients_for_d


def test_one_doctor_multiple_patient_bad():
    """Test for when there is one doctor and multiple patients, and that the
    doctor does NOT have enough time to meet with all patients. Also, none of
    the patients should require more hours than the doctor has free."""
    d = Doctor("D1", 8)
    p1 = Patient("P1", 2)
    p2 = Patient("P2", 3)
    p3 = Patient("P3", 4)

    actual_schedule = {d: set()}  
    # initial schedule is empty

    result = doctors.can_schedule_all([d], [p1, p2, p3], actual_schedule)

    assert result == False
    assert actual_schedule[d] == set()  
    # No patients should be assigned


def test_two_doctors_multiple_patient_ok():
    """Test for when there are two doctor and multiple patients, and that 
    (1) We can't schedule all the patients with a single doctor.
    (2) We can schedule all the patients across the two doctors.
    (3) Each doctor will be assigned at least two patients."""
    d1 = Doctor("D1", 6)
    d2 = Doctor("D2", 8)
    p1 = Patient("P1", 2)
    p2 = Patient("P2", 3)
    p3 = Patient("P3", 5)
    p4 = Patient("P4", 4)

    actual_schedule = {d1: set(), d2: set()}  # initial schedule is empty

    result = doctors.can_schedule_all([d1, d2], [p1, p2, p3, p4], actual_schedule)

    assert result == True
    assert len(actual_schedule[d1]) >= 2
    assert len(actual_schedule[d2]) >= 2


def test_two_doctors_multiple_patient_bad():
    """Test for when there are two doctor and multiple patients, and that 
    (1) We can't schedule all the patients with the two doctors.
    (2) None of the patients by themselves require more hours than either of
    the doctors."""
    d1 = Doctor("D1", 5)
    d2 = Doctor("D2", 6)
    p1 = Patient("P1", 3)
    p2 = Patient("P2", 4)
    p3 = Patient("P3", 7)

    actual_schedule = {d1: set(), d2: set()} 
     # initial schedule is empty

    result = doctors.can_schedule_all([d1, d2], [p1, p2, p3], actual_schedule)

    assert result == False
    assert actual_schedule[d1] == set()
    assert actual_schedule[d2] == set()

if __name__ == "__main__":
    pytest.main(['test_doctors.py'])
