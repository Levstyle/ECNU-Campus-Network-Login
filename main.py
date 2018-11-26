import requests
from lxml import html
from apscheduler.schedulers.blocking import BlockingScheduler


def login(username, password):
    sess = requests.session()
    login_url = "https://login.ecnu.edu.cn/srun_portal_pc.php?ac_id=1&"

    def user_login():
        tree = html.fromstring(sess.get(login_url).text)

        keys = ["action", "ac_id", "user_ip", "ip", "nas_ip", "user_mac", "url", "is_second"]
        values = [(tree.xpath("//input[@name='{}']/@value".format(key))[0]) for key in keys]

        payload = {
            "ajax": "1",
            "save_me": "0",
            "username": username,
            "password": password
        }

        return sess.post(login_url, data={**dict(zip(keys, values)), **payload}, headers=dict(referer=login_url))

    return user_login


if __name__ == "__main__":
    scheduler = BlockingScheduler()
    scheduler.add_job(login("username", "password"), 'interval', minutes=15)
    scheduler.start()
