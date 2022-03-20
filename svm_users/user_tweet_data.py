class UserTweetData:
    total = 0
    positive = 0
    negative = 0
    neutral = 0

    def __str__(self) -> str:
        return 'total: %d, positive: %d, negative: %d, neutral: %d' % (
            self.total, self.positive, self.negative, self.neutral)
