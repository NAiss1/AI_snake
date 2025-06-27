
import random
import numpy as np
from constants import DIRECTIONS

class QAgent:
    def __init__(self,
                 gamma: float = 0.9,
                 epsilon: float = 1.0,
                 epsilon_decay: float = 0.995,
                 lr: float = 0.1):
        self.q_table: dict[tuple, np.ndarray] = {}
        self.gamma = gamma
        self.epsilon = epsilon
        self.epsilon_decay = epsilon_decay
        self.lr = lr

    def _qs(self, state):
        return self.q_table.get(state, np.zeros(len(DIRECTIONS)))

    def act(self, state):
        if np.random.rand() < self.epsilon:
            return random.choice(DIRECTIONS)
        return int(np.argmax(self._qs(state)))

    def train(self, s, a, r, s2, done):
        old_q = self._qs(s)[a]
        future_q = 0 if done else np.max(self._qs(s2))
        new_q = old_q + self.lr * (r + self.gamma * future_q - old_q)
        self.q_table[s] = self._qs(s)
        self.q_table[s][a] = new_q
        if done:
            self.epsilon = max(0.01, self.epsilon * self.epsilon_decay)
