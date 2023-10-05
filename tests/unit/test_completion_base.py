from app.core.completion.base import SplitTooLongMessage


def test_split_too_long_message_with_backticks():
    long_message = "This is a long message with triple backticks ``` that should be preserved.``` this the end of the message"
    spliter = SplitTooLongMessage(long_message, 50)
    messages = spliter._split_with_backticks()
    assert len(messages) == 3
    assert messages[0] == "This is a long message with triple backticks"
    assert messages[1] == "``` that should be preserved.```"


def test_split_a_too_long_part():
    long_message = "whatever"
    spliter = SplitTooLongMessage(long_message, 50)

    part = "This is a long part for test.\n the method split a too long part"

    result = spliter._split_a_too_long_part(part)
    assert len(result) == 2
    assert all([len(part) <= 50 for part in result])


def test_split_a_too_long_part_with_backticks():
    long_message = "whatever"
    spliter = SplitTooLongMessage(long_message, 50)

    part = "```\nthe method split a too long part\nsplit a too long part\nreturn a + b\n```"

    result = spliter._split_a_too_long_part_with_backticks(part)
    assert len(result) == 2
    assert all([len(part) <= 50 for part in result])


def test_split_a_long_complete_message():
    long_message = (
        "This is a long message\nwith triple backticks\n```\nthat should be preserved.\nwith lines\nre```\nthis the end of the message\nbut long"
    )
    spliter = SplitTooLongMessage(long_message, 25)
    messages = spliter.result()
    assert len(messages) == 6
    assert all([len(part) <= 50 for part in messages])


def test_split_a_short_complete_message():
    long_message = "This is a short message"
    spliter = SplitTooLongMessage(long_message, 1000)
    messages = spliter.result()
    assert len(messages) == 1
    assert messages == ["This is a short message"]


def test_split_a_too_long_part_with_backticks_in_python():
    long_message = "whatever"
    spliter = SplitTooLongMessage(long_message, 50)

    part = "```python\nthe method split a too long part\nsplit a too long part\nreturn a + b\n```"

    result = spliter._split_a_too_long_part_with_backticks(part)
    assert len(result) == 2
    assert all([len(part) <= 50 for part in result])
    assert all([part.startswith("```python") for part in result])


def test_split_a_too_long_part_with_backticks_in_bash():
    long_message = "whatever"
    spliter = SplitTooLongMessage(long_message, 50)

    part = "```bash\nthe method split a too long part\nsplit a too long part\nreturn a + b\n```"

    result = spliter._split_a_too_long_part_with_backticks(part)
    assert len(result) == 2
    assert all([len(part) <= 50 for part in result])
    assert all([part.startswith("```bash") for part in result])
