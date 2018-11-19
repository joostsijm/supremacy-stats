"""Scheduler class"""

from datetime import timedelta
from app import scheduler
from app.models import Game
import sync


class Job():
    """Class for handling scheduler"""

    game = None
    job = None
    game_id = None

    def __init__(self, game):
        """Initialize api"""
        self.game = game
        self.game_id = str(game.game_id)
        self.job = scheduler.get_job(self.game_id)

    def start(self):
        """Start job for game"""
        scheduler.add_job(
            id=self.game_id,
            func=run,
            args=[self.game.game_id],
            trigger="interval",
            seconds=5,
        )
#            days=1,
#            start_date=self.game.next_day_time + timedelta(minutes=5)

    def stop(self):
        """Stop job for game"""
        self.job.remove()

    def check(self):
        """Check for existing job"""
        if self.game.end_of_game and self.job is not None:
            self.stop()
        elif not self.game.end_of_game and self.job is None:
            self.start()


def run(game_id):
    """Run the job"""
    print(game_id)

    game = Game.query.filter(Game.game_id == game_id).first()

    if game.track_game:
        sync.update_game(game)
    if game.track_players:
        sync.update_players(game)
    if game.track_score:
        sync.update_score(game)
    if game.track_relations:
        sync.update_relations(game)
    if game.track_coalitions:
        sync.update_coalitions(game)
    if game.track_market:
        sync.update_market(game)


if __name__ == "__main__":
    run.__module__ = "scheduler"

