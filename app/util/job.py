"""Scheduler class"""

from datetime import timedelta
from app import scheduler
from app.models import Game


class BaseJob():
    """Base class for jobs"""

    game = None
    game_id = None
    job = None

    def __init__(self, game):
        """Standard constructor for jobs"""
        self.game = game
        self.game_id = str(game.game_id)

    def start(self):
        """Start the scheduler"""
        pass

    def stop(self):
        """Stop job for game"""
        if self.job is not None:
            self.job.remove()
            self.job = None

    def check(self):
        """Check for existing job"""
        if self.game.end_of_game and self.job is not None:
            self.stop()
        elif not self.game.end_of_game and self.job is None:
            self.start()


class Job(BaseJob):
    """Class for handling scheduler"""

    def __init__(self, game):
        """Initialize Job"""
        BaseJob.__init__(self, game)
        self.game_id = str(game.game_id)
        self.job = scheduler.get_job(self.game_id)

    def start(self):
        """Start job for game"""
        if self.job is None:
            self.job = scheduler.add_job(
                id=self.game_id,
                func=run,
                args=[self.game.game_id],
                trigger="interval",
                days=1,
                start_date=self.game.next_day_time + timedelta(minutes=5)
            )


class MarketJob(Job):
    """Class for market job"""

    def __init__(self, game):
        """Initialize MarketJob"""
        Job.__init__(self, game)
        self.job = scheduler.get_job("market_%s" % self.game_id)

    def start(self):
        """Start job"""
        if self.job is None:
            self.job = scheduler.add_job(
                id="market_%s" % self.game_id,
                func=run,
                args=[self.game.game_id, "market"],
                trigger="interval",
                hours=1,
            )


def run(game_id, job_type=None):
    """Run the job"""

    game = Game.query.filter(Game.game_id == game_id).first()

    import sync

    if job_type == "market":
        sync.update_market(game)
    else:
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


if __name__ == "__main__":
    run.__module__ = "scheduler"
