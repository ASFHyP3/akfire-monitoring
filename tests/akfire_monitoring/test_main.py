import main


def test_prepare_feds():
    name = 'test_FEDS'
    feds_job = main.prepare_feds(name)

    assert feds_job['name'] == name
    assert feds_job['job_type'] == 'AK_FIRE_SAFE'


def test_prepare_firetrack():
    name = 'test_FIRETRACK'
    firetrack_job = main.prepare_firetrack(name)

    assert firetrack_job['name'] == name
    assert firetrack_job['job_type'] == 'FIRE_TRACK'
