
import argparse
import pickle
import numpy as np
import pygame
import imageio

from constants import WIDTH, HEIGHT, FPS
from game import SnakeGame


def play_with_trained_agent(qtable_path: str = "qtable.pkl",
                            gif_output: str = "snake_ai.gif",
                            max_frames: int = 300):
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Snake AI – Playback")
    clock = pygame.time.Clock()

    # Load Q‑table
    with open(qtable_path, "rb") as f:
        q_table = pickle.load(f)

    policy = lambda st: int(np.argmax(q_table.get(st, np.zeros(4))))

    game = SnakeGame()
    state, done, frames = game.reset(), False, []

    while not done:
        action = policy(state)
        state, _, done = game.step(action)
        game.render(screen)

        # collect frame for GIF
        frames.append(np.transpose(pygame.surfarray.array3d(screen), (1, 0, 2)))
        clock.tick(FPS)

        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                done = True
        if max_frames and len(frames) >= max_frames:
            done = True

    pygame.quit()
    if frames and gif_output:
        imageio.mimsave(gif_output, frames, fps=FPS)
        print(f"GIF saved to {gif_output}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Watch the trained agent play")
    parser.add_argument("--gif", type=str, default="snake_ai.gif", help="Output GIF file path (empty to skip)")
    parser.add_argument("--max_frames", type=int, default=300, help="Limit GIF length (None = unlimited)")
    args = parser.parse_args()

    play_with_trained_agent(gif_output=args.gif, max_frames=args.max_frames)
