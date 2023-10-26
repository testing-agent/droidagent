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
    d.app_start("org.odk.collect.android")
    wait()
    current_app = d.app_current()
    
    print(current_app)
    while True:
        current_app = d.app_current()
        print(current_app['package'])
        print(current_app['activity'])
        if current_app['package'] == "org.odk.collect.android" and \
                "FirstLaunch" in current_app['activity']:
            break
        if current_app['package'] == "org.odk.collect.android" and \
                "MainMenu" in current_app['activity']:
            break
        time.sleep(2)
    
    out = d(className="android.widget.TextView", resourceIdMatches=".*try_collect").click()
    wait()
    current_app = d.app_current()
    print(current_app['package'])
    print(current_app['activity'])
    if current_app['package'] == "org.odk.collect.android" and \
            "MainMenu" in current_app['activity']:
        print("****SUCCESS******")
    else:
        print("Demo version activation failed")

    while True:
        d.service("uiautomator").stop()
        time.sleep(2)
        out = d.service("uiautomator").running()
        if not out:
            print("DISCONNECT UIAUTOMATOR2 SUCCESS")
            break
        time.sleep(2)



