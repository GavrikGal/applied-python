# -*- encoding: utf-8 -*-
from datetime import datetime
import collections


def reader(filename):
    with open(filename) as f:
        log = f.read()
    return log


def parse(
        ignore_files=False,
        ignore_urls=[],
        start_at=None,
        stop_at=None,
        request_type=None,
        ignore_www=False,
        slow_queries=False
):
    log = reader('log.log')
    data = parse_data(log, ignore_www, start_at, stop_at, request_type, ignore_urls)

    counter = collections.Counter()
    for line in data:
        counter[line['url']] += 1

    if slow_queries:
        result = most_slow_queries(counter, data, 5)
        return result

    result = [val for key, val in counter.most_common(5)]
    return result


def parse_data(log, ignore_www=False, start_at=None, stop_at=None, needed_request_type=None, ignore_urls=None) -> list:
    data = []
    if start_at:
        start_at = datetime.strptime(start_at, '%d/%b/%Y %H:%M:%S')
    if stop_at:
        stop_at = datetime.strptime(stop_at, '%d/%b/%Y %H:%M:%S')

    line: str
    for line in log.split('\n'):
        try:
            str_date, str_data = line.split('] "')
            str_date = str_date[1:]
            request_date = datetime.strptime(str_date, '%d/%b/%Y %H:%M:%S')
            if start_at and request_date < start_at:
                continue
            if stop_at and request_date > stop_at:
                break

            str_data, response_code_and_time = str_data.split('" ')
            request_type, request, protocol = str_data.split(' ')
            if needed_request_type and needed_request_type != request_type:
                continue

            response_code, response_time = response_code_and_time.split(' ')
            url = request.split('://')[1]
            if ignore_www:
                url = str(url).replace('web.', '')
            if ignore_urls and url in ignore_urls:
                continue

            data.append({'request_date': request_date,
                         'request_type': request_type,
                         'request': request,
                         'protocol': protocol,
                         'response_code': int(response_code),
                         'response_time': int(response_time),
                         'url': url,
                         })
        except ValueError:
            pass
    return data


def most_slow_queries(counter, data, count_number) -> list:
    res = []
    for url in counter:
        sum_time = 0
        for data_line in data:
            if data_line['url'] == url:
                sum_time += data_line['response_time']
        res.append(sum_time // counter.get(url))
    return sorted(res, reverse=True)[:count_number]
