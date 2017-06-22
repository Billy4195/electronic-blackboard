from test_mysql import Mysql
from test_env_init import Env_init
from test_arrange_schedule import Arrange_Schedule
import unittest

def main():
    testcases = [Mysql,Env_init,Arrange_Schedule]
    suite = unittest.TestSuite()
    for case in testcases:
        tmp = unittest.TestLoader().loadTestsFromTestCase(case)
        suite.addTests(tmp)

    unittest.TextTestRunner(verbosity=2).run(suite)

if __name__ == "__main__":
    main()
