from collections import defaultdict


def print_result(prob, state):
    print("Probability:", prob)
    print("State:", state)


pi = {
    "p": 0.46,
    "q": 0.1,
    "r": 0.44,
}

a = {
    "p": {
        "p": 0.55,
        "q": 0.18,
        "r": 0.27,
    },
    "q": {
        "p": 0.13,
        "q": 0.05,
        "r": 0.82,
    },
    "r": {
        "p": 0.54,
        "q": 0.09,
        "r": 0.37,
    },
}

b = {
    "0": {
        "p": 0.78,
        "q": 0.68,
        "r": 0.59,
    },
    "1": {
        "p": 0.22,
        "q": 0.32,
        "r": 0.41,
    },
}

Q = list(a.keys())
SIGMA = list(b.keys())


def delta(time: int, now_state, output: str, dp) -> tuple[float, str | None]:
    if time == 0:
        return pi[now_state] * b[output][now_state], None
    else:
        preds = [dp[time - 1][before_state] * a[before_state][now_state] * b[output][now_state] for before_state in Q]
        return max(preds), Q[preds.index(max(preds))]


o = input()

ans = []
dp = defaultdict(lambda: defaultdict(float))
bp: defaultdict[int, defaultdict[str, str | None]] = defaultdict(lambda: defaultdict(lambda: None))

for t in range(len(o)):
    assert o[t] in SIGMA
    for state in Q:
        dp[t][state], bp[t][state] = delta(t, state, o[t], dp)


max_state = None
max_prob = -1
for q in Q:
    prob = dp[len(dp) - 1][q]
    if max_state is None or prob > max_prob:
        max_prob = prob
        max_state = q
assert max_prob >= 0 and max_prob <= 1
assert max_state is not None

before_state = max_state
ans: list[str] = []
for t in range(len(o) - 1, -1, -1):
    assert before_state is not None
    ans.append(before_state)
    before_state = bp[t][before_state]

ans = ans[::-1]
print_result(max_prob, "".join(ans))
