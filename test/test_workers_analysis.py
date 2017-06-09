import sc2reader
from sc2reader.engine.plugins import ContextLoader, APMTracker
from sc2reader.engine.plugins import SelectionTracker, GameHeartNormalizer
from workers_analysis import *


# Test 1

def do_thing():

    replay = sc2reader.load_replay(
        'replays/Neeb vs Nerchio PvZ  Honorgrounds LE WCS Austin.SC2Replay',
        engine=sc2reader.engine.GameEngine(plugins=[
            APMTracker(),
            SelectionTracker(),
            ContextLoader(),
            GameHeartNormalizer(),
            workers_analysis(),
        ])
    )
    assert(replay.player[1].at_40_workers_frame == -1)
    assert(replay.player[2].at_40_workers_frame == 5760)
    assert(replay.player[1].at_50_workers_frame == -1)
    assert(replay.player[2].at_50_workers_frame == -1)
    assert(replay.player[1].at_60_workers_frame == -1)
    assert(replay.player[2].at_60_workers_frame == -1)
    assert(replay.player[1].at_70_workers_frame == -1)
    assert(replay.player[2].at_70_workers_frame == -1)



# Test 2


def do_other_thing():

    replay = sc2reader.load_replay(
        'replays/Neeb vs Nerchio PvZ  NewKirk.SC2Replay',
        engine=sc2reader.engine.GameEngine(plugins=[
            APMTracker(),
            SelectionTracker(),
            ContextLoader(),
            GameHeartNormalizer(),
            workers_analysis(),
        ])
    )

    #assert(neeb, at 4:06, 40 workers)
    #assert(nerchio, at 4:32, 40 workers)
    #assert(nerchio, at 5:26, 50 workers)
    #assert(neeb, at 5:34, 50 workers)
    #assert(neeb, at 6:28, 60 workers)
    #assert(neeb, at 10:56, 70 workers)
    #assert(nerchio, at 12:23, 60 workers)


def test_frame_to_time():
    assert frame_to_time(160) == '0:10'
    assert frame_to_time(460) == '0:28'
    assert frame_to_time(2990) == '3:06'

def test_time_to_frame():
    assert time_to_frame('0:10') == 160
    assert time_to_frame('0:28') == 448
    assert time_to_frame('3:06') == 2976


def frame_to_time(frame):
    # note for future python3 work
    game_seconds = int(frame / 16)

    minutes = int(game_seconds / 60)
    seconds = game_seconds - (60 * minutes)
    return '{0}:{1:02d}'.format(minutes, seconds)
