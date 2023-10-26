import sys
import time

import uiautomator2 as u2


def wait(seconds=3):
    for i in range(0, seconds):
        print("wait 1 second ..")
        time.sleep(1)

    
if __name__ == '__main__':
    avd_serial = sys.argv[1]
    d = u2.connect(avd_serial)
    # d.WAIT_FOR_DEVICE_TIMEOUT = 70
    d.app_start("me.zeeroooo.materialfb")
    wait()
    current_app = d.app_current()
    
    print(current_app)
    while True:
        current_app = d.app_current()
        print(current_app['package'])
        print(current_app['activity'])
        if current_app['package'] == "me.zeeroooo.materialfb" and \
                "MainActivity" in current_app['activity']:
            break
        time.sleep(2)
    
    out = d(className="android.widget.EditText", resourceIdMatches=".*login_email").set_text("anony1017mous@gmail.com")
    if out:
        print("SUCCESS")
    wait()

    out = d(className="android.widget.EditText", resourceIdMatches=".*login_password").set_text("green1029*")
    if out:
        print("SUCCESS")
    wait()

    out = d(className="android.widget.Button", textMatches="Log in.*").click()
    if out:
        print("SUCCESS")
    wait()

    while True:
        d.service("uiautomator").stop()
        time.sleep(2)
        out = d.service("uiautomator").running()
        if not out:
            print("DISCONNECT UIAUTOMATOR2 SUCCESS")
            break
        time.sleep(2)



