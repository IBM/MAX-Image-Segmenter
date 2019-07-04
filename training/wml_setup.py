import os
import sys
import ruamel.yaml
from setup.token_generate import TokenGenerate
from setup.service_handling import ServiceHandler
from setup.yaml_handling import YAMLHandler
from setup.setup_functions import InstanceHandler
from setup.instance_handling import MainHandler

setup_goal = """
Setup goal:

1. Manage Watson Machine Learing and Cloud Object Storage services.
2. Set environment variables required for initiating the training process.
3. Configure YAML file.
4. Configure GPU settings.
"""

print(setup_goal)

if len(sys.argv) == 1:
    print(" Please provide the configuration YAML file name")
    print('\nUsage: python {} <training_config_file> [command] \n'
          .format(sys.argv[0]))
    sys.exit()

if len(sys.argv) == 2:
    file_name = sys.argv[1]
    yaml = ruamel.yaml.YAML(typ='rt')
    yaml.allow_duplicate_keys = True
    yaml.preserve_quotes = True
    yaml.indent(mapping=6, sequence=4)
    try:
        with open(file_name) as fp:
            # Loading configuration file
            config = yaml.load(open(file_name))
            assert ("bucket" in config['train'][
                'data_source']['training_data'])
            assert ("bucket" in config['train'][
                'model_training_results']['trained_model'])
            assert ("path" in config['train'][
                'data_source']['training_data_local'])
            assert ("name" in config['train'][
                'execution']['compute_configuration'])
            assert ("path" in config['train']['data_source'][
                'training_data'])
    except Exception as e:
        print("Exception is: ", e)
        print("[DEBUG] Provide a valid configuration YAML "
              "file for initiating the training process")
        sys.exit()


def yaml_handle(read_flag, input_bucket_name, local_directory,
                result_bucket_name, compute_config):
    """
    This function handles:

    1. Reading configuration variables from YAML file.
    2. Updating configuration variables to YAML file.
    3. Updating only compute configuration to YAML file.

    :param read_flag: indicator for choosing the operation
           to be performed.
    :param input_bucket_name: input bucket name
    :param local_directory: local directory from where data
           needs to be uploaded
    :param result_bucket_name: result bucket name
    :param compute_config: compute configuration
    :return:
      - Configuration variables if read flag is not set to 'Y'.
      - `True` after successful configuration changes.

    Exit on error in any of the steps.
    """
    file_name = sys.argv[1]
    yaml = ruamel.yaml.YAML(typ='rt')
    yaml.allow_duplicate_keys = True
    yaml.preserve_quotes = True
    yaml.indent(mapping=6, sequence=4)
    try:
        with open(file_name) as fp:
            # Loading configuration file
            config = yaml.load(open(file_name))
            # Reading configuration variables from configuration file.
            if read_flag == 'Y':
                cfg_inp_bucket = config['train']['data_source'][
                    'training_data']['bucket']
                cfg_out_bucket = config['train'][
                    'model_training_results']['trained_model'][
                    'bucket']
                cfg_loc_path = config['train']['data_source'][
                    'training_data_local']['path']
                cfg_cmp_config = config['train']['execution'][
                    'compute_configuration']['name']
                cfg_key_prefix = config['train']['data_source'][
                    'training_data']['path']
                return \
                    cfg_inp_bucket, cfg_out_bucket, cfg_loc_path, \
                    cfg_cmp_config, cfg_key_prefix
            if read_flag == 'N':
                with open(file_name, 'w') as fp:
                    config['train']['data_source'][
                        'training_data']['bucket'] = input_bucket_name
                    config['train']['model_training_results'][
                        'trained_model']['bucket'] = result_bucket_name
                    config['train']['data_source'][
                        'training_data_local']['path'] = local_directory
                    config['train']['execution'][
                        'compute_configuration']['name'] = compute_config
                    # Updating configuration file with new values
                    yaml.dump(config, fp)
                    return True
            if read_flag == 'C':
                with open(file_name, 'w') as fp:
                    # Updating configuration file with new compute
                    # configuration values.
                    config['train']['execution'][
                        'compute_configuration']['name'] = compute_config
                    yaml.dump(config, fp)
                    return True
    except Exception as ex:
        print(type(ex), '::', ex)
        sys.exit()


def env_extract(access_key, secret_access_key, username,
                password, instance_id, url):
    """
    This function:
    1. Extract current configuration values from the YAML file.
    2. Handle input and result buckets. Upload data to input
    bucket if necessary.
    3. Retrieve compute configuration value.
    4. Update YAML file with new values.
    5. Display environment variables value required to be set
    for initiating training process.
    :param access_key: cloud object storage access key.
    :param secret_access_key: cloud object storage secret access key
    :param username: watson machine learning username
    :param password: watson machine learning password
    :param instance_id: watson machine learning instance id
    :param url: watson machine learning url

    The function exits by displaying environment variables value to be
    set along with configuration variables
    values that have been updated in YAML file.
    """
    (cfg_inp_bucket, cfg_out_bucket, cfg_loc_path, cfg_cmp_config,
     cfg_key_prefix) = yaml_handle('Y', '', '', '', '')
    yaml_handler = YAMLHandler(cfg_inp_bucket, cfg_out_bucket,
                               cfg_loc_path, cfg_cmp_config,
                               access_key, secret_access_key,
                               cfg_key_prefix)
    input_bucket_name, local_directory = yaml_handler.input_bucket_handle()
    result_bucket_name = yaml_handler.result_bucket_handle(input_bucket_name)
    compute_config = yaml_handler.configuration_check()
    print('--------------------------------------------------------'
          '----------------------')
    print('NEW YAML CONFIGURATION VALUES')
    print('---------------------------------------------------------'
          '---------------------')
    print('input_bucket  :', input_bucket_name)
    print('local directory  :', local_directory)
    print('result bucket  :', result_bucket_name)
    print('compute  :', compute_config)
    print('---------------------------------------------------------'
          '---------------------')
    config_result = yaml_handle('N', input_bucket_name,
                                local_directory, result_bucket_name,
                                compute_config)
    if config_result:
        print('**********************    Setup successfully completed '
              '     ***********************')
        print('                                                       ')
        print('                                 NEXT STEPS             '
              '                           ')
        print('                                                        '
              '                           ')
        print('  1. Update or set the following environment variables   '
              '                          ')
        print('        i) ML_USERNAME={0}                               '
              '              '.format(username))
        print('       ii) ML_PASSWORD={}                                '
              '              '.format(password))
        print('      iii) ML_INSTANCE={}                                '
              '              '.format(instance_id))
        print('       iv) ML_ENV={}                                     '
              '              '.format(url))
        print('        v) AWS_ACCESS_KEY_ID={}                          '
              '              '.format(access_key))
        print('       vi) AWS_SECRET_ACCESS_KEY={}                      '
              '              '.format(secret_access_key))
        print('                                                         '
              '                          ')
        print('  2. Run `python wml_train.py {} prepare` to verify your '
              'step.         '.format(sys.argv[1]))
        print('  3. Run `python wml_train.py {} package` to train the '
              'model using your data.  '.format(sys.argv[1]))
        print('                                                           '
              '                        ')
        print('***********************************************************'
              '*************************')
    sys.exit()


env_check = """
*------------------------------------------------------------------------*
|                     Model Asset Exchange                               |
| One place for all state of the art Open Source deep learning models.   |
*------------------------------------------------------------------------*

       *****    MODEL TRAINING ENVIRONMENT SETUP    *****


Now checking for existing environment variables....................

*************    PRE-REQUISITE FOR TRAINING SETUP       ******************
*                                                                        *
*                    Create IBM Cloud API Key                            *
*  This step is required if IBM Cloud API Key JSON file has not          *
*  been downloaded before.                                               *
*                                                                        *
*                                                                        *
*       1. Login to IBM Cloud                                            *
*       2. Go to Manage -> Access(IAM) -> IBM Cloud API Keys             *
*       3. Click `Create an IBM Cloud API Key`. Provide `name` and       *
*           `description`.                                               *
*       4. Click `Create` and download the JSON Key file when prompted.  *
*                                                                        *
**************************************************************************

            """
print(env_check)
# Watson Machine Learning environment variables check flag
wml_env_check_flag = 'Y'
# Cloud Object Storage environment check flag
cos_env_check_flag = 'Y'
# Change setting flag
change_setting_flag = 'N'
# Checking WML environment variables
for env_var in ['ML_ENV', 'ML_USERNAME', 'ML_PASSWORD', 'ML_INSTANCE']:
    if os.environ.get(env_var) is None:
        wml_env_check_flag = 'N'
if wml_env_check_flag == 'N':
    print(' ')
    print('[MESSAGE] Watson Machine Learning environment variables '
          'are not defined.')
else:
    print('[MESSAGE] Watson Machine Learning environment variables '
          'are set.')
# Checking COS environment variables
for env_var in ['AWS_ACCESS_KEY_ID', 'AWS_SECRET_ACCESS_KEY']:
    if os.environ.get(env_var) is None:
        cos_env_check_flag = 'N'
if cos_env_check_flag == 'N':
    print(' ')
    print('[MESSAGE] Cloud Object Storage environment variables '
          'are not defined.')
else:
    print('[MESSAGE] Cloud Object Storage environment variables '
          'are set.')

# steps to perform if environment variables are set
if cos_env_check_flag == 'Y' and wml_env_check_flag == 'Y':
    selection = """
*--------------------------------------------------------------------*
|     Environment variables have already been set.                   |
|     Choose an option from below for next steps                     |
|--------------------------------------------------------------------|
|    MENU                                                            |
|                                                                    |
|    1. Proceed with current settings.                               |
|                                                                    |
|    2. Change settings.                                             |
|                                                                    |
|    3. Change GPU configuration settings.                           |
|                                                                    |
*--------------------------------------------------------------------*
            """
    print(selection)
    while True:
        # Get user option
        user_option = input("[PROMPT] Your selection:  ")
        if user_option == '':
            print("[MESSAGE] Enter number between 1 and 3.")
            continue
        elif not user_option.isdigit():
            print("[MESSAGE] Enter number between 1 and 3.")
            continue
        elif int(user_option) < 1 or int(user_option) > 3:
            print("[MESSAGE] Enter number between 1 and 3.")
            continue
        else:
            break
    # Steps for option 1: User wants to proceed with current settings.
    if user_option == '1':
        print('[MESSAGE] Proceeding with current settings.....')
        access_key = os.environ['AWS_ACCESS_KEY_ID']
        secret_access_key = os.environ['AWS_SECRET_ACCESS_KEY']
        username = os.environ['ML_USERNAME']
        password = os.environ['ML_PASSWORD']
        instance_id = os.environ['ML_INSTANCE']
        url = os.environ['ML_ENV']
        # update configuration values
        env_extract(access_key, secret_access_key, username, password,
                    instance_id, url)
    # Steps for option 2: User wants to change the current settings.
    if user_option == '2':
        cos_env_check_flag = 'N'
        wml_env_check_flag = 'N'
        change_setting_flag = 'Y'
    # Steps for option 3: User wants to change only compute configuration.
    if user_option == '3':
        (cfg_inp_bucket, cfg_out_bucket, cfg_loc_path, cfg_cmp_config,
         cfg_key_prefix) = yaml_handle('Y', '', '', '', '')
        # Extract environment variables
        access_key = os.environ['AWS_ACCESS_KEY_ID']
        secret_access_key = os.environ['AWS_SECRET_ACCESS_KEY']
        # Call function to change configuration
        yaml_handler = YAMLHandler(cfg_inp_bucket, cfg_out_bucket,
                                   cfg_loc_path, cfg_cmp_config,
                                   access_key, secret_access_key,
                                   cfg_key_prefix)
        compute_config = yaml_handler.configuration_check()
        config_result = yaml_handle('C', '', '', '', compute_config)
        if config_result:
            print('-------------------------------------------------------'
                  '-----------------------')
            print("[MESSAGE] Compute configured has been changed to "
                  "{}.".format(compute_config))
            print('-------------------------------------------------------'
                  '-----------------------')
        sys.exit()

resource_id_display = """
*--------------------------------------------------------------------------*
|                                                                          |
|   IBM resource group id retrieval.                                       |
|                                                                          |
|   A resource group is a way for you to organize your account resources   |
|   in customizable groupings. When you create a service instance for one  |
|   of the services (e.g. Watson Machine Learning), it is assigned to a    |
|   particular resource group. Once assigned to a resource group, it can't |
|   be changed.                                                            |
|                                                                          |
*--------------------------------------------------------------------------*
                          """

config_display = """
*--------------------------------------------------------------------------*
|                                                                          |
|   Time to configure Watson Machine Learning and Cloud Object Storage     |
|                                                                          |
|  Instance: When you purchase a service on IBM Cloud, an instance of      |
|            that service is provisioned for you to use.                   |
|                                                                          |
|  Service Credentials(Key): Service credentials are authentication        |
|           credentials associated with a service. It is used for          |
|           interacting with a service.                                    |
|                                                                          |
|  To design, train, and deploy machine learning models in IBM Watson      |
|  Studio, you need to associate an IBM Watson Machine Learning service    |
|  instance as well as some supporting services (such as IBM Cloud Object  |
|  Storage for storage) with a project.                                    |
|                                                                          |
*--------------------------------------------------------------------------*
    """

# Steps for changing configuration
if cos_env_check_flag == 'N' or wml_env_check_flag == 'N':  # noqa
    flow_check_flag = 'N'
    if cos_env_check_flag == 'N' and wml_env_check_flag == 'N' and \
            change_setting_flag == 'N' and flow_check_flag == 'N':
        print('   ')
        print("*------------------------------------------------------"
              "-------------------------*")
        print("|  Configuring both Watson Machine Learning and "
              "Cloud Object Storage.           |")
        print("*------------------------------------------------------"
              "-------------------------*")
        option = 'both'
        flow_check_flag = 'Y'

    if cos_env_check_flag == 'N' and change_setting_flag == 'N' \
            and flow_check_flag == 'N':
        selection = """
*---------------------------------------------------------------------------*
|                                   MENU                                    |
|----------------------------------------------------------------------------
|                                                                           |
|    1. Configure both Watson Machine Learning and Cloud Object Storage.    |
|                                                                           |
|    2. Configure only Cloud Object Storage                                 |
|                                                                           |
*---------------------------------------------------------------------------*
                           """
        print(selection)
        while True:
            option = input("[PROMPT] Your selection:  ")
            if option == '':
                print("[MESSAGE] Enter a number 1 or 2.")
                continue
            elif not option.isdigit():
                print("[MESSAGE] Enter a number 1 or 2.")
                continue
            elif int(option) < 1 or int(option) > 2:
                print("[MESSAGE] Enter a number 1 or 2.")
                continue
            else:
                if option == '1':
                    option = 'both'
                elif option == '2':
                    option = 'cos'
                flow_check_flag = 'Y'
                break

    if wml_env_check_flag == 'N' and change_setting_flag == 'N' \
            and flow_check_flag == 'N':
        selection = """
*---------------------------------------------------------------------------*
|                                   MENU                                    |
|----------------------------------------------------------------------------
|                                                                           |
|    1. Configure both Watson Machine Learning and Cloud Object Storage.    |
|                                                                           |
|    2. Configure only Watson Machine Learning.                             |
|                                                                           |
*---------------------------------------------------------------------------*
                           """
        print(selection)
        while True:
            option = input("[PROMPT] Your selection:  ")
            if option == '':
                print("[MESSAGE] Enter a number 1 or 2.")
                continue
            elif not option.isdigit():
                print("[MESSAGE] Enter a number 1 or 2.")
                continue
            elif int(option) < 1 or int(option) > 2:
                print("[MESSAGE] Enter a number 1 or 2.")
                continue
            else:
                if option == '1':
                    option = 'both'
                elif option == '2':
                    option = 'wml'
                flow_check_flag = 'Y'
                break

    if change_setting_flag == 'Y' and flow_check_flag == 'N':
        selection = """
*--------------------------------------------------------------------------*
|                                   MENU                                   |
|--------------------------------------------------------------------------|
|                                                                          |
|    1. Configure both Watson Machine Learning and Cloud Object Storage.   |
|                                                                          |
|    2. Configure only Watson Machine Learning.                            |
|                                                                          |
|    3. Configure only Cloud Object Storage                                |
|                                                                          |
*--------------------------------------------------------------------------*
                   """
        print(selection)
        while True:
            option = input("[PROMPT] Your selection:  ")
            if option == '':
                print("[MESSAGE] Enter a number between 1 and 3.")
                continue
            elif not option.isdigit():
                print("[MESSAGE] Enter a number between 1 and 3.")
                continue
            if int(option) < 1 or int(option) > 4:
                print("[MESSAGE] Enter a number between 1 and 3.")
                continue
            else:
                if option == '1':
                    option = 'both'
                elif option == '2':
                    option = 'wml'
                elif option == '3':
                    option = 'cos'
                flow_check_flag = 'Y'
                break
    # Pre-requisite check
    # Generating iam access token
    token_obj = TokenGenerate()
    iam_access_token = token_obj.get_api_location()
    print('[MESSAGE] IAM Access Token has been generated')
    #
    ins_obj = ServiceHandler(iam_access_token)
    # Retrieve resource id
    print(resource_id_display)
    resource_id = ins_obj.get_resources_id()
    ins_handle = InstanceHandler(iam_access_token)
    main_handle = MainHandler(resource_id, iam_access_token,
                              ins_obj, ins_handle)
    #
    print(config_display)
    # steps for configuring both COS and WML
    if option == 'both':
        try:
            # Retrieving WML details
            username, password, instance_id, url = main_handle.wml_block()
        except KeyError as ex:
            print(type(ex), '::', ex)
            sys.exit()
        try:
            # Retrieving COS details
            resource_instance_id, apikey, access_key, secret_access_key = \
                main_handle.cos_block()
        except KeyError as ex:
            print(type(ex), '::', ex)
            sys.exit()
        # Updating config YAML file
        env_extract(access_key, secret_access_key, username, password,
                    instance_id, url)
        sys.exit()
    # steps for configuring only WML
    if option == 'wml':
        try:
            # Retrieving WML details
            username, password, instance_id, url = main_handle.wml_block()
        except KeyError:
            print("[DEBUG] Error in key retrieval details")
            sys.exit()
        print('***** Watson Machine Learning setting has been '
              'completed. *****')
        access_key = os.environ['AWS_ACCESS_KEY_ID']
        secret_access_key = os.environ['AWS_SECRET_ACCESS_KEY']
        env_extract(access_key, secret_access_key, username, password,
                    instance_id, url)
        sys.exit()
    # steps for configuring only COS
    if option == 'cos':
        try:
            resource_instance_id, apikey, access_key, secret_access_key = \
                main_handle.cos_block()
        except KeyError:
            print("Error in creating new COS key and retrieving details")
            sys.exit()
        print('***** Cloud Object Storage setting has been completed *****')
        username = os.environ['ML_USERNAME']
        password = os.environ['ML_PASSWORD']
        instance_id = os.environ['ML_INSTANCE']
        url = os.environ['ML_ENV']
        env_extract(access_key, secret_access_key, username, password,
                    instance_id, url)
        sys.exit()
