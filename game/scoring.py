"""Scoring system: base + time bonus + streak bonus."""


class ScoreManager:
    BASE_SCORE = 100
    TIME_BONUS_PER_SEC = 3
    STREAK_BONUS = 10

    def __init__(self):
        self.total = 0
        self.streak = 0

    def add_correct(self, remaining_seconds):
        score = self.BASE_SCORE + remaining_seconds * self.TIME_BONUS_PER_SEC
        score += self.streak * self.STREAK_BONUS
        self.streak += 1
        self.total += score
        return score

    def add_wrong(self):
        self.streak = 0
        return 0

    def reset(self):
        self.total = 0
        self.streak = 0
