# Barangay Residents and Population Information System DOCUMENTATION

 ---

## Project Overview
**Barangay Residents and Population Information System**  is a web-based application designed to modernize local government administration. It allows barangay officials and staff to record, manage, and securely retrieve resident profiles, while generating real-time population-related summaries and demographic reports. This digital system replaces manual, paper-based workflows to ensure faster data processing, higher data integrity, and organized community tracking. 


---

## Main Features

*Resident Management*
- Allows staff to add, edit, view, and update resident information
- Staff can securely open and view the complete recorded details of an individual resident. Can search/filter (by name, sex, age) to find resident profiles in the registry without manual sorting

*Household & Family Mapping*
- Can create unique household records, dynamically link individual residents to their respective family units, ensuring an organized household roster.

*Population Reports*
- Generates an automated summary showing the total population count of the barangay. 
- Tracks and monitors data regarding the number of residents mapped inside each home. 
- Breaks down current population statistics based on specific age groups and sex distribution. 
- Allows users to easily export or print generated census sheets for documentation and planning 

*User Accounts & Access Control*
- Log in for Barangay Staff/Officers: Has a secure gateway interface for authorized personnel authentication
- Restricts system modules by tiers (Admin, Encoder, Viewer) to protect private records.
- Limits who can edit sensitive records and how much data they can view 

*Data Integrity & Tracking*
- Basic Audit Trail: Implements a background log tracking exactly who created or updated a record and when.
- Validation for required fields (e.g., birthdate, name format) 

---
## Typical Use-cases
- Barangay staff registers new residents and assigns them to the correct household.
- Barangay officer searches a resident’s record instantly.
- The barangay generates a report such as total population, number of households, and
demographic breakdowns.

---

## Tech Stack
- **Backend**: Python
- **Frontend**: Streamlit
- **Simulated Data Base**: SQLite
- **Libraries**: pandas, streamlit, sqlite3, matplotlib.pyplot, datetime

---

## Prerequisites
- *Python (3.12.3+)*
- *pip*
- *Virtual environment setup*

---

## How to Setup
- *Clone the repo*
- *Create a virtual environment and activate*
- *Install the required libraries (pandas, streamlit, sqlite3, matplotlib.pyplot, datetime)*
- *Verify if database files exist in the main folder* 

---


## How to deploy the app locally

*Run the Streamlit server from your main project workspace folder:*
- streamlit run app.py

---

## System Integration Workflow

[Physical / Digital Intake Form]
              |
              v
   [Data Capture & Encoders] ----> [Input Validation Filters]
                                              |
                                              v
 [Real-Time Analytics & Reports] <---- [Secure Database Store]


## System Access Control

| Feature Modules              | Admin Role  | Encoder Role | Viewer Role |

| **System Configurations**    | Full Access | No Access    | No Access |
| **Add/Edit Profiles**        | Full Access | Full Access  | No Access |
| **View Audit Trails**        | Full Access | No Access    | No Access |
| **Search / Filter Records**  | Full Access | Full Access  | Limited Access |
| **Export/Print Reports**     | Full Access | Full Access  | Limited Access |


## Validation and Security Protocols

*Mandatory Input fields*
- All critical identifier inputs (Names, brhdates, addresses) mustt match specific regex rules before parsing to database files. Blank submissions are rejected automatically.

*Privacy Impact Assessment(PIA)*
- Sensitive data points such as birthdates and specific address strings are hidden behind API token guardrails
Changes to any profile row trigger a non-destructible log writing the User ID, Action Type, and Timestamp.


## How to Use
*Barangay Staff*
- Select the add resident option in the sidebar
- Input the required resident details in the mandatory fields
- Click the save new resident to save the record to the database
- Select the view profile option to view or modify the profile data

*Barangay Officer*
- Search and filter through the complete resident registry by name, sex, or age
- Export or print the generated population and household summaries

---

## System Limitations
- Relies on basic local field-level validation protocols
- Future developers must introduce end-to-end field encryption for data-at-rest and implement multi-factor authentication (MFA) for administrative logins to fully secure local data pools.
- Deployed only locally through a local Streamlit server instead of a production cloud web service.
- Relies on a local file-based SQLite database (Residents.db and Users.db) stored inside the workspace directory, which can risk data loss if deleted or overwritten during local development.


## Contributors

*Back end*
### [**Demate, Ace**] (https://github.com/PixelatedCorn)
- Backend Features
- Project idea
- Prototype


### [**Diaz, Marcus**] (https://github.com/Marribel)
- Backend Features
- Project Idea
- Prototype

### [**Belen, James**] (https://github.com/jameszup)
- Backend Features

*Front end*
### [**Nebrao, Faith**] (https://github.com/fey3)
- Frontend UI

### [*Erro, Keith**] (https://github.com/Kerro-orre)
- Frontend UI

*Documentation*
### [**Barcil, Angel**] (https://github.com/zyeayi)
- Documentation
- Bug Testing
