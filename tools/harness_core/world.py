"""A world that acts back (gap 2): persisted grid with energy tokens.

An oracle answers questions; nothing is downstream. This module gives the
loop a world whose next state already contains the loop's last action:
a grid where energy tokens regrow, the loop spends energy to move and
think, harvests by standing on tokens, and starves when it spends more
than it harvests. State persists to JSON so the world outlives any
single session — the loop meets consequences, not prompts.

Rules (fixed, stated once here):
  * Grid WxH, tokens regrow +regen per empty cell per step up to cap.
  * move costs move_cost energy; think (a model call) costs think_cost.
  * harvest collects the token on the loop's cell, if any.
  * Energy floor at 0: a broke loop cannot move or think until regrow
    puts a token back under it. No credit. No rescue.
  * Every step appends to an event log: (turn, action, energy_before,
    energy_after, harvested). The log is the world's own ledger.

The world never edits the loop and the loop never edits the world
except through act(). Both sides keep their own records.
"""

from __future__ import annotations

import json
import os
import random


class World:
    """Persisted energy grid. One instance = one environment lifetime."""

    def __init__(self, width: int = 8, height: int = 8, *,
                 regen: float = 0.15, token_cap: int = 3,
                 move_cost: float = 1.0, think_cost: float = 2.0,
                 seed: int = 0) -> None:
        self.width = width
        self.height = height
        self.regen = regen
        self.token_cap = token_cap
        self.move_cost = move_cost
        self.think_cost = think_cost
        self.rng = random.Random(seed)
        self.cells: dict[tuple[int, int], int] = {}
        self.agent_xy: tuple[int, int] = (width // 2, height // 2)
        self.energy: float = 5.0
        self.turn: int = 0
        self.harvested_total: int = 0
        self.events: list[dict] = []
        self._seed_tokens()

    # -- setup ----------------------------------------------------------

    def _seed_tokens(self) -> None:
        for _ in range(self.width * self.height // 3):
            x = self.rng.randrange(self.width)
            y = self.rng.randrange(self.height)
            self.cells[(x, y)] = min(
                self.token_cap, self.cells.get((x, y), 0) + 1)

    # -- observation -----------------------------------------------------

    def sense(self) -> dict:
        """What the loop gets as input: position, energy, local tokens."""
        x, y = self.agent_xy
        here = self.cells.get((x, y), 0)
        nearby = sum(
            self.cells.get((x + dx, y + dy), 0)
            for dx in (-1, 0, 1) for dy in (-1, 0, 1)
            if 0 <= x + dx < self.width and 0 <= y + dy < self.height)
        return {'turn': self.turn, 'xy': [x, y], 'energy': self.energy,
                'here': here, 'nearby': nearby,
                'move_cost': self.move_cost, 'think_cost': self.think_cost}

    # -- action ----------------------------------------------------------

    def act(self, action: str) -> dict:
        """Apply one action; the world updates and answers with consequences.

        Actions: harvest | think | up | down | left | right | rest.
        Returns the consequence dict, which becomes the loop's next input.
        """
        before = self.energy
        harvested = 0
        x, y = self.agent_xy
        if action == 'harvest':
            harvested = self.cells.get((x, y), 0)
            self.cells[(x, y)] = 0
            self.energy += harvested
            self.harvested_total += harvested
        elif action in ('up', 'down', 'left', 'right'):
            if self.energy >= self.move_cost:
                dx, dy = {'up': (0, -1), 'down': (0, 1),
                          'left': (-1, 0), 'right': (1, 0)}[action]
                nx, ny = x + dx, y + dy
                if 0 <= nx < self.width and 0 <= ny < self.height:
                    self.agent_xy = (nx, ny)
                    self.energy -= self.move_cost
        elif action == 'think':
            if self.energy >= self.think_cost:
                self.energy -= self.think_cost
        elif action == 'rest':
            pass
        else:
            raise ValueError(f"unknown action {action!r}")
        self.turn += 1
        self._regrow()
        consequence = {'turn': self.turn, 'action': action,
                       'energy_before': before, 'energy_after': self.energy,
                       'harvested': harvested, 'xy': list(self.agent_xy)}
        self.events.append(consequence)
        return consequence

    def _regrow(self) -> None:
        for _ in range(int(self.regen * self.width * self.height) + 1):
            if self.rng.random() < self.regen:
                x = self.rng.randrange(self.width)
                y = self.rng.randrange(self.height)
                self.cells[(x, y)] = min(
                    self.token_cap, self.cells.get((x, y), 0) + 1)

    # -- persistence ------------------------------------------------------

    def to_dict(self) -> dict:
        return {'width': self.width, 'height': self.height,
                'regen': self.regen, 'token_cap': self.token_cap,
                'move_cost': self.move_cost, 'think_cost': self.think_cost,
                'cells': [[x, y, v] for (x, y), v in self.cells.items()],
                'agent_xy': list(self.agent_xy), 'energy': self.energy,
                'turn': self.turn, 'harvested_total': self.harvested_total,
                'events': self.events}

    def save(self, path: str) -> None:
        tmp = path + ".tmp"
        with open(tmp, "w") as f:
            json.dump(self.to_dict(), f)
        os.replace(tmp, path)

    @classmethod
    def load(cls, path: str) -> "World":
        with open(path) as f:
            d = json.load(f)
        w = cls(width=d['width'], height=d['height'], regen=d['regen'],
                token_cap=d['token_cap'], move_cost=d['move_cost'],
                think_cost=d['think_cost'])
        w.cells = {(x, y): v for x, y, v in d['cells']}
        w.agent_xy = tuple(d['agent_xy'])
        w.energy = d['energy']
        w.turn = d['turn']
        w.harvested_total = d['harvested_total']
        w.events = d['events']
        return w
