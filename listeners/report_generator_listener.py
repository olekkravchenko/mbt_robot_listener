import robot.result.model as RRM
from robot.reporting import ResultWriter
from robot.result.executionresult import Result
from robot.api import logger

import os


class ReportGeneratorListener(object):
    ROBOT_LISTENER_API_VERSION = 2

    def __init__(self, logdir=''):
        """
        :param logdir: folder where temoprary execution result files are stored,
                       if not provided - temoprary results are not generated
        """
        self.logdir = logdir  # folder where temporary robot execution result files are stored
        self.current_report_suite = None
        self.current_report_test = None
        self.current_report_keyword = None
        self.current_parent = None
        self.hierarchy_stack = []

    def generate_output_file_names(self):
        """ Method generates valid file names for temporary robot execution result files from provided logdir parameter
        It also creates logdir folder if it does not exist

        :return:
        """
        if self.logdir and not os.path.isdir(self.logdir):
            os.mkdir(self.logdir)
        return os.path.join(self.logdir, 'tmp_output.xml'), \
               os.path.join(self.logdir, 'tmp_report.html'), \
               os.path.join(self.logdir, 'tmp_log.html')

    def save_intermediate_results(self):
        """Method creates intermediate robot result files during test execution

        :return:
        """
        if not self.logdir:
            return
        xml_path, html_path, log_path = self.generate_output_file_names()
        execution_result = Result(root_suite=self.current_report_suite)
        ResultWriter(execution_result).write_results(
            output=xml_path, report=html_path, log=log_path
        )

    @staticmethod
    def copy_object_attributes(result, attributes):
        """Method attempts to assign all attributes in robot.result.model object to corresponding values from
        attributes dictionary

        :param result: robot.result.model object
        :param attributes: dictionary passed to listener methods by robot
        :return:
        """
        for attr, value in attributes.iteritems():
            try:
                if attr.lower() == u'status' and type(result) != RRM.TestSuite:
                    result.passed = value.lower() == u'pass'
                    continue
                if attr.lower() in \
                        [u'elapsedtime', u'critical', u'longname', u'id', u'type', u'tests', u'statistics', u'status']:
                    continue
                if hasattr(result, attr):
                    setattr(result, attr, value)
            except (AttributeError, TypeError) as e:
                logger.warn("Cann't set {} to {}: {}".format(attr, value, e))

    def get_keyword_object_by_name(self, name):
        """

        :param name: keyword name
        :return:robot.result.model.Keyword object from keywords stack matching the keywords name
        """
        return (keyword for keyword in reversed(self.hierarchy_stack) if keyword.name.lower() == name.lower()).next()

    """
         Listener Methods
    """

    def start_suite(self, name, attributes):
        self.current_report_suite = RRM.TestSuite(name)
        self.hierarchy_stack.append(self.current_report_suite)

    def end_suite(self, name, attributes):
        ReportGeneratorListener.copy_object_attributes(self.current_report_suite, attributes)

    def start_test(self, name, attributes):
        self.current_report_test = RRM.TestCase(name)
        self.current_report_suite.tests.append(self.current_report_test)
        self.hierarchy_stack.append(self.current_report_test)

    def end_test(self, name, attributes):
        ReportGeneratorListener.copy_object_attributes(self.current_report_test, attributes)
        self.hierarchy_stack.pop()
        self.save_intermediate_results()

    def start_keyword(self, name, attributes):
        self.current_parent = self.hierarchy_stack[-1]
        self.current_report_keyword = RRM.Keyword(
            kwname=name, args=attributes['args'], tags=attributes['tags'],
        )
        self.current_parent.keywords.append(self.current_report_keyword)
        self.hierarchy_stack.append(self.current_report_keyword)

    def end_keyword(self, name, attributes):
        keyword = self.get_keyword_object_by_name(name)
        ReportGeneratorListener.copy_object_attributes(keyword, attributes)
        self.hierarchy_stack.pop()

    def log_message(self, attributes):
        message = RRM.Message(
            message=attributes['message'], level=attributes["level"],
            timestamp=attributes["timestamp"], html=attributes["html"]
        )
        self.current_report_keyword.messages.append(message)
