#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Log analyzer for nginx log
"""
import datetime
import gzip
import json
import os
import re
import sys
from collections import namedtuple
from itertools import groupby
from statistics import mean, median
from string import Template
import logging
import yaml

# log_format ui_short '$remote_addr  $remote_user $http_x_real_ip [$time_local] "$request" '
#                     '$status $body_bytes_sent "$http_referer" '
#                     '"$http_user_agent" "$http_x_forwarded_for" "$http_X_REQUEST_ID"'
#                     '"$http_X_RB_USER" $request_time';

config = {
    "REPORT_SIZE": 1000,
    "REPORT_DIR": "./reports",
    "LOG_DIR": "./log"
}

if os.listdir("./config"):
    try:
        with open("./config/config.yaml", "r", encoding="utf-8") as f:
            config_file = yaml.safe_load(f)
            config_file = config_file["constants"]
        config.update(config_file)
        logging.basicConfig(level=logging.INFO, filename=os.path.join(config["LOG_FILE"],
                          "log_analyzer.log"), format="[%(asctime)s] %(levelname).1s %(message)s")
    except KeyError:
        logging.error("KeyError")
    except EOFError:
        logging.error("EOFError")
else:
    logging.basicConfig(level=logging.INFO, filename=None,
                        format="[%(asctime)s] %(levelname).1s %(message)s")


def search_log(conf):
    """
    Search log nginx in directory LOG_DIR
    """
    logging.info("Run def search_log()")
    try:
        path = conf["LOG_DIR"]
        files_log = os.listdir(path)
        if len(files_log) == 0:
            sys.exit(1)
        day = 0
        for file in files_log:
            if re.fullmatch(r'nginx-access-ui.log-\d{8}.gz', file) \
                    or re.fullmatch(r'nginx-access-ui.log-\d{8}.plain', file):
                dt_int = re.search(r'\d{8}', file)
                if int(dt_int[0]) > day:
                    day = int(dt_int[0])
                    full_path = os.path.join(path, file).replace("\\", "/")
                    extension = os.path.splitext(file)[1]
        day = datetime.datetime.strptime(str(day), '%Y%m%d')
        f_log = namedtuple('f_log', 'full_path date extension')
        last_file_log = f_log(full_path=full_path, date=day, extension=extension)
        return last_file_log
    except ValueError:
        logging.error("ValueError")
    except IndexError:
        logging.error("IndexError")
    return None


def parse_generator(log):
    """
    Generator for parse nginx log
    """
    logging.info("Run def parse_generator()")
    try:
        list_url = []
        cnt_error = 0
        cnt_line = 0
        for line in log:
            try:
                list_line = line.decode().split("\"")
                url = list_line[1].split(' ')[1]
                time_url = float(list_line[-1][:-2])
                list_url.append((url, time_url))
                cnt_line += 1
            except IndexError:
                cnt_error += 1

        if cnt_error / cnt_line < 0.3:
            list_url.sort(key=lambda x: x[0])
            for key, group in groupby(list_url, lambda x: x[0]):
                yield key, [i[1] for i in group]
        else:
            logging.error("High percentage of log parsing errors")
            sys.exit(1)
    except ValueError:
        logging.error("ValueError")
    except IndexError:
        logging.error("IndexError")


def statistic_urls(urls, conf):
    """
    Calculation statistics on urls
    """
    logging.info("Run def statistic_urls()")
    try:
        count_all = 0
        sum_all = 0
        value = urls.values()
        list_urls = []
        for val in value:
            count_all += len(val)
            sum_all += sum(val)
        dict_url = {}
        for key, value in urls.items():
            dict_url.update({"url": key})
            dict_url.update({"count": len(value)})
            dict_url.update({"count_perc": len(value) / count_all})
            dict_url.update({"time_sum": sum(value)})
            dict_url.update({"time_perc": sum(value) / sum_all})
            dict_url.update({"time_avg": mean(value)})
            dict_url.update({"time_max": max(value)})
            dict_url.update({"time_med": median(value)})
            list_urls.append(dict_url)
            dict_url = {}

        sort_list_urls = sorted(list_urls, key=lambda x: x["time_sum"], reverse=True)
        return sort_list_urls[:conf["REPORT_SIZE"]]
    except ValueError:
        logging.error("ValueError")
    except IndexError:
        logging.error("IndexError")
    return None


def main():
    """
    Main function
    """
    logging.info("Run def main()")
    try:
        data_log = search_log(config)
        for file in os.listdir(config["REPORT_DIR"]):
            if str(data_log.date.strftime("%Y.%m.%d")) in file:
                logging.error("Report with this date already exists")
                sys.exit(1)
        urls = {}
        with gzip.open(data_log.full_path, 'rb') if data_log.extension == '.gz' else open(
                data_log.full_path, 'r', encoding="utf-8") as log:
            for url, statistic in parse_generator(log):
                urls.update({url: statistic})
        sort_list_urls = statistic_urls(urls, config)
        table_json = json.dumps(sort_list_urls)
        dict_urls = {"table_json": table_json}
        with open(os.path.join(config["REPORT_DIR"], 'report.html'), "r", encoding="utf-8") as file:
            text = file.read()
            temp = Template(text)
        with open(os.path.join(config["REPORT_DIR"], f'report-'
                                                 f'{data_log.date.strftime("%Y.%m.%d")}.html'), "w",
                  encoding="utf-8") as file:
            file.write(temp.safe_substitute(dict_urls))
    except ValueError:
        logging.error("ValueError")
    except IndexError:
        logging.error("IndexError")
    except EOFError:
        logging.error("EOFError")
    except FileExistsError:
        logging.error("FileExistsError")
    except FileNotFoundError:
        logging.error("FileNotFoundError")
    except Exception as err:
        logging.exception(err)


if __name__ == "__main__":
    main()
