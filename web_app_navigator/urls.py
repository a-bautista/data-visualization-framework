from django.conf.urls import url
from . import views


urlpatterns = [
    # ================================ Home =============================================
    url(r'^$', views.index, name='index'),  # render the header_home view


        # ================================ Security =============================================

        ########### Daily URLs

        # View to see the quantitative vs qualitative daily
        url(r'quantitative_qualitative_daily/$', views.tickets_quantitative_qualitative_daily),
        url(r'quantitative_qualitative_daily/$', views.tickets_quantitative_qualitative_daily,
            name='quantitative_qualitative_daily'),

        ########### Weekly URLs

        #View to see the quantitative vs qualitative weekly
        url(r'^quantitative_qualitative_weekly/$', views.tickets_quantitative_qualitative_weekly),
        url(r'^quantitative_qualitative_weekly/$', views.tickets_quantitative_qualitative_weekly,
            name='quantitative_qualitative_weekly'),

        # View to see the count of tickets
        url(r'^tickets_counting_weekly/$', views.tickets_counting_weekly),
        url(r'^tickets_counting_weekly/$', views.tickets_counting_weekly,
            name='tickets_counting_weekly'),

        # View to see the ticket status
        url(r'^tickets_status_weekly/$', views.tickets_status_weekly),
        url(r'^tickets_status_weekly/$', views.tickets_status_weekly,
            name='tickets_status_weekly'),

        # View to see the tickets per affected devices
        url(r'^tickets_affected_devices_weekly/$', views.tickets_affected_devices_weekly),
        url(r'^tickets_affected_devices_weekly/$', views.tickets_affected_devices_weekly,
            name='tickets_affected_devices_weekly'),

        # View to see the problem category
        url(r'^tickets_problem_category_weekly/$', views.tickets_problem_category_weekly),
        url(r'^tickets_problem_category_weekly/$', views.tickets_problem_category_weekly,
            name='tickets_problem_category_weekly'),

        # View to see the reason for creating
        url(r'^tickets_reason_for_creating_weekly/$', views.tickets_reason_for_creating_weekly),
        url(r'^tickets_reason_for_creating_weekly/$', views.tickets_reason_for_creating_weekly,
            name='tickets_reason_for_creating_weekly'),

        ########### Monthly URLs

        # View to see the problem category
        url(r'^tickets_affected_devices_monthly/$', views.tickets_affected_devices_monthly),
        url(r'^tickets_affected_devices_monthly/$', views.tickets_affected_devices_monthly,
            name='tickets_affected_devices_monthly'),

        # View to see the problem category
        url(r'^tickets_problem_category_monthly/$', views.tickets_problem_category_monthly),
        url(r'^tickets_problem_category_monthly/$', views.tickets_problem_category_monthly,
            name='tickets_problem_category_monthly'),


        # View to see the reason for creating
        url(r'^tickets_reason_for_creating_monthly/$', views.tickets_reason_for_creating_monthly),
        url(r'^tickets_reason_for_creating_monthly/$', views.tickets_reason_for_creating_monthly,
            name='tickets_reason_for_creating_monthly'),

        url(r'^tickets_bidimensional_analysis_monthly/$',views.tickets_bidimensional_analysis_monthly),
        url(r'^tickets_bidimensional_analysis_monthly/$',views.tickets_bidimensional_analysis_monthly,
            name='tickets_bidimensional_analysis_monthly'),

        ########### Yearly URLs

        url(r'quantitative_qualitative_yearly/$', views.tickets_quantitative_qualitative_per_engineer_yearly),
        url(r'quantitative_qualitative_yearly/$', views.tickets_quantitative_qualitative_per_engineer_yearly,
            name='quantitative_qualitative_yearly'),

        # View to see the problem category
        url(r'^tickets_affected_devices_yearly/$', views.tickets_affected_devices_yearly),
        url(r'^tickets_affected_devices_yearly/$', views.tickets_affected_devices_yearly,
            name='tickets_affected_devices_yearly'),


        # View to see the problem category
        url(r'^tickets_problem_category_yearly/$', views.tickets_problem_category_yearly),
        url(r'^tickets_problem_category_yearly/$', views.tickets_problem_category_yearly,
            name='tickets_problem_category_yearly'),

        # View to see the reason for creating
        url(r'^tickets_reason_for_creating_yearly/$', views.tickets_reason_for_creating_yearly),
        url(r'^tickets_reason_for_creating_yearly/$', views.tickets_reason_for_creating_yearly,
            name='tickets_reason_for_creating_yearly'),


        url(r'^tickets_bidimensional_analysis_yearly/$',views.tickets_bidimensional_analysis_yearly),
        url(r'^tickets_bidimensional_analysis_yearly/$',views.tickets_bidimensional_analysis_yearly,
            name='tickets_bidimensional_analysis_yearly'),
]
