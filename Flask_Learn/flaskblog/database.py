from sqlalchemy import create_engine, text

db_connection_string = "mysql+pymysql://2naahj3wjte7sag4lgll:pscale_pw_aHoiZ6aD6S7rZCyYDAlUAXxjie1DrD5oxLxXDTaBCqh@ap-southeast.connect.psdb.cloud/sportsgowhere_db?charset=utf8mb4"

engine = create_engine(
    db_connection_string,
    connect_args={
        "ssl": {
            "ssl_ca": "/etc/ssl/cert.pem"
        }
    })
