from django import forms
from datetime import date, datetime
from .models import SecurityAuditEngineer


class DropDownMenuForm(forms.Form):
    # start the current week in Monday and end in Sunday
    week = forms.ChoiceField(choices=[(x,x) for x in range (1,53)],initial=date.today().isocalendar()[1])
    year = forms.ChoiceField(choices=[(x,x) for x in range (2016,2021)],initial=date.today().year)

class DropDownMenuFormTicketsPerWeek(forms.Form):
    week_comparison_one = forms.ChoiceField(choices=[(x, x) for x in range(1, 53)],
                                            initial=date.today().isocalendar()[1])
    year_comparison_one = forms.ChoiceField(choices=[(x, x) for x in range(2016, 2021)], initial=date.today().year)

    week_comparison_two = forms.ChoiceField(choices=[(x, x) for x in range(1, 53)],
                                            initial=date.today().isocalendar()[1] - 1)
    year_comparison_two = forms.ChoiceField(choices=[(x, x) for x in range(2016, 2021)], initial=date.today().year)


class DropDownMonthlyMenuForm(forms.Form):
    months = ("1",'January'),("2",'February'),("3",'March'),("4",'April'),("5",'May'),("6",'June'),\
             ("7",'July'), ("8",'August'),("9",'September'),("10",'October'),("11",'November'),("12",'December')

    month = forms.ChoiceField(choices=[x for x in months], initial=date.today().month)
    year  = forms.ChoiceField(choices=[(x,x) for x in range (2016,2021)],initial=date.today().year)


class DropDownYearlyMenuFormSecurityAudit(forms.Form):
    year = forms.ChoiceField(choices=[(x, x) for x in range(2017, 2021)], initial=date.today().year)

#class DropDownMenuFormSecurityAudit(forms.Form):
#    # the line from below indicates to start the current week in Sunday and end in Saturday
#    #week = forms.ChoiceField(choices=[(x, x) for x in range(1, 53)], initial=datetime.now().strftime("%U"))
#    week = forms.ChoiceField(choices=[(x, x) for x in range(1, 53)], initial=date.today().isocalendar()[1])
#    year = forms.ChoiceField(choices=[(x, x) for x in range(2017, 2021)], initial=date.today().year)


class DropDownMenuFormQuantitativeQualitativeDaily(forms.Form):
    months = ("1", 'January'), ("2", 'February'), ("3", 'March'), ("4", 'April'), ("5", 'May'), ("6", 'June'), \
             ("7", 'July'), ("8", 'August'), ("9", 'September'), ("10", 'October'), ("11", 'November'), (
             "12", 'December')
    day   = forms.ChoiceField(choices=[(x,x) for x in range(1,32)], initial=date.today().day)
    month = forms.ChoiceField(choices=[x for x in months], initial=date.today().month)
    year  = forms.ChoiceField(choices=[(x,x) for x in range(2017,2021)], initial=date.today().year)

class DropDownMenuFormQuantitativeQualitativeYearly(forms.Form):
    list_of_engineers = []
    querySet = SecurityAuditEngineer.objects.all()

    for engineer in querySet:
        list_of_engineers.append(engineer.engineer_name + " " + engineer.engineer_last_name)

    engineer = forms.ChoiceField(choices=[(x,x) for x in list_of_engineers], initial=list_of_engineers[0])
    week_comparison_one = forms.ChoiceField(choices=[(x,x) for x in range(1,53)], initial=date.today().isocalendar()[1])
    week_comparison_two = forms.ChoiceField(choices=[(x, x) for x in range(1, 53)], initial=date.today().isocalendar()[1])
    year = forms.ChoiceField(choices=[(x, x) for x in range(2017, 2021)], initial=date.today().year)

class DropDownMonthlyBidimensionalMenuFormSecurityAudit(forms.Form):
    months = ("1", 'January'), ("2", 'February'), ("3", 'March'), ("4", 'April'), ("5", 'May'), ("6", 'June'), \
             ("7", 'July'), ("8", 'August'), ("9", 'September'), ("10", 'October'), ("11", 'November'), (
                 "12", 'December')
    list_of_categories = ("issue status","Issue Status"),("problem category","Problem Category"),\
                         ("reason for creating","Reason for Creating"), ("category","Category"), \
                         ("affected devices","Affected Devices"), ("vendor", "Vendor"), ("priority", "Priority")
    list_of_categories_y = ("issue status","Issue Status"),("problem category","Problem Category"),\
                           ("reason for creating","Reason for Creating"),("category","Category"), \
                           ("affected devices", "Affected Devices"), ("vendor", "Vendor"), ("priority","Priority")

    x_axis = forms.ChoiceField(choices=[x for x in list_of_categories], initial=list_of_categories[0])
    y_axis = forms.ChoiceField(choices=[y for y in list_of_categories_y], initial=list_of_categories_y[1])
    month  = forms.ChoiceField(choices=[x for x in months], initial=date.today().month)
    year   = forms.ChoiceField(choices=[(x, x) for x in range(2017, 2021)], initial=date.today().year)


class DropDownYearlyBidimensionalMenuFormSecurityAudit(forms.Form):
    list_of_categories = ("issue status", "Issue Status"), ("problem category", "Problem Category"), \
                         ("reason for creating", "Reason for Creating"), ("category", "Category"), \
                         ("affected devices", "Affected Devices"), ("vendor", "Vendor"), ("priority", "Priority")
    list_of_categories_y = ("issue status", "Issue Status"), ("problem category", "Problem Category"), \
                           ("reason for creating", "Reason for Creating"), ("category", "Category"), \
                           ("affected devices", "Affected Devices"), ("vendor", "Vendor"), ("priority", "Priority")

    x_axis = forms.ChoiceField(choices=[x for x in list_of_categories], initial=list_of_categories[0])
    y_axis = forms.ChoiceField(choices=[y for y in list_of_categories_y], initial=list_of_categories_y[1])
    year = forms.ChoiceField(choices=[(x, x) for x in range(2017, 2021)], initial=date.today().year)

