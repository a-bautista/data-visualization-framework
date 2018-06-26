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
                 #elements_kpi_i = None,
                 #weights_kpi_i = None
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

    #------------------------------- Initialize main components of each engineer --------------------------#

    engineer_alekz_horne   = Engineer("Alekz","Horne", random.randint(7,9)) #lists are not declared here
    engineer_annette_smith = Engineer("Annette","Smith", random.randint(6,8))  #lists are not declared here)

    generated_tickets_alekz_horne = []
    generated_tickets_annette_smith = []

    #---------------------------------Generate tickets for Alekz Horne-------------------------------------#

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

    for day in range(int(engineer_alekz_horne.amount_of_tickets_solved_day)):
        generated_tickets_alekz_horne.append(choice(engineer_alekz_horne.elements_category, p=engineer_alekz_horne.weight_category))
        generated_tickets_alekz_horne.append(choice(engineer_alekz_horne.elements_problem_category, p=engineer_alekz_horne.weights_problem_category))
        generated_tickets_alekz_horne.append(choice(engineer_alekz_horne.elements_affected_devices, p=engineer_alekz_horne.weights_affected_devices))
        generated_tickets_alekz_horne.append(choice(engineer_alekz_horne.elements_reason_for_creating, p=engineer_alekz_horne.weights_reason_for_creating))
        generated_tickets_alekz_horne.append(choice(engineer_alekz_horne.elements_issue_status, p=engineer_alekz_horne.weights_issue_status))
        generated_tickets_alekz_horne.append(choice(engineer_alekz_horne.elements_sla_met, p=engineer_alekz_horne.weights_sla_met))
        generated_tickets_alekz_horne.append(choice(engineer_alekz_horne.elements_priority, p=engineer_alekz_horne.weights_priority))
        generated_tickets_alekz_horne.append("KPI_I")
        generated_tickets_alekz_horne.append(random.randint(0, 45))
        generated_tickets_alekz_horne.append("KPI_II")
        generated_tickets_alekz_horne.append(random.randint(0, 24))
        generated_tickets_alekz_horne.append("KPI_III")
        generated_tickets_alekz_horne.append(random.randint(0, 31))
        generated_tickets_alekz_horne.append("KPI_IV")
        generated_tickets_alekz_horne.append(random.randint(0, 28))
        generated_tickets_alekz_horne.append(";")
        #print(choice(engineer_alekz_horne.elements_category, p=engineer_alekz_horne.weight_category))
    print(generated_tickets_alekz_horne)

    #---------------------------------Generate tickets for Annette Smith -------------------------------------#

    print(engineer_annette_smith.first_name)
    print(engineer_annette_smith.last_name)
    print(engineer_annette_smith.amount_of_tickets_solved_day)

    # this
    engineer_annette_smith.elements_category = ["CyberSecurity"]
    engineer_annette_smith.weight_category = [1]

    engineer_annette_smith.elements_problem_category = ["Bad security policies", "Compromised data",
                                                      "DDoS attack","Erroneous data load",
                                                      "Identity spoofing","Lack of CERT",
                                                      "Penetration breach", "Ransomware virus"]

    engineer_annette_smith.weights_problem_category = [0.267, 0.017, 0.156, 0.004, 0.003, 0.037, 0.146, 0.371]

    engineer_annette_smith.elements_affected_devices = ["Company main devices", "Personal user devices",
                                                      "Third party devices"]
    engineer_annette_smith.weights_affected_devices = [0.326, 0.530, 0.145]

    engineer_annette_smith.elements_reason_for_creating = ["Bi-weekly Analysis","Daily Analysis", "Hourly Analysis", "Random Analysis", "Special Request"]
    engineer_annette_smith.weights_reason_for_creating = [0.001, 0.112, 0.644, 0.121, 0.122]

    engineer_annette_smith.elements_issue_status = ["Closed", "In Progress", "Transferred"]
    engineer_annette_smith.weights_issue_status = [0.327, 0.011, 0.662]

    engineer_annette_smith.elements_sla_met = ["Yes"]
    engineer_annette_smith.weights_sla_met = [1]

    engineer_annette_smith.elements_priority = ["P2", "P3"]
    engineer_annette_smith.weights_priority = [0.334, 0.666]

    for day in range(int(engineer_annette_smith.amount_of_tickets_solved_day)):
        generated_tickets_annette_smith.append(
            choice(engineer_alekz_horne.elements_category, p=engineer_alekz_horne.weight_category))
        generated_tickets_annette_smith.append(
            choice(engineer_alekz_horne.elements_problem_category, p=engineer_alekz_horne.weights_problem_category))
        generated_tickets_annette_smith.append(
            choice(engineer_alekz_horne.elements_affected_devices, p=engineer_alekz_horne.weights_affected_devices))
        generated_tickets_annette_smith.append(choice(engineer_alekz_horne.elements_reason_for_creating,
                                                    p=engineer_alekz_horne.weights_reason_for_creating))
        generated_tickets_annette_smith.append(
            choice(engineer_alekz_horne.elements_issue_status, p=engineer_alekz_horne.weights_issue_status))
        generated_tickets_annette_smith.append(
            choice(engineer_alekz_horne.elements_sla_met, p=engineer_alekz_horne.weights_sla_met))
        generated_tickets_annette_smith.append(
            choice(engineer_alekz_horne.elements_priority, p=engineer_alekz_horne.weights_priority))
        generated_tickets_annette_smith.append("KPI_I")
        generated_tickets_annette_smith.append(random.randint(0, 45)) # KPIs should be adjusted to random choice to get more accurate data
        generated_tickets_annette_smith.append("KPI_II")
        generated_tickets_annette_smith.append(random.randint(0, 48))
        generated_tickets_annette_smith.append("KPI_III")
        generated_tickets_annette_smith.append(random.randint(0, 64))
        generated_tickets_annette_smith.append("KPI_IV")
        generated_tickets_annette_smith.append(random.randint(0, 47))
        generated_tickets_annette_smith.append(";")
        # print(choice(engineer_alekz_horne.elements_category, p=engineer_alekz_horne.weight_category))
    print(generated_tickets_annette_smith)


if __name__ == "__main__":
    main()
