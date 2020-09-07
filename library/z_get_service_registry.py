import csv

from common import LoginBlueprint
from common import AosApi

token_bp_id_address = LoginBlueprint().blueprint()
token = token_bp_id_address[0]
bp_id = token_bp_id_address[1]
address = token_bp_id_address[2]


class GetServiceRegistry(object):

    def __init__(self):
        pass

    def service_registry_list(self):
        iba_storage_schema_path = {}
        for service in AosApi().telemetry_service_registry_get(token, bp_id, address)['items']:
            storage_schema_path = service['storage_schema_path'].replace('aos.sdk.telemetry.schemas.', '')
            if storage_schema_path not in iba_storage_schema_path:
                iba_storage_schema_path[storage_schema_path] = []
            iba_storage_schema_path[storage_schema_path].append(service['service_name'])
        print (iba_storage_schema_path)

if __name__ == '__main__':
    GetServiceRegistry().service_registry_list()
