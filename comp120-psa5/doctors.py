"""
Module: doctors

An application to solve the Doctors Without Orders problem.

"""

from sys import argv, exit
from dataclasses import dataclass

def hour_or_hours(num_hours: int) -> str:
    """Helper function to get correct pluralization."""
    assert num_hours >= 0
    return "hour" if num_hours == 1 else "hours"


@dataclass(frozen=True)
class Doctor:
    """A representation of a Doctor, including their name and the maximum
    available hours for scheduling (max_hours).

    Doctors are immutable (i.e. can't change any of their two attributes).

    DO NOT MODIFY THIS CLASS IN ANY WAY!!!

    >>> dr_sat = Doctor("Doctor A", 7)
    >>> dr_sat.name
    'Doctor A'
    >>> dr_sat.max_hours
    7
    >>> dr_sat.max_hours = 11
    Traceback (most recent call last):
        ...
    dataclasses.FrozenInstanceError: cannot assign to field 'max_hours'
    """
    name: str
    max_hours: int

    def __str__(self) -> str:
        h = hour_or_hours(self.max_hours)
        return f"Doctor {self.name} ({self.max_hours} {h})"


@dataclass(frozen=True)
class Patient:
    """A representation of a Patient, including their name and the number of
    hours they need to be seen for (needed_hours).

    Patients are immutable (i.e. can't change any of their two attributes).

    DO NOT MODIFY THIS CLASS IN ANY WAY!!!

    >>> ouchy = Patient("Patient A", 3)
    >>> ouchy.name
    'Patient A'
    >>> ouchy.needed_hours
    3
    >>> ouchy.needed_hours = 1
    Traceback (most recent call last):
        ...
    dataclasses.FrozenInstanceError: cannot assign to field 'needed_hours'
    """
    name: str
    needed_hours: int

    def __str__(self) -> str:
        h = hour_or_hours(self.needed_hours)
        return f"Patient {self.name} ({self.needed_hours} {h})"


def parse_scheduling_data(filename: str) -> tuple[list[Doctor], list[Patient]]:
    """
    Reads the doctor and patient data from <filename>, returning a list of
    Doctors and and a list of Patients.

    DO NOT MODIFY THIS FUNCTION IN ANY WAY!!!

    Parameters:
        filename (str): Name of the file containing doctor and patient info.

    Returns:
        (tuple[list[Doctor], list[Patient]]): Two lists: the first of doctors
            and the second of patients, gathered from the specified file.
    """
    docs = []
    patients = []

    with open(filename, 'r') as f:
        all_lines = f.readlines()

        i = 0
        while i < len(all_lines) and (all_lines[i][0] == '#' or
                                      all_lines[i].strip() == ""):
            i += 1

        for line_num in range(i, len(all_lines)):
            line = all_lines[line_num]
            person_info, hours = line.split(':')
            person_split = person_info.split()
            title = person_split[0]
            name = " ".join(person_split[1:])

            if title == "Doctor":
                docs.append(Doctor(name, int(hours)))
            else:
                patients.append(Patient(name, int(hours)))

    return docs, patients

from collections import defaultdict

from collections import defaultdict

def can_schedule_all(doctors: list[Doctor], patients: list[Patient], schedule: dict[Doctor, set[Patient]]) -> bool:
    """
    Determines if all patients can be scheduled with the doctors provided.
    Updates the schedule parameter with a valid schedule if possible.

    Parameters:
        doctors (list[Doctor]): A list of doctors with available hours.
        patients (list[Patient]): A list of patients with required hours.
        schedule (dict[Doctor, set[Patient]]): A mapping of doctors to the patients they see.

    Returns:
        bool: True if a valid schedule exists, False otherwise.
    """
    #Base case
    if not patients:
        return True

    #Get the next patient to schedule
    patient = patients[0]
    remaining_patients = patients[1:]

    #Check remaining hours for each doctor
    remaining_hours={}
    for doct in doctors: #loops through every doctor in list
        total=0 #accumulator variable
        for i in schedule[doct]:
            total+=i.needed_hours #i represents the current patient being looped through in the doctor being looped through in the schedule dictionary
        remaining_hours[doct]=doct.max_hours - total #subtracts doctors total working hours with current scheduled hours, finding the leftover hours allowed to be scheduled

    for doctor in doctors:
        # Checks if the doctor has enough hours to see this patient
        if remaining_hours[doctor] >= patient.needed_hours:
            # Temporarily assign the patient to this doctor
            schedule[doctor].add(patient)
            remaining_hours[doctor] -= patient.needed_hours

            # Recursion with the updated schedule
            if can_schedule_all(doctors, remaining_patients, schedule):
                return True

            # Backtracks by removing the patient from this doctor's schedule
            schedule[doctor].remove(patient)
            remaining_hours[doctor] += patient.needed_hours

    #Returns false if no assignment
    return False









if __name__ == "__main__":
    if len(argv) != 2:
        print("Error: wrong number of command line parameters")
        exit(1)

    docs, patients = parse_scheduling_data(argv[1])

    # create initial schedule, with each doctor assigned to no one!
    proposed_schedule: dict[Doctor, set[Patient]] = {d: set() for d in docs}

    if can_schedule_all(docs, patients, proposed_schedule):
        print("Proposed schedule:")
        for doc, docs_patients in proposed_schedule.items():
            patient_names = ", ".join([str(p) for p in docs_patients])
            print(f"\t{doc} -> {patient_names}")
    else:
        print("No valid schedule possible!")
