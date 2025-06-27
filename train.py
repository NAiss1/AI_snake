
import argparse
import pickle
import pygame
from constants import WIDTH, HEIGHT, FPS
from game import SnakeGame
from agent import QAgent


def train_snake_ai(episodes: int = 1000, render: bool = False):
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Snake AI – Training")
    clock = pygame.time.Clock()

    game = SnakeGame()
    agent = QAgent()

    for ep in range(episodes):
        state, done = game.reset(), False
        while not done:
            action = agent.act(state)
            nxt, reward, done = game.step(action)
            agent.train(state, action, reward, nxt, done)
            state = nxt
            if render:
                game.render(screen)
                clock.tick(FPS)
        print(f"Episode {ep+1}/{episodes} | Score: {game.score} | Epsilon: {agent.epsilon:.3f}")

    with open("qtable.pkl", "wb") as f:
        pickle.dump(agent.q_table, f)
    pygame.quit()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Train the Q‑Learning Snake AI")
    parser.add_argument("--episodes", type=int, default=1000, help="Number of training episodes")
    parser.add_argument("--render", action="store_true", help="Render during training")
    args = parser.parse_args()

    train_snake_ai(episodes=args.episodes, render=args.render)
