import robot.running.model as RMM
import robot.parsing.model as RPM
from robot.reporting import ResultWriter
from robot.result.executionresult import Result
from robot.result import ExecutionResult
from robot.api import logger

from mbt_generators.mbt_generators import MBTGeneratorFactory

import yaml
import os


class MBTGeneratorListener(object):
    ROBOT_LISTENER_API_VERSION = 3
    MAX_TEST_NUMBER = 1
    REMOVE_NAME = "Empty Dummy Test"
    INIT_STATE = 'INIT'
    CLEANUP_STATE = 'CLEANUP'
    STATE_PREDICATE_KEYWORD = "Verify {} Predicates"

    def __init__(self, generator="random", model=None, test_number=MAX_TEST_NUMBER, logdir=''):
        """

        :param generator:
        :param model: path to yaml file when mbt model is defined
        :param test_number: maximum number of tested transitions
        :param logdir: folder where temoprary execution result files are stored,
                       if not provided - temoprary results are not generated
        """
        model_dict = yaml.load(open(model))
        self.generator = MBTGeneratorFactory.create_generator(generator, model=model_dict)
        self.test_number = int(test_number)
        self.test_file_counter = 0  # the ID of currently generated test file
        self.test_id_counter = 0   # the ID of the currently running test
        self.current_state = MBTGeneratorListener.INIT_STATE
        self.logdir = logdir  # folder where temporary robot execution result files are stored
        self.current_running_suite = None
        self.current_parsing_suite = None
        self.current_suite_result = None
        self.output_file_path = None
        self.report_file_path = None
        self.transition = None
        self.logger = logger

    def generate_dummy_testcases(self):
        """ Method adds empty test cases to currently executed suite

        :return:
        """
        for _ in xrange(0, self.test_number):
            self.current_running_suite.tests.create(name=self.REMOVE_NAME)

    def create_parsing_suite(self):
        """ Method creates robot.parsing.model test suite to generate static test cases for issue reproduction

        :return: None
        """
        self.current_parsing_suite = RPM.TestData(source=self.current_running_suite.resource.source)
        self.current_parsing_suite.testcase_table = RPM.TestCaseTable(self.current_parsing_suite)

    def overwrite_output_file(self):
        """ Method removes all dummy test results from output.xml file together with messages related with those tests
        It overwrites output.xml file generated by robot executor
        :return: None
        """
        result = ExecutionResult(self.output_file_path)
        result.suite.tests = [test for test in result.suite.tests if self.REMOVE_NAME.lower() not in test.name.lower()]

        ResultWriter(result).write_results(
            output=self.output_file_path, report=self.report_file_path, log=self.logger_file_path
        )

    def generate_valid_test_file_name(self, suffix=''):
        """ Method uses a counter to generate a valid name for static MBT suite used for issue reproduction

        :return: file name
        """
        suffix = suffix or self.test_file_counter
        file_name = "issue_repr_{}.robot".format(suffix)
        self.test_file_counter += 1
        return file_name

    def create_test_file(self, suffix=''):
        """ Method generates a robot file from robot.parsing.model test suite object

        :return: None
        """
        robot_file_name = self.generate_valid_test_file_name(suffix)
        with open(robot_file_name, 'w') as robot_file:
            self.current_parsing_suite.save(output=robot_file, format='robot')

    def add_parsing_model_test(self, running_model_test):
        """ Method converts robot.running.model test object to robot.parsing.model test object and adds it to
        current robot.parsing.model suite

        :param running_model_test: robot.running.model currently executed test case object
        :return:
        """
        parsing_model_test = self.current_parsing_suite.testcase_table.add(name=running_model_test.name)
        for keyword in running_model_test.keywords:
            parsing_model_test.add_step([keyword.name] + list(keyword.args))

    def modify_next_test_name(self):
        """Method replaces a dummy test name with a meaningful name for next state transition

        :return: None
        """
        test_name = "Transition from {} to {} Test {}".format(
            self.current_state, self.transition[1], self.test_id_counter)
        if self.test_id_counter < len(self.current_running_suite.tests) - 1:
            self.test_id_counter += 1
            self.current_running_suite.tests[self.test_id_counter].name = test_name

    def precondition_failed(self, result):
        """Method returns True if test case fails because of precondition keyword failure, False otherwise

        :param result: robot.running.model.TestCase object
        :return: True/False
        """
        if 'precondition' in result.message.lower():
            return True
        return False

    def generate_test_keywords(self):
        """Method adds precondition, transition and state verification keywords to the current
        robot.running.model.TestCase object based on transition selected by generator

        :return: None
        """
        transition, next_state, precondition, _ = self.transition
        self.logger.info("Prepare transition from {} to {}".format(self.current_state, next_state))
        # Add precondition keyword
        if precondition:
            precondition_keyword = RMM.Keyword(name=str(precondition))
            self.current_test.keywords.append(precondition_keyword)
        # Add transition keyword
        transition_keyword = RMM.Keyword(name=str(transition))
        self.current_test.keywords.append(transition_keyword)
        # Add verification keyword
        verification_keyword = RMM.Keyword(name=MBTGeneratorListener.STATE_PREDICATE_KEYWORD.format(next_state))
        self.current_test.keywords.append(verification_keyword)

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
        xml_path, html_path, log_path = self.generate_output_file_names()
        execution_result = Result(root_suite=self.current_suite_result)
        ResultWriter(execution_result).write_results(
            output=xml_path, report=html_path, log=log_path
        )

    """
         Listener Methods
    """
    def start_suite(self, suite, result):
        self.current_running_suite = suite
        self.create_parsing_suite()
        self.generate_dummy_testcases()
        self.current_suite_result = result

    def start_test(self, test, result):
        if self.transition:
            self.current_test = test
            self.generate_test_keywords()

    def end_test(self, test, result):
        # Do nothing if test is skipped because of --exitonfailure flag
        if 'robot-exit' in result.tags:
            return
        # Add current test to static parsing model suite
        self.add_parsing_model_test(test)
        # Store current test execution results
        if self.logdir:
            self.save_intermediate_results()
        # Verify test status
        if not result.passed:
            if not self.precondition_failed(result):
                # If test fails generate a test file to reproduce an issue and create new parsing suite
                self.create_test_file()
                self.create_parsing_suite()
                self.current_state = MBTGeneratorListener.CLEANUP_STATE
                # Another possibility is just fail the whole suite w/o cleanup/rollback and stop the execution
            else:
                # Update results to Passed if Precondition keyword fails
                result.passed = True
        else:
            # Update current state after successful transition
            if self.transition:
                self.current_state = self.transition[1]
        # Generate transition to the next state
        self.transition = self.generator.select_transition_from_current_state(self.current_state)
        self.modify_next_test_name()

    def output_file(self, path):
        self.output_file_path = path

    def log_file(self, path):
        self.logger_file_path = path

    def report_file(self, path):
        self.report_file_path = path

    def close(self):
        self.overwrite_output_file()
        self.create_test_file(suffix="last")
