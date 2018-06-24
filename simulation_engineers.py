'''
Author: Alejandro Bautista Ramos

The following is a python file that tries to simulate the behaviour of each engineer from the
COL_TriageTickets_ExportV2_01_04_2018_modified_data_analysis.xlsx.
'''
from numpy.random import choice
import numpy as np
import random

class Engineer:

    def __init__(self,
                 first_name,
                 last_name,
                 amount_of_tickets_solved_day,
                 elements_category = None,
                 weight_category   = None,
                 elements_problem_category = None,
                 weight_problem_category = None,
                 elements_affected_devices = None,
                 weight_affected_devices = None,
                 elements_reason_for_creating = None,
                 weights_reason_for_creating  = None,
                 elements_issue_status = None,
                 weights_issue_status = None,
                 elements_sla_met = None,
                 weights_sla_met  = None,
                 elements_priority = None,
                 weights_priority = None,
                 elements_kpi_i = None,
                 weights_kpi_i = None
                 ):

        ''' Define the Engineer constructor. If one variable is non-public then it must contain the getters and setters
            properties. '''

        self.first_name                   = first_name
        self.last_name                    = last_name
        self.amount_of_tickets_solved_day = amount_of_tickets_solved_day # non-public attribute, can be changed because there is a setter

        if elements_category is None:
            elements_category         = []

        if weight_category is None:
            weight_category           = []

        if elements_problem_category is None:
            elements_problem_category = []

        if weight_problem_category is None:
            weight_problem_category   = []

        if elements_affected_devices is None:
            elements_affected_devices = []

        if weight_affected_devices is None:
            weight_affected_devices = []

        if elements_reason_for_creating is None:
            elements_reason_for_creating = []

        if weights_reason_for_creating is None:
            weights_reason_for_creating = []

        if elements_issue_status is None:
            elements_issue_status = []

        if weights_issue_status is None:
            weights_issue_status = []

        if elements_sla_met is None:
            elements_sla_met = []

        if weights_sla_met is None:
            weights_sla_met = []

        if elements_priority is None:
            elements_priority = []

        if weights_priority is None:
            weights_priority = []

        # ------------------------- Other methods ---------------------------------#

        def print_full_name(self):
            return self.first_name+" "+self.last_name

        #def weights_category(self):


def main():

    #Define engineers
    engineer_alekz_horne = Engineer("Alekz","Horne", random.randint(8,10)) #lists are not declared here

    generated_tickets = []

    print(engineer_alekz_horne.first_name)
    print(engineer_alekz_horne.last_name)
    print(engineer_alekz_horne.amount_of_tickets_solved_day)

    #this
    engineer_alekz_horne.elements_category = ["IoT"]
    engineer_alekz_horne.weight_category = [1]

    engineer_alekz_horne.elements_problem_category = ["Breach in SCADA systems","Compromised data","Erroneous data load",
                                                      "Hijack of device", "Internal flaws in device", "Malware installed",
                                                      "Penetration breach"]
    engineer_alekz_horne.weights_problem_category  = [0.065, 0.232, 0.094, 0.082, 0.034, 0.165,0.328]

    engineer_alekz_horne.elements_affected_devices = ["Company main devices", "Personal user devices", "Third party devices"]
    engineer_alekz_horne.weights_affected_devices = [0.117, 0.775, 0.108]

    engineer_alekz_horne.elements_reason_for_creating = ["Daily Analysis", "Hourly Analysis","Special Request"]
    engineer_alekz_horne.weights_reason_for_creating = [0.754, 0.092, 0.154]


    engineer_alekz_horne.elements_issue_status = ["Closed","In Progress","Transferred"]
    engineer_alekz_horne.weights_issue_status  = [0.117, 0.093, 0.790]

    engineer_alekz_horne.elements_sla_met = ["Yes"]
    engineer_alekz_horne.weights_sla_met  = [1]

    engineer_alekz_horne.elements_priority = ["P1","P2","P3"]
    engineer_alekz_horne.weights_priority = [0.082, 0.293, 0.625]

    engineer_alekz_horne.elements_kpi_i = random.randint(1,68)

    for day in range(int(engineer_alekz_horne.amount_of_tickets_solved_day)):
        generated_tickets.append(choice(engineer_alekz_horne.elements_category, p=engineer_alekz_horne.weight_category))
        generated_tickets.append(choice(engineer_alekz_horne.elements_problem_category, p=engineer_alekz_horne.weights_problem_category))
        generated_tickets.append(choice(engineer_alekz_horne.elements_affected_devices, p=engineer_alekz_horne.weights_affected_devices))
        generated_tickets.append(choice(engineer_alekz_horne.elements_reason_for_creating, p=engineer_alekz_horne.weights_reason_for_creating))
        generated_tickets.append(choice(engineer_alekz_horne.elements_issue_status, p=engineer_alekz_horne.weights_issue_status))
        generated_tickets.append(choice(engineer_alekz_horne.elements_sla_met, p=engineer_alekz_horne.weights_sla_met))
        generated_tickets.append(choice(engineer_alekz_horne.elements_priority, p=engineer_alekz_horne.weights_priority))
        generated_tickets.append("KPI_I")
        generated_tickets.append(random.randint(0, 45))
        generated_tickets.append("KPI_II")
        generated_tickets.append(random.randint(0, 45))
        generated_tickets.append("KPI_III")
        generated_tickets.append(random.randint(0, 31))
        generated_tickets.append("KPI_IV")
        generated_tickets.append(random.randint(0, 45))
        generated_tickets.append(";")

        #print(choice(engineer_alekz_horne.elements_category, p=engineer_alekz_horne.weight_category))

    print(generated_tickets)







'''
>>> elements = ['one','two','three']
>>> weights = [0.2, 0.3, 0.5]
>>> from numpy.random import choice
>>> print(choice(elements, p = weights))
'''




if __name__ == "__main__":
    main()
