from django.shortcuts import render
from .forms import DropDownMenuForm, DropDownMenuFormQuantitativeQualitativeDaily, DropDownMonthlyMenuForm, \
    DropDownYearlyMenuFormSecurityAudit, DropDownMonthlyBidimensionalMenuFormSecurityAudit, DropDownYearlyBidimensionalMenuFormSecurityAudit,\
    DropDownMenuFormQuantitativeQualitativeYearly

from datetime import date, datetime, timedelta
from .models import SecurityAuditEngineer, SecurityAuditStatusTicket, SecurityAuditAffectedDevicesCategory, \
    SecurityAuditReasonForCreatingTicket, SecurityAuditProblemCategory, SecurityAuditVendor, SecurityAuditPriorityTicket,\
    SecurityAuditCategory
import json, dateutil.parser, calendar, psycopg2, operator
import numpy as np, pandas as pd


###################### declare the html views ###########################

def index(request):
    return render(request, 'web_app_navigator/header_home.html')

################################ API views ##########################


#################### Main views in Security  #################################

 ############################ Daily #####################################

# needs debugging
def tickets_quantitative_qualitative_daily(request):
    if request.method == "GET":
        template_name = 'web_app_navigator/country_A/no_results/daily/quantitative_qualitative.html'
        form = DropDownMenuFormQuantitativeQualitativeDaily()
        return render(request, template_name, {'form': form})

    elif request.method == "POST":
        template_name = 'web_app_navigator/country_A/results/daily/quantitative_qualitative.html'

        dict_lists_of_lists_data_engineers, initial_date, ending_date, year, month, day = get_rows_of_data_daily(request)

        field_to_count = "Issue_Status"

        # get list of active engineers
        list_of_engineers = get_current_engineers(dict_lists_of_lists_data_engineers)

        quantitative_value = get_quantitative_value()

        current_market = get_market()

        # create dictionary to store the count of engineers
        dict_engineer_count_lists_of_lists = {}

        # sorted quant dictionary values
        sorted_dict_engineer_count_lists_of_lists = {}

        # create dictionary to store the quality of engineers
        dictionary_quality_engineers = {}

        # sorted quality dictionary values
        sorted_dictionary_quality_engineers = {}

        # dictionary that stores the total amount of tickets per engineer by week needed for the quality measure
        total_amount_tickets_per_engineer = {}

        initial_date, ending_date = convert_date_to_datetime(initial_date, ending_date)

        list_of_categories = get_fields_ticket_status()

        # populate dictionary of count of tickets and quality with those enginers that have data in their lists
        for engineer in list_of_engineers:
            dict_engineer_count_lists_of_lists[engineer] = dict_engineer_count_lists_of_lists.get(engineer, 0)
            total_amount_tickets_per_engineer[engineer]  = total_amount_tickets_per_engineer.get(engineer, 0)
            dictionary_quality_engineers[engineer]       = dictionary_quality_engineers.get(engineer,0)

        ##################### Quantitative measure ##################################
        for index_category, value_category in enumerate(list_of_categories):
            for index_engineer, value_engineer in enumerate(dict_lists_of_lists_data_engineers):
                # if the dictionary contains data
                if dict_lists_of_lists_data_engineers[value_engineer]:
                    # I am counting the number of times a ticket with any status except Queued appears for each engineer - quant values
                    dict_engineer_count_lists_of_lists[value_engineer] = int(dict_engineer_count_lists_of_lists[value_engineer] + \
                    generic_count(dict_lists_of_lists_data_engineers[value_engineer], field_to_count,
                    value_category,initial_date, ending_date) * quantitative_value)

                    # I am counting the number of times an ticket with any status except Queued appears for each engineer - measure for the quality
                    total_amount_tickets_per_engineer[value_engineer] = total_amount_tickets_per_engineer[value_engineer] + \
                    generic_count(dict_lists_of_lists_data_engineers[value_engineer], field_to_count,value_category,
                    initial_date, ending_date)


        ##################### Quality measure ############################################
        # get the bad tickets and the count of bad tickets that were detected
        dictionary_values_to_display_table, dictionary_quality_engineers = detect_bad_tickets_quantitative_qualitative(
            dict_lists_of_lists_data_engineers, dictionary_quality_engineers)

        #print("total amount of tickets: ", total_amount_tickets_per_engineer)
        quality_results = {key: int(
            ((total_amount_tickets_per_engineer[key] - dictionary_quality_engineers.get(key, 0)) * 100) /
            total_amount_tickets_per_engineer[key]) for key in dictionary_quality_engineers.keys()}

        # dictionaries synchronization of quant and qualitative values - necessary for keys and values to be in the same order  #

        for key, value in sorted(dict_engineer_count_lists_of_lists.items()):
            sorted_dict_engineer_count_lists_of_lists[key] = value

        for key, value in sorted(quality_results.items()):
            sorted_dictionary_quality_engineers[key] = value

        # separate keys and values for the quantitative measure
        keys, values = zip(*sorted_dict_engineer_count_lists_of_lists.items())
        #print("quant values: ",keys, values)
        # patch to avoid the empty dictionaries when no data is found
        # separate keys and values for the qualitative measure
        engineer_keys, quality = verify_data_dictionary_no_sorted_charts(sorted_dictionary_quality_engineers)
        #print("quality values: ",engineer_keys, quality)


        '''Separate the incident id and the values that are contained in the dictionary which are the bad tickets.
        If the dictionary is empty which means that no bad tickets were detected then, display an empty list.'''
        if len(dictionary_values_to_display_table) != 0:
            incident_id, incident_value = zip(*dictionary_values_to_display_table.items())
        else:
            incident_value = []

        data = {
            "label_engineers": keys,
            "quantitative": values,
            "quality": quality,
            "year": year,
            "month": month,
            "day": day,
            "table_values": incident_value,
            "market": current_market,
        }

        # convert this to JSON and then to a dictionary
        my_data = {'my_data': json.dumps(data)}
        return render(request, template_name, my_data)

 ####################### Weekly ################################

# needs debugging
def tickets_quantitative_qualitative_weekly(request):
    if request.method == "GET":
        template_name = 'web_app_navigator/Country_A/no_results/weekly/quantitative_qualitative.html'
        form = DropDownMenuForm()
        return render(request, template_name, {'form': form})

    elif request.method == "POST":
        template_name = 'web_app_navigator/country_A/results/weekly/quantitative_qualitative.html'

        dict_lists_of_lists_data_engineers, initial_date, ending_date, year, week = get_rows_of_data_weekly(request)

        field_to_count = "Issue_Status"

        # get list of active engineers
        list_of_engineers = get_current_engineers(dict_lists_of_lists_data_engineers)

        quantitative_value = get_quantitative_value()

        current_market = get_market()

        # create dictionary to store the count of engineers
        dict_engineer_count_lists_of_lists = {}

        # sorted quant dictionary values
        sorted_dict_engineer_count_lists_of_lists = {}

        # create dictionary to store the quality of engineers
        dictionary_quality_engineers = {}

        # sorted quality dictionary values
        sorted_dictionary_quality_engineers = {}

        # dictionary that stores the total amount of tickets per engineer by week needed for the quality measure
        total_amount_tickets_per_engineer = {}

        initial_date, ending_date = convert_date_to_datetime(initial_date, ending_date)

        list_of_categories = get_fields_ticket_status()

        # populate dictionary of count of tickets and quality with those enginers that have data in their lists
        for engineer in list_of_engineers:
            dict_engineer_count_lists_of_lists[engineer] = dict_engineer_count_lists_of_lists.get(engineer, 0)
            total_amount_tickets_per_engineer[engineer] = total_amount_tickets_per_engineer.get(engineer, 0)
            dictionary_quality_engineers[engineer] = dictionary_quality_engineers.get(engineer, 0)

        ##################### Quantitative measure ##################################
        for index_category, value_category in enumerate(list_of_categories):
            for index_engineer, value_engineer in enumerate(dict_lists_of_lists_data_engineers):
                # if the dictionary contains data
                if dict_lists_of_lists_data_engineers[value_engineer]:
                    # I am counting the number of times a ticket with any status except Queued appears for each engineer - quant values
                    dict_engineer_count_lists_of_lists[value_engineer] = int(
                        dict_engineer_count_lists_of_lists[value_engineer] + \
                        generic_count(dict_lists_of_lists_data_engineers[value_engineer], field_to_count,
                                               value_category, initial_date, ending_date) * quantitative_value)

                    # I am counting the number of times an ticket with any status except Queued appears for each engineer - measure for the quality
                    total_amount_tickets_per_engineer[value_engineer] = total_amount_tickets_per_engineer[value_engineer] + \
                    generic_count(dict_lists_of_lists_data_engineers[value_engineer], field_to_count,value_category,initial_date, ending_date)

        ##################### Quality measure ############################################
        # get the bad tickets and the count of bad tickets that were detected
        dictionary_values_to_display_table, dictionary_quality_engineers = detect_bad_tickets_quantitative_qualitative(
            dict_lists_of_lists_data_engineers, dictionary_quality_engineers)


        quality_results = {key: int(
            ((total_amount_tickets_per_engineer[key] - dictionary_quality_engineers.get(key, 0)) * 100) /
            total_amount_tickets_per_engineer[key]) for key in dictionary_quality_engineers.keys()}

        # dictionaries synchronization of quant and qualitative values - necessary for keys and values to be in the same order  #

        for key, value in sorted(dict_engineer_count_lists_of_lists.items()):
            sorted_dict_engineer_count_lists_of_lists[key] = value

        for key, value in sorted(quality_results.items()):
            sorted_dictionary_quality_engineers[key] = value

        # separate keys and values for the quantitative measure
        keys, values = zip(*sorted_dict_engineer_count_lists_of_lists.items())

        # patch to avoid the empty dictionaries when no data is found
        # separate keys and values for the qualitative measure
        engineer_keys, quality = verify_data_dictionary_no_sorted_charts(sorted_dictionary_quality_engineers)

        '''Separate the incident id and the values that are contained in the dictionary which are the bad tickets.
        If the dictionary is empty which means that no bad tickets were detected then, display an empty list.'''
        if len(dictionary_values_to_display_table) != 0:
            incident_id, incident_value = zip(*dictionary_values_to_display_table.items())
        else:
            incident_value = []

        data = {
            "label_engineers": engineer_keys,
            "quantitative": values,
            "quality":quality,
            "year": year,
            "week": week,
            "table_values": incident_value,
            "market": current_market,
        }

        # convert this to JSON and then to a dictionary
        my_data = {'my_data': json.dumps(data)}
        return render(request, template_name, my_data)

def tickets_counting_weekly(request):
    if request.method == "GET":
        template_name = 'web_app_navigator/Country_A/no_results/weekly/tickets_counting_weekly.html'
        form = DropDownMenuForm()
        return render(request, template_name, {'form': form})

    elif request.method == "POST":
        current_market = get_market()
        dict_lists_of_lists_data_engineers, initial_date, ending_date, year, week = get_rows_of_data_weekly(request)
        # convert the dates to datetime objects
        initial_date, ending_date = convert_date_to_datetime(initial_date, ending_date)
        list_of_categories = get_fields_ticket_status()
        dictionary_count = {}
        temp_dictionary = {}

        # cleaning process
        list_of_engineers = remove_zero_values_in_dictionary_ca(dict_lists_of_lists_data_engineers)

        # show the results in the table
        values_to_display_table = get_values_table(list_of_engineers, dict_lists_of_lists_data_engineers,
                                                            initial_date, ending_date)
        list_of_days = get_label_days(initial_date)

        # variables that change
        field_to_count = "Issue_Status"
        template_name = 'web_app_navigator/Country_A/results/weekly/tickets_counting_weekly.html'

        # populate dictionary of status for creating with label and value of 0
        for category in list_of_categories:
            dictionary_count[category] = dictionary_count.get(category, [])

        # get the count of tickets per category so you can display them in graphs
        for index_category, value_category in enumerate(list_of_categories):
            for day in range(len(list_of_days)):
                temp_list = []
                for index_engineer, value_engineer in enumerate(dict_lists_of_lists_data_engineers):
                    temp_list.append(generic_count(dict_lists_of_lists_data_engineers[value_engineer],
                    field_to_count, value_category, initial_date + timedelta(days=day),initial_date + timedelta(days=day + 1)))
                dictionary_count[value_category].append(int(np.sum(temp_list)))

        # this line contains all the tickets of each engineer by category but some of these engineers have 0 tickets for all categories
        #no need to patch this line of code because there is data on the legend chart which is the days of the week
        legend_of_chart, values = zip(*dictionary_count.items())

        # transpose the list with tickets of each engineer
        transpose_list = list(map(list, zip(*values)))

        # store the sum of all the tickets for each day
        for index, value in enumerate(list_of_days):
            temp_dictionary[index] = int(np.sum(transpose_list[index]))

        #no need to patch this line of code with verify_data_dictionary() because there is data on the days variable
        days, values_in_days = zip(*temp_dictionary.items())

        data = {
            "labels": list_of_days,
            "label_values": values_in_days,
            "year": year,
            "week": week,
            "table_values": values_to_display_table,
            "market": current_market,
        }

        my_data = {'my_data': json.dumps(data)}
        return render(request, template_name, my_data)

def tickets_status_weekly(request):
    if request.method == "GET":
        template_name = 'web_app_navigator/Country_A/no_results/weekly/tickets_status.html'
        form = DropDownMenuForm()
        return render(request, template_name, {'form': form})

    elif request.method == "POST":
        # variables that do NOT change
        current_market = get_market()
        dict_lists_of_lists_data_engineers, initial_date, ending_date, year, week = get_rows_of_data_weekly(request)
        # create dictionary to store the count of categories
        dict_category_lists_of_lists = {}
        # convert the dates to datetime objects
        initial_date, ending_date = convert_date_to_datetime(initial_date, ending_date)

        # cleaning process
        list_of_engineers = remove_zero_values_in_dictionary_ca(dict_lists_of_lists_data_engineers)

        # values to display in table
        values_to_display_table = get_values_table(list_of_engineers, dict_lists_of_lists_data_engineers,
                                                            initial_date, ending_date)

        # variables that change
        field_to_count = "Issue_Status"
        template_name = 'web_app_navigator/Country_A/results/weekly/tickets_status.html'
        # get list of categories
        list_of_categories = get_fields_ticket_status()

        # populate dictionary of status for creating with label and value of 0
        for category in list_of_categories:
            dict_category_lists_of_lists[category] = dict_category_lists_of_lists.get(category, 0)

        # get the count of tickets per category so you can display them in graphs
        for index_category, value_category in enumerate(list_of_categories):
            for index_engineer, value_engineer in enumerate(dict_lists_of_lists_data_engineers):
                dict_category_lists_of_lists[value_category] = dict_category_lists_of_lists[value_category] + \
                generic_count(dict_lists_of_lists_data_engineers[value_engineer], field_to_count, value_category,
                initial_date, ending_date)

        # clean the dictionary to remove the zero values
        temp_dict = remove_zero_values_in_dictionary_ca(dict_category_lists_of_lists)

        # sort the dictionary from the biggest to smallest number
        # this line of code was patched with verify_data_dictionary()
        keys, values = verify_data_dictionary_sorted_charts(temp_dict)

        data = {
            "labels": keys,
            "label_values": values,
            "year": year,
            "week": week,
            "table_values": values_to_display_table,
            "market": current_market
        }

        # convert this to JSON and then to a dictionary
        my_data = {'my_data': json.dumps(data)}
        return render(request, template_name, my_data)

def tickets_affected_devices_weekly(request):
    if request.method == "GET":
        template_name = 'web_app_navigator/Country_A/no_results/weekly/tickets_affected_devices.html'
        form = DropDownMenuForm()
        return render(request, template_name, {'form': form})
    elif request.method == "POST":
        ########### variables that do NOT change
        current_market = get_market()
        dict_lists_of_lists_data_engineers, initial_date, ending_date, year, week = get_rows_of_data_weekly(request)
        # create dictionary to store the count of categories
        dict_category_lists_of_lists = {}
        # convert the dates to date objects
        initial_date, ending_date = convert_date_to_datetime(initial_date, ending_date)

        # cleaning process
        list_of_engineers = remove_zero_values_in_dictionary_ca(dict_lists_of_lists_data_engineers)

        # display the values in the table
        values_to_display_table = get_values_table(list_of_engineers, dict_lists_of_lists_data_engineers,
                                                            initial_date, ending_date)

        ########### variables that change
        field_to_count = 'Affected_Devices'
        template_name = 'web_app_navigator/Country_A/results/weekly/tickets_affected_devices.html'
        # get list of categories
        list_of_categories = get_fields_affected_devices()

        # populate dictionary of reason for creating with label and value of 0
        for category in list_of_categories:
            dict_category_lists_of_lists[category] = dict_category_lists_of_lists.get(category, 0)

        # get the count of tickets per category so you can display them in graphs
        for index_category, value_category in enumerate(list_of_categories):
            for index_engineer, value_engineer in enumerate(dict_lists_of_lists_data_engineers):
                dict_category_lists_of_lists[value_category] = dict_category_lists_of_lists[value_category] + generic_count \
                (dict_lists_of_lists_data_engineers[value_engineer], field_to_count, value_category, initial_date,ending_date)

        # clean the dictionary to remove the zero values
        temp_dict = remove_zero_values_in_dictionary_ca(dict_category_lists_of_lists)

        # sort the dictionary from the biggest to smallest number
        # this line of code was patched with verify_data_dictionary()
        keys, values = verify_data_dictionary_sorted_charts(temp_dict)

        data = {
            "labels": keys,
            "label_values": values,
            "year": year,
            "week": week,
            "table_values": values_to_display_table,
            "market": current_market
        }

        # convert this to JSON and then to a dictionary
        my_data = {'my_data': json.dumps(data)}
        return render(request, template_name, my_data)

def tickets_problem_category_weekly(request):
    if request.method == "GET":
        template_name = 'web_app_navigator/Country_A/no_results/weekly/tickets_problem_category.html'
        form = DropDownMenuForm()
        return render(request, template_name, {'form': form})
    elif request.method == "POST":
        ########### variables that do NOT change
        current_market = get_market()
        dictionary_data_of_engineers, initial_date, ending_date, year, week = get_rows_of_data_weekly(request)
        # create dictionary to store the count of categories
        dict_category_lists_of_lists = {}
        # convert the dates to date objects
        initial_date, ending_date = convert_date_to_datetime(initial_date, ending_date)

        # cleaning process
        list_of_engineers = remove_zero_values_in_dictionary_ca(dictionary_data_of_engineers)

        # display the values in the table
        values_to_display_table = get_values_table(list_of_engineers, dictionary_data_of_engineers,
                                                            initial_date, ending_date)

        ########### variables that change
        field_to_count = 'Problem_Category'
        template_name = 'web_app_navigator/Country_A/results/weekly/tickets_problem_category.html'
        # get list of categories
        list_of_categories = get_fields_problem_category()

        # populate dictionary of reason for creating with label and value of 0
        for category in list_of_categories:
            dict_category_lists_of_lists[category] = dict_category_lists_of_lists.get(category, 0)

        # get the count of tickets per category so you can display them in graphs
        for index_category, value_category in enumerate(list_of_categories):
            for index_engineer, value_engineer in enumerate(dictionary_data_of_engineers):
                dict_category_lists_of_lists[value_category] = dict_category_lists_of_lists[value_category] + \
                generic_count(dictionary_data_of_engineers[value_engineer], field_to_count, value_category,
                initial_date, ending_date)

        # clean the dictionary to remove the zero values
        temp_dict = remove_zero_values_in_dictionary_ca(dict_category_lists_of_lists)

        # sort the dictionary from the biggest to smallest number
        # this line of code was patched with verify_data_dictionary()
        keys, values = verify_data_dictionary_sorted_charts(temp_dict)

        data = {
            "labels": keys,
            "label_values": values,
            "year": year,
            "week": week,
            "table_values": values_to_display_table,
            "market": current_market
        }

        # convert this to JSON and then to a dictionary
        my_data = {'my_data': json.dumps(data)}
        return render(request, template_name, my_data)

def tickets_reason_for_creating_weekly(request):
    if request.method == "GET":
        template_name = 'web_app_navigator/Country_A/no_results/weekly/tickets_reason_for_creating.html'
        form = DropDownMenuForm()
        return render(request, template_name, {'form': form})

    elif request.method == "POST":
        ########### variables that do NOT change
        current_market = get_market()
        dict_lists_of_lists_data_engineers, initial_date, ending_date, year, week = get_rows_of_data_weekly(request)
        # create dictionary to store the count of categories

        ######### processing ##############
        dict_category_lists_of_lists = {}
        # convert the dates to date objects
        initial_date, ending_date = convert_date_to_datetime(initial_date, ending_date)

        # cleaning process
        list_of_engineers = remove_zero_values_in_dictionary_ca(dict_lists_of_lists_data_engineers)

        # extract these fields so you can display them in the tables
        values_to_display_table = get_values_table(list_of_engineers, dict_lists_of_lists_data_engineers,
                                                            initial_date, ending_date)

        ########### variables that change
        field_to_count = 'Reason_for_Creating'
        template_name = 'web_app_navigator/Country_A/results/weekly/tickets_reason_for_creating.html'
        # get list of categories
        list_of_categories = get_fields_reason_for_creating()

        # populate dictionary of reason for creating with label and value of 0
        for category in list_of_categories:
            dict_category_lists_of_lists[category] = dict_category_lists_of_lists.get(category, 0)

        # get the count of tickets per category so you can display them in graphs
        for index_category, value_category in enumerate(list_of_categories):
            for index_engineer, value_engineer in enumerate(dict_lists_of_lists_data_engineers):
                dict_category_lists_of_lists[value_category] = dict_category_lists_of_lists[value_category] + \
                generic_count(dict_lists_of_lists_data_engineers[value_engineer], field_to_count,
                value_category, initial_date, ending_date)

        # clean the dictionary to remove the zero values
        temp_dict = remove_zero_values_in_dictionary_ca(dict_category_lists_of_lists)

        # sort the dictionary from the biggest to smallest number
        # this line of code was patched with verify_data_dictionary()
        keys, values = verify_data_dictionary_sorted_charts(temp_dict)

        data = {
            "labels": keys,
            "label_values": values,
            "year": year,
            "week": week,
            "table_values": values_to_display_table,
            "market": current_market
        }

        # convert this to JSON and then to a dictionary
        my_data = {'my_data': json.dumps(data)}
        return render(request, template_name, my_data)


####################### Monthly ################################

def tickets_affected_devices_monthly(request):
    if request.method == "GET":
        template_name = 'web_app_navigator/Country_A/no_results/monthly/tickets_affected_devices.html'
        form = DropDownMonthlyMenuForm()
        return render(request, template_name, {'form': form})
    elif request.method == "POST":
        ########### variables that do NOT change
        current_market = get_market()
        dict_lists_of_lists_data_engineers, initial_date, ending_date, year, month = get_rows_of_data_monthly(request)
        # create dictionary to store the count of categories
        dict_category_lists_of_lists = {}
        # convert the dates to date objects
        initial_date, ending_date = convert_date_to_datetime_monthly_yearly(initial_date, ending_date)

        # cleaning process
        list_of_engineers = remove_zero_values_in_dictionary_ca(dict_lists_of_lists_data_engineers)

        # show the values in the graphs
        values_to_display_table = get_values_table(list_of_engineers, dict_lists_of_lists_data_engineers,
                                                            initial_date, ending_date)

        ########### variables that change
        field_to_count = 'Affected_Devices'
        template_name = 'web_app_navigator/Country_A/results/monthly/tickets_affected_devices.html'
        # get list of categories
        list_of_categories = get_fields_affected_devices()

        # populate dictionary of reason for creating with label and value of 0
        for category in list_of_categories:
            dict_category_lists_of_lists[category] = dict_category_lists_of_lists.get(category, 0)

        # get the count of tickets per category so you can display them in graphs
        for index_category, value_category in enumerate(list_of_categories):
            for index_engineer, value_engineer in enumerate(dict_lists_of_lists_data_engineers):
                dict_category_lists_of_lists[value_category] = dict_category_lists_of_lists[value_category] + \
                generic_count(dict_lists_of_lists_data_engineers[value_engineer], field_to_count, value_category,
                initial_date, ending_date)

        # clean the dictionary to remove the zero values
        temp_dict = remove_zero_values_in_dictionary_ca(dict_category_lists_of_lists)

        # sort the dictionary from the biggest to smallest number
        # this line of code was patched with verify_data_dictionary()
        keys, values = verify_data_dictionary_sorted_charts(temp_dict)

        data = {
            "labels": keys,
            "label_values": values,
            "year": year,
            "month": month,
            "table_values": values_to_display_table,
            "market": current_market
        }

        # convert this to JSON and then to a dictionary
        my_data = {'my_data': json.dumps(data)}
        return render(request, template_name, my_data)

def tickets_problem_category_monthly(request):
    if request.method == "GET":
        template_name = 'web_app_navigator/Country_A/no_results/monthly/tickets_problem_category.html'
        form = DropDownMonthlyMenuForm()
        return render(request, template_name, {'form': form})

    elif request.method == "POST":
        ########### variables that do NOT change
        current_market = get_market()
        dict_lists_of_lists_data_engineers, initial_date, ending_date, year, month = get_rows_of_data_monthly(request)
        # create dictionary to store the count of categories
        dict_category_lists_of_lists = {}
        # convert the dates to date objects
        initial_date, ending_date = convert_date_to_datetime_monthly_yearly(initial_date, ending_date)

        # cleaning process
        list_of_engineers = remove_zero_values_in_dictionary_ca(dict_lists_of_lists_data_engineers)

        # display values in table
        values_to_display_table = get_values_table(list_of_engineers, dict_lists_of_lists_data_engineers,
                                                            initial_date, ending_date)

        ########### variables that change
        field_to_count = 'Problem_Category'
        template_name = 'web_app_navigator/Country_A/results/monthly/tickets_problem_category.html'
        # get list of categories
        list_of_categories = get_fields_problem_category()

        # populate dictionary of reason for creating with label and value of 0
        for category in list_of_categories:
            dict_category_lists_of_lists[category] = dict_category_lists_of_lists.get(category, 0)

        # get the count of tickets per category so you can display them in graphs
        for index_category, value_category in enumerate(list_of_categories):
            for index_engineer, value_engineer in enumerate(dict_lists_of_lists_data_engineers):
                dict_category_lists_of_lists[value_category] = dict_category_lists_of_lists[value_category] + generic_count \
                    (dict_lists_of_lists_data_engineers[value_engineer], field_to_count, value_category, initial_date,
                     ending_date)

        # clean the dictionary to remove the zero values
        temp_dict = remove_zero_values_in_dictionary_ca(dict_category_lists_of_lists)

        # sort the dictionary from the biggest to smallest number
        # this line of code was patched with verify_data_dictionary()
        keys, values = verify_data_dictionary_sorted_charts(temp_dict)

        data = {
            "labels": keys,
            "label_values": values,
            "year": year,
            "month": month,
            "table_values": values_to_display_table,
            "market": current_market
        }

        # convert this to JSON and then to a dictionary
        my_data = {'my_data': json.dumps(data)}
        return render(request, template_name, my_data)

def tickets_reason_for_creating_monthly(request):
    if request.method == "GET":
        template_name = 'web_app_navigator/Country_A/no_results/monthly/tickets_reason_for_creating.html'
        form = DropDownMonthlyMenuForm()
        return render(request, template_name, {'form': form})

    elif request.method == "POST":
        ########### variables that do NOT change
        current_market = get_market()
        dict_lists_of_lists_data_engineers, initial_date, ending_date, year, month = get_rows_of_data_monthly(request)
        # create dictionary to store the count of categories
        dict_category_lists_of_lists = {}
        # convert the dates to date objects
        initial_date, ending_date = convert_date_to_datetime_monthly_yearly(initial_date, ending_date)

        # cleaning process
        list_of_engineers = remove_zero_values_in_dictionary_ca(dict_lists_of_lists_data_engineers)

        # display values in table
        values_to_display_table = get_values_table(list_of_engineers, dict_lists_of_lists_data_engineers,
                                                            initial_date, ending_date)

        ########### variables that change
        field_to_count = 'Reason_for_Creating'
        template_name = 'web_app_navigator/Country_A/results/monthly/tickets_reason_for_creating.html'
        # get list of categories
        list_of_categories = get_fields_reason_for_creating()

        # populate dictionary of reason for creating with label and value of 0
        for category in list_of_categories:
            dict_category_lists_of_lists[category] = dict_category_lists_of_lists.get(category, 0)

        # get the count of tickets per category so you can display them in graphs
        for index_category, value_category in enumerate(list_of_categories):
            for index_engineer, value_engineer in enumerate(dict_lists_of_lists_data_engineers):
                dict_category_lists_of_lists[value_category] = dict_category_lists_of_lists[value_category] + generic_count \
                (dict_lists_of_lists_data_engineers[value_engineer], field_to_count, value_category, initial_date,
                ending_date)

        # clean the dictionary to remove the zero values
        temp_dict = remove_zero_values_in_dictionary_ca(dict_category_lists_of_lists)

        # sort the dictionary from the biggest to smallest number
        # this line of code was patched with verify_data_dictionary()
        keys, values = verify_data_dictionary_sorted_charts(temp_dict)

        data = {
            "labels": keys,
            "label_values": values,
            "year": year,
            "month": month,
            "table_values": values_to_display_table,
            "market": current_market
        }

        # convert this to JSON and then to a dictionary
        my_data = {'my_data': json.dumps(data)}
        return render(request, template_name, my_data)

# needs debugging
def tickets_bidimensional_analysis_monthly(request):
    if request.method == "GET":
        template_name = 'web_app_navigator/Country_A/no_results/monthly/tickets_bidimensional_analysis.html'
        form = DropDownMonthlyBidimensionalMenuFormSecurityAudit()
        return render(request, template_name, {'form': form})

    elif request.method == "POST":
        # declare the variables that will not change in the different views
        current_market = get_market()
        list_of_engineers = get_all_engineers()
        main_dictionary = {}
        # variables that change in the rest of the views
        template_name = 'web_app_navigator/Country_A/results/monthly/tickets_bidimensional_analysis.html'

        x_axis = str(request.POST.get('select_x_axis', None))
        y_axis = str(request.POST.get('select_y_axis', None))

        # retrieval of data
        dict_lists_of_lists_data_engineers, initial_date, ending_date, year, month = get_rows_of_data_monthly(request)
        initial_date, ending_date = convert_date_to_datetime_monthly_yearly(initial_date, ending_date)

        # x retrieval values
        if x_axis == "issue status":
            x_categories_list = get_fields_ticket_status()

        elif x_axis == "reason for creating":
            x_categories_list = get_fields_reason_for_creating()

        elif x_axis == "priority":
            x_categories_list = get_fields_priority()

        elif x_axis == "problem category":
            x_categories_list = get_fields_problem_category()

        elif x_axis == "affected devices":
            x_categories_list = get_fields_affected_devices()

        elif x_axis == "category":
            x_categories_list = get_fields_category()

        elif x_axis == "vendor":
            x_categories_list = get_fields_vendors()

        elif x_axis == "engineer":
            x_categories_list = get_all_engineers()

        else:
            x_categories_list = ""

        # y retrieval values
        if y_axis == "issue status":
            y_categories_list = get_fields_ticket_status()

        elif y_axis == "reason for creating":
            y_categories_list = get_fields_reason_for_creating()

        elif y_axis == "problem category":
            y_categories_list = get_fields_problem_category()

        elif y_axis == "priority":
            y_categories_list = get_fields_priority()

        elif y_axis == "affected devices":
            y_categories_list = get_fields_affected_devices()

        elif y_axis == "category":
            y_categories_list = get_fields_category()

        elif y_axis == "vendor":
            y_categories_list = get_fields_vendors()

        elif y_axis == "engineer":
            y_categories_list = get_all_engineers()

        else:
            y_categories_list = ""

        for value in y_categories_list:
            main_dictionary[value] = main_dictionary.get(value, [])

        # x axis
        for category in range(len(x_categories_list)):
            for index, y_category in enumerate(y_categories_list):
                temp_list = []
                for index_engineer, value_engineer in enumerate(dict_lists_of_lists_data_engineers):
                    temp_list.append(
                        generic_count_bidimensional(dict_lists_of_lists_data_engineers[value_engineer],
                        initial_date, ending_date, x_axis, x_categories_list[category], y_axis, y_category))
                main_dictionary[y_category].append(int(np.sum(temp_list)))

        # give the highest value in the Y axis based on the sum of items
        # no need to patch this line of code because it will always contain data
        legend_of_chart, values = zip(*sorted(main_dictionary.items(), key=lambda x: sum(x[1]), reverse=True))

        #display values of table
        values_to_display_table = get_values_table(list_of_engineers, dict_lists_of_lists_data_engineers,
                                                            initial_date, ending_date)
        data = {
            "labels": x_categories_list,
            "label_values": values,
            "legend": legend_of_chart,
            "year": year,
            "month": month,
            "table_values": values_to_display_table,
            "market": current_market,
            "x_axis": x_axis,
            "y_axis": y_axis
        }

        # convert the data to json
        my_data = {'my_data': json.dumps(data)}
        return render(request, template_name, my_data)


####################### Yearly ################################

def tickets_affected_devices_yearly(request):
    if request.method == "GET":
        template_name = 'web_app_navigator/Country_A/no_results/yearly/tickets_affected_devices.html'
        form = DropDownYearlyMenuFormSecurityAudit()
        return render(request, template_name, {'form': form})
    elif request.method == "POST":
        ########### variables that do NOT change
        current_market = get_market()
        dict_lists_of_lists_data_engineers, initial_date, ending_date, year = get_rows_of_data_yearly(request)
        # create dictionary to store the count of categories
        dict_category_lists_of_lists = {}
        # convert the dates to date objects
        initial_date, ending_date = convert_date_to_datetime_monthly_yearly(initial_date, ending_date)

        # cleaning process
        list_of_engineers = remove_zero_values_in_dictionary_ca(dict_lists_of_lists_data_engineers)

        # display results in the table
        values_to_display_table = get_values_table(list_of_engineers, dict_lists_of_lists_data_engineers,
                                                            initial_date, ending_date)

        ########### variables that change
        field_to_count = 'Affected_Devices'
        template_name = 'web_app_navigator/Country_A/results/yearly/tickets_affected_devices.html'
        # get list of categories
        list_of_categories = get_fields_affected_devices()

        # populate dictionary of reason for creating with label and value of 0
        for category in list_of_categories:
            dict_category_lists_of_lists[category] = dict_category_lists_of_lists.get(category, 0)

        # get the count of tickets per category so you can display them in graphs
        for index_category, value_category in enumerate(list_of_categories):
            for index_engineer, value_engineer in enumerate(dict_lists_of_lists_data_engineers):
                dict_category_lists_of_lists[value_category] = dict_category_lists_of_lists[value_category] + generic_count \
                (dict_lists_of_lists_data_engineers[value_engineer], field_to_count, value_category, initial_date,ending_date)

        # clean the dictionary to remove the zero values
        temp_dict = remove_zero_values_in_dictionary_ca(dict_category_lists_of_lists)

        # sort the dictionary from the biggest to smallest number
        # this line of code was patched with verify_data_dictionary()
        keys, values = verify_data_dictionary_sorted_charts(temp_dict)

        data = {
            "labels": keys,
            "label_values": values,
            "year": year,
            "table_values": values_to_display_table,
            "market": current_market
        }

        # convert this to JSON and then to a dictionary
        my_data = {'my_data': json.dumps(data)}
        return render(request, template_name, my_data)

def tickets_problem_category_yearly(request):
    if request.method == "GET":
        template_name = 'web_app_navigator/Country_A/no_results/yearly/tickets_problem_category.html'
        #we start from year 2017 to 2021
        form = DropDownYearlyMenuFormSecurityAudit()
        return render(request, template_name, {'form': form})

    elif request.method == "POST":
        ########### variables that do NOT change
        current_market = get_market()
        dict_lists_of_lists_data_engineers, initial_date, ending_date, year = get_rows_of_data_yearly(request)
        # create dictionary to store the count of categories
        dict_category_lists_of_lists = {}
        # convert the dates to date objects
        initial_date, ending_date = convert_date_to_datetime_monthly_yearly(initial_date, ending_date)

        # cleaning process
        list_of_engineers = remove_zero_values_in_dictionary_ca(dict_lists_of_lists_data_engineers)

        # display the values in the table
        values_to_display_table = get_values_table(list_of_engineers, dict_lists_of_lists_data_engineers,
                                                            initial_date, ending_date)

        ########### variables that change
        field_to_count = 'Problem_Category'
        template_name = 'web_app_navigator/Country_A/results/yearly/tickets_problem_category.html'
        # get list of categories
        list_of_categories = get_fields_problem_category()

        # populate dictionary of reason for creating with label and value of 0
        for category in list_of_categories:
            dict_category_lists_of_lists[category] = dict_category_lists_of_lists.get(category, 0)


        # get the count of tickets per category so you can display them in graphs
        for index_category, value_category in enumerate(list_of_categories):
            for index_engineer, value_engineer in enumerate(dict_lists_of_lists_data_engineers):
                dict_category_lists_of_lists[value_category] = dict_category_lists_of_lists[value_category] + generic_count \
                (dict_lists_of_lists_data_engineers[value_engineer], field_to_count, value_category, initial_date, ending_date)

        # clean the dictionary to remove the zero values
        temp_dict = remove_zero_values_in_dictionary_ca(dict_category_lists_of_lists)

        # sort the dictionary from the biggest to smallest number
        # this line of code was patched with verify_data_dictionary()
        keys, values = verify_data_dictionary_sorted_charts(temp_dict)


        data = {
            "labels": keys,
            "label_values": values,
            "year": year,
            "table_values": values_to_display_table,
            "market": current_market
        }

        # convert this to JSON and then to a dictionary
        my_data = {'my_data': json.dumps(data)}
        return render(request, template_name, my_data)

def tickets_reason_for_creating_yearly(request):
    if request.method == "GET":
        template_name = 'web_app_navigator/Country_A/no_results/yearly/tickets_reason_for_creating.html'
        form = DropDownYearlyMenuFormSecurityAudit()
        return render(request, template_name, {'form': form})

    elif request.method == "POST":
        ########### variables that do NOT change
        current_market = get_market()
        dict_lists_of_lists_data_engineers, initial_date, ending_date, year = get_rows_of_data_yearly(request)
        # create dictionary to store the count of categories
        dict_category_lists_of_lists = {}
        # convert the dates to date objects
        initial_date, ending_date = convert_date_to_datetime_monthly_yearly(initial_date, ending_date)

        # cleaning process
        list_of_engineers = remove_zero_values_in_dictionary_ca(dict_lists_of_lists_data_engineers)

        # display values in table
        values_to_display_table = get_values_table(list_of_engineers, dict_lists_of_lists_data_engineers,
                                                            initial_date, ending_date)

        ########### variables that change
        field_to_count = 'Reason_for_Creating'
        template_name = 'web_app_navigator/Country_A/results/yearly/tickets_reason_for_creating.html'
        # get list of categories
        list_of_categories = get_fields_reason_for_creating()

        # populate dictionary of reason for creating with label and value of 0
        for category in list_of_categories:
            dict_category_lists_of_lists[category] = dict_category_lists_of_lists.get(category, 0)

        # get the count of tickets per category so you can display them in graphs
        for index_category, value_category in enumerate(list_of_categories):
            for index_engineer, value_engineer in enumerate(dict_lists_of_lists_data_engineers):
                dict_category_lists_of_lists[value_category] = dict_category_lists_of_lists[value_category] + generic_count \
                    (dict_lists_of_lists_data_engineers[value_engineer], field_to_count, value_category, initial_date,
                     ending_date)

        # clean the dictionary to remove the zero values
        temp_dict = remove_zero_values_in_dictionary_ca(dict_category_lists_of_lists)

        # sort the dictionary from the biggest to smallest number
        # this line of code was patched with verify_data_dictionary()
        keys, values = verify_data_dictionary_sorted_charts(temp_dict)

        data = {
            "labels": keys,
            "label_values": values,
            "year": year,
            "table_values": values_to_display_table,
            "market": current_market
        }

        # convert this to JSON and then to a dictionary
        my_data = {'my_data': json.dumps(data)}
        return render(request, template_name, my_data)

# needs debugging
def tickets_quantitative_qualitative_per_engineer_yearly(request):
    if request.method == "GET":
        template_name = 'web_app_navigator/Country_A/no_results/yearly/quantitative_qualitative.html'
        form = DropDownMenuFormQuantitativeQualitativeYearly()
        return render(request, template_name, {'form': form})

    elif request.method == "POST":
        template_name = 'web_app_navigator/Country_A/results/yearly/quantitative_qualitative.html'
        number_of_days = get_current_days_of_week()
        dictionary_data_of_engineers, engineer, initial_date, ending_date, year, list_of_weeks = \
            get_rows_of_data_quantitative_qualitative_yearly(request)

        dictionary_quality = {}

        field_to_count = "Issue_Status"

        initial_date, ending_date = convert_date_to_datetime_monthly_yearly(initial_date, ending_date)

        list_of_categories = get_fields_ticket_status()

        #create dictionary to store the quality for each week
        for week in list_of_weeks:
            dictionary_quality[week] = dictionary_quality.get(week, 0)

        quantitative_value = get_quantitative_value()

        # populate dictionary of count of tickets
        dictionary_count_engineer   = {engineer: []}

        # get the tickets for each week to get the quant values
        while (initial_date<ending_date):
            #initialize the week(s)
            current_date = initial_date
            tomorrow = initial_date + timedelta(days=1)
            count_of_tickets = 0
            #get the tickets by engineer per day, starting day is Sunday and ending day is Saturday
            for index_category, value_category in enumerate(list_of_categories):
                for day in range(number_of_days):
                    count_of_tickets = count_of_tickets + generic_count(dictionary_data_of_engineers[engineer],
                                       field_to_count, value_category, current_date, tomorrow)
                    # go on to the next day
                    current_date = tomorrow
                    tomorrow = tomorrow + timedelta(days=1)
                current_date = initial_date
                tomorrow = initial_date + timedelta(days=1)
            # store the count of weekly tickets and get the quantitative measure
            dictionary_count_engineer[engineer].append(count_of_tickets)
            #go on to the next week
            initial_date = initial_date + timedelta(days=7)

        ################## Quant values #######################

        list_quant_values_per_week = []
        list_total_amount_tickets  = []
        counter_values = []
        for value in dictionary_count_engineer[engineer]:
            list_quant_values_per_week.append(int(value * quantitative_value))
            #patch 1: avoid the division by zero error
            if value == 0:
                #if there is a zero value then replace it by 1
                list_total_amount_tickets.append(1)
                #patch 2: fix the problem with the 100 quality value, that is, when no tickets are detected then add 0
                counter_values.append(0)
            else:
                #if there is not a zero value then get the value
                list_total_amount_tickets.append(value)
                # patch 2: fix the problem with the 100 quality value, that is, when tickets are detected then add 1
                counter_values.append(1)

        total_amount_tickets_per_engineer = dict(zip(list_of_weeks, list_total_amount_tickets))
        #counter_values_dict = sorted(dict(zip(list_of_weeks, counter_values)).items(), key=operator.itemgetter(0), reverse=True)
        counter_values_dict = dict(zip(list_of_weeks, counter_values))

        ##################### Quality measure ############################################
        # get the bad tickets and the count of bad tickets that were detected

        values_to_display_table, dictionary_quality_engineers = detect_bad_tickets_quantitative_qualitative_yearly(
            dictionary_data_of_engineers, dictionary_quality, engineer, year)

        '''we multiply by a counter value given the week number as the key, if no tickets were detected in a 
        given week then multiply the result by 0 but if tickets were detected then multiply the result by 1'''
        quality_results = {int(key): int((((total_amount_tickets_per_engineer[key] - dictionary_quality_engineers.get(key, 0)) * 100) /
              total_amount_tickets_per_engineer[key]) * counter_values_dict[key]) for key in dictionary_quality_engineers.keys()}


        '''Separate the incident id and the values that are contained in the dictionary which are the bad tickets.
        If the dictionary is empty which means that no bad tickets were detected then, display an empty list.'''
        # separate keys and values for the qualitative measure
        engineer_keys, quality = zip(*sorted(quality_results.items(), key=operator.itemgetter(0), reverse=False))


        data = {
            "label_engineers": list_of_weeks,
            "quantitative": list_quant_values_per_week,
            "quality": quality,
            "engineer": engineer,
            "year": year,
            "table_values": values_to_display_table,
        }

        # convert this to JSON and then to a dictionary
        my_data = {'my_data': json.dumps(data)}
        return render(request, template_name, my_data)

# needs debugging
def tickets_bidimensional_analysis_yearly(request):
    if request.method == "GET":
        template_name = 'web_app_navigator/Country_A/no_results/yearly/tickets_bidimensional_analysis.html'
        form = DropDownYearlyBidimensionalMenuFormSecurityAudit()
        return render(request, template_name, {'form': form})

    elif request.method == "POST":
        # declare the variables that will not change in the different views
        current_market = get_market()
        list_of_engineers = get_all_engineers()
        main_dictionary = {}
        # variables that change in the rest of the views
        template_name = 'web_app_navigator/Country_A/results/yearly/tickets_bidimensional_analysis.html'

        x_axis = str(request.POST.get('select_x_axis', None))
        y_axis = str(request.POST.get('select_y_axis', None))

        # retrieval of data
        dictionary_data_of_engineers, initial_date, ending_date, year = get_rows_of_data_yearly(request)
        initial_date, ending_date = convert_date_to_datetime_monthly_yearly(initial_date, ending_date)

        # x retrieval values
        if x_axis == "issue status":
            x_categories_list = get_fields_ticket_status()

        elif x_axis == "reason for creating":
            x_categories_list = get_fields_reason_for_creating()

        elif x_axis == "priority":
            x_categories_list = get_fields_priority()

        elif x_axis == "problem category":
            x_categories_list = get_fields_problem_category()

        elif x_axis == "affected devices":
            x_categories_list = get_fields_affected_devices()

        elif x_axis == "category":
            x_categories_list = get_fields_category()

        elif x_axis == "vendor":
            x_categories_list = get_fields_vendors()

        elif x_axis == "engineer":
            x_categories_list = get_all_engineers()

        else:
            x_categories_list = ""

        # y retrieval values
        if y_axis == "issue status":
            y_categories_list = get_fields_ticket_status()

        elif y_axis == "reason for creating":
            y_categories_list = get_fields_reason_for_creating()

        elif y_axis == "problem category":
            y_categories_list = get_fields_problem_category()

        elif y_axis == "priority":
            y_categories_list = get_fields_priority()

        elif y_axis == "affected devices":
            y_categories_list = get_fields_affected_devices()

        elif y_axis == "category":
            y_categories_list = get_fields_category()

        elif y_axis == "vendor":
            y_categories_list = get_fields_vendors()

        elif y_axis == "engineer":
            y_categories_list = get_all_engineers()

        else:
            y_categories_list = ""


        for value in y_categories_list:
            main_dictionary[value] = main_dictionary.get(value, [])

        # x axis
        for category in range(len(x_categories_list)):
            for index, y_category in enumerate(y_categories_list):
                temp_list = []
                for index_engineer, value_engineer in enumerate(dictionary_data_of_engineers):
                    temp_list.append(generic_count_bidimensional(dictionary_data_of_engineers[value_engineer],
                    initial_date,ending_date, x_axis,x_categories_list[category],y_axis, y_category))
                main_dictionary[y_category].append(int(np.sum(temp_list)))

        # give the highest value in the Y axis based on the sum of items
        legend_of_chart, values = zip(*sorted(main_dictionary.items(), key=lambda x: sum(x[1]), reverse=True))

        values_to_display_table = get_values_table(list_of_engineers, dictionary_data_of_engineers,
                                                            initial_date, ending_date)
        data = {
            "labels": x_categories_list,
            "label_values": values,
            "legend": legend_of_chart,
            "year": year,
            "table_values": values_to_display_table,
            "market": current_market,
            "x_axis": x_axis,
            "y_axis": y_axis
        }

        # convert the data to json
        my_data = {'my_data': json.dumps(data)}
        return render(request, template_name, my_data)


############ main methods that are used for counting and bad tickets detection #########################

# working correctly but the only problem seems to be with the tickets with the same id, they won't appear
# because they are not attached to a list
def detect_bad_tickets_quantitative_qualitative(dictionary_data_of_engineers, dictionary_quality_engineers):
    dictionary_reason_bad_ticket = {}

    ''''{"Id": [], 0
        "Vendor": [], 1
    "Category": [], 2
    "Problem_Category": [], 3
    "Initial_Detection": [], 4
    "Last_Day_Track": [], 5
    "Issue_Closed_Date": [], 6
    "Action_Date": [], 7
    "Affected_Devices": [], 8
    "Security_Engineer": [], 9
    "Reason_For_Creating": [], 10
    "SLA_MET": [], 11
    "Issue_Status": [], 12
    "Issue_Re_Assigned_Date": [], 13
    "Priority": [], 14
    "KPI_I": [], 15 24
    "KPI_II": [], 16 25
    "KPI_III": [], 17 26
    "KPI_IV": [] 18 27}
    
    '''

    for engineer, engineer_list in dictionary_data_of_engineers.items():
        for element in engineer_list:
            if element[12] ==  "Transferred" or element[12] == "Closed" or element[12] == "In Progress":
                if element[12] == "Closed":
                    if element[15] != "None":
                        try:
                            if int(element[15]) < 0 or int(element[15]) > 48:
                                #print(engineer, "rule 5")
                                #print(element[0])
                                dictionary_quality_engineers[engineer] = dictionary_quality_engineers[engineer] + 1
                                dictionary_reason_bad_ticket[element[0]] = (element[0],"KPI_I value was either lower than 0 or greater than 48",
                                element[9], element[7],element[12], element[2], element[6], element[13],element[14], element[15],
                                element[16],element[17], element[18])
                        except ValueError:
                            pass

                    if element[16] != "None":
                        try:
                            if int(element[16]) < 0 or int(element[16]) > 48:
                                #print(engineer, " entered rule 6")
                                #print(element[0])
                                dictionary_quality_engineers[engineer] = dictionary_quality_engineers[engineer] + 1
                                dictionary_reason_bad_ticket[element[0]] = (element[0], "KPI_II value was either lower than 0 or greater than 48",
                                element[9], element[7], element[12],element[2], element[6], element[13], element[14], element[15],
                                element[16], element[17], element[18])
                        except ValueError:
                            pass

                    if element[17] != "None":
                        try:
                            if int(element[17]) >= 72:
                                #print(engineer, "rule 7")
                                #print(element[0])
                                dictionary_quality_engineers[engineer] = dictionary_quality_engineers[engineer] + 1
                                dictionary_reason_bad_ticket[element[0]] = (element[0], "KPI_III value was greater than 72",
                                element[9], element[7], element[12], element[2], element[6], element[13], element[14], element[15],
                                element[16], element[17], element[18])
                        except ValueError:
                            pass

                elif element[12] == "Transferred":
                    if element[15] != "None":
                        try:
                            if int(element[15]) < 0 or int(element[15]) > 48:
                                #print(engineer, "rule 8")
                                dictionary_quality_engineers[engineer] = dictionary_quality_engineers[engineer] + 1
                                dictionary_reason_bad_ticket[element[0]] = (element[0], "KPI_I value was either lower than 0 or greater than 48",
                                element[9], element[7], element[12], element[2], element[6], element[13], element[14], element[15],
                                element[16], element[17], element[18])
                        except ValueError:
                            pass

                    if element[18] != "None":
                        try:
                            if int(element[18]) < 0 or int(element[18]) > 48:
                                #print(engineer, "rule 9")
                                dictionary_quality_engineers[engineer] = dictionary_quality_engineers[engineer] + 1
                                dictionary_reason_bad_ticket[element[0]] = (element[0],"KPI_IV value was either lower than 0 or greater than 48",
                                element[9], element[7], element[12], element[2], element[6], element[13], element[14],
                                element[15],element[16], element[17], element[18])
                        except ValueError:
                            pass

            elif (element[12] == "Queued" or element[12] == "Open"):
                if element[15] != "None":
                    try:
                        if (int(element[15]) < 0 or int(element[15]) > 48):
                            #print(engineer, "rule 11")
                            dictionary_quality_engineers[engineer] = dictionary_quality_engineers[engineer] + 1
                            dictionary_reason_bad_ticket[element[0]] = (element[0], "KPI_I value was lower than 0 or greater than 48",
                            element[9], element[7], element[12], element[2], element[6], element[13], element[14],
                            element[15], element[16], element[17],element[18])
                    except ValueError:
                        pass

                if element[16] != "None":
                    try:
                        if int(element[16]) < 0 or int(element[16]) > 48:
                            #print(engineer, "rule 12")
                            dictionary_quality_engineers[engineer] = dictionary_quality_engineers[engineer] + 1
                            dictionary_reason_bad_ticket[element[0]] = (element[0], "KPI_II value was lower than 0 or greater than 48",
                            element[9], element[7], element[12], element[2], element[6], element[13], element[14],
                            element[15], element[16], element[17],element[18])
                    except ValueError:
                        pass

    return dictionary_reason_bad_ticket, dictionary_quality_engineers

#working correctly
def detect_bad_tickets_quantitative_qualitative_yearly(dictionary_data_of_engineers, dictionary_quality_engineers,
                                      engineer,year):
    list_reason_bad_ticket = []

    list_of_weeks, values = zip(*dictionary_quality_engineers.items())
    # iterate over a dictionary with lists with this nested loop
    for index in list_of_weeks:
        #retrieve the initial days of the current week (each week is given in the index)
        initial_date = get_start_end_date(year, index)[0]  # index 0 contains the initial date
        beginning_year = str(initial_date).split("-")[0]
        beginning_month = str(initial_date).split("-")[1]
        beginning_day = str(initial_date).split("-")[2]

        # Default time values
        beginning_hour = 00
        beginning_minute = 00
        beginning_second = 00

        # filtered data for the SQL DB
        beginning_datetime_date_format = datetime(int(beginning_year), int(beginning_month), int(beginning_day),
                                                  beginning_hour, beginning_minute, beginning_second)
        ending_datetime_date_format = beginning_datetime_date_format + timedelta(days=7)

        for value in dictionary_data_of_engineers[engineer]:
            if dateutil.parser.parse(value[7]) >= beginning_datetime_date_format and dateutil.parser.parse(value[7]) < ending_datetime_date_format:
                if value[12] == "Transferred" or value[12] == "Closed" or value[12] == "In Progress":
                    if value[12] == "Closed":
                        if value[15] != "None":
                            # a ticket with same id can appear twice because of the rules which is correct
                            # the try and except are necessary to avoid reading values that are not int type
                            try:
                                if int(value[15]) < 0 or int(value[15]) > 48:
                                    dictionary_quality_engineers[index] = dictionary_quality_engineers[index] + 1
                                    list_reason_bad_ticket.append(
                                        (value[0], "KPI_I value was either lower than 0 or greater than 48",
                                         value[9],  value[7], value[12], value[2], value[6], value[13],
                                         value[14], value[15],value[16], value[17], value[18]))
                            except ValueError:
                                pass

                        if value[16] != "None":
                            try:
                                if int(value[16]) < 0 or int(value[16]) > 48:
                                    dictionary_quality_engineers[index] = dictionary_quality_engineers[index] + 1
                                    list_reason_bad_ticket.append((value[0], "KPI_II value was either lower than 0 or greater than 48",
                                    value[9], value[7], value[12], value[2], value[6], value[13],
                                    value[14], value[15], value[16], value[17], value[18]))
                            except ValueError:
                                pass

                        if value[17] != "None":
                            try:
                                if int(value[17]) >= 72:
                                    dictionary_quality_engineers[index] = dictionary_quality_engineers[index] + 1
                                    list_reason_bad_ticket.append((value[0], "KPI_III value was either lower than 0 or greater than 48",
                                    value[9], value[7], value[12], value[2], value[6], value[13],
                                    value[14], value[15], value[16], value[17], value[18]))
                            except ValueError:
                                pass

                    elif value[12] == "Transferred":
                        if value[15] != "None":
                            try:
                                if int(value[15]) < 0 or int(value[15]) > 48:
                                    dictionary_quality_engineers[index] = dictionary_quality_engineers[index] + 1
                                    list_reason_bad_ticket.append((value[0], "KPI_I value was either lower than 0 or greater than 48",
                                    value[9], value[7], value[12], value[2], value[6], value[13],
                                    value[14], value[15], value[16], value[17], value[18]))
                            except ValueError:
                                pass

                        if value[18] != "None":
                            try:
                                if int(value[18]) < 0 or int(value[18]) > 48:
                                    dictionary_quality_engineers[index] = dictionary_quality_engineers[index] + 1
                                    list_reason_bad_ticket.append((value[0], "KPI_IV value was either lower than 0 or greater than 48",
                                    value[9], value[7], value[12], value[2], value[6], value[13],
                                    value[14], value[15], value[16], value[17], value[18]))
                            except ValueError:
                                pass

                elif (value[12] == "Queued" or value[12] == "Open"):
                    if value[15] != "None":
                        try:
                            if (int(value[15]) < 0 or int(value[15]) > 48):
                                dictionary_quality_engineers[index] = dictionary_quality_engineers[index] + 1
                                list_reason_bad_ticket.append((value[0], "KPI_I value was either lower than 0 or greater than 48",
                                value[9], value[7], value[12], value[2], value[6], value[13],
                                value[14], value[15], value[16], value[17], value[18]))
                        except ValueError:
                            pass

                    if value[16] != "None":
                        try:
                            if int(value[16]) < 0 or int(value[16]) > 48:
                                # print(engineer, "rule 12")
                                dictionary_quality_engineers[index] = dictionary_quality_engineers[index] + 1
                                list_reason_bad_ticket.append((value[0], "KPI_II value was either lower than 0 or greater than 48",
                                value[9], value[7], value[12], value[2], value[6], value[13],
                                value[14], value[15], value[16], value[17], value[18]))
                        except ValueError:
                            pass

    return list_reason_bad_ticket, dictionary_quality_engineers

def get_values_table(dictionary_engineers,lists_of_lists_data_engineer,
                              initial_date,ending_date):
    list_data_by_engineer = []
    values_to_display_table = []
    for index_engineer, value_engineer in enumerate(dictionary_engineers):
        for value in lists_of_lists_data_engineer[value_engineer]:
            if  dateutil.parser.parse(value[7]) >= initial_date and dateutil.parser.parse(value[7]) < ending_date:
                # get the fields to extract, so you can display the selected values in a table
                list_data_by_engineer.append(value[0])  # id
                list_data_by_engineer.append(value[9]) # security engineer
                list_data_by_engineer.append(value[4])  # initial detection
                list_data_by_engineer.append(value[7]) # action date
                list_data_by_engineer.append(value[12]) # issue_status
                list_data_by_engineer.append(value[10]) # reason_for_creating
                list_data_by_engineer.append(value[3])  # problem_category
                list_data_by_engineer.append(str(value[8])) # affected devices
                values_to_display_table.append(list_data_by_engineer)
                list_data_by_engineer = []
    return values_to_display_table

def generic_count(complete_data,field_to_count,category,initial_date,ending_date):
    counter = 0
    #category can be Open, Queued, Hourly Mover, Daily Mover, etc because it is an element from all the categories

    #define the element from the list, so you can retrieve the count of the category you are searching
    if field_to_count == "Issue_Status":
        index_in_element_list = 12
    elif field_to_count == "Affected_Devices":
        index_in_element_list = 8
    elif field_to_count == "Problem_Category":
        index_in_element_list = 3
    elif field_to_count == "Reason_for_Creating":
        index_in_element_list = 10
    elif field_to_count == "Category":
        index_in_element_list = 2
    elif field_to_count == "Security_Engineer":
        index_in_element_list = 9
    else:
        index_in_element_list = 0

    #do the counting process
    for element_list in complete_data:
        #print("This is the element list: ",element_list)
        #print("This is the 12th element: ", element_list[12])
        # element_list[12] is the triage_date and element_list[22] is the issue status, we need some
        if dateutil.parser.parse(element_list[7]) >= initial_date and dateutil.parser.parse(
        element_list[7])< ending_date and element_list[index_in_element_list] == category :
            counter += 1
    return counter


def generic_count_bidimensional(complete_data, beginning_date, ending_date, x_axis, x_category, y_axis, y_category):
    # Extract the year, month, day for the beginning and ending dates
    counter = 0

    #define the element from the list, so you can retrieve the count of the category you are searching
    if x_axis == "issue status":
        x_index = 12
    elif x_axis == "problem category":
        x_index = 3
    elif x_axis  == "affected devices":
        x_index = 8
    elif x_axis  == "category":
        x_index = 2
    elif x_axis  == "reason for creating":
        x_index = 10
    elif x_axis  == "vendor":
        x_index = 1
    elif x_axis  == "priority":
        x_index = 14
    elif x_axis == "engineer":
        x_index = 9
    else:
        x_index = 0

    if y_axis == "issue status":
        y_index = 12
    elif y_axis == "problem category":
        y_index = 3
    elif y_axis  == "affected devices":
        y_index = 8
    elif y_axis  == "category":
        y_index = 2
    elif y_axis  == "reason for creating":
        y_index = 10
    elif y_axis  == "vendor":
        y_index = 1
    elif y_axis  == "priority":
        y_index = 14
    elif y_axis == "engineer":
        y_index = 9
    else:
        y_index = 0

    for value in complete_data:
        if value[x_index] == x_category and value[y_index] == y_category and dateutil.parser.parse(
        value[7]) >= beginning_date and dateutil.parser.parse(value[7]) < ending_date:
            counter += 1
    return counter

def get_start_end_date(year,week):
    '''Given the year and week, return the first and last day of the given week and year.
       The first day is Sunday and last day is Saturday'''

    year = int(year)
    week = int(week)

    d = date(year, 1, 1)
    # patch to fix the problem of the retrieval of data for the first weeks of the year
    dlt = timedelta(days=(week - 1) * 7)

    if (d.weekday() <= 3):
        d = d - timedelta(d.weekday())
    else:
        # this line  d = d + timedelta(6 - d.weekday()) indicates to start in Sunday and end in Saturday
        # but it breaks when the retrieval is during the first weeks of the year, so we have to change the code
        # back to d = d + timedelta(7 - d.weekday())
        d = d + timedelta(7 - d.weekday())
    return d + dlt, d + dlt + timedelta(days=6)

def connection_database_postgresql(initial_date, end_date):

    dictionary_key_values = {"Id":[],
                             "Vendor": [],
                             "Category": [],
                             "Problem_Category": [],
                             "Initial_Detection": [],
                             "Last_Day_Track": [],
                             "Issue_Closed_Date": [],
                             "Action_Date": [],
                             "Affected_Devices": [],
                             "Security_Engineer": [],
                             "Reason_For_Creating": [],
                             "SLA_MET": [],
                             "Issue_Status": [],
                             "Issue_Re_Assigned_Date": [],
                             "Priority": [],
                             "KPI_I": [],
                             "KPI_II":[],
                             "KPI_III": [],
                             "KPI_IV": []
                             }

    connection = psycopg2.connect(host = "localhost", database = "postgres", user = "postgres", password = "Ab152211@")

    cursor = connection.cursor()
    # if we get the error failed to execute an empty string is because there is no data in the database, you need to execute
    # with previous dates, 2017-11-01 - 2018-01-01 are the range of valid dates

    cursor.execute("select * from securitytickets where Action_Date between '" + str(initial_date) +"' and '" + str(end_date) + "';")

    # records is a list
    records = cursor.fetchall()
    cursor.close()

    for index, tuple_value in enumerate(records):
        dictionary_key_values["Id"].append(str(tuple_value[0]))
        dictionary_key_values["Vendor"].append(str(tuple_value[1]))
        dictionary_key_values["Category"].append(str(tuple_value[2]))
        dictionary_key_values["Problem_Category"].append(str(tuple_value[3]))
        dictionary_key_values["Initial_Detection"].append(str(tuple_value[4]))
        dictionary_key_values["Last_Day_Track"].append(str(tuple_value[5]))
        dictionary_key_values["Issue_Closed_Date"].append(str(tuple_value[6]))
        dictionary_key_values["Action_Date"].append(str(tuple_value[7]))
        dictionary_key_values["Affected_Devices"].append(str(tuple_value[8]))
        dictionary_key_values["Security_Engineer"].append(str(tuple_value[9]))
        dictionary_key_values["Reason_For_Creating"].append(str(tuple_value[10]))
        dictionary_key_values["SLA_MET"].append(str(tuple_value[11]))
        dictionary_key_values["Issue_Status"].append(str(tuple_value[12]))
        dictionary_key_values["Issue_Re_Assigned_Date"].append(str(tuple_value[13]))
        dictionary_key_values["Priority"].append(str(tuple_value[14]))
        dictionary_key_values["KPI_I"].append(str(tuple_value[15]))
        dictionary_key_values["KPI_II"].append(str(tuple_value[16]))
        dictionary_key_values["KPI_III"].append(str(tuple_value[17]))
        dictionary_key_values["KPI_IV"].append(str(tuple_value[18]))

    data_frame = pd.DataFrame(dictionary_key_values)
    return data_frame

#working correctly
def get_rows_of_data_yearly(request):
    year          = request.POST.get('select_year', None)
    initial_year  = str(year)
    initial_month = str("01") #first month of the year
    initial_day   = str("01")  # first day of month as a zero padded decimal number
    initial_date  = str(datetime(int(initial_year), int(initial_month), int(initial_day))).split(" ")[0]

    ending_year   = str(year)
    ending_month  = str("12") #last month of the year
    ending_day    = str("31")  # get the last day of the month
    ending_date   = str(datetime(int(ending_year), int(ending_month), int(ending_day))).split(" ")[0]

    # Default time values
    beginning_hour   = 00
    beginning_minute = 00
    beginning_second = 00

    # Default time values
    ending_hour   = 23
    ending_minute = 59
    ending_second = 59


    beginning_datetime_date_format = datetime(int(initial_year), int(initial_month), int(initial_day),
                                              beginning_hour, beginning_minute, beginning_second)
    ending_datetime_date_format = datetime(int(ending_year), int(ending_month), int(ending_day),
                                              ending_hour, ending_minute, ending_second)


    # Retrieval to the SQL database
    dataframe_filtered_data = connection_database_postgresql(beginning_datetime_date_format,
                                                                      ending_datetime_date_format)

    dict_engineers_lists_of_lists_data = clear_engineer_names(dataframe_filtered_data)

    return dict_engineers_lists_of_lists_data, initial_date, ending_date, year

#working correctly
def get_rows_of_data_monthly(request):
    year = request.POST.get('select_year', None)
    month = request.POST.get('select_month', None)
    list_of_months = ["1", "2", "3", "4", "5", "6", "7", "8", "9"]
    initial_year = str(year)

    #patch that fixes the problem of monthly retrieval of data for the first 9 months of the year
    if str(month) in list_of_months:
        initial_month = str(0)+str(month)
    else:
        initial_month = str(month)

    initial_day = str("01")  # first day of month as a zero padded decimal number
    initial_date = str(datetime(int(initial_year), int(initial_month), int(initial_day))).split(" ")[0]

    ending_year = str(year)
    ending_month = str(month)
    ending_day = str(calendar.monthrange(int(year), int(month))[1])  # get the last day of the month
    ending_date = str(datetime(int(ending_year), int(ending_month), int(ending_day))).split(" ")[0]

    # Default time values
    beginning_hour = 00
    beginning_minute = 00
    beginning_second = 00

    # Default time values
    ending_hour = 23
    ending_minute = 59
    ending_second = 59

    # filtered data for the SQL DB
    beginning_datetime_date_format = datetime(int(initial_year), int(initial_month), int(initial_day),
                                              beginning_hour, beginning_minute, beginning_second)
    ending_datetime_date_format    = datetime(int(ending_year), int(ending_month), int(ending_day),
                                              ending_hour, ending_minute, ending_second)

    dataframe_filtered_data = connection_database_postgresql(beginning_datetime_date_format,
                                                                      ending_datetime_date_format)

    dict_engineers_lists_of_lists_data = clear_engineer_names(dataframe_filtered_data)

    return dict_engineers_lists_of_lists_data, initial_date, ending_date, year, month

#working correctly
def get_rows_of_data_weekly(request):
    year = request.POST.get('select_year', None)
    week = request.POST.get('select_week', None)
    initial_date = get_start_end_date(year, week)[0]  # index 0 contains the initial date
    # ending_date  = get_start_end_date_colombia(year, week)[1]  # index 0 contains the initial date

    beginning_year = str(initial_date).split("-")[0]
    beginning_month = str(initial_date).split("-")[1]
    beginning_day = str(initial_date).split("-")[2]

    # Default time values
    beginning_hour = 00
    beginning_minute = 00
    beginning_second = 00

    # 1 week of data equal to 7
    ending_date = initial_date + timedelta(days=7)

    # filtered data for the SQL DB
    beginning_datetime_date_format = datetime(int(beginning_year), int(beginning_month), int(beginning_day),
                                              beginning_hour, beginning_minute, beginning_second)
    ending_datetime_date_format = beginning_datetime_date_format + timedelta(days=7)

    # Retrieval to the SQL database
    dataframe_filtered_data = connection_database_postgresql(beginning_datetime_date_format,
                                                                                 ending_datetime_date_format)

    dict_engineers_lists_of_lists_data = clear_engineer_names(dataframe_filtered_data)
    return dict_engineers_lists_of_lists_data, initial_date, ending_date, year, week

def get_rows_of_data_daily(request):
    # patch to retrieve the data of the tickets during the first months of the year
    list_of_months = ["1", "2", "3", "4", "5", "6", "7", "8", "9"]

    year  = request.POST.get('select_year', None)
    month = request.POST.get('select_month', None)
    day   = request.POST.get('select_day', None)

    # patch that fixes the problem of monthly retrieval of data for the first 9 months of the year
    if str(month) in list_of_months:
        month = str(0) + str(month)
    else:
        month = str(month)

    # Default time values
    beginning_hour = 00
    beginning_minute = 00
    beginning_second = 00

    beginning_datetime_date_format = datetime(int(year), int(month), int(day),
                                              beginning_hour, beginning_minute, beginning_second)

    # Ending date is equal to the next day from the initial day
    ending_datetime_date_format = beginning_datetime_date_format + timedelta(days=1)


    dataframe_filtered_data = connection_database_postgresql(beginning_datetime_date_format,
                                                                      ending_datetime_date_format)

    dict_engineers_lists_of_lists_data = clear_engineer_names(dataframe_filtered_data)
    return dict_engineers_lists_of_lists_data, beginning_datetime_date_format, ending_datetime_date_format, year, month, day

#working correctly
def clear_engineer_names(dataframe_filtered_data):
    # get the list of all engineers from database
    list_of_engineers = get_all_engineers()

    # set engineer and number of tickets, default number of tickets start at 0
    dict_engineers_lists_of_lists_data = {}

    '''create a dictionary from a list where each engineer will have an initial count of 0 tickets, so we can compare
        these values against the fetched data from SQL.'''
    for engineer in list_of_engineers:
        dict_engineers_lists_of_lists_data[engineer] = dict_engineers_lists_of_lists_data.get(engineer, [])

    # convert this data frame to a list of dictionaries

    required_space = " "
    # hold the count of tickets per engineer and then erase the content once the next engineer comes from the list
    for index_e, value_e in enumerate(list_of_engineers):
        # reset the rows of data per engineer list that stores each row of data for a given engineer
        # rows_data_per_engineer = []
        '''If there is a space or dot that separates each engineer name then separate its name by " " or by . and then
                compare each engineer name with the engineers that are in the list of dictionaries. '''
        # original
        # for index_f, value_f in enumerate(list_of_dictionaries_filtered_data):
        for index_f, value_f in enumerate(dataframe_filtered_data["Security_Engineer"]):
            # print(index_f, value_f)
            # patch to avoid reading None type values
            if value_f != 'None':
                # print("First condition: ",value_f)
                # original to clean the names of engineers because some of them have dots or spaces between their names
                # if value_f['triage engineer'] != None:
                rows_data_per_engineer = []
                if " " in value_f:
                    # print("Second condition: ",value_f)
                    # original
                    # if " " in value_f['triage engineer']:
                    '''compare the value_e of engineers that are stored in our database against the engineers that we 
                        found in the SQL data. '''
                    if value_e.lower() == str(value_f).lower().split(' ')[0] + required_space + \
                            str(value_f).lower().split(' ')[1]:
                        # original
                        # if value_e.lower() == str(value_f['triage engineer']).lower().split(' ')[0] + required_space + \
                        #        str(value_f['triage engineer']).lower().split(' ')[1]:
                        # once you have found the engineer that you are looking for, append its data dictionary
                        rows_data_per_engineer.append(dataframe_filtered_data["Id"][index_f])
                        rows_data_per_engineer.append(dataframe_filtered_data["Vendor"][index_f])
                        rows_data_per_engineer.append(dataframe_filtered_data["Category"][index_f])
                        rows_data_per_engineer.append(dataframe_filtered_data["Problem_Category"][index_f])
                        rows_data_per_engineer.append(dataframe_filtered_data["Initial_Detection"][index_f])
                        rows_data_per_engineer.append(dataframe_filtered_data["Last_Day_Track"][index_f])
                        rows_data_per_engineer.append(dataframe_filtered_data["Issue_Closed_Date"][index_f])
                        rows_data_per_engineer.append(dataframe_filtered_data["Action_Date"][index_f])
                        rows_data_per_engineer.append(dataframe_filtered_data["Affected_Devices"][index_f])
                        rows_data_per_engineer.append(dataframe_filtered_data["Security_Engineer"][index_f])
                        rows_data_per_engineer.append(dataframe_filtered_data["Reason_For_Creating"][index_f])
                        rows_data_per_engineer.append(dataframe_filtered_data["SLA_MET"][index_f])
                        rows_data_per_engineer.append(dataframe_filtered_data["Issue_Status"][index_f])
                        rows_data_per_engineer.append(dataframe_filtered_data["Issue_Re_Assigned_Date"][index_f])
                        rows_data_per_engineer.append(dataframe_filtered_data["Priority"][index_f])
                        rows_data_per_engineer.append(dataframe_filtered_data["KPI_I"][index_f])
                        rows_data_per_engineer.append(dataframe_filtered_data["KPI_II"][index_f])
                        rows_data_per_engineer.append(dataframe_filtered_data["KPI_III"][index_f])
                        rows_data_per_engineer.append(dataframe_filtered_data["KPI_IV"][index_f])

                        # temp_list.append(rows_data_per_engineer)
                        # rows_data_per_engineer.append(";")
                # if you found a point or any other division character such as .,/
                else:
                    # print("Second condition (else): ", value_f)
                    if value_e.lower() == value_e.lower() == str(value_f).lower().split('.')[0] + required_space + \
                            str(value_f).lower().split('.')[1]:
                        # original
                        # if value_e.lower() == value_e.lower() == str(value_f['triage engineer']).lower().split('.')[0] + \required_space + str(value_f['triage engineer']).lower().split('.')[1]:
                        rows_data_per_engineer.append(dataframe_filtered_data["Id"][index_f])
                        rows_data_per_engineer.append(dataframe_filtered_data["Vendor"][index_f])
                        rows_data_per_engineer.append(dataframe_filtered_data["Category"][index_f])
                        rows_data_per_engineer.append(dataframe_filtered_data["Problem_Category"][index_f])
                        rows_data_per_engineer.append(dataframe_filtered_data["Initial_Detection"][index_f])
                        rows_data_per_engineer.append(dataframe_filtered_data["Last_Day_Track"][index_f])
                        rows_data_per_engineer.append(dataframe_filtered_data["Issue_Closed_Date"][index_f])
                        rows_data_per_engineer.append(dataframe_filtered_data["Action_Date"][index_f])
                        rows_data_per_engineer.append(dataframe_filtered_data["Affected_Devices"][index_f])
                        rows_data_per_engineer.append(dataframe_filtered_data["Security_Engineer"][index_f])
                        rows_data_per_engineer.append(dataframe_filtered_data["Reason_For_Creating"][index_f])
                        rows_data_per_engineer.append(dataframe_filtered_data["SLA_MET"][index_f])
                        rows_data_per_engineer.append(dataframe_filtered_data["Issue_Status"][index_f])
                        rows_data_per_engineer.append(dataframe_filtered_data["Issue_Re_Assigned_Date"][index_f])
                        rows_data_per_engineer.append(dataframe_filtered_data["Priority"][index_f])
                        rows_data_per_engineer.append(dataframe_filtered_data["KPI_I"][index_f])
                        rows_data_per_engineer.append(dataframe_filtered_data["KPI_II"][index_f])
                        rows_data_per_engineer.append(dataframe_filtered_data["KPI_III"][index_f])
                        rows_data_per_engineer.append(dataframe_filtered_data["KPI_IV"][index_f])
                        # temp_list.append(rows_data_per_engineer)
                # insert only rows with data into the dictionary
                if rows_data_per_engineer:
                    dict_engineers_lists_of_lists_data[value_e].append(rows_data_per_engineer)

    '''The dictionary contains all the engineers as keys but some engineers might have a value of 0 because they could 
    be on vacation or might have quit, but the counting process does not take into account these engineers with 0 values .'''
    return dict_engineers_lists_of_lists_data

def get_rows_of_data_quantitative_qualitative_yearly(request):
    engineer = request.POST.get('engineer',None)
    week_one = request.POST.get('week_comparison_one', None)
    week_two = request.POST.get('week_comparison_two', None)
    year     = str(request.POST.get('year', None))

    inclusive_value = 1
    list_of_weeks   = list(range(int(week_one),int(week_two)+inclusive_value))

    initial_date = get_start_end_date(year, week_one)[0]  # index 0 contains the initial date
    ending_date  = get_start_end_date(year, week_two)[1]  # index 1 contains the ending date

    initial_month = str(initial_date).split("-")[1]
    initial_day   = str(initial_date).split("-")[2]

    ending_month  = str(ending_date).split("-")[1]
    ending_day    = str(ending_date).split("-")[2]

    # Default time values
    default_hour   = 00
    default_minute = 00
    default_second = 00

    beginning_datetime_date_format = datetime(int(year), int(initial_month), int(initial_day),
                                              default_hour, default_minute, default_second)

    ending_datetime_date_format = datetime(int(year), int(ending_month), int(ending_day),
                                           default_hour, default_minute, default_second)


    # This data is already filtered by the number of week.
    dataframe_filtered_data = connection_database_postgresql(beginning_datetime_date_format,
                                                                      ending_datetime_date_format)

    # set the selected engineer and number of tickets, default number of tickets start at 0
    dictionary_count_engineer = {engineer: []}

    required_space = " "
    # hold the count of tickets per engineer and then erase the content once the next engineer comes from the list

    for index_f, value_f in enumerate(dataframe_filtered_data["Security_Engineer"]):
    # patch to avoid reading None type values
        if value_f != 'None':
            rows_data_per_engineer = []
            if " " in value_f:
                '''compare the value_e of engineers that are stored in our database against the engineers that we 
                    found in the SQL data. '''
                if engineer.lower() == str(value_f).lower().split(' ')[0] + required_space + \
                        str(value_f).lower().split(' ')[1]:
                    # original
                    # if value_e.lower() == str(value_f['triage engineer']).lower().split(' ')[0] + required_space + \
                    #        str(value_f['triage engineer']).lower().split(' ')[1]:
                    # once you have found the engineer that you are looking for, append its data dictionary
                    rows_data_per_engineer.append(dataframe_filtered_data["Id"][index_f])
                    rows_data_per_engineer.append(dataframe_filtered_data["Vendor"][index_f])
                    rows_data_per_engineer.append(dataframe_filtered_data["Category"][index_f])
                    rows_data_per_engineer.append(dataframe_filtered_data["Problem_Category"][index_f])
                    rows_data_per_engineer.append(dataframe_filtered_data["Initial_Detection"][index_f])
                    rows_data_per_engineer.append(dataframe_filtered_data["Last_Day_Track"][index_f])
                    rows_data_per_engineer.append(dataframe_filtered_data["Issue_Closed_Date"][index_f])
                    rows_data_per_engineer.append(dataframe_filtered_data["Action_Date"][index_f])
                    rows_data_per_engineer.append(dataframe_filtered_data["Affected_Devices"][index_f])
                    rows_data_per_engineer.append(dataframe_filtered_data["Security_Engineer"][index_f])
                    rows_data_per_engineer.append(dataframe_filtered_data["Reason_For_Creating"][index_f])
                    rows_data_per_engineer.append(dataframe_filtered_data["SLA_MET"][index_f])
                    rows_data_per_engineer.append(dataframe_filtered_data["Issue_Status"][index_f])
                    rows_data_per_engineer.append(dataframe_filtered_data["Issue_Re_Assigned_Date"][index_f])
                    rows_data_per_engineer.append(dataframe_filtered_data["Priority"][index_f])
                    rows_data_per_engineer.append(dataframe_filtered_data["KPI_I"][index_f])
                    rows_data_per_engineer.append(dataframe_filtered_data["KPI_II"][index_f])
                    rows_data_per_engineer.append(dataframe_filtered_data["KPI_III"][index_f])
                    rows_data_per_engineer.append(dataframe_filtered_data["KPI_IV"][index_f])
                    # temp_list.append(rows_data_per_engineer)
                    # rows_data_per_engineer.append(";")
            # if you found a point or any other division character such as .,/
            else:
                # print("Second condition (else): ", value_f)
                if engineer.lower() == engineer.lower() == str(value_f).lower().split('.')[0] + required_space + \
                        str(value_f).lower().split('.')[1]:
                    # original
                    # if value_e.lower() == value_e.lower() == str(value_f['triage engineer']).lower().split('.')[0] + \required_space + str(value_f['triage engineer']).lower().split('.')[1]:
                    rows_data_per_engineer.append(dataframe_filtered_data["Id"][index_f])
                    rows_data_per_engineer.append(dataframe_filtered_data["Vendor"][index_f])
                    rows_data_per_engineer.append(dataframe_filtered_data["Category"][index_f])
                    rows_data_per_engineer.append(dataframe_filtered_data["Problem_Category"][index_f])
                    rows_data_per_engineer.append(dataframe_filtered_data["Initial_Detection"][index_f])
                    rows_data_per_engineer.append(dataframe_filtered_data["Last_Day_Track"][index_f])
                    rows_data_per_engineer.append(dataframe_filtered_data["Issue_Closed_Date"][index_f])
                    rows_data_per_engineer.append(dataframe_filtered_data["Action_Date"][index_f])
                    rows_data_per_engineer.append(dataframe_filtered_data["Affected_Devices"][index_f])
                    rows_data_per_engineer.append(dataframe_filtered_data["Security_Engineer"][index_f])
                    rows_data_per_engineer.append(dataframe_filtered_data["Reason_For_Creating"][index_f])
                    rows_data_per_engineer.append(dataframe_filtered_data["SLA_MET"][index_f])
                    rows_data_per_engineer.append(dataframe_filtered_data["Issue_Status"][index_f])
                    rows_data_per_engineer.append(dataframe_filtered_data["Issue_Re_Assigned_Date"][index_f])
                    rows_data_per_engineer.append(dataframe_filtered_data["Priority"][index_f])
                    rows_data_per_engineer.append(dataframe_filtered_data["KPI_I"][index_f])
                    rows_data_per_engineer.append(dataframe_filtered_data["KPI_II"][index_f])
                    rows_data_per_engineer.append(dataframe_filtered_data["KPI_III"][index_f])
                    rows_data_per_engineer.append(dataframe_filtered_data["KPI_IV"][index_f])
                    # temp_list.append(rows_data_per_engineer)
            # insert only rows with data into the dictionary
            if rows_data_per_engineer:
                dictionary_count_engineer[engineer].append(rows_data_per_engineer)


    '''The dictionary contains all the engineers as keys but some engineers might have a value of 0 because they could be on vacation or might have quit, so we need 
    to count only those engineers that contain data. For this case, see def get_labels_from_keys() which counts only the engineers that do not contain a value of 0.'''
    return dictionary_count_engineer, engineer, initial_date, ending_date, year, list_of_weeks

def convert_date_to_datetime(beginning_date,ending_date):
    required_space = " "
    beginning_time_string_format = "00:00:00"
    ending_time_string_format    = "00:00:00" # check get_rows_of_data_weekly() to see why we have 00:00:00
    beginning_date_date_format_to_string = str(beginning_date).split(" ")[
                                               0] + required_space + beginning_time_string_format
    ending_date_date_format_to_string = str(ending_date).split(" ")[
                                            0] + str() + required_space + ending_time_string_format

    ####################### convert the string to datetime.datetime ##################
    beginning_date_string_to_datetime = datetime.strptime(beginning_date_date_format_to_string, "%Y-%m-%d %H:%M:%S")
    ending_date_string_to_datetime = datetime.strptime(ending_date_date_format_to_string, "%Y-%m-%d %H:%M:%S")

    return beginning_date_string_to_datetime, ending_date_string_to_datetime

def convert_date_to_datetime_monthly_yearly(beginning_date,ending_date):
    required_space = " "
    beginning_time_string_format = "00:00:00"
    ending_time_string_format    = "23:59:59"
    beginning_date_date_format_to_string = str(beginning_date).split(" ")[0] + required_space + beginning_time_string_format
    ending_date_date_format_to_string = str(ending_date).split(" ")[0] + str() + required_space + ending_time_string_format

    ####################### convert the string to datetime.datetime ##################
    beginning_date_string_to_datetime = datetime.strptime(beginning_date_date_format_to_string, "%Y-%m-%d %H:%M:%S")
    ending_date_string_to_datetime = datetime.strptime(ending_date_date_format_to_string, "%Y-%m-%d %H:%M:%S")

    return beginning_date_string_to_datetime, ending_date_string_to_datetime


######### Retrieve data from models db

def get_market():
    current_market = "Country A"
    return current_market

def get_quantitative_value():
    quantitative_value = 2.5
    return quantitative_value

def get_all_engineers():
    querySet = SecurityAuditEngineer.objects.all()
    list_of_engineers = []
    for engineer in querySet:
        list_of_engineers.append(engineer.engineer_name + " " + engineer.engineer_last_name)
    return list_of_engineers

def get_fields_problem_category():
    querySet = SecurityAuditProblemCategory.objects.all()
    list_of_problem_categories = []
    for problem in querySet:
        list_of_problem_categories.append(problem.problem_category)
    return list_of_problem_categories

def get_fields_triage_category():
    querySet = SecurityAuditAffectedDevicesCategory.objects.all()
    list_of_triage_categories = []
    for problem in querySet:
        list_of_triage_categories.append(problem.ticket_category)
    return list_of_triage_categories

def get_fields_ticket_status():
    querySet = SecurityAuditStatusTicket.objects.all()
    list_categories = []
    for status in querySet:
        list_categories.append(status.ticket_status)
    return list_categories

def get_fields_reason_for_creating():
    querySet = SecurityAuditReasonForCreatingTicket.objects.all()
    list_of_problem_categories = []
    for reason in querySet:
        list_of_problem_categories.append(reason.reason_category)
    return list_of_problem_categories

def get_fields_priority():
    querySet = SecurityAuditPriorityTicket.objects.all()
    list_of_priorities = []
    for priority in querySet:
        list_of_priorities.append(priority.ticket_priority)
    return list_of_priorities

def get_fields_vendors():
    querySet = SecurityAuditVendor.objects.all()
    list_of_vendors = []
    for vendor in querySet:
        list_of_vendors.append(vendor.vendor)
    return list_of_vendors

def get_fields_affected_devices():
    querySet = SecurityAuditAffectedDevicesCategory.objects.all()
    list_of_affected_devices = []
    for affected_device in querySet:
        list_of_affected_devices.append(affected_device.affected_device_category)
    return list_of_affected_devices

def get_fields_category():
    querySet = SecurityAuditCategory.objects.all()
    list_of_categories = []
    for category in querySet:
        list_of_categories.append(category.category)
    return list_of_categories

#this works for daily and weekly graphs
def get_current_engineers(dictionary_of_rows):
    engineer_labels = []
    # iterate over a dictionary
    for key, value in dictionary_of_rows.items():
        # if the default value is different from empty then these engineers should appear in the graphs
        if value != []:
            engineer_labels.append(key)
    return engineer_labels

########## main methods that are being used for Finances and Security #################
def get_current_days_of_week():
    days_of_week = 7
    return days_of_week

def remove_zero_values_in_dictionary_ca(dictionary):
    dictionary_with_values = {}
    for index, value in dictionary.items():
        if value!=0:
            dictionary_with_values[index] = value
    return dictionary_with_values

def get_label_days(initial_date):
    list_of_days = []
    for day in range(get_current_days_of_week()):
        list_of_days.append(str((initial_date + timedelta(days=day)).strftime("%A")) + " " +
                            str((initial_date + timedelta(days=day)).strftime("%d")) + " " +
                            str((initial_date + timedelta(days=day)).strftime("%b")))
    return list_of_days

def remove_zero_values_stacked_chart(values,list_of_engineers):
    temporary_dictionary = {}
    dictionary_no_zero_values = {}

    # transpose the list with tickets of each engineer
    transpose_list_of_lists = list(map(list, zip(*values)))

    # store all the tickets for each engineer in dictionaries
    for index_engineer, value_engineer in enumerate(list_of_engineers):
        temporary_dictionary[value_engineer] = transpose_list_of_lists[index_engineer]


    # Cleaning process: do not store those engineers that have zero tickets in all the categories
    for key in temporary_dictionary:
        for engineer_list in temporary_dictionary[key]:
            if np.sum(engineer_list) != 0:
                dictionary_no_zero_values[key] = temporary_dictionary[key]

    # cleaned values
    # patch to avoid the problem with the display of values if no data was found for stacked charts
    keys_zero_values, zero_values = verify_data_dictionary_no_sorted_charts(dictionary_no_zero_values)

    # transpose the cleaned values to make them fit into the categories, i.e., O&M:[1,2,3,4], Capacity:[5,6,7,8]
    transpose_zero_values = list(map(list, zip(*zero_values)))

    return keys_zero_values, transpose_zero_values

# patch to avoid the problem with the display of values if no data was found for stacked charts
def verify_data_dictionary_no_sorted_charts(dictionary_no_zero_values):
    if dictionary_no_zero_values:
        # this line contains all the tickets of each engineer by category
        legend_of_chart, values = zip(*dictionary_no_zero_values.items())
    else:
        # return empty tuples in case no values are found
        legend_of_chart = ()
        values = ()
    return legend_of_chart, values

# patch to avoid the problem with the display of values if no data was found for pie charts
def verify_data_dictionary_sorted_charts(dictionary_no_zero_values):
    if dictionary_no_zero_values:
        # sort the dictionary from the biggest to smallest number
        legend_of_chart, values = zip(*sorted(dictionary_no_zero_values.items(), key=lambda x: x[1], reverse=True))
    else:
        # return empty tuples in case no values are found
        legend_of_chart = ()
        values = ()
    return legend_of_chart, values