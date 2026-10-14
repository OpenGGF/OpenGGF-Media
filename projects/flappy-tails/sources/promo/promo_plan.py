"""The Flappy Tails promo's edit decision list. Capture times are seconds into each capture;
run tick T of seed 0x5eed appears at capture second (T + 3) / 60."""


def sec(run_tick):
    return (run_tick + 3) / 60


def PLAN(card, clip, root):
    caps = root / "caps"
    tour = caps / "tour" / "tour.mp4"
    title = caps / "title" / "title.wav"
    miniboss = root / "soundboard" / "music-2E" / "music.wav"
    final_boss = root / "soundboard" / "music-30" / "music.wav"
    theme = root / "soundboard" / "music-2F" / "music.wav"   # mus_DataSelect, the title theme, 40 s
    s = []
    # The rating card, in silence, as trailers do.
    s.append(lambda: card("00-approved", 150))
    # Cold open: trailer slams over the miniboss theme, each with a ROM stinger.
    s.append(lambda: card("01-this-season", 84, sfx="boom", music=miniboss, music_from=0.0, music_gain=0.8))
    s.append(lambda: card("02-one-hero", 72, sfx="flying", sfx_at=0.15, music=miniboss, music_from=1.4, music_gain=0.8))
    s.append(lambda: card("03-one-button", 72, sfx="switch", sfx_gain=1.4, music=miniboss, music_from=2.6, music_gain=0.8))
    s.append(lambda: card("04-no-mercy", 60, sfx="death", music=miniboss, music_from=3.8, music_gain=0.8))
    # The title, then five zones, carried on the title theme.
    s.append(lambda: clip("title", caps / "title" / "title.mp4", 0.0, 4.6))
    s.append(lambda: card("05-five-zones", 150, sfx="dash", music=title, music_from=4.6, music_gain=1.0))
    # The tour: each zone's own music under its own cut, a flash at every cut.
    s.append(lambda: clip("aiz1", tour, 4.2, 2.8, flash_at=(0.0,)))
    s.append(lambda: clip("aiz2", tour, sec(1114) - 0.3, 3.0, flash_at=(0.0,)))
    s.append(lambda: clip("hcz", tour, sec(2241) - 0.2, 2.8, flash_at=(0.0,)))
    s.append(lambda: clip("lbz", tour, sec(3305) - 0.2, 2.8, flash_at=(0.0,)))
    s.append(lambda: clip("ssz", tour, sec(4313) - 0.2, 2.8, flash_at=(0.0,)))
    # The ROM's own flight, proved in slow motion on a close call.
    s.append(lambda: card("06-rom-flight", 120, sfx="flying", sfx_at=0.0))
    s.append(lambda: clip("close-call", tour, sec(2557) - 1.0, 1.6, speed=0.4))
    # Rings save you: 32 rings burst at capture tick 861.
    s.append(lambda: card("07-rings-save-you", 72, sfx="ring", sfx_at=0.05))
    s.append(lambda: clip("rings", caps / "rings" / "rings.mp4", 13.4, 4.4, flash_at=(861 / 60 - 13.4,)))
    # The critics.
    s.append(lambda: card("08-reviews", 240, music=theme, music_from=8.0, music_gain=1.0))
    # Super Tails.
    s.append(lambda: card("09-super", 90, sfx="super", sfx_gain=1.2))
    s.append(lambda: clip("super-on", tour, sec(5218) - 0.4, 2.6, flash_at=(0.4,)))
    smashes = [5583, 5666, 5749, 5832, 5914, 5997, 6080]
    start = sec(smashes[0]) - 0.5
    s.append(lambda: clip("super-smash", tour, start, 8.4,
                          punches=tuple(sec(t) - start for t in smashes)))
    # Even heroes fall. Then the end card, and the stinger after it.
    s.append(lambda: clip("crash", caps / "crash" / "crash.mp4", 42.4, 9.6))
    s.append(lambda: card("10-end", 300, sfx="bigring", sfx_at=1.2, music=theme, music_from=0.0, music_gain=1.0))
    s.append(lambda: card("11-post-credits", 180, sfx="rumble", sfx_at=0.0, music=final_boss, music_from=4.0, music_gain=0.9))
    return s
