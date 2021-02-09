import pygame
import pygame.draw

import Constants


class Screen:

    def __init__(self):
        pygame.init()
        self.display = pygame.display.set_mode(Constants.SCREEN_RESOLUTION)
        self.last_update_completed = 0
        self.desired_milliseconds_between_updates = (1.0 / Constants.MAX_FPS) * 1000.0

    def draw_grid(self, grid):
        for row in range(grid.num_rows):
            for col in range(grid.num_cols):
                if grid.is_alive(row, col):
                    self.draw_cell(row, col, Constants.ALIVE_COLOR)
                else:
                    self.draw_cell(row, col, Constants.DEAD_COLOR)
        pygame.display.flip()
        pygame.display.update()

    def draw_cell(self, row, col, color):
        # draw a grid cell upon the screen, given the screen size, cell size and color
        pygame.draw.circle(self.display,
                           color,
                           (int(col * Constants.CEL_SIZE + (Constants.CEL_SIZE / 2)),
                            int(row * Constants.CEL_SIZE + (Constants.CEL_SIZE / 2))),
                           int(Constants.CEL_SIZE / 2),
                           0)

    def clear(self):
        self.display.fill(Constants.DEAD_COLOR)

    @staticmethod
    def num_rows():
        return int(Constants.SCREEN_HEIGHT / Constants.CEL_SIZE)

    @staticmethod
    def num_cols():
        return int(Constants.SCREEN_WIDTH / Constants.CEL_SIZE)

    def cap_frame_rate(self):
        # delay redraw (sleep) for desired_milliseconds_between_updates
        now = pygame.time.get_ticks()
        milliseconds_since_last_update = now - self.last_update_completed
        time_to_sleep = self.desired_milliseconds_between_updates - milliseconds_since_last_update
        if time_to_sleep > 0:
            pygame.time.delay(int(time_to_sleep))
        self.last_update_completed = now
