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
        if "tang" not in line.lower() or "wu" not in line.lower():
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

    with open('records.tsv', 'w') as tsvfile:
        book = xlwt.Workbook()
        sheet = book.add_sheet('sheet1')
        for row, fname in enumerate(file_list):
            with open(os.path.join(args.dir, fname)) as f:
                content = f.read()
                score, line = get_cited_line(content, args.title)
                line = line or "0"
                match = re.findall(r'\[(\d*)\]', line)
                match = match or ['0']
                # res = content.index(str(match[0]))
                # pattern = r'\[^\]*{match[0]}^\]*\]'
                # print(r'\[^\]*{match[0]}^\]*\]')
                # res = re.findall(pattern, content)
                res = re.findall(r'\[[^\]]*' + str(match[0]) + r'[^\]]*\]', content)
                # res = content.index(match[0])
                # print(res)
                if res == []:
                    res = [content[0]]
                res = content.index(res[0])
                res = content[res-100:res+100].replace('\n', ' ')
                # res = '.'.join(res.split('.')[1:-1]) + '.'
                for col, s in enumerate([fname, score, line, str(match[0]), res]):
                    sheet.write(row,col,s)
        book.save('papers.xls')
