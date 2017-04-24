#!/usr/bin/env python
from novaclient import client as nova_client
import os
import simplejson as json

def get_nova_session(region):
    '''
    Returns a nova client connection to selected region
    '''
    nova_session = nova_client.Client('2',
                                      os.environ['OS_USERNAME'],
                                      os.environ['OS_PASSWORD'],
                                      os.environ['OS_TENANT_NAME'],
                                      os.environ['OS_AUTH_URL'],
                                      region_name=region,
                                      connection_pool=True
                                      )

    return nova_session

def get_servers(session, srv_name=None, net_name=None):
    '''
    Returns a list of servers 
    '''
    if srv_name is None and net_name is None:
        return session.servers.list()
    else:
        if net_name is not None and srv_name is None:
            net_filter = filter(lambda servers: servers.networks.keys()[0] == net_name, get_servers(session))
            return net_filter

        srv_filter = filter(lambda servers: servers.name == srv_name, get_servers(session, net_name=net_name))
        return srv_filter

def main():
    regions = ['REG01', 'REG02']
    inventory = {}
    inventory['_meta'] = {"hostvars" : {}} 

    for region in regions:
      nova_session = get_nova_session(region) 
      servers = get_servers(nova_session)
      for server in servers:  
          if server.metadata.has_key('ansible_host_groups'):
            tags = server.metadata['ansible_host_groups'].split(',')
            for tag in tags:
              if inventory.has_key(tag):
                inventory[tag]['hosts'].append(server.name)
                inventory['_meta']['hostvars'][server.name] = {}
                inventory['_meta']['hostvars'][server.name]['ansible_host'] = server.networks.items()[0][1][0]
              else:
                inventory[tag] = {"hosts" : [server.name]}
                inventory['_meta']['hostvars'][server.name] = {}
                inventory['_meta']['hostvars'][server.name]['ansible_host'] = server.networks.items()[0][1][0]

          if server.metadata.has_key('ansible_host_vars'):
            hostvars = server.metadata['ansible_host_vars'].split(',')

            for hostvar in hostvars:
              key, value = hostvar.split(':')
              inventory['_meta']['hostvars'][server.name][key] = value

    my_json = json.dumps(inventory, sort_keys=True, indent=4 * ' ')
    print my_json


if __name__ == "__main__":
    main()