import requests
import os
from env import BASE_DIR
from core.config import ssh_key
import subprocess

URL_BASE="http://localhost:3000"

API_URL=f"{URL_BASE}/api"

def eval_tunnel_conection():
  is_tunnel_alive = False

  try:
    response_result = requests.get(f"{URL_BASE}")
    if response_result.status_code == 200:
      is_tunnel_alive = True
  except requests.ConnectionError:
    is_tunnel_alive = False

  return is_tunnel_alive

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
  except requests.ConnectionError:
    print('conn error')

def create_tunnel_ssh():
  if ssh_key == None:
    print("conection failed: missing private key")
    return

  ssh_key_path = os.path.join(BASE_DIR, ssh_key)


