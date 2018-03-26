from django.contrib import admin
from .models import SecurityAuditEngineer, SecurityAuditCategory, SecurityAuditReasonForCreatingTicket, \
    SecurityAuditStatusTicket, SecurityAuditAffectedDevicesCategory, SecurityAuditProblemCategory, \
    SecurityAuditVendor, SecurityAuditPriorityTicket

############ Security ###################

admin.site.register(SecurityAuditEngineer)
admin.site.register(SecurityAuditCategory)
admin.site.register(SecurityAuditReasonForCreatingTicket)
admin.site.register(SecurityAuditStatusTicket)
admin.site.register(SecurityAuditAffectedDevicesCategory)
admin.site.register(SecurityAuditProblemCategory)
admin.site.register(SecurityAuditVendor)
admin.site.register(SecurityAuditPriorityTicket)

