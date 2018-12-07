"""Scheduler class"""

from datetime import timedelta
from app import scheduler
from app.models import Game


class Job():
    """Class for handling scheduler"""

    game = None
    job = None
    market_job = None
    game_id = None

    def __init__(self, game):
        """Initialize api"""
        self.game = game
        self.game_id = str(game.game_id)
        self.job = scheduler.get_job(self.game_id)
        self.market_job = scheduler.get_job(self.game_id)

    def start(self):
        """Start job for game"""
        scheduler.add_job(
            id=self.game_id,
            func=run,
            args=[self.game.game_id],
            trigger="interval",
            days=1,
            start_date=self.game.next_day_time + timedelta(minutes=5)
        )


    def start_market(self):
        """Start job for market"""
        scheduler.add_job(
            id="market_%s" % self.game_id,
            func=run_market,
            args=[self.game.game_id],
            trigger="interval",
            hours=1,
        )


    def stop(self):
        """Stop job for game"""
        self.job.remove()

    def stop_market(self):
        """Stop job for game"""
        self.market_job.remove()

    def check(self):
        """Check for existing job"""
        if self.game.end_of_game and self.job is not None:
            self.stop()
        elif not self.game.end_of_game and self.job is None:
            self.start()


    def check(self):
        """Check for existing job"""
        if self.game.end_of_game and self.job is not None:
            self.stop()
        elif not self.game.end_of_game and self.job is None:
            self.start()



def run(game_id):
    """Run the job"""

    game = Game.query.filter(Game.game_id == game_id).first()

    import sync

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


def run_market(game_id):
    """Run market job"""

    game = Game.query.filter(Game.game_id == game_id).first()

    import sync

    sync.update_market(game)


if __name__ == "__main__":
    run.__module__ = "scheduler"
    run_market.__module__ = "scheduler"
