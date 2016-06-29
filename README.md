# Ansible Dynamic Inventory OpenStack
The dynamic_inventory_openstack.py file will allow you to dynamically populate an Ansible inventory file using metadata tags on OpenStack instances.

***Before using this dynamic inventory file, you will need to modify the 'regions' variable on line 36 to reflect the region(s) that you are targeting in your OpenStack setup.***

#### Host Groups
To set host groups you can add the 'ansible_host_groups' metadata tag to the openstack instances that you would like to target:

```
$ nova meta <serevr-id> set "ansible_host_groups=<ansible-group-name>" 
```

You can set multiple host groups using a comma to separate groups:

```
$ nova meta <serevr-id> set "ansible_host_groups=<ansible-group-name1>,<ansible-group-name2>,<ansible-group-name3>" 
```

#### Host Variables
To set host variables add a metadata tag for 'ansible_host_vars' to your instances:

```
$ nova meta <serevr-id> set "ansible_host_vars=<key>:<value>" 
```

You can set multiple host groups using a comma to separate groups:

```
$ nova meta <serevr-id> set "ansible_host_vars=<key1>:<value1>,<key2>:<value2>,<key3>:<value3>" 
```

To ensure that your instances are being picked up by the dynamic inventory file you can simply run the python script and examine the output:

```
$ source <your-openstack-rc-file>.sh
$ python dynamic_inventory_openstack.py
```

You can then use the dynamic inventory file with the 'ansible-playbook' commad using a '-i' flag.