from IPython.core.magic import (register_line_magic, register_cell_magic)
import os
import shutil
import configparser
import pandas as pd
from io import StringIO
import json
from string import Template
import subprocess
import time

import filecmp
import oci
from oci.object_storage.models import CreateBucketDetails
import zipfile
import shutil

@register_line_magic
def setup_jupyter(line):
    if not os.path.isfile("/root/ipython/config/user.ini"):
        print("="*50)
        print("Please create user.ini in /root/ipython/confi")

    # loading user_info
    user_config = configparser.ConfigParser()
    user_config.read('/root/ipython/config/user.ini')
    user_ocid=user_config.get('user_info', 'user_ocid')
    tenancy_ocid=user_config.get('user_info', 'tenancy_ocid')
    region_id=user_config.get('user_info', 'region_id') 

    if not "ocid1.user.oc1" in user_ocid and len(user_ocid) != 76:
        print("Please check user_ocid in 'user.ini'!!!")
        print("Value of user_ocid is invalid.")
        return   
    
    if not "ocid1.tenancy.oc1" in tenancy_ocid and len(tenancy_ocid) != 79:
        print("Please check tenency_ocid in 'user.ini'!!!")
        print("Value of tenency_ocid is invalid.")
        return   

    if not os.path.exists('/root/keys/'):
        os.mkdir('/root/keys/')
    
    base_key_path = "/root/keys/{}".format(user_ocid)

    if not os.path.exists(base_key_path):
        os.mkdir(base_key_path)
    
    if not os.path.exists(base_key_path+'/oci_api_key'):
        str_command='ssh-keygen -b 2048 -t rsa -f {}/oci_api_key  -q -N ""'.format(base_key_path)
        p = subprocess.Popen(str_command, shell=True, stdout=subprocess.PIPE)

    key_file_path=base_key_path+'/oci_api_key'
    time.sleep(1)
    pem_command = 'openssl rsa -in {}/oci_api_key  -pubout -out {}/oci_api_key.pem'.format(base_key_path, base_key_path)
    p = subprocess.Popen(pem_command, shell=True, stdout=subprocess.PIPE)
    time.sleep(1)
    fingerprint_command= 'openssl pkey -in {}/oci_api_key.pem -pubin -pubout -outform DER | openssl md5 -c'.format(base_key_path)
    p = subprocess.Popen(fingerprint_command, shell=True, stdout=subprocess.PIPE)
    result = p.communicate()[0]
    finger_print=result.decode('utf-8')
    finger_print=finger_print.replace("(stdin)= ","")
    finger_print=finger_print.replace("\n","")

    config_template="""[DEFAULT]
user=$user_ocid
fingerprint=$finger_print
key_file=$key
tenancy=$tenancy_ocid
region=$region"""
    
    src = Template(config_template)
    data={ 
        'user_ocid':user_ocid, 
        'tenancy_ocid':tenancy_ocid,
        'finger_print':finger_print, 
        'region':region_id,
        'key':key_file_path
    }
    result = src.substitute(data)

    if not os.path.exists('/root/.oci'):
        os.mkdir('/root/.oci')
    
    with open('/root/.oci/config', "w") as file:
        file.write(result)

    print("- 아래 공개키를 OCI 사용자 API 키로 등록하시기 바랍니다. ")
    print()
    print("="*50)
    print("Finger Print: "+finger_print)
    print("="*50)
    print()
    print("="*50)    
    print("public key")
    print("="*50)
    print()
            
    with open('/root/keys/'+user_ocid+'/oci_api_key.pem') as f:
        publickey = f.read()
        print(publickey)
    
    print()
    print("="*50)


    os.chmod('/root/keys/'+user_ocid+'/oci_api_key', 0o600)
    os.chmod('/root/.oci/config', 0o600)

    print("- 위 공개키를 OCI 계정에 등록했면, ")
    print("- 새로운 Cell에서 다음 명령을 실행하여 설정 상태를 확인해 주세요.")
    print("="*50)
    print("!oci os ns get")


@register_cell_magic
def config_db_info(line, cell):

    lines = cell.splitlines()
    [key0, adb_id] = lines[0].split("=")
    adb_id = adb_id.strip()
    if not key0.strip() == "adb_id":
        print("- 첫번째 옵션 에러: adb_id")
        print("- 첫번째 옵션을 확인해 주세요.")
        return

    [key1, user] = lines[1].split("=")
    user = user.strip()
    if not key1.strip() == "user":
        print("- 두번째 옵션 에러: user")
        print("- 두번째 옵션을 확인해 주세요.")
        return 

    [key2, password] = lines[2].split("=")
    password = password.strip()
    if not key2.strip() == "password":
        print("- 세번째 옵션 오류: password")
        print("- 세번째 옵션을 확인해 주세요.")
        return

    [key3, profile] = lines[3].split("=")
    profile = profile.strip()
    if not key3.strip() == "profile":
        print("- 네번째 옵션 오류: profile")
        print("- 네번째 옵션을 확인해 주세요. ")
        return 

    config = configparser.ConfigParser()
    config.read('/root/ipython/config/adb.ini')
    sections = config.sections()
    if not adb_id in sections:
        config.add_section(adb_id)
    
    config.set(adb_id, "user", user)
    config.set(adb_id, "password", password)
    config.set(adb_id, "profile", profile)

    with open('/root/ipython/config/adb.ini', 'w') as configfile:    
        config.write(configfile)  

    print("- 설정 파일(/root/ipython/config/adb.ini) 저장 완료.")
    print("- 현재 Cell은 중요 정보가 포함되어 있습니다.") 
    print("- 현재 Cell은 삭제해 주세요.") 

@register_line_magic
def list_compartments(line):
    config = oci.config.from_file()
    tenancy_id = config["tenancy"]
    identity = oci.identity.IdentityClient(config)
    list_compartments_response = oci.pagination.list_call_get_all_results(
        identity.list_compartments,
        compartment_id=tenancy_id).data

    str = "Name, Compartment ID\n"

    root=identity.get_compartment(tenancy_id).data
    str = str + "{}, {}\n".format("root", root.id)

    for c in list_compartments_response:
        detail=identity.get_compartment(c.id).data
        str = str + "{}, {}\n".format(detail.name, detail.id)

    sio = StringIO(str)
    pd.set_option('max_colwidth',90)
    return pd.read_csv(sio)

## magic for autonomous database
@register_cell_magic 
def list_adb(line, cell):
    cell = cell.strip()
    [key0, compartment_id] = cell.split("=")
    compartment_id = compartment_id.strip()
    if not key0.strip() == "compartment_id":
        print("- 옵션 에러: compartment_id")
        print("- 첫번째 옵션을 확인해 주세요.")
        return

    config = oci.config.from_file()
    db_list_client = oci.database.DatabaseClient(config)
    response = db_list_client.list_autonomous_databases(compartment_id)

    str = "DB Name, Workload, CPU, Storage(TB),Status,Auto Scaling, ID\n"
    for db in response.data:
        str = str+"{},{},{},{},{},{},{}\n".format(db.db_name,
        db.db_workload,
        db.cpu_core_count,
        db.data_storage_size_in_tbs,
        db.lifecycle_state,
        db.is_auto_scaling_enabled,
        db.id) 

    sio = StringIO(str)
    pd.set_option('max_colwidth',110)
    return pd.read_csv(sio)

@register_cell_magic 
def stop_adb(line, cell):
    cell = cell.strip()
    [key0, adb_ocid] = cell.split("=")
    adb_ocid = adb_ocid.strip()
    if not key0.strip() == "adb_ocid":
        print("- 옵션 에러: adb_ocid")
        print("- 첫번째 옵션을 확인해 주세요.")
        return

    config = oci.config.from_file()
    db_list_client = oci.database.DatabaseClient(config)
    response = db_list_client.stop_autonomous_database(adb_ocid)
    print("ADB 종료중:{}".format(response.data.db_name))

@register_cell_magic 
def start_adb(line, cell):
    cell = cell.strip()
    [key0, adb_ocid] = cell.split("=")
    adb_ocid = adb_ocid.strip()
    if not key0.strip() == "adb_ocid":
        print("- 옵션 에러: adb_ocid")
        print("- 첫번째 옵션을 확인해 주세요.")
        return

    config = oci.config.from_file()
    db_list_client = oci.database.DatabaseClient(config)
    response = db_list_client.start_autonomous_database(adb_ocid)
    print("ADB 시작중:{}".format(response.data.db_name))

@register_cell_magic 
def delete_adb(line, cell):
    cell = cell.strip()
    [key0, adb_ocid] = cell.split("=")
    adb_ocid = adb_ocid.strip()
    if not key0.strip() == "adb_ocid":
        print("- 옵션 에러: adb_ocid")
        print("- 첫번째 옵션을 확인해 주세요.")
        return

    config = oci.config.from_file()
    db_list_client = oci.database.DatabaseClient(config)
    response = db_list_client.delete_autonomous_database(adb_ocid)
    print("ADB 인스턴스 삭제 시작.")

@register_cell_magic
def change_adb(line, cell):

    lines = cell.splitlines()
    [key0, adb_ocid] = lines[0].split("=")
    adb_ocid = adb_ocid.strip()
    if not key0.strip() == "adb_ocid":
        print("- 첫번째 옵션 에러: adb_ocid")
        print("- 첫번째 옵션을 확인해 주세요.")
        return

    [key1, cpu] = lines[1].split("=")
    cpu = cpu.strip()
    if not key1.strip() == "cpu":
        print("- 두번째 옵션 에러: cpu")
        print("- 두번째 옵션을 확인해 주세요.")
        return 

    [key2, storage] = lines[2].split("=")
    storage = storage.strip()
    if not key2.strip() == "storage":
        print("- 세번째 옵션 오류: storage")
        print("- 세번째 옵션을 확인해 주세요.")
        return         

    config = oci.config.from_file()
    db_client = oci.database.DatabaseClient(config)
    adb_request = oci.database.models.UpdateAutonomousDatabaseDetails()

    adb_request.cpu_core_count = int(cpu)
    adb_request.data_storage_size_in_tbs = int(storage)

    adb_response = db_client.update_autonomous_database(
        adb_ocid,
        update_autonomous_database_details=adb_request,
        retry_strategy=oci.retry.DEFAULT_RETRY_STRATEGY)
    print("ADB 인스턴스 변경 시작:{}".format(adb_response.data.db_name))

@register_cell_magic
def create_adb(line, cell):
    lines = cell.splitlines()
    [key0, compartment_id] = lines[0].split("=")
    compartment_id = compartment_id.strip()
    if not key0.strip() == "compartment_ocid":
        print("- 1번째 옵션 에러: compartment_ocid")
        print("- 1번째 옵션을 확인해 주세요.")
        return

    [key1, cpu] = lines[1].split("=")
    cpu = cpu.strip()
    if not key1.strip() == "cpu":
        print("- 2번째 옵션 에러: cpu")
        print("- 2번째 옵션을 확인해 주세요.")
        return 

    [key2, storage] = lines[2].split("=")
    storage = storage.strip()
    if not key2.strip() == "storage":
        print("- 3째 옵션 오류: storage")
        print("- 3째 옵션을 확인해 주세요.")
        return

    [key3, db_name] = lines[3].split("=")
    db_name = db_name.strip()
    if not key3.strip() == "db_name":
        print("- 4째 옵션 오류: db_name")
        print("- 4째 옵션을 확인해 주세요. ")
        return 

    [key4, display_name] = lines[4].split("=")
    display_name = display_name.strip()
    if not key4.strip() == "display_name":
        print("- 5번째 옵션 오류: display_name")
        print("- 5번째 옵션을 확인해 주세요. ")
        return 

    [key5, workload] = lines[5].split("=")
    workload = workload.strip()
    if not key5.strip() == "workload":
        print("- 6번째 옵션 오류: workload")
        print("- 6번째 옵션을 확인해 주세요. ")
        return     

    [key6, password] = lines[6].split("=")
    password = password.strip()
    if not key6.strip() == "password":
        print("- 7번째 옵션 오류: password")
        print("- 7번째 옵션을 확인해 주세요. ")
        return   
    
    [key7, auto_scaling] = lines[7].split("=")
    auto_scaling = auto_scaling.strip()
    if not key7.strip() == "auto_scaling":
        print("- 8번째 옵션 오류: auto_scaling")
        print("- 8번째 옵션을 확인해 주세요. ")
        return           

    config = oci.config.from_file()
    db_client = oci.database.DatabaseClient(config)
    adb_request = oci.database.models.CreateAutonomousDatabaseDetails()

    adb_request.compartment_id = compartment_id
    adb_request.cpu_core_count = int(cpu)
    adb_request.data_storage_size_in_tbs = int(storage)
    adb_request.db_name = db_name
    adb_request.display_name = display_name
    adb_request.db_workload = workload
    adb_request.license_model = adb_request.LICENSE_MODEL_BRING_YOUR_OWN_LICENSE

    adb_request.admin_password = password
    adb_request.is_auto_scaling_enabled = bool(auto_scaling)

    adb_response = db_client.create_autonomous_database(
        create_autonomous_database_details=adb_request,
        retry_strategy=oci.retry.DEFAULT_RETRY_STRATEGY)
    print("ADB 인스턴스 생성 시작:{}".format(adb_response.data.db_name))

@register_cell_magic 
def use_adb(line, cell):
    cell = cell.strip()
    [key0, adb_ocid] = cell.split("=")
    adb_ocid = adb_ocid.strip()
    if not key0.strip() == "adb_ocid":
        print("- 옵션 에러: adb_ocid")
        print("- 첫번째 옵션을 확인해 주세요.")
        return    

    TNS_ADMIN_DIR=os.environ["TNS_ADMIN_DIR"]
    shutil.rmtree(TNS_ADMIN_DIR, ignore_errors=True)
    os.mkdir(TNS_ADMIN_DIR)

    if not os.path.exists('/root/wallets/'):
        os.mkdir('/root/wallets/')
    
    adb_wallet_dir = "/root/wallets/{}".format(adb_ocid)

    if not os.path.exists(adb_wallet_dir):
        os.mkdir(adb_wallet_dir)
    
    adb_wallet_path = "{}/wallet.zip".format(adb_wallet_dir)
    
    if not os.path.exists(adb_wallet_path):
        command= 'oci db autonomous-database generate-wallet --autonomous-database-id {} --password Welcome123456 --file /root/wallets/{}/wallet.zip'.format(adb_ocid, adb_ocid)
        p = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE)

    ##환경 변수 설정
    config = configparser.ConfigParser()
    config.read('/root/ipython/config/adb.ini')
    sections = config.sections()
    if not adb_ocid in sections:
        print("- ADB 설정 오류")
        print("- %%config_db_info를 이용하여 데이터베이스 정보를 설정해야 합니다.")
        return 
    
    user = config.get(adb_ocid, "user")
    password = config.get(adb_ocid, "password")
    profile = config.get(adb_ocid, "profile")

    config = oci.config.from_file()
    db_list_client = oci.database.DatabaseClient(config)
    data = db_list_client.get_autonomous_database(adb_ocid).data

    os.environ['SQLPLUS_TNS_STR']=user+"/"+password+"@"+data.db_name+"_"+profile
    conn_str = "oracle+cx_oracle://"+user+":"+password+"@"+data.db_name+"_"+profile
    os.environ['PY_CONNECTION_STR']=conn_str

    time.sleep(2)

    with zipfile.ZipFile(adb_wallet_path, 'r') as zip_ref:
        zip_ref.extractall(TNS_ADMIN_DIR)
    
    os.remove('/root/tns/sqlnet.ora')
    shutil.copyfile('/root/.oci_jupyter/sqlnet.ora' , '/root/tns/sqlnet.ora' )

    message = "- Database({}) 설정 완료!!!".format(data.db_name)
    print(message) 

    conn_str = os.environ['PY_CONNECTION_STR']    
    ipython = get_ipython()
    print(ipython.run_line_magic("sql", conn_str))
    print("Connected with ADW.")

@register_line_magic
def connect_db(line):
    conn_str = os.environ['PY_CONNECTION_STR']
    ipython = get_ipython()
    print(ipython.run_line_magic("sql", conn_str))
    print("Connected with ADW.")

@register_cell_magic
def script(line, cell):
    conn_str = os.environ['SQLPLUS_TNS_STR']


    script = "sqlplus -s "+ conn_str + " <<EOF \n\n"
    script = script + cell + "\n\n"
    script = script + "EOF"

    ipython = get_ipython()
    ipython.run_cell_magic("sh", "", script)

def load_ipython_extension(ipython):
    ipython.register_magic_function(setup_jupyter, "line", 'setup_jupyter')
    ipython.register_magic_function(list_compartments, "line", 'list_compartments')
    ipython.register_magic_function(config_db_info, "cell", 'config_db_info')

    ipython.register_magic_function(list_adb, "cell", 'list_adb')
    ipython.register_magic_function(stop_adb, "cell", 'stop_adb')
    ipython.register_magic_function(start_adb, "cell", 'start_adb')
    ipython.register_magic_function(delete_adb, "cell", 'delete_adb')
    ipython.register_magic_function(create_adb, "cell", 'create_adb')
    ipython.register_magic_function(change_adb, "cell", 'change_adb')
    ipython.register_magic_function(use_adb, "cell", 'use_adb')
    ipython.register_magic_function(connect_db, "line", 'connect_db')
    ipython.register_magic_function(script, "cell", 'script')


    
    

    
    
