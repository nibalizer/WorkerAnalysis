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



def test_workers_at_frame():

    replay = sc2reader.load_replay(
        'replays/Nerchio vs Neeb ZvP  Newkirk Precinct TE (Void) WCS Austin.SC2Replay',
        engine=sc2reader.engine.GameEngine(plugins=[
            APMTracker(),
            SelectionTracker(),
            ContextLoader(),
            GameHeartNormalizer(),
            workers_analysis(),
        ])
    )
    if replay.players[0].name == "Neeb":
        neeb_pid = 0
        nerchio_pid = 1
    else:
        nerchio_pid = 0
        neeb_pid = 1

    assert workers_at_frame(replay.players[neeb_pid], time_to_frame('4:06')) == 40
    assert workers_at_frame(replay.players[nerchio_pid], time_to_frame('4:32')) == 40
    assert workers_at_frame(replay.players[nerchio_pid], time_to_frame('5:26')) == 50
    assert workers_at_frame(replay.players[neeb_pid], time_to_frame('5:34')) == 50
    assert workers_at_frame(replay.players[neeb_pid], time_to_frame('6:28')) == 60
    assert workers_at_frame(replay.players[neeb_pid], time_to_frame('10:56')) == 70
    assert workers_at_frame(replay.players[nerchio_pid], time_to_frame('12:23')) == 60

    #assert(nerchio, at 4:32, 40 workers)
    #assert(nerchio, at 5:26, 50 workers)
    #assert(neeb, at 5:34, 50 workers)
    #assert(neeb, at 6:28, 60 workers)
    #assert(neeb, at 10:56, 70 workers)
    #assert(nerchio, at 12:23, 60 workers)

