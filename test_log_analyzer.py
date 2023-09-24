import unittest
from collections import namedtuple
import datetime
import gzip

from log_analyzer import search_log, parse_generator, statistic_urls


class MyTestClass(unittest.TestCase):

    def test_search_log(self):
        config = {"LOG_DIR": "./log"}
        f_log = namedtuple('f_log', 'full_path date extension')
        self.assertEqual(search_log(config), f_log(full_path='./log\\nginx-access-ui.log-20170630.gz',
                                                   date=datetime.datetime.strptime('20170630', '%Y%m%d'),
                                                   extension='.gz'))

    @unittest.skip("demonstrating skipping")
    def test_parse_generator(self):
        tuple_test = ('/',
                      [0.12, 0.12, 0.12, 0.0, 0.12, 0.11, 0.0, 0.02, 0.12, 0.0, 0.01, 0.0, 0.02, 0.12, 0.0, 0.01, 0.0,
                       0.02, 0.0, 0.12, 0.01, 0.12, 0.12, 0.03, 0.24, 0.01, 0.11, 0.0, 0.01, 0.01, 0.11, 0.03, 0.02,
                       0.11, 0.04, 0.01, 0.01, 0.02, 0.0, 0.02, 0.02, 0.0, 0.12, 0.02, 0.11, 0.0, 0.14, 0.03, 0.05,
                       0.05, 0.0, 0.02, 0.02, 0.11, 0.0, 0.01, 0.0, 0.02, 0.09, 0.0, 0.02, 0.1, 0.09, 0.09, 0.0, 0.02,
                       0.12, 0.03, 0.0, 0.03, 0.13, 104.44, 261.52, 299.7, 459.36, 3.16, 142.38, 133.45, 235.88, 184.71,
                       0.02, 0.02, 0.01, 0.0, 0.02, 0.0, 0.02, 0.0, 0.01, 0.0, 0.02, 0.0, 0.0, 0.0, 0.0, 0.11, 0.0,
                       0.01, 0.04, 0.02, 0.01, 0.0, 0.01, 0.0, 0.0, 0.0, 0.0, 0.02, 0.01, 0.12, 0.01, 0.01, 0.07, 0.0,
                       0.02, 0.24, 0.03, 0.01, 0.02, 0.12, 0.01, 4.7, 0.0, 0.01, 0.02, 0.0, 0.22, 0.01, 0.01, 0.03,
                       0.02, 0.64, 0.06, 0.01, 0.06, 0.02, 0.02, 0.11, 0.03, 0.02, 0.02, 0.0, 0.08, 0.01, 0.03, 0.02,
                       0.11, 0.03, 0.02, 0.02, 0.01, 0.01, 0.02, 0.01, 0.18, 0.03, 0.03, 0.02, 0.02, 0.02, 0.02, 0.02,
                       0.0, 0.98, 0.0, 0.11, 0.0, 0.02, 0.03, 0.02, 0.01, 0.01, 0.01, 0.03, 0.66, 0.02, 0.02, 0.01,
                       0.11, 0.03, 0.86, 0.87, 0.01, 0.01, 0.11, 0.02, 0.01, 0.01, 0.02, 0.02, 0.01, 0.03, 0.02, 0.01,
                       0.06, 0.01, 0.02, 0.02, 0.02, 0.01, 0.0, 0.02, 0.02, 0.02, 0.03, 0.02, 0.03, 0.01, 0.01, 0.01,
                       0.12, 0.02, 0.04, 0.02, 0.03, 0.01, 0.03, 0.15, 0.0, 0.06, 0.01, 0.02, 0.0, 3.01, 0.02, 0.03,
                       3.74, 0.03, 0.02, 0.0, 0.02, 0.02, 0.04, 0.02, 0.02, 3.4, 0.02, 0.02, 0.0, 0.02, 0.02, 0.12,
                       0.03, 0.02, 0.02, 0.02, 0.02, 0.02, 0.01, 0.01, 0.01, 0.01, 0.01, 0.04, 0.02, 0.01, 0.02, 0.12,
                       0.02, 0.01, 0.02, 0.02, 0.23, 0.02, 0.03, 0.03, 0.07, 0.01, 0.08, 0.02, 0.02, 0.02, 0.02, 0.02,
                       0.0, 0.02, 0.01, 0.01, 0.03, 0.03, 0.02, 0.02, 0.02, 0.02, 0.02, 0.18, 0.0, 0.02, 0.09, 0.03,
                       0.12, 0.02, 0.01, 0.01, 0.13, 0.02, 0.02, 0.01, 0.02, 0.02, 0.02, 0.0, 0.02, 0.0, 0.01, 0.02,
                       0.01, 0.01, 0.1, 0.02, 0.01, 0.02, 0.04, 0.0, 0.13, 0.01, 0.01, 0.11, 0.02, 0.02, 0.02, 0.0, 0.0,
                       0.01, 0.01, 0.03, 0.0, 0.01, 0.04, 0.01, 0.02, 0.03, 0.03, 0.02, 0.02, 0.05, 0.02, 0.02, 0.03,
                       0.04, 0.02, 0.01, 0.02, 0.02, 0.11, 0.02, 0.02, 0.02, 0.25, 0.0, 0.97, 0.0, 0.41, 0.03, 0.0, 0.0,
                       0.02, 0.01, 0.02, 0.16, 0.02, 0.02, 0.02, 0.02, 0.06, 0.01, 0.02, 0.12, 0.0, 0.02, 0.09, 0.01,
                       0.02, 0.01, 0.02, 0.02, 0.02, 0.0, 0.13, 0.03, 0.03, 0.03, 0.05, 0.02, 0.02, 0.03, 0.11, 0.02,
                       0.02, 0.02, 0.01, 0.07, 0.02, 0.02, 0.0, 0.01, 0.02, 0.02, 0.14, 0.02, 0.14, 0.0, 0.02, 0.09,
                       0.05, 0.02, 0.02, 0.02, 0.01, 0.09, 0.03, 0.19, 0.02, 0.01, 0.01, 0.01, 0.12, 0.06, 0.04, 0.16,
                       0.02, 0.04, 0.07, 0.09, 0.01, 0.03, 0.02, 0.03, 0.02, 0.02, 0.02, 0.01, 0.02, 0.19, 0.01, 0.02,
                       0.02, 0.02, 0.03, 0.02, 0.03, 0.13, 0.02, 0.0, 0.01, 0.01, 0.01, 0.02, 0.02, 0.2, 0.02, 0.03,
                       0.03, 0.03, 0.01, 0.03, 0.06, 0.5, 0.03, 0.01, 0.03, 0.02, 0.02, 0.01, 0.02, 0.0, 0.02, 0.02,
                       0.01, 0.01, 0.38, 0.08, 0.06, 0.01, 0.03, 0.01, 0.12, 0.02, 0.02, 0.03, 0.0, 0.02, 0.01, 0.02,
                       0.03, 0.01, 0.02, 0.01, 0.05, 0.12, 0.02, 0.03, 0.49, 0.13, 0.02, 0.02, 0.02, 0.01, 0.01, 0.32,
                       0.03, 0.04, 0.03, 0.09, 0.02, 0.02, 0.02, 0.01, 0.02, 0.02, 0.02, 0.02, 0.02, 0.16, 0.02, 0.02,
                       0.04, 0.0, 0.01, 0.01, 0.02, 0.11, 0.0, 0.03, 0.02, 0.39, 0.85, 0.01, 0.22, 0.04, 0.01, 0.02,
                       0.18, 0.21, 0.01, 0.01, 0.0, 0.06, 0.02, 0.23, 0.02, 0.02, 0.03, 0.02, 0.01, 0.02, 0.03, 0.02,
                       0.03, 0.13, 0.01, 0.09, 0.02, 0.02, 0.16, 0.01, 0.02, 0.0, 0.03, 0.02, 0.02, 0.02, 0.02, 0.07,
                       0.01, 0.0, 0.01, 0.62, 0.02, 0.02, 0.02, 0.18, 0.02, 0.32, 0.02, 0.0, 0.01, 0.12, 0.02, 0.02,
                       0.01, 0.02, 0.01, 0.01, 0.03, 0.01, 0.0, 0.02, 0.06, 0.04, 0.04, 0.02, 0.19, 0.03, 0.13, 0.04,
                       0.03, 0.03, 0.02, 0.11, 0.02, 0.21, 0.07, 0.0, 0.03, 0.01, 0.01, 0.03, 0.01, 0.0, 0.01, 0.12,
                       0.02, 0.02, 0.05, 0.01, 0.02, 0.02, 0.01, 0.02, 0.08, 0.07, 0.02, 0.01, 0.02, 0.12, 0.02, 0.02,
                       0.04, 0.01, 0.01, 0.01, 0.02, 0.0, 0.02, 0.02, 0.02, 0.02, 0.02, 0.03, 0.0, 0.01, 0.03, 0.06,
                       0.01, 0.0, 0.12, 0.07, 0.0, 0.02, 0.0, 0.02, 0.01, 0.02, 0.02, 0.01, 0.02, 0.02, 0.16, 0.02,
                       0.05, 0.03, 0.12, 0.02, 0.09, 0.08, 0.02, 0.0, 0.01, 0.01, 0.01, 0.02, 0.07, 0.03, 0.07, 0.08,
                       0.12, 0.02, 0.01, 0.13, 0.01, 0.01, 0.03, 0.01, 0.0, 0.01, 0.02, 0.02, 0.15, 0.02, 0.23, 0.04,
                       0.05, 0.03, 0.02, 0.0, 0.02, 0.02, 0.02, 0.12, 0.04, 0.0, 0.0, 0.04, 0.02, 0.01, 0.02, 0.02,
                       0.02, 0.07, 0.02, 0.0, 0.0, 0.02, 0.02, 0.02, 0.02, 0.02, 0.02, 0.03, 0.09, 0.02, 0.03, 0.13,
                       0.01, 0.02, 0.07, 0.02, 0.02, 0.01, 0.0, 0.01, 0.03, 0.02, 0.03, 0.02, 0.05, 0.01, 0.02, 0.0,
                       0.05, 0.12, 0.01, 0.03, 0.02, 0.06, 0.01, 0.01, 0.65, 0.09, 0.02, 0.46, 0.13, 0.0, 0.08, 0.02,
                       0.05, 0.02, 0.01, 0.01, 0.02, 0.02, 0.02, 0.03, 0.12, 0.09, 0.02, 0.0, 0.12, 0.02, 0.02, 0.01,
                       0.04, 0.02, 0.02, 0.0, 0.0, 0.07, 0.03, 0.12, 0.0, 0.0, 0.02, 0.09, 0.02, 0.02, 0.0, 0.12, 0.0,
                       0.0, 0.01, 0.0, 0.0, 0.0, 0.0, 0.0, 0.01, 0.01, 0.02, 0.04, 0.0, 0.02, 0.01, 0.29, 0.01, 0.02,
                       0.02, 0.04, 0.17, 0.03, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.05, 0.01, 0.12, 0.15, 0.02, 0.02, 0.03,
                       0.01, 0.03, 0.02, 0.02, 0.01, 0.1, 0.01, 0.02, 0.02, 0.11, 0.0, 0.01, 0.03, 0.03, 0.03, 0.0,
                       0.01, 0.12, 0.05, 0.09, 0.0, 0.03, 0.02, 0.01, 0.02, 0.02, 2.38, 2.2, 0.01, 0.01, 0.05, 0.12,
                       2.53, 0.03, 0.12, 0.02, 0.01, 0.0, 0.03, 0.02, 0.04, 0.02, 0.02, 0.02, 0.03, 0.02, 0.01, 0.01,
                       0.02, 0.02, 0.0, 0.02, 0.04, 0.0, 0.0, 0.02, 0.02, 0.0, 0.12, 0.09, 0.0, 0.03, 0.02, 0.0, 0.02,
                       0.03, 0.04, 0.0, 0.02, 0.0, 0.02, 0.02, 0.03, 0.13, 0.02, 0.41, 0.02, 0.02, 0.03, 0.0, 0.02,
                       0.11, 0.03, 0.05, 0.02, 0.16, 0.0, 0.02, 0.02, 0.19, 0.03, 0.01, 0.02, 0.05, 0.0, 0.04, 0.0,
                       0.02, 0.02, 0.02, 0.04, 0.18, 0.01, 0.05, 0.01, 0.02, 0.12, 0.01, 0.02, 0.02, 0.02, 0.01, 0.02,
                       0.02, 0.01, 0.08, 0.06, 0.02, 0.02, 0.02, 0.13, 0.21, 0.0, 0.01, 0.02, 0.02, 0.0, 0.12, 0.02,
                       0.02, 0.02, 0.02, 0.05, 0.02, 0.13, 0.16, 0.2, 0.2, 0.0, 0.0, 0.12, 0.03, 0.03, 0.0, 0.12, 0.02,
                       0.0, 0.02, 0.03, 0.0, 0.13, 0.02, 0.02, 0.0, 2.14, 0.01, 0.18, 0.04, 0.04, 0.14, 0.0, 0.01, 0.01,
                       0.04, 0.02, 0.04, 0.03, 0.02, 0.01, 0.03, 0.05, 0.02, 0.03, 0.12, 0.03, 0.03, 0.0, 0.01, 0.12,
                       0.04, 0.02, 0.02, 0.03, 0.02, 0.01, 0.04, 0.04, 0.32, 0.12, 0.13, 0.03, 0.03, 0.03, 0.04, 0.01,
                       0.13, 0.03, 0.01, 0.01, 0.17, 0.01, 0.02, 0.17, 0.02, 0.02, 0.16, 0.02, 0.12, 0.01, 0.02, 0.01,
                       0.03, 0.01, 0.18, 0.44, 0.15, 0.03, 0.02, 0.02, 0.11, 0.16, 0.16, 0.03, 0.01, 0.09, 0.06, 0.05,
                       0.03, 0.02, 0.17, 0.16, 0.11, 0.02, 0.17, 0.01, 0.02, 0.02, 0.03, 0.02, 0.12, 0.35, 0.15, 0.12,
                       0.02, 0.02, 0.02, 0.0, 0.12, 0.18, 0.02, 0.0, 0.53, 0.02, 0.04, 0.02, 0.02, 0.01, 0.02, 0.02,
                       0.02, 0.02, 0.16, 0.02, 0.0, 0.11, 0.03, 0.11, 0.0, 0.17, 0.0, 0.12, 0.02, 0.02, 0.01, 0.03,
                       0.11, 0.0, 0.01, 0.01, 0.0, 0.0, 0.11, 0.0, 0.24, 0.12, 0.01, 0.02, 0.03, 0.11, 0.12, 0.02, 0.0,
                       0.11, 0.12, 0.04, 0.11, 0.01, 0.0, 0.12, 0.0, 0.09, 0.0, 0.02, 0.01, 0.1, 0.12, 0.01, 0.02, 0.0,
                       0.03, 0.0, 0.02, 0.11, 0.0, 0.01, 0.0, 0.01, 0.01, 0.0, 0.0, 0.0, 0.12, 0.12, 0.05, 0.09, 0.11,
                       0.01, 0.01, 0.11, 0.0, 0.02, 0.11, 0.0, 0.02, 0.85, 0.0, 0.11, 0.12, 0.12, 0.12, 0.02, 0.14, 0.0,
                       0.02, 0.12, 0.12, 0.01, 0.0, 0.02, 0.0, 0.01, 0.0, 0.02, 0.11, 0.0, 0.01, 0.0, 0.02, 0.11, 0.01,
                       0.05, 0.13, 0.12, 0.12, 0.11])
        with gzip.open('./log\\nginx-access-ui.log-20170630.gz', 'rb') as log:
            self.assertEqual(next(parse_generator(log)), tuple_test)

    @unittest.skip("demonstrating skipping")
    def test_statistic_urls(self):
        dict_test = {'url': '/api/v2/internal/html5/phantomjs/queue/?wait=1m', 'count': 2767,
                     'count_perc': 0.0010586581555703325, 'time_sum': 174294.12000000084,
                     'time_perc': 0.09093489199980347, 'time_avg': 62.990285507770146, 'time_max': 9843.56,
                     'time_med': 60.07}
        config = {'REPORT_SIZE': 1000, 'REPORT_DIR': './reports', 'LOG_DIR': './log', 'LOG_FILE': './'}
        urls = {}
        with gzip.open('./log\\nginx-access-ui.log-20170630.gz', 'rb') as log:
            for url, statistic in parse_generator(log):
                urls.update({url: statistic})
        self.assertEqual(statistic_urls(urls, config)[0], dict_test)


if __name__ == '__main__':
    unittest.main()