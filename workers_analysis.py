import sc2reader
from sc2reader.engine.plugins import ContextLoader, APMTracker
from sc2reader.engine.plugins import SelectionTracker, GameHeartNormalizer


class workers_analysis():
    def __init__(self):
        self.name = "workers analysis"

    def handleInitGame(self, event, replay):
        for human in replay.humans:
            human.at_40_workers_frame = -1
            human.at_50_workers_frame = -1
            human.at_60_workers_frame = -1
            human.at_70_workers_frame = -1


    def handlePlayerStatsEvent(self, event, replay):
        if event.workers_active_count > 40:
            if replay.players[event.player.pid].at_40_workers_frame == -1:
                replay.players[event.player.pid].at_40_workers_frame = event.workers_active_count
        if event.workers_active_count > 50:
            if replay.players[event.player.pid].at_50_workers_frame == -1:
                replay.players[event.player.pid].at_50_workers_frame = event.workers_active_count
        if event.workers_active_count > 60:
            if replay.players[event.player.pid].at_60_workers_frame == -1:
                replay.players[event.player.pid].at_60_workers_frame = event.workers_active_count
        if event.workers_active_count > 70:
            if replay.players[event.player.pid].at_70_workers_frame == -1:
                replay.players[event.player.pid].at_70_workers_frame = event.workers_active_count


obj = {}

replay = sc2reader.load_replay(
    'thereplay.SC2Replay',
    engine=sc2reader.engine.GameEngine(plugins=[
        ContextLoader(),
        APMTracker(),
        SelectionTracker(),
        ContextLoader(),
        GameHeartNormalizer(),
        workers_analysis(),
    ])
)

for player in replay.players:
    print(player.name, player.at_40_workers_frame)


