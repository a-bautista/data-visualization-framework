from django.db import models

##################################### SecurityAudit ########################################

class SecurityAuditEngineer(models.Model):
    engineer_name       = models.CharField(max_length = 120, null = False, blank = False)
    engineer_last_name  = models.CharField(max_length = 120, null = False, blank = False)

    def __str__(self):
        return self.engineer_name + " "+self.engineer_last_name

class SecurityAuditCategory(models.Model):
    category    = models.CharField(max_length = 120, null = False, blank = False)

    def __str__(self):
        return self.category

class SecurityAuditReasonForCreatingTicket(models.Model):
    reason_category     = models.CharField(max_length = 120, null = False, blank = False)

    def __str__(self):
        return self.reason_category

class SecurityAuditStatusTicket(models.Model):
    ticket_status       = models.CharField(max_length=120, null=False, blank=False)

    def __str__(self):
        return self.ticket_status

class SecurityAuditAffectedDevicesCategory(models.Model):
    affected_device_category = models.CharField(max_length=120, null=False, blank=False)

    def __str__(self):
        return self.affected_device_category


class SecurityAuditProblemCategory(models.Model):
    problem_category = models.CharField(max_length=120, null=False, blank=False)

    def __str__(self):
        return self.problem_category

class SecurityAuditVendor(models.Model):
    vendor = models.CharField(max_length=120, null=False, blank=False)

    def __str__(self):
        return self.vendor


class SecurityAuditPriorityTicket(models.Model):
    ticket_priority = models.CharField(max_length=120, null=False, blank=False)

    def __str__(self):
        return self.ticket_priority


