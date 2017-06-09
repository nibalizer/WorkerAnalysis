import sc2reader
from sc2reader.engine.plugins import ContextLoader, APMTracker
from sc2reader.engine.plugins import SelectionTracker, GameHeartNormalizer
from workers_analysis import *


def test_frame_to_time():
    assert frame_to_time(0) == '0:00'
    assert frame_to_time(1) == '0:00'
    assert frame_to_time(22) == '0:00'
    assert frame_to_time(23) == '0:01'
    assert frame_to_time(24) == '0:01'
    assert frame_to_time(44) == '0:01'
    assert frame_to_time(45) == '0:02'
    assert frame_to_time(160) == '0:07'
    assert frame_to_time(460) == '0:20'
    assert frame_to_time(2990) == '2:13'


def test_time_to_frame():
    assert time_to_frame('0:01') == 22
    assert time_to_frame('0:02') == 44
    assert time_to_frame('0:03') == 67
    assert time_to_frame('0:10') == 224
    assert time_to_frame('0:28') == 627
    assert time_to_frame('3:06') == 4166
    assert time_to_frame('12:48') == 17203


def test_alive_at_this_time():

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
        neeb = replay.players[0]
        nerchio = replay.players[1]
    else:
        nerchio = replay.players[0]
        neeb = replay.players[1]

    probe = neeb.units[54]

    assert alive_at_this_time(probe, 0, replay.frames) is False
    assert alive_at_this_time(probe, 28870, replay.frames) is False
    assert alive_at_this_time(probe, 26000, replay.frames) is False
    assert alive_at_this_time(probe, 4500, replay.frames) is True
    assert alive_at_this_time(probe, 2000, replay.frames) is False


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
        neeb = replay.players[0]
        nerchio = replay.players[1]
    else:
        nerchio = replay.players[0]
        neeb = replay.players[1]

    assert workers_at_frame(neeb, time_to_frame('4:06')) == 40
    assert workers_at_frame(nerchio, time_to_frame('4:31')) == 40
    assert workers_at_frame(nerchio, time_to_frame('5:25')) == 50
    assert workers_at_frame(neeb, time_to_frame('5:34')) == 50
    assert workers_at_frame(neeb, time_to_frame('6:28')) == 60
    assert workers_at_frame(neeb, time_to_frame('10:56')) == 70
    assert workers_at_frame(nerchio, time_to_frame('12:22')) == 58
    assert workers_at_frame(nerchio, time_to_frame('12:23')) == 61
