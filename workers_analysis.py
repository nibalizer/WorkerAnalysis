import sc2reader
from sc2reader.engine.plugins import ContextLoader, APMTracker
from sc2reader.engine.plugins import SelectionTracker, GameHeartNormalizer


class workers_analysis():
    def __init__(self):
        self.name = "workers analysis"

    def frame_to_time(self, frame):
        # This forces everything up to the next second into
        # the previous second
        # ex
        # frame 0 : 0:00
        # frame 1 - 22: 0:01
        # frame 23 - 45: 0:02
        game_seconds = int(frame / 22.4)

        minutes = int(game_seconds / 60)
        seconds = game_seconds - (60 * minutes)
        return '{0}:{1:02d}'.format(minutes, seconds)

    def time_to_frame(self, time):
        # This always returns the bottom frame so there will be frames
        # that can never be accessed with this function
        # ex:
        # time 0:01: frame 22
        # time 0:02: frame 44
        # time 0:03: frame 67
        if ':' not in time:
            raise SyntaxError("Must be a MM:SS formatted time string")
        minutes, seconds = map(int, time.split(":"))
        total_seconds = minutes * 60 + seconds
        frames = int(total_seconds * 22.4)
        return frames


    def alive_at_this_time(self, unit, time, frames):
        if unit.died_at is None:
            unit.died_at = frames
        if time >= unit.finished_at and time <= unit.died_at:
            return True
        else:
            return False


    def workers_at_frame(self, player, frame):
        workers = 0
        workers_array = []
        for unit in player.units:
            if unit.is_worker:
                if alive_at_this_time(unit, frame, player.total_replay_frames):
                    workers += 1
                    workers_array.append(unit)
        return workers

    def handleInitGame(self, event, replay):
        for human in replay.humans:
            human.total_replay_frames = replay.frames
            # For zerg these are a bit funky around buildings
            # we count the drone in here until the building is completely finished
            # This is an obvious place to work to improve
            human.worker_milestones = {
                40: None,
                50: None,
                60: None,
                70: None,
            }

    def handleEndGame(self, event, replay):
        total_frames = replay.frames
        for human in replay.humans:
            for milestone in [40, 50, 60, 70]:
                for frame in range(0, total_frames):
                    workers = workers_at_frame(human, frame)
                    if workers >= milestone:
                        human.worker_milestones[milestone] = frame
                        break



def frame_to_time(frame):
    # This forces everything up to the next second into
    # the previous second
    # ex
    # frame 0 : 0:00
    # frame 1 - 22: 0:01
    # frame 23 - 45: 0:02
    game_seconds = int(frame / 22.4)

    minutes = int(game_seconds / 60)
    seconds = game_seconds - (60 * minutes)
    return '{0}:{1:02d}'.format(minutes, seconds)

def time_to_frame(time):
    # This always returns the bottom frame so there will be frames
    # that can never be accessed with this function
    # ex:
    # time 0:01: frame 22
    # time 0:02: frame 44
    # time 0:03: frame 67
    if ':' not in time:
        raise SyntaxError("Must be a MM:SS formatted time string")
    minutes, seconds = map(int, time.split(":"))
    total_seconds = minutes * 60 + seconds
    frames = int(total_seconds * 22.4)
    return frames


def alive_at_this_time(unit, time, frames):
    if unit.died_at is None:
        unit.died_at = frames
    if time >= unit.finished_at and time <= unit.died_at:
        return True
    else:
        return False


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
            APMTracker(),
            SelectionTracker(),
            ContextLoader(),
            GameHeartNormalizer(),
            workers_analysis(),
        ])
    )
