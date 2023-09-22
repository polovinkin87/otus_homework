#!/usr/bin/env python
# -*- coding: utf-8 -*-
import datetime
import gzip
import json
import os
import re
from collections import namedtuple
from itertools import groupby
from statistics import mean, median
from string import Template
import yaml
import logging


# log_format ui_short '$remote_addr  $remote_user $http_x_real_ip [$time_local] "$request" '
#                     '$status $body_bytes_sent "$http_referer" '
#                     '"$http_user_agent" "$http_x_forwarded_for" "$http_X_REQUEST_ID" "$http_X_RB_USER" '
#                     '$request_time';

config = {
    "REPORT_SIZE": 2000,
    "REPORT_DIR": "./reports",
    "LOG_DIR": "./log"
}

logging.basicConfig(level=logging.INFO, filename="py_log.log", format="%(asctime)s %(levelname)s %(message)s")

with open("./config/config.yaml", "r", encoding="utf-8") as f:
    config_file = yaml.safe_load(f)
    config_file = config_file["constants"]

config.update(config_file)


def search_log(config):
    path = config["LOG_DIR"]
    files_log = os.listdir(path)
    dt = 0
    for f in files_log:
        if re.fullmatch(r'nginx-access-ui.log-\d{8}.gz', f) or re.fullmatch(r'nginx-access-ui.log-\d{8}.plain', f):
            dt_int = re.search(r'\d{8}', f)
            if int(dt_int[0]) > dt:
                dt = int(dt_int[0])
                full_path = os.path.join(path, f)
                extension = os.path.splitext(f)[1]
    dt = datetime.datetime.strptime(str(dt), '%Y%m%d')
    f_log = namedtuple('f_log', 'full_path date extension')
    last_file_log = f_log(full_path=full_path, date=dt, extension=extension)
    return last_file_log


def parse_generator(log):
    list_url = []
    k = 0
    for line in log:
        try:
            list_line = line.decode().split("\"")
            url = list_line[1].split(' ')[1]
            time_url = float(list_line[-1][:-2])
            list_url.append((url, time_url))
        except IndexError as err:
            print(err)
            k += 1

    print(k)
    list_url.sort(key=lambda x: x[0])
    for key, group in groupby(list_url, lambda x: x[0]):
        yield key, [i[1] for i in group]


def statistic_urls(urls, config):
    count_all = 0
    sum_all = 0
    val = urls.values()
    list_urls = []
    for el in val:
        count_all += len(el)
        sum_all += sum(el)
    dict_url = {}
    for k, v in urls.items():
        dict_url.update({"url": k})
        count = len(v)
        dict_url.update({"count": count})
        count_perc = count / count_all
        dict_url.update({"count_perc": count_perc})
        time_sum = sum(v)
        dict_url.update({"time_sum": time_sum})
        time_perc = time_sum / sum_all
        dict_url.update({"time_perc": time_perc})
        time_avg = mean(v)
        dict_url.update({"time_avg": time_avg})
        time_max = max(v)
        dict_url.update({"time_max": time_max})
        time_med = median(v)
        dict_url.update({"time_med": time_med})
        list_urls.append(dict_url)
        dict_url = {}

    sort_list_urls = sorted(list_urls, key=lambda x: x["time_sum"], reverse=True)
    return sort_list_urls[:config["REPORT_SIZE"]]


def main():
    data_log = search_log(config)
    urls = {}
    with gzip.open(data_log.full_path, 'rb') if data_log.extension == '.gz' else open(data_log.full_path, 'rb') as log:
        for url, statistic in parse_generator(log):
            urls.update({url: statistic})
    sort_list_urls = statistic_urls(urls, config)
    # table_dict = {i[0]: i[1:] for i in sort_list_urls}
    table_json = json.dumps(sort_list_urls)
    d = dict(table_json=table_json)
    with open(os.path.join(config["REPORT_DIR"], 'report.html'), "rb") as file:
        text = file.read()
        t = Template(text.decode())
    with open(
            os.path.join(config["REPORT_DIR"],
                         f'report-{data_log.date.strftime("%Y.%m.%d")}.html'),
            "w") as file:
        file.write(t.safe_substitute(d))


if __name__ == "__main__":
    main()
