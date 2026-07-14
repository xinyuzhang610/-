from init_db import server_url_from_database_url


def test_server_url_keeps_mysql_driver_and_credentials():
    url = "mysql+pymysql://zjiaotong_app:secret@127.0.0.1:3306/zjiaotong"

    assert server_url_from_database_url(url) == "mysql+pymysql://zjiaotong_app:secret@127.0.0.1:3306"
