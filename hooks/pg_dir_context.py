# Copyright (c) 2015, PLUMgrid Inc, http://plumgrid.com

# This file contains the class that generates context for PLUMgrid template files.

from charmhelpers.core.hookenv import (
    config,
    unit_get,
)
from charmhelpers.contrib.openstack import context
from charmhelpers.contrib.openstack.utils import get_host_ip
from charmhelpers.contrib.network.ip import get_address_in_network

import re
from socket import gethostname as get_unit_hostname


class PGDirContext(context.NeutronContext):

    @property
    def plugin(self):
        '''
        Over-riding function in NeutronContext Class to return 'plumgrid'
        as the neutron plugin.
        '''
        return 'plumgrid'

    @property
    def network_manager(self):
        '''
        Over-riding function in NeutronContext Class to return 'neutron'
        as the network manager.
        '''
        return 'neutron'

    def _save_flag_file(self):
        '''
        Over-riding function in NeutronContext Class.
        Function only needed for OVS.
        '''
        pass

    def pg_ctxt(self):
        '''
        Generated Config for all PLUMgrid templates inside the templates folder.
        '''
        pg_ctxt = super(PGDirContext, self).pg_ctxt()
        if not pg_ctxt:
            return {}

        conf = config()
        pg_ctxt['local_ip'] = \
            get_address_in_network(network=None,
                                   fallback=get_host_ip(unit_get('private-address')))
        pg_ctxt['virtual_ip'] = conf['plumgrid-virtual-ip']
        pg_ctxt['pg_hostname'] = "pg-director"
        pg_ctxt['interface'] = "juju-br0"
        pg_ctxt['label'] = get_unit_hostname()
        pg_ctxt['fabric_mode'] = 'host'
        virtual_ip_array = re.split('\.', conf['plumgrid-virtual-ip'])
        pg_ctxt['virtual_router_id'] = virtual_ip_array[3]

        return pg_ctxt
