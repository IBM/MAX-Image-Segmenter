from .debug import debug

import re
from watson_machine_learning_client.wml_client_error import ApiRequestFailure


class WMLWrapperException(Exception):
    pass


class WMLWrapper:
    """Basic wrapper class for common WML tasks
    """
    def __init__(self, wml_client=None):
        self.client = wml_client

    def start_training(self,
                       model_building_archive,
                       model_definition_metadata,
                       training_configuration_metadata):
        """
        Start WML training
        :param model_building_archive: path to zipped model_definition
        :type model_building_archive: str

        :param model_definition_metadata: model definition metadata
        :type model_definition_metadata: dict

        :param training_configuration_metadata: training definition metadata
        :type training_configuration_metadata: dict

        :returns: training run guid
        :rtype: str

        :raises WMLWrapperException: an error occurred
        """

        assert model_building_archive is not None, \
            'Parameter model_building_archive cannot be None'
        assert model_definition_metadata is not None, \
            'Parameter model_definition_metadata cannot be None'
        assert training_configuration_metadata is not None, \
            'Parameter training_configuration_metadata cannot be None'

        debug('parm training_configuration_metadata:',
              training_configuration_metadata)
        debug('parm model_definition_metadata:', model_definition_metadata)

        try:

            # Store training definition into Watson Machine Learning
            # repository on IBM Cloud.
            definition_details = \
                self.client.repository.store_definition(
                                        model_building_archive,
                                        model_definition_metadata)

            debug('store_definition details:', definition_details)

            # Get uid of stored definition
            definition_uid = \
                self.client.repository.get_definition_uid(definition_details)

            debug('get_definition_uid:', definition_uid)

            # Train model
            training_run_details = \
                self.client.training.run(definition_uid,
                                         training_configuration_metadata)

            debug('run details: ', training_run_details)

            # Get uid of training run
            run_uid = self.client.training.get_run_uid(training_run_details)

            debug('run uid: {}'.format(run_uid))

            return run_uid
        except Exception as ex:
            raise(WMLWrapperException(ex))

    def get_training_status(self,
                            training_guid,
                            ignore_server_error=False):
        """ Get status of a training run.

            :param training_guid: Existing WML training run guid
            :type training_guid: str

            :param ignore_server_error: if set, None is returned
            if an HTTP 5xx status code was returned by the service
            :type ignore_server_error: bool

            :returns: training run status, or None
            :rtype: dict

            :raises WMLWrapperException: an error occurred
        """

        assert training_guid is not None, \
            'Parameter training_guid cannot be None'

        status = None
        try:
            status = self.client.training.get_status(training_guid)
        except ApiRequestFailure as arf:
            debug('Exception type: {}'.format(type(arf)))
            debug('Exception: {}'.format(arf))
            # terrible hack to obtain HTTP status code from
            # the exception's error message text
            if arf.error_msg:
                status_code = None
                for line in arf.error_msg.split('\n'):
                    m = re.match(r'Status code: (\d\d\d)',
                                 line)
                    if m:
                        status_code = int(m.group(1))
                if status_code:
                    debug('HTTP status code: {}'.format(status_code))
                    if status_code >= 500 and ignore_server_error:
                        return None
            raise WMLWrapperException(arf)
        except Exception as ex:
            debug('Exception type: {}'.format(type(ex)))
            debug('Exception: {}'.format(ex))
            raise WMLWrapperException(ex)

        debug('Training status: ', status)

        # Example status
        # {
        #   "state": "completed",
        #   "finished_at": "2019-04-15T22:24:58.648Z",
        #   "submitted_at": "2019-04-15T22:21:15.907Z",
        #   "running_at": "2019-04-15T22:21:52.940Z",
        #   "message": "training-Ax5PvBRWg: ",
        #   "metrics": [],
        #   "current_at": "2019-04-15T22:25:25.500Z"
        # }

        return status

    def get_training_results_references(self,
                                        training_guid,
                                        ignore_server_error=False):
        """ Get status of a training run
            :param training_guid: Existing WML training run guid
            :type training_guid: str

            :param ignore_server_error: if set, None is returned
            if an HTTP 5xx status code was returned by the service
            :type ignore_server_error: bool

            :returns: training run status
            :rtype: dict

            :raises WMLWrapperException: an error occurred
        """

        assert training_guid is not None, \
            'Parameter training_guid cannot be None'

        details = None
        try:
            # fetch details for this training run
            details = self.client.training.get_details(training_guid)
            debug('Training run details:', details)
        except ApiRequestFailure as arf:
            debug('Exception type: {}'.format(type(arf)))
            debug('Exception: {}'.format(arf))
            # terrible hack to obtain HTTP status code from
            # the exception's error message text
            if arf.error_msg:
                status_code = None
                for line in arf.error_msg.split('\n'):
                    m = re.match(r'Status code: (\d\d\d)',
                                 line)
                    if m:
                        status_code = int(m.group(1))
                if status_code:
                    debug('HTTP status code: {}'.format(status_code))
                    if status_code >= 500 and ignore_server_error:
                        return None
            raise WMLWrapperException(arf)
        except Exception as ex:
            debug('Exception type: {}'.format(type(ex)))
            debug('Exception: {}'.format(ex))
            raise WMLWrapperException(ex)

        # extract results bucket name and model location from the response
        if ((details.get('entity', None) is not None) and
            (details['entity']
                .get('training_results_reference', None) is not None) and
            (details['entity']['training_results_reference']
                .get('location', None) is not None)):
            return(
                details['entity']['training_results_reference']['location'])
        # the response did not contain the expected results
        return {}
