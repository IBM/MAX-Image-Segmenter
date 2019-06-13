import requests


class MainHandler():

    def __init__(self, resource_id, iam_access_token, ins_obj, ins_handle):

        assert iam_access_token is not None, 'Parameter access token cannot be None'
        assert resource_id is not None, 'Parameter resource_id cannot be None'
        assert ins_obj is not None, 'Parameter ins_obj (ServiceHandler instance) cannot be None.'
        assert ins_handle is not None, 'Parameter ins_handle (InstanceHandler instance) cannot be None'

        self.ins_obj = ins_obj
        self.ins_handle = ins_handle
        self.resource_id = resource_id
        self.iam_access_token = iam_access_token

    def wml_block(self):
        """
        Handles Watson Machine Learning related operations.
        1. Get all WML available instances.
        2. Create new WML instance and Key if desired.
        3. Use existing instance and key if chosen.
        4. Use existing instance and create a new key, if chosen.
        :return: WML environment variables such as username, password, url and instance id.
        """
        headers = {
            'Authorization': self.iam_access_token,
        }
        print('------------------------------------------------------------------------------')
        print('Available Watson Machine Learning instances are:                              ')
        print('------------------------------------------------------------------------------')
        # Call function to retrieve available instances and their respective ids
        existing_instances, instance_option, existing_guids = self.ins_handle.available_instance('wml', self.resource_id)
        # Prompt new instance name for creation.
        # If user did not provide any name, prompt again.
        # If the entered name already exists, prompt again.
        if existing_instances[int(instance_option) - 1] == 'Create New Instance':
            wml_location, wml_plan, wml_resource_plan_id = self.ins_obj.get_wml_deployment_details()
            print('------------------------------------------------------------------------------')
            print('Creating Watson Machine Learning instance                                     ')
            print('------------------------------------------------------------------------------')
            while True:
                wml_name = input("[PROMPT] Enter Watson Machine Learning instance name: ")
                if wml_name == '':
                    print("[MESSAGE] Watson Machine Learning instance name not specified. Please provide a new name")
                    continue
                elif wml_name in existing_instances:
                    print("[MESSAGE] Watson Machine Learning instance name already taken. Please provide a new name")
                    continue
                else:
                    break
            # create a new Watson Machine Learning instance using the provided name, selected location,
            # resource and plan id. Instance id is retrieved on successful completion of creation.
            wml_instance_guid = self.ins_obj.service_create(wml_name, wml_location, self.resource_id,  \
                                                            wml_resource_plan_id)
            print('------------------------------------------------------------------------------')
            print('Creating Watson Machine Learning key                                          ')
            print('------------------------------------------------------------------------------')
            while True:
                wml_key_name = input("[PROMPT] Enter Watson Machine Learning Key (service credential) name: ")
                if wml_key_name == '':
                    print("[MESSAGE] Watson Machine Learning Key name not specified. Please provide a new name")
                    continue
                else:
                    break
            # WML key creation using user and credential retrieval
            username, password, instance_id, url = self.ins_obj.wml_key_create(wml_key_name, wml_instance_guid)
            return username, password, instance_id, url
        else:
            print("[MESSAGE] Using existing WML instance '{}'. ".format(existing_instances[int(instance_option) - 1]))
            print('   ')
            print('------------------------------------------------------------------------------')
            print('Available Watson Machine Learning keys are:                                   ')
            print('------------------------------------------------------------------------------')
            # Get existing keys and their guid.
            existing_keys, key_option, existing_key_guid = self.ins_handle.wml_key_check(existing_guids \
                                                                                [int(instance_option) - 1])
            if existing_keys[int(key_option) - 1] == 'Create New Key':
                print('------------------------------------------------------------------------------')
                print('Creating Watson Machine Learning Key                                          ')
                print('------------------------------------------------------------------------------')
                while True:
                    wml_key = input("[PROMPT] Enter Watson Machine Learning key name: ")
                    if wml_key == '':
                        print("[MESSAGE] Watson Machine Learning Key name not specified. Please provide new name")
                        continue
                    if wml_key in existing_keys:
                        print("[MESSAGE] Watson Machine Learning Key name already taken. Please provide a new name")
                        continue
                    else:
                        break
                # WML Key creation and credential retrieval
                username, password, instance_id, url = self.ins_obj.wml_key_create(wml_key, existing_guids[int(instance_option) - 1])
                return username, password, instance_id, url
            else:
                print("[MESSAGE] Using existing Watson Machine Learning key '{}'. ".format(existing_keys[int(key_option) - 1]))
                # Retrieve details from the existing key details.
                wml_key_details = requests.get('https://resource-controller.cloud.ibm.com/v2/resource_keys/' +
                                                existing_key_guid[int(key_option) - 1], headers=headers)
                if wml_key_details.status_code == 200:
                    wml_key_details = wml_key_details.json()
                    try:
                        # Extract necessary environment variables from the credentials.
                        username = wml_key_details['credentials']['username']
                        password = wml_key_details['credentials']['password']
                        instance_id = wml_key_details['credentials']['instance_id']
                        url = wml_key_details['credentials']['url']
                        return username, password, instance_id, url
                    except KeyError:
                        print(''''  ERROR !!!!    ''')
                        raise KeyError("Choose appropriate Cloud Object Storage guid corresponding to the key name")

    def cos_block(self):
        """
        Handles Cloud Object Storage related operations.
        1. Get all COS available instances.
        2. Create new instance and Key if desired.
        3. Use existing instance and key if chosen.
        4. Use existing instance and create a new key, if chosen.
        :return: COS environment variables such as resource_instance_id, apikey, access_key and secret_access_key.
        """
        headers = {
            'Authorization': self.iam_access_token,
        }
        print('------------------------------------------------------------------------------')
        print('Available Cloud Object Storage instances are:                                 ')
        print('------------------------------------------------------------------------------')
        # Call function to retrieve available instances and their respective ids
        existing_instances, instance_option, existing_guids = self.ins_handle.available_instance('cos', self.resource_id)
        # Prompt new instance name for creation.
        # If user did not provide any name, prompt again.
        # If the entered name already exists, prompt again.
        if existing_instances[int(instance_option) - 1] == 'Create New Instance':
            cos_plan, cos_resource_plan_id = self.ins_obj.get_cos_deployment_details()
            print('------------------------------------------------------------------------------')
            print('Creating Cloud Object Storage instance                                        ')
            print('------------------------------------------------------------------------------')
            while True:
                cos_name = input("[PROMPT] Enter Cloud Object Storage instance name: ")
                if cos_name == '':
                    print("[PROMPT] Cloud Object Storage name not specified. Please provide a new name")
                    continue
                elif cos_name in existing_instances:
                    print("[PROMPT] Cloud Object Storage name already taken. Please provide a new name")
                    continue
                else:
                    break
            # create a new Watson Machine Learning instance using the provided name, selected location,
            # resource and plan id. Instance id is retrieved on successful completion of creation.
            cos_instance_guid = self.ins_obj.service_create(cos_name, "global", self.resource_id, cos_resource_plan_id)
            print('------------------------------------------------------------------------------')
            print('Creating Cloud Object Storage key                                             ')
            print('------------------------------------------------------------------------------')
            cos_key_name = input("[PROMPT] Enter Cloud Object Storage key name: ")
            # COS Key creation and environment variable retrieval
            resource_instance_id, apikey, access_key, secret_access_key = self.ins_obj.cos_key_create(cos_key_name,
                                                                                                 cos_instance_guid)
            return resource_instance_id, apikey, access_key, secret_access_key
        else:
            print("[MESSAGE] Using existing COS instance '{}'. ".format(existing_instances[int(instance_option) - 1]))
            print('  ')
            print('------------------------------------------------------------------------------')
            print('Available Cloud Object Storage keys are:                                      ')
            print('------------------------------------------------------------------------------')
            # Get existing keys and their guid.
            existing_keys, key_option, existing_key_guid = self.ins_handle.cos_key_check(existing_guids[int(instance_option) - 1])
            if existing_keys[int(key_option) - 1] == 'Create New Key':
                print('------------------------------------------------------------------------------')
                print('Creating Cloud Object Storage Key                                             ')
                print('------------------------------------------------------------------------------')
                while True:
                    cos_key = input("[PROMPT] Enter COS key name: ")
                    if cos_key == '':
                        print("[MESSAGE] Cloud Object Storage key name not specified. Please provide a new name")
                        continue
                    elif cos_key in existing_keys:
                        print("[MESSAGE] Cloud Object Storage key name already taken. Please provide a new name")
                        continue
                    else:
                        break
                resource_instance_id, apikey, access_key, secret_access_key = self.ins_obj.cos_key_create(cos_key,
                                                                 existing_guids[int(instance_option) - 1])
                return resource_instance_id, apikey, access_key, secret_access_key
            else:
                print("[MESSAGE] Using existing Cloud Object Storage key '{}'. ".format(existing_keys[int(key_option) - 1]))
                # Retrieve details from the existing key details.
                obj_key_details = requests.get('https://resource-controller.cloud.ibm.com/v2/resource_keys/' +
                                               existing_key_guid[int(key_option) - 1], headers=headers)
                if obj_key_details.status_code == 200:
                    obj_key_details = obj_key_details.json()
                    try:
                        # Extract necessary environment variables from the credentials.
                        resource_instance_id = obj_key_details['credentials']['resource_instance_id']
                        apikey = obj_key_details['credentials']['apikey']
                        access_key = obj_key_details['credentials']['cos_hmac_keys']['access_key_id']
                        secret_access_key = obj_key_details['credentials']['cos_hmac_keys']['secret_access_key']
                        return resource_instance_id, apikey, access_key, secret_access_key
                    except KeyError:
                        print(''''  ERROR !!!!    ''')
                        raise KeyError("Choose appropriate Cloud Object Storage guid corresponding to the key name")
