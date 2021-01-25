class VoteInter:

    def calc_avg_rate(self, votes):
        """Calculate drink average rate.

        Function gets list of votes assigned to specific drinks and calculate
        average rate rounded to 2 decimal digits.

        Parameters
        ----------
        votes: list of Vote objects

        Returns
        -------
        0
            If there are no Votes assigned to Drink.
        float
            If there are Votes assigned to Drink it returns calculated rate.
        """
        v_amount = len(votes)
        s = 0
        if v_amount > 0:
            for v in votes:
                s += v.value
            rate = s/v_amount
            return round(rate, 2)
        else:
            return 0
