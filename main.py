import pandas as pd
from datetime import datetime
import os

# Idea for the best seed is a sequence with all different digits.
# TODO: I didn't consider the first digit to be '-' although the answers can be negative.

def find_best_seed():
    i = 0
    j = 0
    op = ["*", "-", "+"]
    valid = []
    noRepeat = {}
    for i in range(100):
        for j in range(100):
            for s in op:
                statement = f"{i}{s}{j}"
                ans = f"{eval(statement)}"
                fullStatement = f"{statement}={ans}"
                if len(fullStatement) == 8 and fullStatement not in noRepeat:
                    valid.append(genDictFromStatement(fullStatement))
                    noRepeat[fullStatement] = True
                    if s == "*" and i != 0:
                        fullStatement = f"{ans}/{i}={j}"
                        assert fullStatement not in noRepeat
                        valid.append(genDictFromStatement(fullStatement))
                        noRepeat[fullStatement] = True
                    if s == "+":
                        fullStatement = f"{ans}-{i}={j}"
                        assert fullStatement not in noRepeat
                        valid.append(genDictFromStatement(fullStatement))
                        noRepeat[fullStatement] = True
                elif len(fullStatement) == 7 and s == "+":
                    fullStatement = f"{i}-{ans}=-{j}"
                    if fullStatement not in noRepeat:
                        valid.append(genDictFromStatement(fullStatement))
                        noRepeat[fullStatement] = True
                elif len(fullStatement) == 6 and (s == "+" or s == "-"):
                    fullStatement = f"-{ans}{s}{j}=-{i}"
                    assert fullStatement not in noRepeat
                    valid.append(genDictFromStatement(fullStatement))
                    noRepeat[fullStatement] = True

    op = ["*", "-", "+", "/"]
    for i in range(100):
        for j in range(100):
            for k in range(100):
                for x in op:
                    for y in op:
                        statement = f"{i}{x}{j}{y}{k}"
                        try:
                            ans = eval(f"{i}{x}{j}{y}{k}")
                        except ZeroDivisionError:
                            continue
                        else:
                            if float(ans).is_integer() and len(f"{statement}={ans:.0f}") == 8:
                                valid.append((genDictFromStatement(f"{statement}={ans:.0f}")))



    for i in range(1000, 10000):
        valid.append(genDictFromStatement(f"{i}*0=0"))
        valid.append(genDictFromStatement(f"0*{i}=0"))
    return valid


def genDictFromStatement(s):
    return {'statement': s,
            '1': s[0],
            '2': s[1],
            '3': s[2],
            '4': s[3],
            '5': s[4],
            '6': s[5],
            '7': s[6],
            '8': s[7],
            'score': score_statement(s)}

def score_statement(s):
    d = {}
    for x in s:
        if x in d:
            d[x] += 1
        else:
            d[x] = 1
    return len(d)


def df_no(df, x):
    d = df
    for i in range(1,9):
        d = d[d[str(i)] != str(x)]
    return d

# This is the typical existence logic statement.
# Easier to consider the negation of the contrapositive.
# If there exists a X then the contrapositive is all positions is not X.


def pos_no(df, pos, x):
    d = df[df[str(pos)] != str(x)]
    y = d['1'] != str(10)  # lazy way to setting an all true vector
    for i in range(1,9):
        if i != pos:
            y = y & (d[str(i)] != str(x))
    return d[~y]


def set_pos(df, pos, x):
    return df[df[str(pos)] == str(x)]


# the reply is the engine
# format is a string using
# O - correct
# X - incorrect
# R - wrong position


def reply(df, ans, reply):
    assert(len(reply) == 8 and len(ans) == 8)
    d = df
    for i in range(8):
        if reply[i] == 'G':
            d = set_pos(d, i+1, ans[i])
        elif reply[i] == 'B':
            found = False  # There is a special case of double digits. Ignore the color of the second one.
                           # TODO: Need to better the algo by locking the right answers.
            for j in range(8):
                if j < i and ans[i] == ans[j]:
                    found = True
                elif j > i and ans[i] == ans[j] and reply[j] == 'G':
                    found = True
            if not found:
                d = df_no(d, ans[i])
        elif reply[i] == 'R':
            d = pos_no(d, i+1, ans[i])
    return d


# TODO: Code may get into a situation with addition where there are multiple answer
# TODO: with a change of only the first digit. May be better to have 2 random guesses
# TODO: initially.


if __name__ == '__main__':
    if os.path.exists('solspace.csv'):
        df = pd.read_csv('solspace.csv', dtype={1: 'str', 2: 'str', 3: 'str', 4: 'str',
                                                5: 'str', 6: 'str', 7: 'str', 8: 'str', 9: 'str',
                                                10: 'int'})
        print(f"Found solution file!")
    else:
        starttime = datetime.now()
        df = pd.DataFrame(find_best_seed())
        endtime = datetime.now()
        print(f"Solution file not found!\nTook {(endtime-starttime).total_seconds()} seconds to generate!")
        df.to_csv('solspace.csv')

    sorted_df = df.sort_values(by='score', ascending=False)
    only8 = sorted_df[sorted_df['score']==8].sort_values(by='statement')
    d = only8
    ans = d.sample().iloc[0].statement
    d = df
    while len(d) != 1:
        print(f"What is the response to {ans}?\nReply Key: G - Green, B - Black, R - Red")
        r = input()
        if ':' in r:
            ans, r = r.split(":")
            assert(len(ans) == 8)
            assert(len(r) == 8)
        if r == "GGGGGGGG":
            print(f"Lucky! There were another {len(d)-1} options.\nThese were:")
            for index, row in d.iterrows():
                if row['statement'] != ans:
                    print(f"{row['statement']}")
        d = reply(d, ans, r)
        ans = d.sample().iloc[0].statement
    print(f"The answer is {d.sample().iloc[0].statement}!")

