from collections import defaultdict


class HMM:
    def __init__(self, pi: dict[str, float], a: dict[str, dict[str, float]], b: dict[str, dict[str, float]]):
        self.pi = pi
        self.a = a
        self.b = b
        self.Q = list(a.keys())
        self.SIGMA = list(b.keys())

    def delta(self, time: int, now_state, output: str, dp) -> tuple[float, str | None]:
        if time == 0:
            return self.pi[now_state] * self.b[output][now_state], None
        else:
            preds = [
                dp[time - 1][before_state] * self.a[before_state][now_state] * self.b[output][now_state]
                for before_state in self.Q
            ]
            return max(preds), self.Q[preds.index(max(preds))]

    def bp(self, time: int, now_state, output: str, dp) -> str:
        if time == 0:
            return now_state
        else:
            preds = [
                dp[time - 1][before_state] * self.a[before_state][now_state] * self.b[output][now_state]
                for before_state in self.Q
            ]
            return self.Q[preds.index(max(preds))]

    def viterbi(self, o: str) -> None:
        dp = defaultdict(lambda: defaultdict(float))
        bp: defaultdict[int, defaultdict[str, str | None]] = defaultdict(lambda: defaultdict(lambda: None))

        for t in range(len(o)):
            assert o[t] in self.SIGMA
            for state in self.Q:
                dp[t][state], bp[t][state] = self.delta(t, state, o[t], dp)

        max_state = None
        max_prob = -1
        for q in self.Q:
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
            before_state = self.bp(t, before_state, o[t], dp)

        ans = ans[::-1]
        self.print_result(max_prob, ans)

    def print_result(self, max_prob, ans):
        print(max_prob)
        print("".join(ans))


if __name__ == "__main__":
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

    hmm = HMM(pi, a, b)
    o = input()
    hmm.viterbi(o)
    