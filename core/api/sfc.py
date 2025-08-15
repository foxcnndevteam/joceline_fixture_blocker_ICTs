import requests
import re
import logging

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

STATUS_CRITERIA_REGEX = re.compile(r'(ICT(_| )(REPAIR|R)|R_ICT)')

def SFC_check_ICT_Repair(serial_number: str) -> int:
    ICT_Repair_found = 0

    session = requests.Session()

    login_success = False

    success = False
    try:
        response = session.post(URL_LOGIN, data=login_data)

        if response.status_code in [200, 302]:
            login_success = True

        if login_success:
            consulta_params = {
                "PPID": serial_number
            }
            consulta_response = session.post(URL_CONSULTA, data=consulta_params, timeout=1)

            if consulta_response.status_code == 200:
                text_resp = consulta_response.text

                found_matches = STATUS_CRITERIA_REGEX.findall(text_resp)
                if found_matches != None:
                    ICT_Repair_found = len(found_matches)
    except requests.RequestException:
        logging.debug(f'consult to SFC failed; conection, tried to check the SN:{serial_number}')
    except requests.exceptions.Timeout:
        logging.debug(f'consult to SFC failed; timeout, tried to check the SN:{serial_number}')

    return ICT_Repair_found

