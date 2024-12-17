from toolkits.capture.recorder import is_captured_url, ApiMonitorRecord, db_client


def test_is_captuerd_url():
    print(is_captured_url("https://www.baidu.com/"))


def test_save_record():
    record = ApiMonitorRecord(
        status_code =200,
        app="test"
    )
    db_client.save(record)

test_save_record()