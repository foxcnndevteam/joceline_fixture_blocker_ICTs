import requests
# import os
# from env import BASE_DIR
# from threading import Thread
import subprocess

URL_BASE="http://localhost:5000"

API_URL=f"{URL_BASE}/api"

def eval_tunnel_conection():
  is_tunnel_alive = False
  
  # result_ping = os.system(f"ping 10.12.206.101 -n 1 -w 100")
  # if result_ping != 0:
  #   is_tunnel_alive = False
  #   return is_tunnel_alive

  try:
    response_result = requests.get(f"{URL_BASE}", timeout=(1,1))
    is_tunnel_alive = True
  except requests.ConnectionError:
    is_tunnel_alive = False
  except requests.exceptions.Timeout:
    is_tunnel_alive = False
  return is_tunnel_alive

def get_config(station: str, ssh_key = None) -> dict | None:
  # created = create_tunnel_ssh(ssh_key)
  # if not created:
  #   return None
  try:
    resp = requests.get(f"{API_URL}/config/{station}", timeout=(1,1))
    if resp.status_code == 200:
      return resp.json()
    return None
  except requests.Timeout:
    return None
  except requests.ConnectionError as ce:
    return None
  except requests.JSONDecodeError as je:
    return None

def send_fixture_state(station: str, state: str, yield_rate):
  try:
    resp = requests.post(f"{API_URL}/state/{station}", timeout=(1, 1), json={ "state": state, "yield": yield_rate })

    if resp.status_code in [200, 201]:
      print("status sended successfully")
  except requests.ConnectionError as ce:
    pass
  except requests.JSONDecodeError as je:
    pass
  except requests.exceptions.Timeout:
    pass

def eval_retest(sn: str):
  result_final = { 'success': False, 'retest': True }

  try:
    result_response = requests.get(f"{API_URL}/records?serial_number={sn}&test_name=ICT&execution_mode=ONLINE&test_result=FAIL")
    
    if result_response.status_code == 200:
      result_json = result_response.json()
      success = result_json['success']
      count = result_json['count']

      result_final['success'] = success
      result_final['retest'] = count > 1
  except requests.ConnectionError:
    pass

  return result_final


def register_test(data: dict):
  try:
    result_response = requests.post(f"{API_URL}/records", json=data, headers={ 'Content-Type': 'application/json' })
    if result_response.status_code in [200,201]:
      print("resultado enviado")
    else:
      print(result_response.content)
  except requests.ConnectionError:
    print('conn error')

def start_tunel(ssh_key_path):
  
  subprocess.Popen(['ssh', '-i', ssh_key_path, '-f', '-N', '-L', '5000:localhost:5000', 'kintaro@10.12.206.101'], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

def create_tunnel_ssh(ssh_key = None) -> bool:
  if ssh_key == None:
    print("conection failed: missing private key")
    return False

  tunnel_alive = eval_tunnel_conection()
  if tunnel_alive:
    return True

  # ssh_key_path = os.path.join(BASE_DIR, ssh_key)
  # print("tunel start")
  # thr = Thread(target=start_tunel, args=(ssh_key_path,))
  # thr.start()
  # print("tunel started")
  return True

