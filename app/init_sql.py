#! /usr/bin/python

import pymysql

def parse_sql(filename):
    data = open(filename, 'r').readlines()
    stmts = []
    DELIMITER = ';'
    stmt = ''

    for nb_line, line in enumerate(data):
        if not line.strip():
            continue
        if line.startswith('--'):
            continue
        if 'DELIMITER' in line:
            DELIMITER = line.split()[1]
            continue
        if (DELIMITER not in line):
            stmt += line.replace(DELIMITER, ';')
            continue
        if stmt:
            stmt += line
            stmts.append(stmt.strip())
            stmt = ''
        else:
            stmts.append(line.strip())
    return stmts