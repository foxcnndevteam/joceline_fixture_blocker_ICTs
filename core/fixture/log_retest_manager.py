import os
from core import config

directory_extern_db = os.path.dirname(config.load_raw_config()['extern_db_path'])

directory_retest_logs = os.path.join(directory_extern_db, "retest_logs")

class FailLogFile:
  name_file: str
  lines: list[str]
  lines_num: int

  def __init__(self, serial: str):
    if not os.path.exists(directory_retest_logs):
      os.makedirs(directory_retest_logs)

    self.name_file = os.path.join(directory_retest_logs, f"{serial}-ICT.txt")
    self.lines = []
    self.lines_num = 0

  def __get_lines_num (self) -> int:
    if not os.path.exists(self.name_file):
      return 0

    with open(self.name_file, 'r') as f:
      lines_num = len(f.readlines())
      f.close()
      return lines_num

  def __stringify_parts_failed(self, failed_parts: list[str]) -> str:
    failed_parts_str = ""

    for part_failed in failed_parts:
      if failed_parts_str == '':
        failed_parts_str += f"{part_failed}"
      else:
        failed_parts_str += f",{part_failed}"
    
    return failed_parts_str

  def add_fail(self, failed_parts: list[str]):
    num_lines = self.__get_lines_num()

    failed_parts_str = self.__stringify_parts_failed(failed_parts)

    with open(self.name_file, '+a') as f:
      if num_lines == 0:
        f.write(f'{failed_parts_str}')
      else:
        f.write(f'\n{failed_parts_str}')
      f.close()

  def remove_file(self):
    if os.path.exists(self.name_file):
      os.remove(self.name_file)

  def __read_lines(self) -> list[str]:
    lines = []
    
    with open(self.name_file, 'r') as fr:
      lines_f = fr.readlines()
      self.lines = lines_f
      self.lines_num = len(lines_f)
      fr.close()

    return lines

  def __count_same_fails(self) -> int:
    fails = 0

    test1 = self.lines[0].replace('\n', '').split(',')
    test2 = self.lines[1].replace('\n', '').split(',')

    for t1 in test1:
      if t1 in test2:
        fails += 1

    return fails

  def allow_retest(self) -> bool:
    self.__read_lines()

    if self.lines_num <= 1:
      return True

    if self.lines_num == 2 and not config.get_force_3t():
      same_fails = self.__count_same_fails()
      if same_fails > 0:
        return False
      else:
        return True

    if self.lines_num >= 3:
      return False

    return False