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
            human.total_replay_frames = replay.frames

    def handlePlayerStatsEvent(self, event, replay):
        #print(event.player, event.frame, event.workers_active_count, frame_to_time(event.frame))
        workers = 0
        #for unit in event.player.units:
        #    if unit.is_worker and alive_at_this_time(unit, event.frame, replay):
        #        print(unit.died_at)
        #        workers += 1
        #print("Workers: ",  workers)
        #event.workers_active_count = workers

def frame_to_time(frame):
    # note for future python3 work
    game_seconds = int(frame / 16)

    minutes = int(game_seconds / 60)
    seconds = game_seconds - (60 * minutes)
    return '{0}:{1:02d}'.format(minutes, seconds)

def time_to_frame(time):
    if ':' not in time:
        raise SyntaxError("Must be a MM:SS formatted time string")
    minutes, seconds = map(int, time.split(":"))
    total_seconds = minutes * 60 + seconds
    frames = total_seconds * 16
    return frames


def alive_at_this_time(unit, time, frames):
    if unit.died_at is None:
        unit.died_at = frames
    if time >= unit.finished_at and time <= unit.died_at:
        return True
    else:
        return False

def frames_at_workers_count(player, count):
    for index in range(len(times)):
        if player.workers_data[index] > count:
            return(times[index])

def workers_at_frame(player, frame):
    workers = 0
    workers_array = []
    for unit in player.units:
        if unit.is_worker:
            if alive_at_this_time(unit, frame, player.total_replay_frames):
                workers += 1
                workers_array.append(unit)
    return workers


if __name__ == "__main__":

    replay = sc2reader.load_replay(
        'thereplay.SC2Replay',
        engine=sc2reader.engine.GameEngine(plugins=[
            ContextLoader(),
            APMTracker(),
            SelectionTracker(),
            GameHeartNormalizer(),
            workers_analysis(),
        ])
    )

    # All done in frames
    game_end = replay.frames
    game_start = 0
    times = range(game_start, game_end, 160)
    replay.times = times

#    for player in replay.players:
#        workers = []
#        worker_count = 0
#        for current_frame in range(game_start, game_end, 160):
#            current_workers = 0
#            # Scan all units owned by player
#            workers_at_time = []
#            for unit in player.units:
#                if unit.is_worker and alive_at_this_time(unit, current_frame, replay):
#                    #print(unit)
#                    #print(unit.died_at)
#                    current_workers += unit.supply
#                    workers_at_time.append(unit)
#            workers.append(current_workers)
#            if current_workers >= 40 and player.name == "Neeb":
#                from pdb import set_trace; set_trace()
#        player.workers_data = workers

#    print(replay.map_name)
#    print(replay.frames /16. /60.)
#    print(40)
#    print(replay.players[1].name)
#    print(frames_at_workers_count(replay.players[1], 40)/ 16)
#    print(frame_to_time(frames_at_workers_count(replay.players[1], 40)))
#    print(40)
#    print(replay.players[0].name)
#    print(frames_at_workers_count(replay.players[0], 40)/ 16)
#    print(frame_to_time(frames_at_workers_count(replay.players[0], 40)))
#    workers_at_frame(replay.players[0], 9500)

    #evs = [i for i in replay.events if i.name == "PlayerStatsEvent"]
    #for e in evs:
    #    print(e.player, e.frame, e.workers)
