import pandas as pd

# Idea for the best seed is a sequence with all different digits.
# TODO: I didn't consider the first digit to be '-' although the answers can be negative.

def find_best_seed():
    i = 0
    j = 0
    op = ["*", "-", "+", "/"]
    valid = []
    while i < 100:
        while j < 100:
            for s in op:
                statement = ""
                if s == "/" and j != 0 and i % j == 0:
                    statement = f"{i}{s}{j}"
                    if len(f"{i}{s}{j}={eval(statement):.0f}") == 8:
                        statement = f"{i}{s}{j}={eval(statement):.0f}"
                    else:
                        statement = ""
                elif s != "/":
                    statement = f"{i}{s}{j}"
                    if len(f"{i}{s}{j}={eval(statement)}") == 8:
                        statement = f"{i}{s}{j}={eval(statement)}"
                    else:
                        statement = ""
                if len(statement) > 0:
                    valid.append({'statement': statement,
                                  '1': statement[0],
                                  '2': statement[1],
                                  '3': statement[2],
                                  '4': statement[3],
                                  '5': statement[4],
                                  '6': statement[5],
                                  '7': statement[6],
                                  '8': statement[7],
                                  'score': score_statement(statement)})
            j += 1
        i += 1
        j = 0
    return valid


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
            d = df_no(d, ans[i])
        elif reply[i] == 'R':
            d = pos_no(d, i+1, ans[i])
    return d


# TODO: Code may get into a situation with addition where there are multiple answer
# TODO: with a change of only the first digit. May be better to have 2 random guesses
# TODO: initially.


if __name__ == '__main__':
    df = pd.DataFrame(find_best_seed())
    sorted_df = df.sort_values(by='score', ascending=False)
    only8 = sorted_df[sorted_df['score']==8].sort_values(by='statement')
    d = only8
    ans = d.sample().iloc[0].statement
    d = df
    while len(d) != 1:
        print(f"What is the response to {ans}?\nReply Key: G - Green, B - Black, R - Red")
        r = input()
        d = reply(d, ans, r)
        ans = d.sample().iloc[0].statement
    print(f"The answer is {d.sample().iloc[0].statement}!")

