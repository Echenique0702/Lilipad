from pyzabbix import ZabbixAPI
from datetime import datetime, timedelta
import time
from statistics import mean
from numpy import percentile, array
from db_handler import insert_data
from db_handler import find_data
from db_handler import get_collection


# Variables declaration

relation_group_groupip = dict()
relation_hostname_hostid = dict()
service_list = ['CPU system time', 'iostat.sda', 'read.sda', 'write.sda', 'RAM-used',
                'Used disk space on /', 'Incoming network traffic on eth0', 'Outgoing network traffic on eth0']

metric_relation = {'CPU system time': 'cpu_', 'iostat.sda': 'iost_', 'read.sda': 'read_', 'write.sda': 'write_', 'RAM-used': 'ram_',
                   'Used disk space on /': 'disk_', 'Incoming network traffic on eth0': 'inco_', 'Outgoing network traffic on eth0': 'outc_'}

server_list = ['CPU system time', 'iostat.sda', 'read.sda', 'write.sda', 'RAM-used', 'Total disk space on /',
               'RAM-total', 'Used disk space on /', 'Incoming network traffic on bond0', 'Outgoing network traffic on bond0']

kvm_list = []

list_future = ['cpu_', 'iost_',  'read_',
               'write_', 'ram_', 'disk_', 'inco_', 'outc_']


# Obtain all groups from Zabbxi Server
def zabbix_group_obtain(ip_zabbix: str, user_zabbix: str, password_zabbix: str):

    # Client for connect to the zabbix server
    zapi = ZabbixAPI("http://"+ip_zabbix+"/zabbix")
    zapi.login(user=user_zabbix, password=password_zabbix)

    # Obtain all groups from Zabbix Server
    groups = zapi.hostgroup.get()

    # Cretae dict for return it 
    for group in groups:
        relation_group_groupip[group['name']] = group['groupid']

    return relation_group_groupip


# Obtain all host from a specific group
def host_per_groups(ip_zabbix: str, user_zabbix: str, password_zabbix: str, services: int):
    
    # Client for connect to the Zabbix Server 
    zapi = ZabbixAPI("http://"+ip_zabbix+"/zabbix")
    zapi.login(user=user_zabbix, password=password_zabbix)

    # Obtain all host for a group
    hosts = zapi.host.get(groupids=[services])

    # Create dict for return
    for host in hosts:
        relation_hostname_hostid[host['name']] = host['hostid']
    
    return relation_hostname_hostid

# Obtain all host for a server
def host_per_server(ip_zabbix: str, user_zabbix: str, password_zabbix: str, servers: dict):

    # Client for connect to the Zabbix Server
    zapi = ZabbixAPI("http://"+ip_zabbix+"/zabbix")
    zapi.login(user=user_zabbix, password=password_zabbix)
    
    for server in servers:
        # For server obtain the hosts inside the group named like server
        hosts = zapi.host.get(groupids=servers[server], output=['name', 'hostid'])

        # Get server hostid for get cpu-frecuency
        host_id = zapi.host.get(filter={"host":server},output=['hostids'])

        # Get server tags
        tags = zapi.host.get(hostids= host_id[0]['hostid'],output="extend",selectTags="extend")[0]['tags']
        
        # Get cpu-frecuency
        for tag in tags:
            if tag['tag'] == 'cpu-frecuency':
                frecuency_cpu = float(tag['value'])
        
        # Create a dicc for return
        dicc_return = {'_id': servers[server],'proxmox_name': server, 'cpu_frecuency': frecuency_cpu,'service': hosts}

        # Insert data at the Database
        insert_data('host_per_server', dicc_return)

    return 'Ok'

# Create list for consult host
def full_sort(servers: dict, hipervisors: list, services: list):

    for server in servers: 
        host_sort = dict()

        # Obtain host for a specific server
        server_loaded = find_data('host_per_server', {'_id': servers[server]})

        try:
            # Sort the host and de hostid for server
            for host in server_loaded['service']:
                host_sort[host['name']] = host['hostid']

            # Obtain host for hipervisor for server
            for hipervisor in hipervisors:
                for service in services:
                    service_host = find_data(
                        collection='host_per_service', data={'_id': service+hipervisor})

                    # Set Service + Hipervisor + Server 
                    intercept_hipervisor = set(
                        host_sort.keys()) & set(service_host.keys())
                    if intercept_hipervisor:

                        # Preparing data for insert in the database
                        for element in list(intercept_hipervisor):
                            full_sort_dicc = dict()
                            full_sort_dicc['name'] = element
                            full_sort_dicc['service'] = service
                            full_sort_dicc['hipervisor'] = hipervisor
                            full_sort_dicc['hostid'] = host_sort[element]
                            full_sort_dicc['server'] = server
                            insert_data('full_sort', full_sort_dicc)
        except:
            pass
    return 'Ok'

# Get metric form zabbix server
def zabbix_metrics(ip_zabbix: str, user_zabbix: str, password_zabbix: str, st: str, et: str, user_actual: int, user_new: int):

    # Client for connect to the zabbix server
    zapi = ZabbixAPI("http://"+ip_zabbix+"/zabbix")
    zapi.login(user=user_zabbix, password=password_zabbix)
    
    # Time convertion for the correct format
    time_till = time.mktime(datetime.strptime(et, "%d/%m/%Y").timetuple())
    time_from = time.mktime(datetime.strptime(st, "%d/%m/%Y").timetuple())
    
    # Get all host
    hosts = get_collection('full_sort')

    # Make mapping for cpu-frecuency
    server_host = get_collection("host_per_server")
    dicc_mapping_cpu_host = dict()
    for server in server_host:
        for host in server['service']:
            dicc_mapping_cpu_host[host['hostid']] = server['cpu_frecuency']
    
    for host in hosts:
        # print(host)
        
        # Creatind dicc for store in a database
        dicc_service = dict()
        dicc_service['name'] = host['name']
        dicc_service['server'] = host['server']
        dicc_service['hipervisor'] = host['hipervisor']        
        dicc_service['service'] = host['service']
        dicc_service['hostid'] = host['hostid']
        list_metrics = list()
        dicc_metrics = dict()
        
        # Get server tags
        tags = zapi.host.get(hostids= host['hostid'],output="extend",selectTags="extend")[0]['tags']
        # print(tags)
        
        # # Get cpu-frecuency
        for tag in tags:
            if tag['tag'] == 'cores':
                cores = float(tag['value'])
            # TODO: esto es un parche hasta que todos los host tengan los nucleos asignados
            else:
                cores = 1
            # print(cores)
        
        # Get metricid for our metrics
        for metric in service_list:
            value_max, value_avg = list(), list()
            metrics_id = zapi.item.get(output=['itemid', 'name'], filter={
                                       'hostid': host['hostid'], 'name': metric})

            # Si exist the metric, get values for the metric
            if metrics_id:
                history = zapi.trend.get(itemids=metrics_id[0]['itemid'],
                                         time_from=time_from,
                                         time_till=time_till,
                                         output=['value_max', 'value_avg'],
                                         limit='5000',
                                         )
            # If have values, procesing the metric
                if history:
                    for element in history:
                        value_max.append(float(element['value_max']))
                        value_avg.append(float(element['value_avg']))

                    # Processing CPU
                    if metric == 'CPU system time':
    
                        dicc_service[metric_relation[metric] +
                                     'max'] = round((max(value_max)*float(dicc_mapping_cpu_host[host['hostid']]))*float(cores), 2)
                        dicc_service[metric_relation[metric] +
                                     'avg'] = round((mean(value_avg)*float(dicc_mapping_cpu_host[host['hostid']]))*float(cores), 2)
                        dicc_service[metric_relation[metric] +
                                     '95p'] = round((percentile(array(value_max), 95)*float(dicc_mapping_cpu_host[host['hostid']]))*float(cores), 2)
                    else:
                        dicc_service[metric_relation[metric] +
                                     'max'] = round(max(value_max), 2)
                        dicc_service[metric_relation[metric] +
                                     'avg'] = round(mean(value_avg), 2)
                        dicc_service[metric_relation[metric] +
                                     '95p'] = round(percentile(array(value_max), 95), 2)
                else:
                    dicc_service[metric_relation[metric] +
                                 'max'] = 'None'
                    dicc_service[metric_relation[metric] +
                                 'avg'] = 'None'
                    dicc_service[metric_relation[metric] +
                                 '95p'] = 'None'
            else:
                dicc_service[metric_relation[metric] +
                             'max'] = 'None'
                dicc_service[metric_relation[metric] +
                             'avg'] = 'None'
                dicc_service[metric_relation[metric] +
                             '95p'] = 'None'
        # Insert to the database
        insert_data('metrics', dicc_service)
    return 'OK'


def futura(user_relation: float):

    # Get the collection where the metrics was stored
    actual = get_collection('metrics')
    future_sender = list()

    # calculating METRIC*USER_RELATION
    for host in actual:
        for metric in list_future:
            if host[metric + 'avg'] == 'None':
                pass
            else:
                host[metric +
                     'avg'] = float(host[metric + 'avg'])*(user_relation)
                host[metric +
                     'max'] = float(host[metric + 'max'])*(user_relation)
                host[metric +
                     '95p'] = float(host[metric + 'max'])*(user_relation)
        # Insert data
        insert_data('future', host)
    return 'Ok'

