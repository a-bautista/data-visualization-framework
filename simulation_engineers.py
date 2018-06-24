'''
Author: Alejandro Bautista Ramos

The following is a python file that tries to simulate the behaviour of each engineer from the
COL_TriageTickets_ExportV2_01_04_2018_modified_data_analysis.xlsx.
'''
from numpy.random import choice
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

        # ------------------------- Getter and setter methods ---------------------------------#

        '''
        # Getter for the non-public variable first name
        @property
        def first_name(self):
            return self._first_name

        # Getter for the non-public variable last name
        @property
        def last_name(self):
            return self._last_name

        # Getter for the non-public variable amount_of_tickets_solved_day
        @property # define the getter
        def amount_of_tickets_solved_day(self):
            return self._amount_of_tickets_solved_day

        # Setter for the non-public variable amount_of_tickets_solved_day
        @amount_of_tickets_solved_day.setter # define the setter
        def amount_of_tickets_solved_day(self, new_value):
            self._amount_of_tickets_solved_day = new_value

        '''
        # ------------------------- Other methods ---------------------------------#

        def print_full_name(self):
            return self.first_name+" "+self.last_name

        #def weights_category(self):



def main():

    #Define engineers
    engineer_alekz_horne = Engineer("Alekz","Horne", random.randint(8,11)) #lists are not declared here

    print(engineer_alekz_horne.first_name)
    print(engineer_alekz_horne.last_name)
    print(engineer_alekz_horne.amount_of_tickets_solved_day)

    #this
    engineer_alekz_horne.elements_category = ["IoT"]
    engineer_alekz_horne.weight_category = [1]

    engineer_alekz_horne.elements_problem_category = ["Breach in SCADA systems","Compromised data","Erroneous data load",
                                                      "Hijack of device", "Internal flaws in device", "Malware installed",
                                                      "Penetration breach"]

    engineer_alekz_horne.weights_problem_category  = [0.0646, 0.2320, 0.0943, 0.0816, 0.0339, 0.1653, 0.3284]

    engineer_alekz_horne.elements_affected_devices = ["Company main devices", "Personal user devices", "Third party devices"]
    engineer_alekz_horne.weights_affected_devices = [0.1165, 0.7754, 0.1081]



    for day in range(int(engineer_alekz_horne.amount_of_tickets_solved_day)):
        print(choice(engineer_alekz_horne.elements_tickets_category, p=engineer_alekz_horne.weight_tickets_category))

    print(engineer_alekz_horne.weight_tickets_category)
    print(engineer_alekz_horne.elements_tickets_category)
    # and not this
    #engineer_alekz_horne = engineer_alekz_horne.amount_of_tickets_solved_day(9)

    #print(engineer_alekz_horne.amount_of_tickets_solved_day)
    print(engineer_alekz_horne.amount_of_tickets_solved_day)





'''
>>> elements = ['one','two','three']
>>> weights = [0.2, 0.3, 0.5]
>>> from numpy.random import choice
>>> print(choice(elements, p = weights))
'''




if __name__ == "__main__":
    main()
