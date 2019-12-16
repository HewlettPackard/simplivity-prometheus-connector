# -*- coding: utf-8 -*-
"""
Python Class Library for the HPE SimpliVity Rest API

Copyright (c) 2019 Hewlett Packard Enterprise

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.
    https://www.gnu.org/licenses/gpl-3.0.en.html 

Requirements:
    requests
    datetime

"""

import requests
import datetime

DEBUG = False  

class SimpliVity:
    """SvtC
    class SimpliVity
    routines for the SimpliVity RestAPI
    """
    def __init__(self, url):
        self.url = url          # base URL
        self.access_token= ''    # session access token
        
    def connect(self, hms_username, hms_password):
        response = requests.post(self.url+'oauth/token', auth=('simplivity', ''), verify=False, data={
                'grant_type':'password',
                'username':hms_username,
                'password':hms_password})
        if(response.status_code == 200):
            self.access_token = response.json()['access_token']
            return response
        else:
            raise SvtError('SimpliVity.connect',response.status_code, response.json())
        
    
    def GetTask(self, task_id):
        headers = {'Authorization':  'Bearer ' + self.access_token, 'Accept' : 'application/vnd.simplivity.v1.7+json'}
        response = requests.get(self.url+'tasks/'+task_id,verify=False,headers=headers)
        if(response.status_code == 200):
            return response.json()
        else:
            raise SvtError('SimpliVity.GetTask',response.status_code, response.json())
    
    """ Certificate Operations ########################################################################"""

    def GetCertificate(self):
        headers = {'Authorization':  'Bearer ' + self.access_token, 'Accept' : 'application/vnd.simplivity.v1.9+json'}
        response = requests.get(self.url+'certificates',verify=False,headers=headers).json()
        if(response.status_code == 200):
            return response.json()
        else:
            raise SvtError('SimpliVity.GetCertificicate',response.status_code, response.json())

    def PostCertificate(self, certificate):
        print("PostCertificate is not yet implemented")
        return 0

    def DeleteCertificate(self, certid):
        print("DeleteCertificate is not yet implemented")
        return 0
    

    """ Host Operations ########################################################################"""
    
    def GetHost(self, name = None ):
        headers = {'Authorization':  'Bearer ' + self.access_token, 'Accept' : 'application/vnd.simplivity.v1.7+json'}
        if name: 
            url = self.url+'hosts?show_optional_fields=true&name='+name
        else:
            url = self.url+'hosts'
        response = requests.get(url,verify=False,headers=headers)
        if(response.status_code == 200):
            return response.json()
        else:
            raise SvtError('SimpliVity.GetHost',response.status_code, response.json())


    def GetHostId(self, name):
        x = self.GetHost(name)['hosts']
        for i in range(len(x)):
            z = x[i]
            if z['state'] == 'ALIVE':
                return z['id']     
        return 0

    def GetHostMetrics(self, name, timerange='43200', resolution='Minute', timeOffset='0'):
        headers = {'Authorization':  'Bearer ' + self.access_token, 'Accept' : 'application/vnd.simplivity.v1.7+json'}
        url = self.url +'hosts/'+self.GetHostId(name)+'/metrics?range='+timerange+'&resolution='+resolution+'&offset='+timeOffset+'&show_optional_fields=true'
        response = requests.get(url,verify=False,headers=headers)
        if(response.status_code == 200):
            return response.json()
        else:
            raise SvtError('SimpliVity.GetHostMetric',response.status_code, response.json())

    def GetHostCapacity(self, name, timerange='43200', resolution='Minute', timeOffset='0'):
        headers = {'Authorization':  'Bearer ' + self.access_token, 'Accept' : 'application/vnd.simplivity.v1.7+json'}
        url = self.url +'hosts/'+self.GetHostId(name)+'/capacity?range='+timerange+'&resolution='+resolution+'&offset='+timeOffset+'&show_optional_fields=true'
        response = requests.get(url,verify=False,headers=headers)        
        if(response.status_code == 200):
            return response.json()
        else:
            raise SvtError('SimpliVity.GetHostCapacity',response.status_code, response.json())      
       
    def GetHostHardware(self, name):
        headers = {'Authorization':  'Bearer ' + self.access_token, 'Accept' : 'application/vnd.simplivity.v1.7+json'}
        url = self.url +'hosts/'+self.GetHostId(name)+'/hardware'    
        response = requests.get(url,verify=False,headers=headers)        
        if(response.status_code == 200):
            return response.json()
        else:
            raise SvtError('SimpliVity.GetHostHardware',response.status_code, response.json()) 
       
    def ShutdownOVC(self, host_id, ha_wait=True):
        headers = {'Authorization':  'Bearer ' + self.access_token, 'Accept' : 'application/vnd.simplivity.v1.7+json'}
        response = requests.post(self.url+'hosts/'+host_id+'/shutdown_virtual_controller',verify=False,headers=headers)
        if(response.status_code == 200):
            return response.json()
        else:
            raise SvtError('SimpliVity.ShutdownOVC',response.status_code, response.json())

    def CancelShutdownOVC(self, host_id):
        headers = {'Authorization':  'Bearer ' + self.access_token, 'Accept' : 'application/vnd.simplivity.v1.7+json'}
        response = requests.post(self.url+'hosts/'+host_id+'/virtual_controller_shutdown_status',verify=False,headers=headers)
        if(response.status_code == 200):
            return response.json()
        else:
            raise SvtError('SimpliVity.CancelShutdownOVC',response.status_code, response.json())

    def GetOVCShutdownStatus(self, host_id):
        headers = {'Authorization':  'Bearer ' + self.access_token, 'Accept' : 'application/vnd.simplivity.v1.7+json'}
        response = requests.post(self.url+'hosts/'+host_id+'/cancel_virtual_controller_shutdown',verify=False,headers=headers)        
        if(response.status_code == 200):
            return response.json()
        else:
            raise SvtError('SimpliVity.GetOVCShutdownStatus',response.status_code, response.json())

    """ VM Operations #######################################################################"""
    
    def GetVM(self, vmname = None):
        headers = {'Authorization':  'Bearer ' + self.access_token, 'Accept' : 'application/vnd.simplivity.v1.7+json'}
        if vmname: 
            url = self.url+'virtual_machines?show_optional_fields=true&name='+vmname
        else:
            url = self.url+'virtual_machines?show_optional_field=true'
        response = requests.get(url,verify=False,headers=headers)
        tmp = response.json()        
        if(response.status_code == 200):
            return response.json()
        else:
            raise SvtError('SimpliVity.GetVM',response.status_code, response.json())

    def GetVMId(self, vmname):
        x = self.GetVM(vmname)['virtual_machines']
        for z in x: 
            if z['state'] == 'ALIVE':
                return z['id']                  
        raise SvtError('SimpliVity.GetVMId', 555, 'VM '+vmname+' is not ALIVE' )
    
    def GetVMMetric(self, vmname, timerange='43200', resolution='Minute', timeOffset='0'):
        headers = {'Authorization':  'Bearer ' + self.access_token, 'Accept' : 'application/vnd.simplivity.v1.7+json'}
        vmid=self.GetVMId(vmname)        
        url = self.url +'virtual_machines/'+self.GetVMId(vmname)+'/metrics?range='+timerange+'&resolution='+resolution+'&offset='+timeOffset+'&show_optional_fields=true'
        response = requests.get(url,verify=False,headers=headers)
        if(response.status_code == 200):
            return response.json()
        else:
            raise SvtError('SimpliVity.GetVMMetric',response.status_code, response.json())

    def SetVMPolicy(self, vmname, policyname):
        headers = {'Authorization':  'Bearer ' + self.access_token, 'Accept' : 'application/vnd.simplivity.v1.9+json'} 
        headers['Content-Type'] = "application/vnd.simplivity.v1.9+json"
        body = '{"virtual_machine_id":"'+self.GetVMId(vmname)+'",\
                 "policy_id":"'+self.GetPolicyId(policyname)+'"}'
        response = requests.post(self.url+'virtual_machinces/set_policy',data=body, verify=False, headers=headers)
        if(response.status_code == 200):
            return response.json()
        else:
            raise SvtError('SimpliVity.GetVMPolicy',response.status_code, response.json())

    def VMmove(self, name, destination):
        headers = {'Authorization':  'Bearer ' + self.access_token, 'Accept' : 'application/vnd.simplivity.v1.7+json'} 
        headers['Content-Type'] = "application/vnd.simplivity.v1.7+json"
        body = '{"virtual_machine_name":"'+name+'",\
                 "destination_datastore_id":"'+self.GetDataStoreId(destination)+'"}'
        response = requests.post(self.url+'virtual_machines/'+self.GetVMId(name)+'/move',data=body,verify=False, headers=headers)
        if(response.status_code == 200):
            return response.json()
        else:
            raise SvtError('SimpliVity.VMmove',response.status_code, response.json())

    def VMclone(self, name, cloneName, appConsistent=False, consistencyType='None'):
        headers = {'Authorization':  'Bearer ' + self.access_token, 'Accept' : 'application/vnd.simplivity.v1.7+json'} 
        headers['Content-Type'] = "application/vnd.simplivity.v1.7+json"
        body = '{"virtual_machine_name":"'+ cloneName +'",\
                 "app_consistent":"'+ appConsistent +'",\
                 "consistency_type":"'+ consistencyType +'"}'
        response = requests.post(self.url+'virtual_machines/'+self.GetVMId(name)+'/clone',data=body,verify=False, headers=headers)
        if(response.status_code == 200):
            return response.json()
        else:
            raise SvtError('SimpliVity.VMclone',response.status_code, response.json())

    def VMcredentials(self, name, username, password):
        headers = {'Authorization':  'Bearer ' + self.access_token, 'Accept' : 'application/vnd.simplivity.v1.9+json'} 
        headers['Content-Type'] = "application/vnd.simplivity.v1.9+json"
        body = '{"guest_username":"'+ username +'",\
                 "guest_password":"'+ password +'"}'
        response = requests.post(self.url+'virtual_machines/'+self.GetVMId(name)+'/validate_backup_credentials',data=body,verify=False, headers=headers)
        if(response.status_code == 200):
            return response.json()
        else:
            raise SvtError('SimpliVity.VMcredentials',response.status_code, response.json())

    """ DataStore Operations ################################################################"""
    
    def GetDataStore(self, name=None):
        headers = {'Authorization':  'Bearer ' + self.access_token, 'Accept' : 'application/vnd.simplivity.v1.7+json'}         
        if name: 
            url = self.url+'datastores?show_optional_fields=true&name='+name
        else:
            url = self.url+'datastores?show_optional_field=true'
        response = requests.get(url,verify=False,headers=headers)         
        if(response.status_code == 200):
            return response.json()
        else:
            raise SvtError('SimpliVity.GetDataStore',response.status_code, response.json())

    def GetDataStoreId(self, name):
        return self.GetDataStore(name)['datastores'][0]['id']


    def NewDataStore(self, name, cluster, policy, size):
        headers = {'Authorization':  'Bearer ' + self.access_token, 'Accept' : 'application/vnd.simplivity.v1.7+json'}
        headers['Content-Type'] = "application/vnd.simplivity.v1.7+json"
        size = size * 1024 * 1024 * 1024        
        body = '{"name":"'+name+'",\
                "omnistack_cluster_id":"'+self.GetClusterId(cluster)+'",\
                "policy_id":"'+self.GetPolicyId(policy)+'",\
                "size":"'+str(size)+'"}'
        response = requests.post(self.url+'datastores',data=body, verify=False, headers=headers)    
        if(response.status_code == 200):
            return response.json()
        else:
            raise SvtError('SimpliVity.NewDataStore',response.status_code, response.json())

    def RemoveDataStore(self, name):
        headers = {'Authorization':  'Bearer ' + self.access_token, 'Accept' : 'application/vnd.simplivity.v1.7+json'}        
        response = requests.delete(self.url+'datastores/'+self.GetDataStoreId(name), verify=False, headers=headers)
        if(response.status_code == 200):
            return response.json()
        else:
            raise SvtError('SimpliVity.RemoveDataStore',response.status_code, response.json()) 

    def ResizeDataStore(self, name, size):
        headers = {'Authorization':  'Bearer ' + self.access_token, 'Accept' : 'application/vnd.simplivity.v1.7+json'}        
        headers['Content-Type'] = "application/vnd.simplivity.v1.7+json"       
        body = '{"size":"'+str(size*1024*1024*1024)+'"}'
        response = requests.post(self.url+'datastores/'+self.GetDataStoreId(name)+'/resize',data=body, verify=False, headers=headers)
        if(response.status_code == 200):
            return response.json()
        else:
            raise SvtError('SimpliVity.ResizeDataStore',response.status_code, response.json())          
         
        
    def SetDataStorePolicy(self, name, policy):
        headers = {'Authorization':  'Bearer ' + self.access_token, 'Accept' : 'application/vnd.simplivity.v1.7+json'}        
        headers['Content-Type'] = "application/vnd.simplivity.v1.7+json"         
        body = '{"policy_id":"'+ self.GetPolicyId(policy) +'"}'
        respones = requests.post(self.url+'datastores/'+self.GetDataStoreId(name)+'/set_policy',data=body, verify=False, headers=headers)
        if(response.status_code == 200):
            return response.json()
        else:
            raise SvtError('SimpliVity.SetDataStorePolicy',response.status_code, response.json())          
    
    """ Cluster Operations ###################################################################"""
    
    def GetCluster(self, name=None):
        headers = {'Authorization':  'Bearer ' + self.access_token, 'Accept' : 'application/vnd.simplivity.v1.7+json'}
        if name: 
            url = self.url+'omnistack_clusters?show_optional_fields=true&name='+name
        else:
            url = self.url+'omnistack_clusters?show_optional_fields=true'
        response = (requests.get(url,verify=False,headers=headers))
        if(response.status_code == 200):
            return response.json()
        else:
            raise SvtError('SimpliVity.GetCluster',response.status_code, response.json())         
       
    def GetClusterId(self, name):
        return self.GetCluster(name)['omnistack_clusters'][0]['id']


    def GetClusterMetric(self, name,timerange='43200', resolution='Minute', timeOffset='0'):
        headers = {'Authorization':  'Bearer ' + self.access_token, 'Accept' : 'application/vnd.simplivity.v1.7+json'}        
        url = self.url +'omnistack_clusters/'+self.GetClusterId(name)+'/metrics?range='+timerange+'&resolution='+resolution+'&offset='+timeOffset+'&show_optional_fields=true'
        response = requests.get(url,verify=False,headers=headers)
        if(response.status_code == 200):
            return response.json()
        else:
            raise SvtError('SimpliVity.GetClusterMetric',response.status_code, response.json()) 
        
    def GetClusterThroughput(self):
        headers = {'Authorization':  'Bearer ' + self.access_token, 'Accept' : 'application/vnd.simplivity.v1.7+json'}        
        response = requests.get(self.url+'omnistack_clusters/throughput',verify=False,headers=headers)
        if(response.status_code == 200):
            return response.json()
        else:
            raise SvtError('SimpliVity.GetClusterThroughput',response.status_code, response.json()) 
    
    def SetClusterTimeZone(self, name, timezone):
        headers = {'Authorization':  'Bearer ' + self.access_token, 'Accept' : 'application/vnd.simplivity.v1.7+json'}        
        headers['Content-Type'] = "application/vnd.simplivity.v1.7+json"       
        body = '{"time_zone":"'+ timezone +'"}'
        response = requests.get(self.url+'omnistack_clusters/set_time_zone',data=body,verify=False,headers=headers)
        if(response.status_code == 200):
            return response.json()
        else:
            raise SvtError('SimpliVity.SetClusterTimeZone',response.status_code, response.json()) 
    
    
    """ Backup & Restore #####################################################################"""
        
    def GetBackups(self, past_hours=None, vmname=None, listOffset=None, listLimit=None):
        headers = {'Authorization':  'Bearer ' + self.access_token, 'Accept' : 'application/vnd.simplivity.v1.7+json'}        
        url=self.url+'backups?show_optional_fields=true'
        if past_hours:
            createdAfter = (datetime.datetime.now() - datetime.timedelta(hours=past_hours)).isoformat(timespec='seconds')+'Z'
            url = url + '&created_after='+createdAfter
        if vmname:
            url = url + '&virtual_machine_name='+vmname
        if listOffset:
            url = url + '&offset='+listOffset
        if listLimit:
            url = url + '&limit='+listLimit
        response = requests.get(url,verify=False,headers=headers)
        if(response.status_code == 200):
            return response.json()
        else:
            raise SvtError('SimpliVity.GetBackups',response.status_code, response.json()) 
        
    def GetVMLastBackup(self, vmname):
        bck = self.GetBackups(vmname=vmname)['backups']
        return (sorted(bck, key=lambda bck:bck['created_at'],reverse=True))[0]
        
    def BackupVM(self, name, destination, retention=0, appConsistent=False, consistencyType='None'):
        headers = {'Authorization':  'Bearer ' + self.access_token, 'Accept' : 'application/vnd.simplivity.v1.7+json'}        
        headers['Content-Type'] = "application/vnd.simplivity.v1.7+json"       
        bname = name + '_' + str(datetime.datetime.now().isoformat(timespec='seconds'))
        body='{\
                "backup_name":"'+ bname +'",\
                "destination_id":"'+ self.GetClusterId(destination) +'",\
                "app_consistent":"'+ appConsistent +',\
                "consistency_type":"'+ consistencyType +'",\
                "retention":'+ retention +'}'
        response = requests.post(self.url+'virtual_machines/'+self.GetVMId(name)+'/backup',data=body, verify=False, headers=headers)
        if(response.status_code == 200):
            return response.json()
        else:
            raise SvtError('SimpliVity.BackupVM',response.status_code, response.json()) 
        
    def RestoreVM(self, vmname, destination, bckid, restore=False):
        headers = {'Authorization':  'Bearer ' + self.access_token, 'Accept' : 'application/vnd.simplivity.v1.7+json'}        
        headers['Content-Type'] = "application/vnd.simplivity.v1.5+json"       
        if restore:
            cmd= self.url+'backups/'+bckid+'/restore?restore_original=true'
            response = requests.post(cmd, verify=False, headers=headers)
        else:        
            body='{\
                    "virtual_machine_name":"'+ vmname +'",\
                    "dastastore_id":"'+ self.GetDataStoreId(destination)+'}'
            response = requests.post(self.url+'backups/'+bckid+'/restore?restore_original=false', data=body, verify=False, headers=headers)
        if(response.status_code == 200):
            return response.json()
        else:
            raise SvtError('SimpliVity.RestoreVM',response.status_code, response.json()) 
       
    def GetBackupId(self, vmname, bckname):
        headers = {'Authorization':  'Bearer ' + self.access_token, 'Accept' : 'application/vnd.simplivity.v1.7+json'}
        response = requests.get(self.url+'backups?show_optional_fields=true&virtual_machine_name='+vmname+'&name='+bckname, verify=False, headers=headers)
        if(response.status_code == 200):
            x = response.json()
            return x['backups'][0]['id']
        else:
            raise SvtError('SimpliVity.GetBackupId',response.status_code, response.json())         
        
    def DeleteBackup(self,bckid):
        headers = {'Authorization':  'Bearer ' + self.access_token, 'Accept' : 'application/vnd.simplivity.v1.7+json'}
        headers['Content-Type'] = "application/vnd.simplivity.v1.7+json"       
        body='{\
                "backup_id":["'+ bckid +'"]}'
        response = requests.post(self.url+'backups/delete',data=body, verify=False, headers=headers)
        if(response.status_code == 200):
            return response.json()
        else:
            raise SvtError('SimpliVity.DeleteBackup',response.status_code, response.json())

    """ Policy Operations ####################################################################"""
    
    def GetPolicy(self, policyname=None):
        headers = {'Authorization':  'Bearer ' + self.access_token, 'Accept' : 'application/vnd.simplivity.v1.7+json'}
        if policyname: 
            url = self.url+'policies?show_optional_fields=true&name='+policyname
        else:
            url = self.url+'policies?show_optional_field=true'
        response = requests.get(url,verify=False,headers=headers)
        if(response.status_code == 200):
            return response.json()
        else:
            raise SvtError('SimpliVity.GetPolicy',response.status_code, response.json())
        
        
    def GetPolicyId(self, policyname):
        return( self.GetPolicy(policyname)['policies'][0]['id'] )
        
        
    def DefinePolicy(self, policyname): 
        headers = {'Authorization':  'Bearer ' + self.access_token, 'Accept' : 'application/vnd.simplivity.v1.7+json'}        
        headers['Content-Type'] = "application/vnd.simplivity.v1.7+json"       
        body='{\
               "name":"'+ policyname +'"\
              }'
        response = requests.post(self.url+'policies',data=body, verify=False, headers=headers)
        if(response.status_code == 200):
            return response.json()
        else:
            raise SvtError('SimpliVity.DefinePolicy',response.status_code, response.json())

        
    def DeletePolicy(self, policyname):
        headers = {'Authorization':  'Bearer ' + self.access_token, 'Accept' : 'application/vnd.simplivity.v1.7+json'}
        response = requests.delete(self.url+'policies/'+self.GetPolicyId(policyname), verify=False, headers=headers)
        if(response.status_code == 200):
            return response.json()
        else:
            raise SvtError('SimpliVity.DeletePolicy',response.status_code, response.json())

        
    def AddPolicyRule(self, policy_id, destination, frequency=1440, retention=1440, days='All', endTime='00:00', startTime='00:00', replace=False, appConsistent="false", consistencyType='NONE'):
        headers = {'Authorization':  'Bearer ' + self.access_token, 'Accept' : 'application/vnd.simplivity.v1.7+json'}        
        headers['Content-Type'] = "application/vnd.simplivity.v1.7+json"       
        body='[ \n {\n\
    "destination_id": "'+ destination +'",\n\
    "frequency": '+ str(frequency) + ',\n\
    "retention": '+ str(retention) + ',\n\
    "days": "'+ days + '",\n\
    "start_time": "'+ startTime + '",\n\
    "end_time": "'+ endTime + '",\n\
    "application_consistent": '+ str(appConsistent) +',\n\
    "consistency_type": "'+ consistencyType +'"\n\
 }\n]'        
        response = requests.post(self.url+'policies/'+policy_id+'/rules?replace_all_rules='+str(replace),data=body, verify=False, headers=headers)
        if(response.status_code == 200):
            return response.json()
        else:
            raise SvtError('SimpliVity.AddPolicyRule',response.status_code, response.json())


    def DeletePolicyRule(self, policy_id, rule_id):
        headers = {'Authorization':  'Bearer ' + self.access_token, 'Accept' : 'application/vnd.simplivity.v1.7+json'}        
        response = requests.delete(self.url+'policies/'+policy_id+'/rules/'+rule_id,verify=False, headers=headers)
        if(response.status_code == 200):
            return response.json()
        else:
            raise SvtError('SimpliVity.RestoreVM',response.status_code, response.json())

class SvtError(Exception):
    """ Base class for SimpliVityClass Errors """
    def __init__(self, expression, status, message):
        self.expression = expression
        self.message = message
        self.status = status


