class VoteInter:

    def calc_avg_rate(self, votes):
        v_amount = len(votes)
        s = 0
        if v_amount > 0:
            for v in votes:
                s += v.value
            rate = s/v_amount
            return round(rate, 2)
        else:
            return 0
