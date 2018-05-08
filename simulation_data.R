# Title     : TODO
# Objective : TODO
# Created by: abautista
# Created on: 5/7/2018


# The code from below won't work because each vector from the data frame is from a different size.
original <- data.frame(Vendor = c("F-Secure", "GE"),
                       Category = c("Cybersecurity", "IoT", "Machine Learning"),
                       Problem_Category = c("Penetration breach", "Lack of CERT", "APT", "Bad security policies",
                                    "Botnet", "Breach in SCADA systems", "Compromised data", "DDoS attack",
                                    "Erroneous data load", "Erroneous forecast algorithm", "Hijack of device",
                                    "Identity spoofing", "Internal flaws in device", "Lack of appropriate hardware",
                                    "Lack of CERT", "Malware installed", "Non-filtered data", "Ransomware virus",
                                    "Theft of intellectual property", "Total destruction of data", "Unpatched software",
                                    "Wiper attack"),
                       Affected_devices = c("Company main devices", "Mobile devices", "Personal user devices",
                                            "Principal devices", "Test devices", "Third party devices"),
                       Security_engineer = c("Alekz Horn", "Annette Smith", "Boris Mikhail", "Dieter Becker",
                       "Florian Klein", "Friederich Voigt", "Gerhard Simon", "Hannes Weber", "Helga Fischer",
                       "Horst Vogel", "Ivan Kolgomorov", "Johannes Dirsch", "Karl Keller", "Klaus Lorenz",
                       "Kristine Schulz", "Kurt Heinz", "Lena Wagner", "Luka Tolso", "Olga Koch", "Pamela Schumacher",
                       "Patrick Benz", "Peter Thomas", "Roger Schmidt", "Sofia Kovalevsky", "Uwe Frank", "Viktor Sauer",
                       "Walter Roth", "Yitin Nguyen"),
                        Reason_for_creating = c("Hourly Analysis", "Bi-weekly Analysis", "Daily Analysis",
                        "Halt Analysis", "Hourly Analysis", "Immediate Analysis", "Monthly Analysis", "Random Analysis",
                        "Special Request", "VIP"),
                        SLA_MET = c("Yes", "No"),
                        Issue_status = c("Closed", "In Progress", "Open", "Queued", "Transferred"),
                        Priority = c("P1", "P2", "P3"))
l <- list(Vendor <- unique(original$Vendor), Category <- unique(original$Category), Problem_Category <- unique(original$Problem_Category),
                    Affected_devices <- unique(original$Affected_devices), Security_engineer <- unique(original$Security_engineer),
                    SLA_MET <- unique(original$SLA_MET), Issue_status <- unique(original$Issue_status), Priority <- unique(original$Priority))

new.data <- do.call(expand.grid,l)
names(new.data) <- c("Vendor","Category","Problem_Category","Affected_devices", "Security_engineer", "SLA_MET", "Issue_status", "Priority")
new.data

# This is how you can fix the problem to get the code from above working.

Vendor           = c("F-Secure", "GE")
Category         = c("Cybersecurity", "IoT", "Machine Learning")
Problem_Category = c("Penetration breach", "Lack of CERT", "APT", "Bad security policies", "Botnet",
                     "Breach in SCADA systems", "Compromised data", "DDoS attack", "Erroneous data load",
                     "Erroneous forecast algorithm", "Hijack of device", "Identity spoofing", "Internal flaws in device",
                     "Lack of appropriate hardware", "Lack of CERT", "Malware installed", "Non-filtered data", "Ransomware virus",
                     "Theft of intellectual property", "Total destruction of data", "Unpatched software", "Wiper attack")
Affected_devices = c("Company main devices", "Mobile devices", "Personal user devices", "Principal devices", "Test devices",
                     "Third party devices")
Security_engineer = c("Alekz Horn", "Annette Smith", "Boris Mikhail", "Dieter Becker", "Florian Klein", "Friederich Voigt",
                      "Gerhard Simon", "Hannes Weber", "Helga Fischer", "Horst Vogel", "Ivan Kolgomorov", "Johannes Dirsch",
                      "Karl Keller", "Klaus Lorenz", "Kristine Schulz", "Kurt Heinz", "Lena Wagner", "Luka Tolso", "Olga Koch",
                      "Pamela Schumacher", "Patrick Benz", "Peter Thomas", "Roger Schmidt", "Sofia Kovalevsky", "Uwe Frank",
                      "Viktor Sauer", "Walter Roth", "Yitin Nguyen")
Reason_for_creating = c("Hourly Analysis", "Bi-weekly Analysis", "Daily Analysis", "Halt Analysis", "Hourly Analysis",
                        "Immediate Analysis", "Monthly Analysis", "Random Analysis", "Special Request", "VIP")
SLA_MET       = c("Yes", "No")
Issue_status  = c("Closed", "In Progress", "Open", "Queued", "Transferred")
Priority      = c("P1", "P2", "P3")

require(reshape2)
df = list(Vendor = Vendor, Category = Category, Problem_Category = Problem_Category, Affected_devices = Affected_devices,
                   Security_engineer = Security_engineer, Reason_for_creating = Reason_for_creating, SLA_MET = SLA_MET,
                   Issue_status = Issue_status, Priority = Priority)
attributes(df)   = list(names = names(df),row.names=1:max(length(Security_engineer), length(SLA_MET)), class='data.frame')

l <- list(Vendor <- unique(df$Vendor), Category <- unique(df$Category), Problem_Category <- unique(df$Problem_Category),
    Affected_devices <- unique(df$Affected_devices), Security_engineer <- unique(df$Security_engineer),
    Reason_for_creating <- unique(df$Reason_for_creating), SLA_MET <- unique(df$SLA_MET), Issue_status <- unique(df$Issue_status),
    Priority <- unique(df$Priority))
new.data <- do.call(expand.grid,l)
names(new.data) <- c("Vendor","Category","Problem_Category","Affected_devices", "Security_engineer", "SLA_MET", "Issue_status", "Priority")
new.data