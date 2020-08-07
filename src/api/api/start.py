from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from zabbix_host_obtain import zabbix_group_obtain as group
from zabbix_host_obtain import host_per_groups as host_group
from zabbix_host_obtain import zabbix_metrics as metrics
from zabbix_host_obtain import host_per_server as host_server
from zabbix_host_obtain import full_sort
from zabbix_host_obtain import futura
import json
import os
from db_handler import insert_data, find_data, drop, get_collection
import time


app = FastAPI()
app.add_middleware(CORSMiddleware, allow_origins=[
                   '*'], allow_methods=['*'], allow_headers=['*'])

gropups_list = list()


class OK(BaseModel):
    service: str


class Zabb_Conf(BaseModel):
    ip: str
    usuario: str
    password: str
    user_actual: str
    user_new: str
    start_time: str
    end_time: str


service_list = ['Proxys', "DNS", "Correo",
                "Firewalls", 'FTP', "Web", 'Otros']

id_groups_list = list()
hipervisor_list = ['LXC', 'KVM']
lista = list()
id_server_group = list()
full_sort_dict = dict()

@app.post('/zabb_conf')
def zabbix_conf(data: Zabb_Conf):


    # Convert data to dict 
    zabbix_credentials = data.dict()
    print(zabbix_credentials)
        # Drop Database for store new values
    drop('lilipad')
    
    # Obtain all groups from Zabbix Server
    groups = group(
        zabbix_credentials['ip'], zabbix_credentials['usuario'], zabbix_credentials['password'])


    for hipervisor in hipervisor_list:
        
        # Add hipervisor group id 
        id_groups_list.append(groups[hipervisor])

        # Obtain all host for hipervisor (LXC and KVM)
        lista = host_group(
            zabbix_credentials['ip'], zabbix_credentials['usuario'], zabbix_credentials['password'],
            int(groups[hipervisor]))
        
        # Add '_id' field to the dict for store in a Mongo DB database 
        lista['_id'] = hipervisor
        
        # Insert data to the MongoDB database
        insert_data(collection='host_per_hipervisor', data=lista)
        
        # Clear list for next iteration
        lista.clear()
    
    # Obtain all lxc services
    lxc_hipervisor = find_data(
        collection='host_per_hipervisor', data={'_id': 'LXC'})

    # Obtain all kvm service
    kvm_hipervisor = find_data(
        collection='host_per_hipervisor', data={'_id': 'KVM'})
    
    
    for service in service_list:
        lxc_service = dict()
        kvm_service = dict()

        # Obtain all host for each service ('Proxys', "DNS", "Correo","Firewalls", 'FTP', "Web", 'Otros')
        host = host_group(
            zabbix_credentials['ip'], zabbix_credentials['usuario'], zabbix_credentials['password'],
            int(groups[service]))
        
        # Create a set with service for hipervisor
        key_service = set(host.keys())
        lxc_intercept = key_service & set(lxc_hipervisor.keys())
        kvm_intercept = key_service & set(kvm_hipervisor.keys())

        # Check if exist service for LXC hipervisor
        try:
            for element in lxc_intercept:
                # print(lxc_hipervisor[element])
                lxc_service[element] = lxc_hipervisor[element]
            
            # Create the MongoDB id of teh form ServiceHipervisor example: SquidLXC, CorreoKVM
            lxc_service['_id'] = service+'LXC'
            lxc_service['hipervisor'] = 'LXC'

            # Insert data in the Database
            insert_data(collection='host_per_service', data=lxc_service)
        except:
            pass

        # Same proccess for the KVM hipervisor
        try:
            for element in kvm_intercept:
                kvm_service[element] = kvm_hipervisor[element]
            kvm_service['_id'] = service+'KVM'
            kvm_service['hipervisor'] = 'KVM'
            insert_data(collection='host_per_service', data=kvm_service)
        except:
            pass

        # Clear all variables for next iteration
        lxc_service.clear()
        kvm_service.clear()
        host.clear()

    # Obtain all host of the Servidores group
    servers = host_group(
        zabbix_credentials['ip'], zabbix_credentials['usuario'], zabbix_credentials['password'],
        int(groups['Servidores']))


    # Creata list that will be passed for obtain all host from a server
    for server in servers:
        full_sort_dict[server] = int(groups[server])
        id_server_group.append(int(groups[server]))

    # Obtain all host for every server
    servers = host_server(
        zabbix_credentials['ip'], zabbix_credentials['usuario'], zabbix_credentials['password'], full_sort_dict)
    
    # Create a sort list for host with basic info
    full_sort(full_sort_dict, hipervisors=hipervisor_list,
              services=service_list)

    # Caluculating metric for all hosts
    metrics(ip_zabbix=zabbix_credentials['ip'], user_zabbix=zabbix_credentials['usuario'], password_zabbix=zabbix_credentials['password'],
            st=zabbix_credentials['start_time'], et=zabbix_credentials['end_time'], user_actual=zabbix_credentials['user_actual'], user_new=['user_new'])

    # Calculatong the user relation
    user_relation = int(zabbix_credentials['user_new']) / \
        int(zabbix_credentials['user_actual'])

    # Future estimation
    futura(user_relation)
    return 'Process Done!!!'


@app.get('/actual')
# @app.route('/actual', methods=['GET'])
def actual_send():
    list_actual = list()
    try:
        actuals = get_collection('metrics')
        for host in actuals:
            del host['_id']
            list_actual.append(host)
    except:
        pass
    return list_actual

@app.get('/futura')
def futura_send():
    list_futura = list()
    try:
        future = get_collection('future')
        for host in future:
            del host['_id']
            list_futura.append(host)
    except:
        pass
    return list_futura



#     if __name__ == '__main__':
#         zabbix_conf({"ip" :"str",
#     "usuario" :"str",
#     "password" :"str",
#     "user_actual" :"str",
#     "user_new" :"str",
#     "start_time" :"dd/mm/yyyy",
#     "end_time" :"dd/mm/yyyy"}
# )
        