from os import environ
import unittest
import tests.all_tests

environ['APP_SETTINGS'] = 'testing'
testSuite = tests.all_tests.create_test_suite()
text_runner = unittest.TextTestRunner().run(testSuite)
