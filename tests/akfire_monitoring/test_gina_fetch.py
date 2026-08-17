import gina_fetch


def test_connection():
    txt_files, nc_files = gina_fetch.fetch_viirs_detections()
    assert len(txt_files) != 0
    assert len(txt_files) == len(nc_files)
