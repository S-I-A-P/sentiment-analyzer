class UserTweetData:
    total = 0
    positive = 0
    negative = 0
    neutral = 0

    def __str__(self) -> str:
        return 'total: %d, positive: %d, negative: %d, neutral: %d' % (
            self.total, self.positive, self.negative, self.neutral)

    def calculate_value(self) -> float:
        coef_positive = 1
        coef_negative = -1
        coef_neutral = 0

        if self.total == 0:
            return 0.0

        sentiment_sum = coef_positive * self.positive + coef_negative * self.negative + coef_neutral * self.neutral
        return sentiment_sum / self.total
