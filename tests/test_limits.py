from payments import limits


def test_default_limit(db):
    assert limits.daily_limit("unknown") == 100000.0


def test_set_and_read_limit(db):
    limits.set_daily_limit("m-1", 5000)
    assert limits.daily_limit("m-1") == 5000.0
