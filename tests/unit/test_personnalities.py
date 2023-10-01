from app.core.personnalities import AvaFront, Sam, JakePy, LilyLinux


def test_personnality_sam():
    bot = Sam()
    assert bot.name == "Sam"
    assert len(bot.instructions) == 0
    assert len(bot.example_convos) == 0


def test_personnality_AvaFront():
    bot = AvaFront()
    assert bot.name == "AvaFront"
    assert len(bot.instructions) > 0
    assert len(bot.example_convos) > 0


def test_personnality_JakePy():
    bot = JakePy()
    assert bot.name == "JakePy"
    assert len(bot.instructions) > 0
    assert len(bot.example_convos) > 0


def test_personnality_LilyLinux():
    bot = LilyLinux()
    assert bot.name == "LilyLinux"
    assert len(bot.instructions) > 0
    assert len(bot.example_convos) > 0
