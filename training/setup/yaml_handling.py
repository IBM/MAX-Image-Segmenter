import sys
from utils.cos import COSWrapper
import glob
import os
import getch


class YAMLHandler:

    def __init__(self, cfg_inp_bucket, cfg_out_bucket, cfg_loc_path,
                 cfg_cmp_config, access_key, secret_access_key,
                 cfg_key_prefix):
        assert access_key is not None, \
            'Parameter access key cannot be None'
        assert secret_access_key is not None, \
            'Parameter secret access key cannot be None'
        self.cfg_inp_bucket = cfg_inp_bucket
        self.cfg_out_bucket = cfg_out_bucket
        self.cfg_loc_path = cfg_loc_path
        self.cfg_cmp_config = cfg_cmp_config
        self.access_key = access_key
        self.secret_access_key = secret_access_key
        self.cfg_key_prefix = cfg_key_prefix
        self.cos = COSWrapper(self.access_key, self.secret_access_key)

    def data_upload(self, bucket_name, path):
        """
        Upload data from the provided local directory to COS bucket
        :param bucket_name: input bucket name to which the data
        needs to be uploaded.
        :param path: local directory path from where data needs
        to be uploaded.
        :return: `True` if file has been uploaded successfully.
        `False` if file upload fails.
        """
        file_count = 0
        if (self.cfg_key_prefix != '' or self.cfg_key_prefix
                is not None):
            key_prefix = self.cfg_key_prefix
        else:
            key_prefix = None
        for file in glob.iglob(path + '**/*', recursive=True):
            if os.path.isfile(file):
                print(' [MESSAGE] Uploading "{}" to training data bucket '
                      '"{}" ...'.format(file, bucket_name))
                self.cos.upload_file(file,
                                     bucket_name,
                                     key_prefix,
                                     file[len(path):]
                                     .lstrip('/'))
                file_count += 1

        if file_count == 0:
            return False
        else:
            return True

    def local_directory_handle(self, bucket_name):
        """
        Handle data upload to the input bucket from local directory.
        1. If the path is configured in YAML file:
           1.1 Prompt user to decide if the configured path
           needs to be updated.
           1.2 Update if needed. Proceed if the user is fine
           with the current configuration.
           1.3 Proceed with the data upload.
        2. If the path is not configured in YAML file, prompt user
         input and proceed with data upload.
        :param bucket_name: input bucket name
        :return: data upload status and local directory path.
        """
        # Steps if local path is configured.
        if self.cfg_loc_path is not None:
            user_data_opt = input("[PROMPT] Data will be uploaded from {}. "
                                  "Press 'Enter' to proceed or provide new "
                                  "directory path if you want to change: ".
                                  format(self.cfg_loc_path))
            # If user press 'Enter`, data will be uploaded from
            # the configured directory.
            if user_data_opt == '':
                return self.data_upload(bucket_name, self.cfg_loc_path), \
                       self.cfg_loc_path
            else:
                # Checks if the provided path is a directory
                if not os.path.isdir(user_data_opt):
                    while True:
                        loc_dir = input("[PROMPT] Provided path is not a "
                                        "directory. Enter path again: ")
                        if loc_dir == '':
                            print("[MESSAGE] 'None' provided as input. "
                                  "Please provide directory path.")
                            continue
                        if not os.path.isdir(loc_dir):
                            print('[MESSAGE] Error. "{}" is not a directory '
                                  'or cannot be accessed.'.
                                  format(user_data_opt))
                            continue
                        else:
                            return self.data_upload(bucket_name, loc_dir), \
                                   loc_dir
                else:
                    return self.data_upload(bucket_name, user_data_opt), \
                           user_data_opt

        else:
            # Steps if local directory path has not been configured.
            print("[PROMPT] Local directory path from where input data needs "
                  "to be uploaded to the input "
                  "bucket is not configured. Press 'ENTER' to configure: ")
            getch.getch()
            # User user to provide directory path.
            while True:
                local_directory = input("[PROMPT] Enter local "
                                        "directory path: ")
                if local_directory == '':
                    print("[MESSAGE] 'None' provided as input. "
                          "Please provide directory path.")
                    continue
                if not os.path.isdir(local_directory):
                    print('[MESSAGE] Error. "{}" is not a directory or '
                          'cannot be accessed.'.format(local_directory))
                    continue
                else:
                    return self.data_upload(bucket_name, local_directory), \
                           local_directory

    def bucket_data_handling(self, bucket_name): # noqa
        """
        Handle Cloud Object Storage bucket data.
        1. If COS bucket is empty:
           1.1 Upload data.
           1.2 Proceed as it is with empty bucket.
        2. If COS bucket is not empty:
           2.1 Add data to the bucket
           2.2 Delete and add data to the bucket.
           2.3 Proceed with an existing data.
        :param bucket_name: bucket name
        :return: local directory path. Exit if data upload fails.
        """
        if self.cos.is_bucket_empty(bucket_name):
            print('----------------------------------------------------'
                  '------------------------')
            user_choice = input("[PROMPT] Bucket is empty. Enter 'Y' "
                                "to upload data from local directory "
                                "or press 'ENTER' if you don't want "
                                "to upload: ")
            if user_choice == 'Y' or user_choice.upper() == 'Y':
                handle_status, upload_path = \
                    self.local_directory_handle(bucket_name)
                if handle_status is False:
                    print('[MESSAGE] Error. No local training data was found '
                          'in the local directory.'.format(upload_path))
                    sys.exit()
                else:
                    print('[MESSAGE] Uploaded files to training data bucket '
                          '"{}".'.format(upload_path))
                    return upload_path
            else:
                print("[MESSAGE] WARNING: Proceeding without data upload")
                if self.cfg_loc_path is not None:
                    return self.cfg_loc_path
                else:
                    return None
        else:
            options = """
|-----------------------------------------------------------------------------|
|              Bucket is not empty. Choose options from below                 |
|-----------------------------------------------------------------------------|
|                                                                             |
|    1. Enter '1' to add data to the bucket                                   |
|    2. Enter '2' to delete current data and upload new data to the bucket    |
|    3. Enter '3' to proceed with the current data                            |
|                                                                             |
|-----------------------------------------------------------------------------|
                      """
            print(options)
            while True:
                user_choice = input("[PROMPT] Your selection: ")
                if user_choice == '':
                    print("[MESSAGE] Enter a number between 1 and 3.")
                    continue
                if not user_choice.isdigit():
                    print("[MESSAGE] Enter a number between 1 and 3.")
                    continue
                if int(user_choice) < 0 or int(user_choice) > 3:
                    print("[MESSAGE] Enter a number between 1 and 3.")
                    continue
                else:
                    # delete existing bucket content for option 2.
                    if int(user_choice) == 2:
                        self.cos.clear_bucket(bucket_name)
                        print('[MESSAGE] Cloud Object Storage input '
                              'bucket data has been deleted. Proceeding '
                              'with data upload')
                    # upload data from directory.
                    if int(user_choice) == 1 or int(user_choice) == 2:
                        handle_status, upload_path = \
                            self.local_directory_handle(bucket_name)
                        if handle_status is False:
                            print('[MESSAGE] Error. No local training data '
                                  'was found in the local directory.'.
                                  format(upload_path))
                            sys.exit()
                        else:
                            print('[MESSAGE] Uploaded files to training '
                                  'data bucket "{}".'.format(upload_path))
                            return upload_path
                    # proceed with existing data.
                    if int(user_choice) == 3 and self.cfg_loc_path is None:
                        print("[MESSAGE] WARNING!!! Local directory not "
                              "configured. Proceeding with existing input "
                              "COS bucket data. ")
                        return None
                    if int(user_choice) == 3 and self.cfg_loc_path is not None:
                        print('[MESSAGE] Local directory is configured as {}. '
                              'Proceeding with existing input COS bucket data'
                              .format(self.cfg_loc_path))
                        return self.cfg_loc_path

    def bucket_list(self):
        """
        Get list of existing Cloud Object Storage buckets.
        :return: available bucket list, user option and number of buckets.
        """
        bucket_list = self.cos.get_bucket_list()
        if len(bucket_list) != 0:
            print('------------------------------------------------------'
                  '----------------------')
            print('Available Cloud Object Storage buckets: ')
            print('-------------------------------------------------------'
                  '----------------------')
            for ind, value in enumerate(bucket_list, start=1):
                print("{}. {}".format(ind, value))
                if value == bucket_list[-1]:
                    print('{}. {}'.format(int(ind) + 1,
                                          '* Create New Bucket *'))
            # User prompt
            while True:
                input_new_bucket = input("[PROMPT] Your selection : ")
                if input_new_bucket == '':
                    print("[MESSAGE] 'None' provided as input. "
                          "Please provide a correct number of choice.")
                    continue
                if not input_new_bucket.isdigit():
                    print("[MESSAGE] Sorry, Please provide a "
                          "correct number of choice.")
                    continue
                if int(input_new_bucket) < 1 or \
                        int(input_new_bucket) > (len(bucket_list) + 1):
                    print("[MESSAGE] Sorry, Please provide a c"
                          "orrect number of choice.")
                    continue
                else:
                    return len(bucket_list), input_new_bucket, bucket_list
        else:
            print('---------------------------------------------------'
                  '------------------------')
            print("There is no existing Cloud Object Storage bucket. "
                  "Proceeding with bucket creation!!")
            print('---------------------------------------------------'
                  '------------------------')
            return len(bucket_list), None, None

    def input_bucket_handle(self): # noqa
        """
        Handle input bucket data.
        1. If input bucket is not configured.
           1.1 Get list of available buckets.
           1.2 If there is no existing bucket or if user decides to
           create new bucket, prompt user for new bucket name.
               Create new bucket and upload data.
           1.3 If user selects any existing bucket, proceed to data handling.
        2. If input bucket is configured.
           2.1 If user wants to proceed with the existing setting,
           try creating the bucket. If bucket exists, proceed
               to data handling.If bucket does not exist, prompt user new
               bucket name and proceed to data handling.
           2.2 If user wants to change the current settings, display all
           available buckets and let user choose one. Then
               proceed with data handling.
        :return: new input bucket name, local directory path. 'None`
        for any error in the process.
        """
        print('--------------------------------------------------------'
              '-------------')
        print('Cloud Object Storage training data bucket handling     ')
        print('--------------------------------------------------------'
              '-------------')
        if self.cfg_inp_bucket is None:
            # Get list of available buckets.
            bucket_list_length, input_new_bucket, bucket_list = \
                self.bucket_list()
            # No available bucket or user wants to create a new bucket
            if bucket_list_length == 0 or (int(input_new_bucket) > 0 and
                                           int(input_new_bucket) ==
                                           (bucket_list_length + 1)):
                # Prompt user for new bucket name
                while True:
                    new_input_bucket_name = input("[PROMPT] Enter a new "
                                                  "training data bucket "
                                                  "name: ")
                    if new_input_bucket_name == '':
                        print("[MESSAGE] 'None' provided as input. "
                              "Please provide a training data valid name.")
                        continue
                    if new_input_bucket_name == self.cfg_out_bucket:
                        print("[MESSAGE] Entered bucket name is same as "
                              "configured training result bucket name. Please "
                              "provide a new name.")
                        continue
                    if bucket_list_length != 0 and \
                            new_input_bucket_name in bucket_list:
                        print("[MESSAGE] Bucket with the entered name already "
                              "exists. Please enter a new training data "
                              "bucket name!!!")
                        continue
                    else:
                        try:
                            create_status = self.cos.create_bucket(
                                new_input_bucket_name)
                        except ValueError:
                            print("[MESSAGE] Bucket name already taken. Please"
                                  " enter a new training data bucket name!!!")
                            continue
                        else:
                            if create_status is True:
                                local_directory_path = \
                                    self.bucket_data_handling(
                                        new_input_bucket_name)
                                return new_input_bucket_name, \
                                    local_directory_path
                            else:
                                print("[DEBUG] Error in creating bucket")
                                return None, None
            # Using the existing bucket
            elif int(input_new_bucket) != (bucket_list_length + 1):
                config_inp_bucket = bucket_list[int(input_new_bucket) - 1]
                print("[MESSAGE] Using existing bucket {} "
                      "as training data input "
                      "bucket.".format(config_inp_bucket))
                local_directory_path = self.bucket_data_handling(
                    config_inp_bucket)
                return config_inp_bucket, local_directory_path
            else:
                print("[DEBUG] Error in handling input COS bucket")
                return None, None
        else:
            # Steps if bucket is configured.
            print("Configured input bucket:  `{}` ".
                  format(self.cfg_inp_bucket))
            bucket_list = self.cos.get_bucket_list()
            # prompt user input
            cfg_option = input("[PROMPT] Press 'ENTER' to proceed with the "
                               "current settings. To select different COS "
                               "bucket from the existing COS buckets enter"
                               " 'Y': ")
            if cfg_option == 'Y' and len(bucket_list) == 0:
                print("[MESSAGE] There is no existing bucket to list. "
                      "Proceeding with bucket creation with provided "
                      "bucket name.")
                cfg_option = ''
            # Steps to follow if user wants to proceed with current settings.
            if cfg_option == '':
                try:
                    result = self.cos.create_bucket(self.cfg_inp_bucket,
                                                    exist_ok=True)
                except ValueError:
                    # get new bucket name if bucket does not exist
                    while True:
                        try:
                            new_input_bucket_name = input("[PROMPT] Bucket "
                                                          "with the entered "
                                                          "name is in "
                                                          "namespace. Please "
                                                          "enter a new "
                                                          "training data "
                                                          "bucket name: ")
                            if self.cfg_out_bucket == new_input_bucket_name:
                                print("[MESSAGE] Entered bucket name is same "
                                      "as configured training result bucket "
                                      "name. Please provide a new name.")
                                continue
                            else:
                                result = self.cos.create_bucket(
                                    new_input_bucket_name, exist_ok=True)
                        except KeyboardInterrupt:
                            sys.exit()
                        except ValueError:
                            print("[MESSAGE] Enter a valid training input"
                                  " data bucket name")
                            continue
                        except TypeError:
                            print("[MESSAGE] Enter a valid training input"
                                  " data bucket name")
                            continue
                        if result is True:
                            print("[MESSAGE] Bucket {} has been created".
                                  format(new_input_bucket_name))
                            local_directory_path = self.bucket_data_handling(
                                new_input_bucket_name)
                            return new_input_bucket_name, local_directory_path
                        else:
                            print("[MESSAGE] Enter a valid training input "
                                  "data bucket name")
                            continue
                else:
                    # if bucket exists
                    if result is True and \
                            self.cfg_out_bucket != self.cfg_inp_bucket:
                        print("[MESSAGE] Bucket {} is ready for use. "
                              "Proceeding with further configuration".
                              format(self.cfg_inp_bucket))
                        local_directory_path = self.bucket_data_handling(
                            self.cfg_inp_bucket)
                        return self.cfg_inp_bucket, local_directory_path
                    if result is True and \
                            self.cfg_out_bucket == self.cfg_inp_bucket:
                        while True:
                            try:
                                new_input_bucket_name = \
                                    input("[PROMPT] Training data input and "
                                          "result bucket names are same "
                                          "in configuration file. Please enter"
                                          " a new training data input bucket "
                                          "name: ")
                                if self.cfg_out_bucket == \
                                        new_input_bucket_name:
                                    print(
                                        "[MESSAGE] Entered bucket name is "
                                        "same as configured training result "
                                        "bucket name. "
                                        "Please provide a new name.")
                                    continue
                                else:
                                    result = self.cos.create_bucket(
                                        new_input_bucket_name, exist_ok=True)
                            except KeyboardInterrupt:
                                sys.exit()
                            except ValueError:
                                print("[MESSAGE] Enter a valid training input"
                                      " data bucket name")
                                continue
                            except TypeError:
                                print("[MESSAGE] Enter a valid training input"
                                      " data bucket name")
                                continue
                            if result is True:
                                print("[MESSAGE] Bucket {} has been created".
                                      format(new_input_bucket_name))
                                local_directory_path = \
                                    self.bucket_data_handling(
                                        new_input_bucket_name)
                                return new_input_bucket_name, \
                                    local_directory_path
                            else:
                                print("[MESSAGE] Enter a valid training input "
                                      "data bucket name")
                                continue

            # Steps to follow if user wants to change the current settings.
            elif (cfg_option.upper() == 'Y'
                  or cfg_option == 'Y') and len(bucket_list) != 0:
                while True:
                    bucket_list_length, input_new_bucket, bucket_list = \
                        self.bucket_list()
                    if int(input_new_bucket) == (bucket_list_length + 1):
                        while True:
                            try:
                                new_input_bucket_name = \
                                    input("[PROMPT] Please enter a new "
                                          "training data input bucket "
                                          "name: ")
                                if self.cfg_out_bucket == \
                                        new_input_bucket_name:
                                    print(
                                        "[MESSAGE] Entered bucket name is "
                                        "same as configured training result "
                                        "bucket name. "
                                        "Please provide a new name.")
                                    continue
                                else:
                                    result = self.cos.create_bucket(
                                        new_input_bucket_name, exist_ok=True)
                            except KeyboardInterrupt:
                                sys.exit()
                            except ValueError:
                                print("[MESSAGE] Bucket name exists in the "
                                      "namespace. Please enter a valid "
                                      "training input data bucket name")
                                continue
                            except TypeError:
                                print("[MESSAGE] Enter a valid training "
                                      "input "
                                      "data bucket name")
                                continue
                            if result is True:
                                print("[MESSAGE] Bucket {} has been "
                                      "created".format(new_input_bucket_name))
                                local_directory_path = \
                                    self.bucket_data_handling(
                                        new_input_bucket_name)
                                return new_input_bucket_name, \
                                    local_directory_path
                            else:
                                print("[MESSAGE] Enter a valid "
                                      "training input "
                                      "data bucket name")
                                continue
                    if self.cfg_out_bucket == bucket_list[int(
                            input_new_bucket) - 1]:
                        print("[MESSAGE] Bucket has been choosen for "
                              "storing results. Provide a new name.")
                        continue
                    if int(input_new_bucket) != (bucket_list_length + 1):
                        print("[MESSAGE] Bucket {} is ready for use. "
                              "Proceeding with further configuration".format(
                                bucket_list[int(input_new_bucket) - 1]))
                        local_directory_path = self.bucket_data_handling(
                            bucket_list[int(input_new_bucket) - 1])
                        return bucket_list[int(input_new_bucket) - 1], \
                            local_directory_path
            else:
                print("[MESSAGE] Invalid option entered. "
                      "Please check and start again.")
                return None, None

    def delete_result_bucket(self, result_bucket):
        """
        Deletes result bucket contents if user wants to.
        :param result_bucket: result bucket name.
        """
        if self.cos.is_bucket_empty(result_bucket) is False:
            print("[MESSAGE] Result Bucket is not empty")
            while True:
                try:
                    bucket_clean_choice = input("[PROMPT] Press 'Y' if you "
                                                "want to delete objects in "
                                                "bucket '{}' and 'N' to "
                                                "proceed with existing "
                                                "data:  "
                                                .format(result_bucket))
                except Exception:
                    print("[MESSAGE] Enter a valid option.")
                    continue
                if bucket_clean_choice == '':
                    print("[MESSAGE] Enter a valid option.")
                    continue
                else:
                    if bucket_clean_choice == 'Y' or \
                            bucket_clean_choice == 'y':
                        print("[MESSAGE]   !!!   WARNING  !!!!  "
                              "Deleting bucket contents")
                        self.cos.clear_bucket(result_bucket)
                        break
                    elif bucket_clean_choice == 'N' or \
                            bucket_clean_choice == 'n':
                        print("[MESSAGE] Result bucket has data "
                              "but proceeding with it")
                        break
                    else:
                        print("[MESSAGE] Enter a valid option.")
                        continue

    def new_bucket_creation(self, bucket_list_length,
                            input_new_bucket, bucket_list): # noqa
        """
        1. Prompt user a new bucket name, if there is no existing
        bucket or user selects option to create a new bucket.
           User will be prompted to enter new name till it gets
           unique bucket name and successful bucket creation.
        2. For other options, retrieve bucket name corresponding
        to the chosen option.
        :param bucket_list_length: number of available buckets.
        :param input_new_bucket: User choice
        :param bucket_list: list containing existing bucket names.
        :return: result bucket name. `None` for any error in process.
        """
        if bucket_list_length == 0 or \
                (int(input_new_bucket) > 0 and
                 int(input_new_bucket) == (bucket_list_length + 1)):
            while True:
                try:
                    new_input_bucket_name = \
                        input("[PROMPT] Enter a new COS "
                              "result bucket name: ")
                except KeyboardInterrupt:
                    sys.exit()
                except Exception:
                    print('[MESSAGE] Enter a valid COS '
                          'result bucket name')
                    continue
                if bucket_list_length != 0 and \
                        new_input_bucket_name in bucket_list:
                    print("[MESSAGE] Bucket with the entered name "
                          "already exists. Please enter a new name!!!")
                    continue
                else:
                    try:
                        create_status = self.cos.create_bucket(
                            new_input_bucket_name)
                    except ValueError:
                        while True:
                            try:
                                new_input_bucket_name = input(
                                    "[PROMPT] Bucket with the entered name "
                                    "is in namespace. Please enter a new "
                                    "result bucket name: ")
                                result_bucket_check = self.cos.create_bucket(
                                    new_input_bucket_name, exist_ok=True)
                            except KeyboardInterrupt:
                                sys.exit()
                            except ValueError:
                                print("[MESSAGE] Enter a valid result "
                                      "bucket name")
                                continue
                            except TypeError:
                                print("[MESSAGE] Enter a valid result "
                                      "bucket name")
                                continue
                            if result_bucket_check is True:
                                print("[MESSAGE] COS result bucket '{}' "
                                      "has been created".format(
                                       new_input_bucket_name))
                                return new_input_bucket_name
                            else:
                                print("[MESSAGE] Enter a valid result"
                                      " bucket name")
                                continue
                    if create_status is True:
                        print("[MESSAGE] Bucket {} is ready for "
                              "use!!!.".format(new_input_bucket_name))
                        return new_input_bucket_name
                    else:
                        print("[MESSAGE] Error in creating bucket "
                              "{}.".format(new_input_bucket_name))
                        return None
        elif int(input_new_bucket) != (bucket_list_length + 1):
            return bucket_list[int(input_new_bucket) - 1]
        else:
            print("[DEBUG] Invalid Entry")
            return None

    def result_bucket_handle(self, input_bucket_name): # noqa
        """
        Handle result bucket.
        1. If result bucket is not configured:
           1.1 Prompt user either to select a bucket name from
           the list of available buckets or choose option to create
               a new bucket.
           1.2 Handle user choice.
        2. If result bucket is configured.
           2.1 Try creating the bucket. If it returns a `ValueError`,
           prompt user to enter a new bucket name.
           2.2 Handle result bucket data if the creation is successful.
        :param input_bucket_name: data input bucket name
        :return: result bucket name. `None` for any error in process.
        """
        print('---------------------------------------------------'
              '----------------')
        print("Cloud Object Storage training result bucket handling")
        print('---------------------------------------------------'
              '----------------')
        if self.cfg_out_bucket is None:
            while True:
                bucket_list_length, input_new_bucket, bucket_list \
                    = self.bucket_list()
                if int(input_new_bucket) != bucket_list_length + 1:
                    if bucket_list[int(input_new_bucket) - 1] \
                            == input_bucket_name:
                        print("[MESSAGE] Same bucket cannot be "
                              "selected for both input and output. "
                              "Try again!!")
                        continue
                    else:
                        break
                else:
                    break
            result_bucket = self.new_bucket_creation(
                bucket_list_length, input_new_bucket, bucket_list)
            if result_bucket is not None:
                self.delete_result_bucket(result_bucket)
                return result_bucket
            else:
                return None
        else:
            print("Configured input bucket:  `{}` ".
                  format(self.cfg_out_bucket))
            if self.cfg_out_bucket == input_bucket_name:
                while True:
                    try:
                        new_input_bucket_name = \
                            input("[PROMPT] Input and result buckets "
                                  "can not be same. Please enter a "
                                  "new name for result bucket: ")
                        if input_bucket_name == new_input_bucket_name:
                            print("[MESSAGE] Input and result bucket "
                                  "names can not be same. Enter a "
                                  "valid result bucket name.")
                            continue
                        else:
                            result_bucket_check = \
                                self.cos.create_bucket(
                                    new_input_bucket_name, exist_ok=True)
                    except KeyboardInterrupt:
                        sys.exit()
                    except ValueError:
                        print("[MESSAGE] Enter a valid result bucket"
                              " name.")
                        continue
                    if result_bucket_check is True:
                        print("[MESSAGE] Bucket {} has been "
                              "created".format(new_input_bucket_name))
                        return new_input_bucket_name
                    else:
                        print("[MESSAGE] Enter a valid "
                              "result bucket name.")
                        continue
            else:
                try:
                    result_bucket_check = \
                        self.cos.create_bucket(
                            self.cfg_out_bucket, exist_ok=True)
                except ValueError:
                    while True:
                        try:
                            new_input_bucket_name = \
                                input("[PROMPT] Bucket with the "
                                      "entered name is in namespace. "
                                      "Please enter a new result "
                                      "bucket name: ")
                            if input_bucket_name \
                                    == new_input_bucket_name:
                                print("[MESSAGE] Input and result "
                                      "bucket names can not be same. "
                                      "Enter a valid result bucket name.")
                                continue
                            else:
                                result_bucket_check = \
                                    self.cos.create_bucket(
                                        new_input_bucket_name,
                                        exist_ok=True)
                        except KeyboardInterrupt:
                            sys.exit()
                        except ValueError:
                            print("[MESSAGE] Enter a valid result "
                                  "bucket name.")
                            continue
                        if result_bucket_check is True:
                            print("[MESSAGE] Bucket {} has been "
                                  "created".format(
                                   new_input_bucket_name))
                            return new_input_bucket_name
                        else:
                            print("[MESSAGE] Enter a valid result "
                                  "bucket name")
                            continue
                else:
                    if result_bucket_check is True:
                        print("[MESSAGE] Bucket {} "
                              "exists.". format(
                               self.cfg_out_bucket))
                        self.delete_result_bucket(self.cfg_out_bucket)
                        return self.cfg_out_bucket

    def configuration_select(self):
        """
        Prompts user to select an appropriate GPU settings
        :return: GPU configuration
        """
        config_options = ['k80', 'k80x2', 'k80x4', 'v100', 'v100x2']
        option_alert = """
*-------------------------------------------------------*
|  NOTE:                                                |
|                                                       |
| Options `v100` and `v100x2` are not for lite plan.    |
| Please choose accordingly.                            |
*-------------------------------------------------------*
                       """
        print(option_alert)
        print('------------------------------------------'
              '-------------------------')
        print('Available compute configurations:    ')
        print('------------------------------------------'
              '-------------------------')
        for ind, value in enumerate(config_options, start=1):
            print("{}. {}".format(ind, value))
        while True:
            config_inp = input("[PROMPT] Your selection: ")
            if config_inp == '':
                print("[MESSAGE] Enter a number between 1 and "
                      "{}.".format(len(config_options)))
                continue
            elif not config_inp.isdigit():
                print("[MESSAGE] Enter a number between 1 and "
                      "{}.".format(len(config_options)))
                continue
            elif int(config_inp) < 1 or \
                    int(config_inp) > len(config_options):
                print("[MESSAGE] Enter a number between 1 and "
                      "{}.".format(len(config_options)))
                continue
            else:
                return config_options[int(config_inp) - 1]

    def configuration_check(self):
        """
        Handle compute configuration setting.
        1. If configured, prompt user whether to proceed with
        same configuration or modify existing config. Prompt
           user to choose from displayed option, if user wishes
           to update the setting.
        2. If not configured, prompt user to choose from the displayed options.
        :return: compute configuration.
        """
        print('------------------------------------------'
              '------------------------')
        print('Configuring GPU resources for training         ')
        print('------------------------------------------'
              '------------------------')
        if self.cfg_cmp_config is None:
            return self.configuration_select()
        else:
            print("[MESSAGE] Configuration has been set as "
                  "{}.".format(self.cfg_cmp_config))
            config_change = input("[PROMPT] Enter 'Y' to "
                                  "proceed as it is and 'N' to "
                                  "change the settings: ")
            if config_change == 'N' or config_change.upper() == 'N':
                return self.configuration_select()
            else:
                return self.cfg_cmp_config
