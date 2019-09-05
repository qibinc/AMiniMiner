import argparse
import csv
import os
import re

import xlwt


def get_file_list(dir):
    file_list = []
    for filename in os.listdir(dir):
        if filename.endswith(".txt"):
            file_list.append(filename)
    return file_list


def lcs(X, Y):
    # find the length of the strings
    m = len(X)
    n = len(Y)

    # declaring the array for storing the dp values
    L = [[None] * (n + 1) for i in range(m + 1)]

    """Following steps build L[m + 1][n + 1] in bottom up fashion
	Note: L[i][j] contains length of LCS of X[0..i-1]
	and Y[0..j-1]"""
    for i in range(m + 1):
        for j in range(n + 1):
            if i == 0 or j == 0:
                L[i][j] = 0
            elif X[i - 1] == Y[j - 1]:
                L[i][j] = L[i - 1][j - 1] + 1
            else:
                L[i][j] = max(L[i - 1][j], L[i][j - 1])

                # L[m][n] contains the length of LCS of X[0..n-1] & Y[0..m-1]
    return L[m][n]


# end of function lcs


def get_cited_line(content, title):
    scores = []
    for line in content.split("\n"):
        if "tang" not in line.lower() or "lou" not in line.lower():
            continue
        scores.append((lcs(line.lower(), title.lower()), line))
    if scores == []:
        return None, None
    return sorted(scores)[-1]


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--dir", type=str, required=True)
    parser.add_argument("--title", type=str, required=True)
    args = parser.parse_args()

    file_list = get_file_list(args.dir)

    book = xlwt.Workbook()
    sheet = book.add_sheet('sheet1')
    for row, fname in enumerate(file_list):
        with open(os.path.join(args.dir, fname)) as f:
            content = f.read()
            score, line = get_cited_line(content, args.title)
            line = line or "-1"
            match = re.findall(r'\[(\d+)\]', line) + re.findall(r'(\d+)\.', line)
            match = match or ['-1']
            res = re.findall(r'\[[^\]]*' + str(match[0]) + r'[^\]]*\]', content)
            if res == []:
                res = re.findall(re.compile("tang.{1,5}et.{1,3}al", re.IGNORECASE), content)
            if res == []:
                res = ""
            else:
                res = content.index(res[0])
                res = content[res-400:res+400].replace('\n', ' ')
            for col, s in enumerate([fname, line, str(match[0]), res]):
                sheet.write(row,col,s)
    book.save('papers.xls')
