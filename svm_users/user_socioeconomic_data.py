class UserSocioeconomicData:
    economic_policy = 0.0
    social_policy = 0.0
    economic_policy_rounded = 0.0
    social_policy_rounded = 0.0

    def __init__(self, economic_policy, social_policy, economic_policy_rounded, social_policy_rounded, ) -> None:
        super().__init__()
        self.economic_policy = economic_policy
        self.social_policy = social_policy
        self.economic_policy_rounded = economic_policy_rounded
        self.social_policy_rounded = social_policy_rounded

    def __str__(self) -> str:
        return \
            'economic_policy: %.2f, social_policy: %.2f, economic_policy_rounded: %.2f, social_policy_rounded: %.2f' % (
                self.economic_policy, self.social_policy, self.economic_policy_rounded, self.social_policy_rounded)
