import requests
import re
import logging

# --- Configuración ---
URL_LOGIN = "http://10.12.171.56:8080/EPD1SFC/System/Login.jsp"
URL_CONSULTA = "http://10.12.171.56:8080/EPD1SFC/L6_Report/PPID_Wip_Tracking.jsp"
URL_LOGOUT = "http://10.12.171.56:8080/EPD1SFC/System/Main.jsp?Logout=true"


USERNAME = "SFC"
PASSWORD = "Newuser01"


# --- Preparar los datos para el POST de login ---
login_data = {
    "Uname": USERNAME,
    "Pwd": PASSWORD
}

STATUS_CRITERIA_REGEX = re.compile(r'(ICT(_| )(REPAIR|R)|R_ICT)')

# R_FBT_REGEX = re.compile(r'R_FBT')

def SFC_check_ICT_Repair(serial_number: str) -> int:
    # threshold = 0
    ICT_Repair_found = 0
    # R_FBT_found = 0

    session = requests.Session()

    login_success = False

    success = False
    try:
        response = session.post(URL_LOGIN, data=login_data)

        if response.status_code in [200, 302]:
            login_success = True
            cookies = session.cookies.get_dict()
            jsessionid = cookies.get('JSESSIONID')
            print(jsessionid)
        if login_success:
            consulta_params = {
                "PPID": serial_number
            }
            consulta_response = session.post(URL_CONSULTA, data=consulta_params, timeout=1)

            if consulta_response.status_code == 200:
                text_resp = consulta_response.text

                found_matches_r_ict = STATUS_CRITERIA_REGEX.findall(text_resp)
                # found_matches_r_fbt = R_FBT_REGEX.findall(text_resp)
                if found_matches_r_ict != None:
                    ICT_Repair_found = len(found_matches_r_ict)
                # if found_matches_r_fbt != None:
                #     R_FBT_found = len(found_matches_r_fbt)
        session.get(f'{URL_LOGOUT}')
    except requests.RequestException:
        logging.debug(f'consult to SFC failed; conection, tried to check the SN:{serial_number}')
    except requests.exceptions.Timeout:
        logging.debug(f'consult to SFC failed; timeout, tried to check the SN:{serial_number}')
    finally:
        session.get(f'{URL_LOGOUT}')

    # threshold = ICT_Repair_found - R_FBT_found

    # if threshold < 0:
    #    threshold = 0

    # return [ICT_Repair_found, threshold]
    return ICT_Repair_found
