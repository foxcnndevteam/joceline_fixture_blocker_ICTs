import requests
import re

# --- Configuración ---
URL_LOGIN = "http://10.12.171.56:8080/EPD1SFC/System/Login.jsp"
URL_CONSULTA = "http://10.12.171.56:8080/EPD1SFC/L6_Report/PPID_Wip_Tracking.jsp"

USERNAME = "SFC"
PASSWORD = "Newuser01"


# --- Preparar los datos para el POST de login ---
login_data = {
    "Uname": USERNAME,
    "Pwd": PASSWORD
}

STATUS_CRITERIA_REGEX = re.compile(r'ICT(_| )REPAIR')

STATUS_CRITERIA = "ICT REPAIR"

STATUS_CRITERIA_LEN = len(STATUS_CRITERIA)

def SFC_check_ICT_Repair(serial_number: str) -> int:
    ICT_Repair_found = 0

    session = requests.Session()

    login_success = False

    success = False

    response = session.post(URL_LOGIN, data=login_data)


    if response.status_code in [200, 302]:
        login_success = True

    if login_success:
        consulta_params = {
            "PPID": serial_number
        }
        consulta_response = session.post(URL_CONSULTA, data=consulta_params)
    
        if consulta_response.status_code == 200:
            text_resp = consulta_response.text

            if STATUS_CRITERIA in text_resp:
                
                for i in range(0, len(text_resp)):
                    start = i
                    end = i + STATUS_CRITERIA_LEN

                    text_chunk = text_resp[start:end]
                    if STATUS_CRITERIA == text_chunk:
                        ICT_Repair_found += 1

    return ICT_Repair_found

