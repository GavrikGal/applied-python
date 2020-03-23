
import argparse
import sys


def output(line):
    print(line)


def grep(lines, params):
    print('params: ', params)
    print('lines: ', lines)
    res_lines = []
    for line in lines:
        line = line.rstrip()
        test_line = line
        print('line: ', line)

        if params.ignore_case:  # Проверка на игнор
            test_line = str(test_line).lower()

        if not params.invert:
            test_line = check_from_pattern(test_line, params.pattern)   # Проверка на соответствие патерну
        else:
            test_line = check_not_from_pattern(test_line, params.pattern)   # Проверка на НЕ соответствие патерну

        if test_line:
            res_lines.append(line)  # Формирование конечного списка для вывода

    if params.count:
        print('\tto output: {}, {}'.format(params.pattern, str(len(res_lines))))
        output(str(len(res_lines)))     # Вывод числа строк соотв. шаблону
    else:
        for res_line in res_lines:
            print('\tto output: {}, {}'.format(params.pattern, res_line))
            output(res_line)            # Вывод строк по заданию


def check_from_pattern(line, pattern):
    if pattern in line:
        return line


def check_not_from_pattern(line, pattern):
    if pattern not in line:
        return line


def parse_args(args):
    parser = argparse.ArgumentParser(description='This is a simple grep on python')
    parser.add_argument(
        '-v', action="store_true", dest="invert", default=False, help='Selected lines are those not matching pattern.')
    parser.add_argument(
        '-i', action="store_true", dest="ignore_case", default=False, help='Perform case insensitive matching.')
    parser.add_argument(
        '-c',
        action="store_true",
        dest="count",
        default=False,
        help='Only a count of selected lines is written to standard output.')
    parser.add_argument(
        '-n',
        action="store_true",
        dest="line_number",
        default=False,
        help='Each output line is preceded by its relative line number in the file, starting at line 1.')
    parser.add_argument(
        '-C',
        action="store",
        dest="context",
        type=int,
        default=0,
        help='Print num lines of leading and trailing context surrounding each match.')
    parser.add_argument(
        '-B',
        action="store",
        dest="before_context",
        type=int,
        default=0,
        help='Print num lines of trailing context after each match')
    parser.add_argument(
        '-A',
        action="store",
        dest="after_context",
        type=int,
        default=0,
        help='Print num lines of leading context before each match.')
    parser.add_argument('pattern', action="store", help='Search pattern. Can contain magic symbols: ?*')
    return parser.parse_args(args)


def main():
    params = parse_args(sys.argv[1:])
    grep(sys.stdin.readlines(), params)


if __name__ == '__main__':
    main()
