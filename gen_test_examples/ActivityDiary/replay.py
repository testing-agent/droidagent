
import sys
import time
import uiautomator2 as u2

def wait(seconds=3):
    for i in range(0, seconds):
        print("wait 1 second ..")
        time.sleep(1)

def wait_until_activity(d, activity_name, max_wait=30):
    for i in range(0, max_wait):
        current_app = d.app_current()
        if current_app['package'] == "de.rampro.activitydiary.debug" and activity_name in current_app['activity']:
            break
        time.sleep(1)
    
    # if the target activity is not launched, raise exception
    current_app = d.app_current()
    if current_app['package'] != "de.rampro.activitydiary.debug" or activity_name not in current_app['activity']:
        raise Exception(f"Action precondition cannot be satisfied: %s is not launched" % activity_name)

def go_back_until_inside_app(d, max_backtrack=10):
    for i in range(0, max_backtrack):
        current_app = d.app_current()
        if current_app['package'] == "de.rampro.activitydiary.debug":
            break
        d.press("back")
    
    raise Exception(f"Backtrack failed: de.rampro.activitydiary.debug is not launched")


avd_serial = sys.argv[1]
d = u2.connect(avd_serial)
assert d.device_info['display']['width'] == 720 and d.device_info['display']['height'] == 1280, "Screen size is different from the original screen size"

d.app_start("de.rampro.activitydiary.debug")
wait()

"""
1. Add a new activity to the diary.
"""
wait_until_activity(d, "Main")
d(descriptionMatches=".*Add Activity", resourceIdMatches=".*action_add_activity").click()
print("Touch on a button that has content_desc 'Add Activity': SUCCESS")
wait()
# Expected behaviour: The performed action opens a new screen for editing a new activity. The previous screen is replaced with a screen that allows the user to enter a new activity title and select an activity color. (page changed from Main to Edit)

wait_until_activity(d, "Edit")
d(textStartsWith="Activity title", resourceIdMatches=".*edit_activity_name").set_text("Yoga Class")
print("Fill a focused textfield that has text 'Activity title' with 'Yoga Class': SUCCESS")
wait()
# Expected behaviour: The focused textfield that had the text "Activity title" has been filled with the text "Yoga Class".

wait_until_activity(d, "Edit")
d(descriptionMatches=".*Save", resourceIdMatches=".*action_edit_done").click()
print("Touch on a button that has content_desc 'Save': SUCCESS")
wait()
# Expected behaviour: After touching the "Save" button, the previous "Edit" screen transitions to the current "Main" screen. The "Save" button remains, but the "Navigate up" button is replaced with an "Open navigation" button, and additional elements such as tabs and buttons for different activities are displayed. (page changed from Edit to Main)

"""
2. Check the statistics of the newly added activity "Yoga Class".
"""
wait_until_activity(d, "Main")
d(textStartsWith="STATISTICS", descriptionMatches=".*Statistics").click()
print("Touch on a selected tab that has text 'STATISTICS': SUCCESS")
wait()
# Expected behaviour: By touching on the "STATISTICS" tab, the text displayed in the "Since a few seconds" and the time-related textviews have been updated to show the elapsed time since the current moment.

wait_until_activity(d, "Main")
d(resourceIdMatches=".*viewpager").swipe(down)
print("Scroll down on a scrollable area that has text 'Since a few seconds, -, -[...and more]': SUCCESS")
wait()
# Expected behaviour: By scrolling down on the scrollable area, the displayed time duration has been updated from "29 sec" to "39 sec".

wait_until_activity(d, "Main")
d(textStartsWith="Yoga Class", resourceIdMatches=".*activity_background").click()
print("Touch on a button that has text 'Yoga Class': SUCCESS")
wait()
# Expected behaviour: Upon touching the "Yoga Class" button, the button text changes to "<No Activity>". Additionally, the timestamp displayed in the textviews "Since just now", "2023 Week 42: 49 sec", and "October 2023: 49 sec" is updated to reflect the new duration.

wait_until_activity(d, "Main")
d(resourceIdMatches=".*nested_scrollview").swipe(down)
print("Scroll down on a scrollable area that has text 'Since just now, -, -[...and more]': SUCCESS")
wait()
# Expected behaviour: After scrolling down, the text "Since just now" in the scrollable area has been updated to "Since a few seconds".

wait_until_activity(d, "Main")
d(textStartsWith="Yoga Class", resourceIdMatches=".*select_card_view").click()
print("Touch on a button that has text 'Yoga Class': SUCCESS")
wait()
# Expected behaviour: By touching on the button with the text "Yoga Class", the previous button with the text "<No Activity>" was replaced with a new button labeled "Yoga Class". Additionally, a new textview with the text "Yoga Class" appeared on the screen, along with buttons labeled "UNDO" and a blank button.

wait_until_activity(d, "Main")
d.click(360, 1178)
print("Touch on a button that has text 'Yoga Class, UNDO': SUCCESS")
wait()
# Expected behaviour: After touching the button "Yoga Class, UNDO", the duration of the yoga class displayed in the text views has changed from 58 seconds to 1 minute and 5 seconds.

wait_until_activity(d, "Main")
d(textStartsWith="Yoga Class", resourceIdMatches=".*activity_background").click()
print("Touch on a button that has text 'Yoga Class': SUCCESS")
wait()
# Expected behaviour: The button "Yoga Class" on the previous screen is replaced with a button "<No Activity>". Some textviews that displayed time durations are now showing "-". Additionally, there was a popup message that showed the updated time duration values, but it disappeared quickly.

wait_until_activity(d, "Main")
d(textStartsWith="STATISTICS", descriptionMatches=".*Statistics").click()
print("Touch on a selected tab that has text 'STATISTICS': SUCCESS")
wait()
# Expected behaviour: The performed action changed the text in one of the textviews from "-" to "Since a few seconds".

wait_until_activity(d, "Main")
d(textStartsWith="Yoga Class", resourceIdMatches=".*select_card_view").click()
print("Touch on a button that has text 'Yoga Class': SUCCESS")
wait()
# Expected behaviour: The action of touching the "Yoga Class" button has updated the screen by replacing the previous button "<No Activity>" with the button "Yoga Class" and adding a new button "UNDO".

wait_until_activity(d, "Main")
d(textStartsWith="Yoga Class", resourceIdMatches=".*select_card_view").click()
print("Touch on a button that has text 'Yoga Class': SUCCESS")
wait()
# Expected behaviour: After touching on the "Yoga Class" button, the text "Yoga Class" is replaced with "<No Activity>" and the duration displayed on the screen is updated to "1' 31''".

wait_until_activity(d, "Main")
d(textStartsWith="STATISTICS", descriptionMatches=".*Statistics").click()
print("Touch on a selected tab that has text 'STATISTICS': SUCCESS")
wait()
# Expected behaviour: The action of touching on the "STATISTICS" tab has updated the text of a textview from "Since just now" to "Since a few seconds".

wait_until_activity(d, "Main")
d(textStartsWith="Yoga Class", resourceIdMatches=".*select_card_view").click()
print("Touch on a button that has text 'Yoga Class': SUCCESS")
wait()
# Expected behaviour: The performed action of touching the button "Yoga Class" has updated the screen by replacing the button "<No Activity>" with the button "Yoga Class" and adding a new text view with the text "Yoga Class". Additionally, two new buttons "UNDO" and a button with no specific text have been added to the screen.

wait_until_activity(d, "Main")
d(resourceIdMatches=".*nested_scrollview").swipe(down)
print("Scroll down on a scrollable area that has text 'Since a few seconds, Average duration: 33 sec, Last start: 2023.10.17 07:19[...and more]': SUCCESS")
wait()
# Expected behaviour: Scrolling down on the scrollable area updates the displayed durations in the textviews to "1' 59''" instead of "1' 39''".

"""
3. Add a detailed note for the "Yoga Class" activity.
"""
wait_until_activity(d, "Main")
d(textStartsWith="Yoga Class", resourceIdMatches=".*activity_background").click()
print("Touch on a button that has text 'Yoga Class': SUCCESS")
wait()
# Expected behaviour: After touching the "Yoga Class" button, the button's text changed to "<No Activity>". The textviews related to the duration of the activity also changed, showing an updated duration of 2 minutes and 29 seconds for the week and month. A popup message briefly appeared, showing the updated duration of 2 minutes and 29 seconds for today and the elapsed time since the action.

wait_until_activity(d, "Main")
d(resourceIdMatches=".*fab_edit_note").click()
print("Touch on a button that has resource_id 'fab_edit_note': SUCCESS")
wait()
# Expected behaviour: After touching the "Edit Note" button, the main screen updated to show the "Since a few seconds" text instead of "Since just now", indicating a change in the time since the note was edited. Additionally, a popup message briefly appeared, stating that an activity needs to be selected to perform the action.

wait_until_activity(d, "Main")
d(textStartsWith="Yoga Class", resourceIdMatches=".*select_card_view").click()
print("Touch on a button that has text 'Yoga Class': SUCCESS")
wait()
# Expected behaviour: By touching the "Yoga Class" button, the previous screen's "<No Activity>" button is replaced with a "Yoga Class" button. Additionally, a new "UNDO" button appears on the current screen.

wait_until_activity(d, "Main")
d(resourceIdMatches=".*detail_content").click()
print("Touch on a button that has text 'Since a few seconds, Average duration: 39 sec, Last start: 2023.10.17 07:19[...and more]': SUCCESS")
wait()
# Expected behaviour: After touching the button, the previous main screen is replaced by the HistoryDetail screen. The button "Navigate up" is added, and the text "Diary entry" is displayed. A new button "Save" is added, and the text "Yoga Class" is displayed. The start and end time buttons are added, along with a checkbox and a text field for notes. A popup message briefly appears showing updated durations for different time periods. (page changed from Main to HistoryDetail)

wait_until_activity(d, "HistoryDetail")
d(textStartsWith="Note", resourceIdMatches=".*edit_activity_note").set_text("I had a great yoga session today and felt really relaxed afterwards.")
print("Fill a focused textfield that has text 'Note' with 'I had a great yoga session today and felt really relaxed afterwards.': SUCCESS")
wait()
# Expected behaviour: The focused textfield in the current screen has been successfully filled with the text "I had a great yoga session today and felt really relaxed afterwards."

wait_until_activity(d, "HistoryDetail")
d(descriptionMatches=".*Save", resourceIdMatches=".*action_edit_done").click()
print("Touch on a button that has content_desc 'Save': SUCCESS")
wait()
# Expected behaviour: After touching the "Save" button, the screen has changed from the "HistoryDetail" page to the "Main" page. The "Navigate up" button, "Diary entry" textview, and the focused textfield with the diary entry text are no longer visible, while the "Open navigation" button, "Activity Diary Debug" textview, "Search" button, "Add Activity" button, and various other buttons and textviews are now visible. (page changed from HistoryDetail to Main)

"""
4. Add a picture to the "Yoga Class" activity.
"""
wait_until_activity(d, "Main")
d(resourceIdMatches=".*fab_attach_picture").click()
print("Touch on a button that has resource_id 'fab_attach_picture': SUCCESS")
wait()
# Expected behaviour: The action of touching on the button with resource_id "fab_attach_picture" has opened the camera screen, where there are buttons for more setting controls, indicator control, and cancel, as well as a shutter button for taking pictures. (page changed from Main to Camera)

wait_until_activity(d, "Camera")
d(descriptionMatches=".*Shutter button", resourceIdMatches=".*shutter_button").click()
print("Touch on a button that has content_desc 'Shutter button': SUCCESS")
wait()
# Expected behaviour: After touching the "Shutter button", the button with resource_id "btn_cancel" is replaced with buttons with resource_id "btn_retake" and "btn_done".

wait_until_activity(d, "Camera")
d(resourceIdMatches=".*btn_done").click()
print("Touch on a button that has resource_id 'btn_done': SUCCESS")
wait()
# Expected behaviour: The previous camera screen has transitioned to the main screen, where various widgets are displayed including a navigation drawer button, activity information, tabs for different categories, and buttons for different activities. (page changed from Camera to Main)

wait_until_activity(d, "Main")
d(textStartsWith="Yoga Class", resourceIdMatches=".*select_card_view").click()
print("Touch on a button that has text 'Yoga Class': SUCCESS")
wait()
# Expected behaviour: After touching the "Yoga Class" button, the button's text changed to "<No Activity>". The duration statistics also updated to show a new value in the "2023 Week 42" and "October 2023" sections. A popup message briefly appeared showing the updated duration for "Tue, 10.17.23".

wait_until_activity(d, "Main")
d(textStartsWith="Yoga Class", resourceIdMatches=".*select_card_view").click()
print("Touch on a button that has text 'Yoga Class': SUCCESS")
wait()
# Expected behaviour: By touching the "Yoga Class" button, the previous screen is updated to show a new button with the text "Yoga Class" and additional information related to the activity, such as average duration and last start time. A popup message briefly appears with the text "Since a few seconds".

wait_until_activity(d, "Main")
d(resourceIdMatches=".*fab_attach_picture").click()
print("Touch on a button that has resource_id 'fab_attach_picture': SUCCESS")
wait()
# Expected behaviour: The action of touching on the "fab_attach_picture" button has opened the Camera screen, where there are buttons for more setting controls, indicator control, and cancel, as well as a shutter button for taking pictures. (page changed from Main to Camera)

wait_until_activity(d, "Camera")
d(descriptionMatches=".*Shutter button", resourceIdMatches=".*shutter_button").click()
print("Touch on a button that has content_desc 'Shutter button': SUCCESS")
wait()
# Expected behaviour: After touching the "Shutter button", the "More setting controls" button and the "indicator_control" button are removed, and the "btn_cancel" button is replaced with the "btn_retake" and "btn_done" buttons.

wait_until_activity(d, "Camera")
d(resourceIdMatches=".*btn_done").click()
print("Touch on a button that has resource_id 'btn_done': SUCCESS")
wait()
# Expected behaviour: After touching the "btn_done" button, the previous camera screen is replaced with the main screen, where there are various widgets such as a navigation button, textviews displaying activity details, tabs for different categories, buttons for different activities, and buttons for attaching pictures and editing notes. (page changed from Camera to Main)

wait_until_activity(d, "Main")
d(textStartsWith="PICTURES", descriptionMatches=".*Pictures").click()
print("Touch on a tab that has text 'PICTURES': SUCCESS")
wait()
# Expected behaviour: After touching on the "PICTURES" tab, the selected tab changed to "PICTURES" and the previous tab "STATISTICS" became unselected. The previous textviews related to statistics disappeared, and a new button with resource_id "detail_card_view" and a scrollable area with resource_id "picture_recycler" appeared. Additionally, a popup message with a duration of 5 minutes and 25 seconds was shown and soon disappeared.

wait_until_activity(d, "Main")
d(resourceIdMatches=".*detail_card_view").click()
print("Touch on a button that has resource_id 'detail_card_view': SUCCESS")
wait()
# Expected behaviour: The action of touching the button with resource_id "detail_card_view" has opened a new screen called "Resolver" where there is a focused listview with resource_id "resolver_list" and new options like "Open with", "Photos", and "Gallery". (page changed from Main to Resolver)

wait_until_activity(d, "Resolver")
d.click(359, 1011)
print("Touch on a button that has text 'Photos': SUCCESS")
wait()
# Expected behaviour: After touching the "Photos" button, two additional buttons with text "JUST ONCE" and "ALWAYS" have appeared on the current screen.

wait_until_activity(d, "Resolver")
d(textStartsWith="JUST ONCE", resourceIdMatches=".*button_once").click()
print("Touch on a button that has text 'JUST ONCE': SUCCESS")
wait()
# Expected behaviour: After touching the button with text "JUST ONCE", the previous Resolver screen is replaced with the current HostPhotoPager screen, where the button with resource_id "photo_view" is added and the buttons with content_desc "Navigate up", "Details", and resource_id "action_bar_overflow" replace the previous widgets. (page changed from Resolver to HostPhotoPager)

wait_until_activity(d, "HostPhotoPager")
d(descriptionMatches=".*Navigate up").click()
print("Touch on a button that has content_desc 'Navigate up': SUCCESS")
wait()
# Expected behaviour: The previous screen was the HostPhotoPager, which had a button with content_desc "Navigate up". After touching the button, the current screen changed to the Main screen, which added various new widgets such as a button with content_desc "Open navigation", textviews with texts "Activity Diary Debug" and "What are you doing?", buttons with content_desc "Search" and "Add Activity", tabs with texts "STATISTICS", "NOTE", and "PICTURES", and more. (page changed from HostPhotoPager to Main)

"""
5. Add a note to the "Cinema" activity.
"""
wait_until_activity(d, "Main")
d(textStartsWith="Cinema", resourceIdMatches=".*select_card_view").click()
print("Touch on a button that has text 'Cinema': SUCCESS")
wait()
# Expected behaviour: After touching the "Cinema" button, a new button labeled "UNDO" and a textview displaying "Cinema" have appeared on the current screen.

wait_until_activity(d, "Main")
d(resourceIdMatches=".*fab_edit_note").click()
print("Touch on a button that has resource_id 'fab_edit_note': SUCCESS")
wait()
# Expected behaviour: By touching the "fab_edit_note" button, the previous screen is replaced with a new screen where a textfield is focused and labeled as "Note". Two buttons labeled as "CANCEL" and "OK" are also displayed.

wait_until_activity(d, "Main")
d(resourceIdMatches=".*noteText").set_text("I watched a great movie at the cinema yesterday!")
print("Fill a focused textfield that has resource_id 'noteText' with 'I watched a great movie at the cinema yesterday!': SUCCESS")
wait()
# Expected behaviour: The focused textfield with resource_id "noteText" has been successfully filled with the text "I watched a great movie at the cinema yesterday!"

wait_until_activity(d, "Main")
d(textStartsWith="OK", resourceIdMatches=".*button1").click()
print("Touch on a button that has text 'OK': SUCCESS")
wait()
# Expected behaviour: The action of touching the "OK" button has changed the screen from a focused textfield and a "CANCEL" button to a main screen with various buttons, tabs, and a scrollable area.

wait_until_activity(d, "Main")
d(textStartsWith="Cinema", resourceIdMatches=".*activity_background").click()
print("Touch on a button that has text 'Cinema': SUCCESS")
wait()
# Expected behaviour: The button with the text "Cinema" has been replaced with a button that has the text "<No Activity>".

"""
6. Review the app's privacy policy.
"""
wait_until_activity(d, "Main")
d(descriptionMatches=".*Open navigation").click()
print("Touch on a button that has content_desc 'Open navigation': SUCCESS")
wait()
# Expected behaviour: The performed action of touching on the "Open navigation" button has changed the content description of the button to "Close navigation" and added several new buttons related to activities, diary, statistics, map, settings, and more.

wait_until_activity(d, "Main")
d(textStartsWith="Privacy Policy", resourceIdMatches=".*design_menu_item_text").click()
print("Touch on a button that has text 'Privacy Policy': SUCCESS")
wait()
# Expected behaviour: The performed action opens the Privacy Policy screen, which displays information about the ActivityDiary application and its purpose. The previous screen's widgets are replaced with a new set of widgets related to the Privacy Policy. (page changed from Main to PrivacyPolicy)

wait_until_activity(d, "PrivacyPolicy")
d.swipe(360, 624, 360, 524)
print("Scroll down on a scrollable area that has text 'Privacy Policy, Privacy Policy  ActivityDiary is a free, libre and[...]': SUCCESS")
wait()
# Expected behaviour: By scrolling down on the Privacy Policy screen, a button with the text "Privacy Policy" is revealed, providing more information about the ActivityDiary application.

wait_until_activity(d, "PrivacyPolicy")
d.swipe(360, 624, 360, 524)
print("Scroll down on a scrollable area that has text 'Privacy Policy  ActivityDiary is a free, libre and[...]': SUCCESS")
wait()
"""
7. View the location of the "Yoga Class" activity on the Map page.
"""
wait_until_activity(d, "PrivacyPolicy")
d.press("back")
print("Press 'BACK' button to navigate back: SUCCESS")
wait()
# Expected behaviour: Pressing the "BACK" button navigates back from the Privacy Policy page to the Main page. The Main page now displays various buttons for adding activities, a scrollable area with activity buttons, and tabs for statistics, notes, and pictures. (page changed from PrivacyPolicy to Main)

wait_until_activity(d, "Main")
d(descriptionMatches=".*Open navigation").click()
print("Touch on a button that has content_desc 'Open navigation': SUCCESS")
wait()
# Expected behaviour: The performed action opens the navigation drawer, replacing the button with content_desc "Open navigation" with a button with content_desc "Close navigation", and adds multiple buttons for various actions such as "Diary", "Statistics", "Map", "Edit Activities", "Settings", "About", and "Privacy Policy".

wait_until_activity(d, "Main")
d(textStartsWith="Map", resourceIdMatches=".*design_menu_item_text").click()
print("Touch on a button that has text 'Map': SUCCESS")
wait()
# Expected behaviour: After touching the "Map" button, the previous screen is replaced with a new screen that displays a map. However, there is no data to show on the map and a message is displayed indicating that location services need to be enabled in the settings. (page changed from Main to Map)

wait_until_activity(d, "Map")
d(descriptionMatches=".*Navigate up").click()
print("Touch on a button that has content_desc 'Navigate up': SUCCESS")
wait()
# Expected behaviour: By touching on the "Navigate up" button, the previous map screen is replaced with the current main screen which displays various options such as opening the navigation drawer, searching, adding an activity, and viewing different tabs for statistics, notes, and pictures. (page changed from Map to Main)

wait_until_activity(d, "Main")
d(descriptionMatches=".*Open navigation").click()
print("Touch on a button that has content_desc 'Open navigation': SUCCESS")
wait()
# Expected behaviour: The performed action of touching the "Open navigation" button has changed the button's content description to "Close navigation" and added a series of new buttons related to different activities, settings, and information.

wait_until_activity(d, "Main")
d.click(186, 741)
print("Touch on a button that has text 'Settings': SUCCESS")
wait()
# Expected behaviour: After touching on the "Settings" button, the previous main screen has changed to the settings screen. The settings screen now displays various options such as "View", "Date format", "Duration format", "Behavior", "Select new activities", "Terminate activity by click", "Notification for current activity", "Silent notifications", "Crash Reporting", "Location", and a "Privacy Policy" button. (page changed from Main to Settings)

wait_until_activity(d, "Settings")
d.click(360, 1098)
print("Touch on a button that has text 'Location Service, User location not tracked at all': SUCCESS")
wait()
# Expected behaviour: After touching the button with the text "Location Service, User location not tracked at all", the button's state changes from "OFF" to "ON".

wait_until_activity(d, "Settings")
d(textStartsWith="Network", resourceIdMatches=".*text1").click()
print("Touch on a button that has text 'Network': SUCCESS")
wait()
# Expected behaviour: After touching the "Network" button, the previous "Location Service" button has been removed and replaced with a new "Update period" button.

wait_until_activity(d, "Settings")
d.press("back")
print("Press 'BACK' button to navigate back: SUCCESS")
wait()
# Expected behaviour: Pressing the "BACK" button navigates back from the Settings page to the Main page. The Main page displays a list of activities with options to search, add activities, and attach pictures or edit notes. (page changed from Settings to Main)

wait_until_activity(d, "Main")
d(textStartsWith="Yoga Class", resourceIdMatches=".*select_card_view").click()
print("Touch on a button that has text 'Yoga Class': SUCCESS")
wait()
# Expected behaviour: The performed action of touching the "Yoga Class" button has added a new button with the text "Yoga Class" to the list of activities.

wait_until_activity(d, "Main")
d(textStartsWith="Yoga Class", resourceIdMatches=".*activity_background").click()
print("Touch on a button that has text 'Yoga Class': SUCCESS")
wait()
# Expected behaviour: After touching on the button with text "Yoga Class", the button's text changes to "<No Activity>".

wait_until_activity(d, "Main")
d(textStartsWith="Yoga Class", resourceIdMatches=".*select_card_view").click()
print("Touch on a button that has text 'Yoga Class': SUCCESS")
wait()
# Expected behaviour: By touching the "Yoga Class" button, the previous button with the text "<No Activity>" is replaced with a new button labeled "Yoga Class". Additionally, a new textview with the text "Yoga Class" and a button labeled "UNDO" are added to the current screen.

wait_until_activity(d, "Main")
d.press("back")
print("Press 'BACK' button to navigate back: SUCCESS")
wait()
wait_until_activity(d, "Main")
d.app_start("de.rampro.activitydiary.debug")
print("Open the app again because the previous action led to closing the app: SUCCESS")
wait()
# Expected behaviour: Navigating back from the current screen returns to the previous screen. The "STATISTICS" tab is now selected, and additional information related to the selected tab is displayed, such as the duration, last start time, and various time intervals. The "PICTURES" tab is no longer selected, and the "UNDO" button is no longer visible.

"""
8. Navigate to the "About" page to read about the app's functionality.
"""
wait_until_activity(d, "Main")
d(descriptionMatches=".*Open navigation").click()
print("Touch on a button that has content_desc 'Open navigation': SUCCESS")
wait()
# Expected behaviour: After touching the "Open navigation" button, the button's content description changes to "Close navigation" and several text views display updated time durations. Additionally, a popup message briefly appears showing updated durations and time information.

wait_until_activity(d, "Main")
d(descriptionMatches=".*Close navigation").click()
print("Touch on a button that has content_desc 'Close navigation': SUCCESS")
wait()
# Expected behaviour: The performed action changed the content description of the button from "Close navigation" to "Open navigation".

wait_until_activity(d, "Main")
d(descriptionMatches=".*Open navigation").click()
print("Touch on a button that has content_desc 'Open navigation': SUCCESS")
wait()
# Expected behaviour: The button with content description "Open navigation" has been changed to a button with content description "Close navigation". Several new buttons have also been added to the current screen, including "Select Activity", "Diary", "Statistics", "Map", "Add Activity", "Edit Activities", "Settings", "About", and "Privacy Policy". The textviews displaying the duration have also been updated to show a different time.

wait_until_activity(d, "Main")
d(descriptionMatches=".*Close navigation").click()
print("Touch on a button that has content_desc 'Close navigation': SUCCESS")
wait()
# Expected behaviour: The performed action has changed the content description of the button from "Close navigation" to "Open navigation" on the current screen.

wait_until_activity(d, "Main")
d(descriptionMatches=".*Open navigation").click()
print("Touch on a button that has content_desc 'Open navigation': SUCCESS")
wait()
# Expected behaviour: The performed action successfully changed the content description of the button from "Open navigation" to "Close navigation". Additionally, the textview displaying the time duration has increased from "Since 2 min" to "Since 3 min", and the time duration in various formats has also increased accordingly.

wait_until_activity(d, "Main")
d(textStartsWith="About", resourceIdMatches=".*design_menu_item_text").click()
print("Touch on a button that has text 'About': SUCCESS")
wait()
# Expected behaviour: After touching the "About" button, the screen transitions to the "About" page where information about the "Activity Diary Debug" app is displayed, including its version and license. (page changed from Main to About)

"""
9. Learn to manage activities in the Activity Diary Debug app.
"""
wait_until_activity(d, "About")
d.press("back")
print("Press 'BACK' button to navigate back: SUCCESS")
wait()
# Expected behaviour: The "About" screen has been navigated back to the "Main" screen. The "Main" screen now displays various buttons for activities, statistics, and notes, along with information about the duration and last start time of the activity. (page changed from About to Main)

wait_until_activity(d, "Main")
d(descriptionMatches=".*Add Activity", resourceIdMatches=".*action_add_activity").click()
print("Touch on a button that has content_desc 'Add Activity': SUCCESS")
wait()
# Expected behaviour: The performed action opened a new screen for editing an activity. The previous screen's button "Add Activity" has been replaced with buttons for navigating back, deleting the activity, and saving changes. The screen also includes a text field for entering the activity title and options for selecting the activity color. Additionally, some popup messages briefly appeared and disappeared. (page changed from Main to Edit)

wait_until_activity(d, "Edit")
d(textStartsWith="Activity title", resourceIdMatches=".*edit_activity_name").set_text("Study Group Session")
print("Fill a focused textfield that has text 'Activity title' with 'Study Group Session': SUCCESS")
wait()
# Expected behaviour: The focused textfield that previously had the text "Activity title" now has the text "Study Group Session".

wait_until_activity(d, "Edit")
d(resourceIdMatches=".*edit_activity_color").click()
print("Touch on a button that has resource_id 'edit_activity_color': SUCCESS")
wait()
# Expected behaviour: After touching the button with resource_id "edit_activity_color", the textview that displays the activity color changed from "#" to "7B1FA2", and a new button with text "SELECT" appeared.

wait_until_activity(d, "Edit")
d(textStartsWith="SELECT", resourceIdMatches=".*okColorButton").click()
print("Touch on a button that has text 'SELECT': SUCCESS")
wait()
# Expected behaviour: The touch on the "SELECT" button has navigated the user to a new activity screen where they can edit and save a study group session. The previous screen's buttons have been replaced with buttons for navigation and activity management.

wait_until_activity(d, "Edit")
d(descriptionMatches=".*Save", resourceIdMatches=".*action_edit_done").click()
print("Touch on a button that has content_desc 'Save': SUCCESS")
wait()
# Expected behaviour: After touching the "Save" button, the previous "Edit" screen is replaced with the current "Main" screen. The button with content description "Open navigation" is added, indicating that the navigation drawer is now open. (page changed from Edit to Main)

wait_until_activity(d, "Main")
d(descriptionMatches=".*Open navigation").click()
print("Touch on a button that has content_desc 'Open navigation': SUCCESS")
wait()
# Expected behaviour: The action of touching the "Open navigation" button changed the content description of the button to "Close navigation". Additionally, the textviews that display the time since a certain event were updated to show the time elapsed in seconds instead of minutes. A popup message briefly displayed the updated time values before disappearing.

wait_until_activity(d, "Main")
d.click(186, 656)
print("Touch on a button that has text 'Edit Activities': SUCCESS")
wait()
# Expected behaviour: After touching the "Edit Activities" button, the screen changed from the main page to the manage page. The "Manage activities" text appeared on the screen, and the "Yoga Class" button was added to the list of activities. Additionally, popup messages with updated time durations were briefly displayed. (page changed from Main to Manage)

wait_until_activity(d, "Manage")
d(textStartsWith="Yoga Class", resourceIdMatches=".*activity_background").click()
print("Touch on a button that has text 'Yoga Class': SUCCESS")
wait()
# Expected behaviour: After touching the "Yoga Class" button, the screen changed from the "Manage" page to the "Edit" page. The "Manage activities" textview was replaced with a focused textfield containing the text "Yoga Class", and new options such as "Delete activity" and "Save" buttons appeared. (page changed from Manage to Edit)

wait_until_activity(d, "Edit")
d(descriptionMatches=".*Save", resourceIdMatches=".*action_edit_done").click()
print("Touch on a button that has content_desc 'Save': SUCCESS")
wait()
# Expected behaviour: After touching the "Save" button, the previous "Edit" screen transitioned to the "Manage" screen. The "Manage" screen now displays a list of activities, including "Yoga Class" and other activity options. (page changed from Edit to Manage)

wait_until_activity(d, "Manage")
d(textStartsWith="Yoga Class", resourceIdMatches=".*activity_background").click()
print("Touch on a button that has text 'Yoga Class': SUCCESS")
wait()
# Expected behaviour: The action of touching the "Yoga Class" button in the previous screen has opened the "Edit" screen, where the "Yoga Class" activity is selected and can be modified or deleted. (page changed from Manage to Edit)

wait_until_activity(d, "Edit")
d(textStartsWith="Yoga Class", resourceIdMatches=".*edit_activity_name").set_text("Study Break Session")
print("Fill a focused textfield that has text 'Yoga Class' with 'Study Break Session': SUCCESS")
wait()
# Expected behaviour: The focused textfield that previously had the text "Yoga Class" is now updated with the text "Study Break Session". Additionally, a new textview appears with the text "New activity name similar to Study Group Session".

wait_until_activity(d, "Edit")
d(descriptionMatches=".*Delete activity", resourceIdMatches=".*action_edit_delete").click()
print("Touch on a button that has content_desc 'Delete activity': SUCCESS")
wait()
# Expected behaviour: After touching the "Delete activity" button, the previous "Edit" screen has been replaced by the current "Manage" screen. The button for deleting the activity is no longer present, and a list of activity buttons, including "Study Group Session," has been added. (page changed from Edit to Manage)

"""
10. Add a new activity and view its history and statistics.
"""
wait_until_activity(d, "Manage")
d(descriptionMatches=".*Add Activity", resourceIdMatches=".*action_add_activity").click()
print("Touch on a button that has content_desc 'Add Activity': SUCCESS")
wait()
# Expected behaviour: By touching on the "Add Activity" button, the previous "Manage" screen is replaced with the current "Edit" screen, where the user can input a new activity title, select an activity color, and save or delete the activity. (page changed from Manage to Edit)

wait_until_activity(d, "Edit")
d(textStartsWith="Activity title", resourceIdMatches=".*edit_activity_name").set_text("Jogging")
print("Fill a focused textfield that has text 'Activity title' with 'Jogging': SUCCESS")
wait()
# Expected behaviour: The focused textfield "Activity title" now contains the text "Jogging" instead of the previous text "Activity title".

wait_until_activity(d, "Edit")
d(resourceIdMatches=".*edit_activity_color").click()
print("Touch on a button that has resource_id 'edit_activity_color': SUCCESS")
wait()
# Expected behaviour: After touching the "edit_activity_color" button, the color picker screen appeared, allowing the user to select a color for the activity. The previous textfield displaying the activity color was replaced with a "#" symbol and a focused textfield displaying the hexadecimal color value "FFA000". A new button labeled "SELECT" was also added to confirm the color selection.

wait_until_activity(d, "Edit")
d(textStartsWith="SELECT", resourceIdMatches=".*okColorButton").click()
print("Touch on a button that has text 'SELECT': SUCCESS")
wait()
# Expected behaviour: The previous screen was an Edit page with a button labeled "SELECT", but the current screen is a different Edit page with new buttons labeled "Navigate up", "Delete activity", and "Save", along with new text views and a focused text field.

wait_until_activity(d, "Edit")
d(descriptionMatches=".*Save", resourceIdMatches=".*action_edit_done").click()
print("Touch on a button that has content_desc 'Save': SUCCESS")
wait()
# Expected behaviour: After touching the "Save" button, the screen has changed from an "Edit" page to a "Manage" page. The "Save" button is still present, but there are additional buttons for adding activities and showing deleted activities. The list of activities has also been updated with new options. (page changed from Edit to Manage)

wait_until_activity(d, "Manage")
d(descriptionMatches=".*Add Activity", resourceIdMatches=".*action_add_activity").click()
print("Touch on a button that has content_desc 'Add Activity': SUCCESS")
wait()
# Expected behaviour: The action of touching the "Add Activity" button has transitioned the screen from the "Manage" page to the "Edit" page. The "Manage activities" textview has been replaced with a "New activity" textview, and additional buttons and textfields related to editing and saving the activity have appeared. (page changed from Manage to Edit)

wait_until_activity(d, "Edit")
d(descriptionMatches=".*Delete activity", resourceIdMatches=".*action_edit_delete").click()
print("Touch on a button that has content_desc 'Delete activity': SUCCESS")
wait()
# Expected behaviour: After touching the "Delete activity" button, the previous screen (Edit) is replaced by the current screen (Manage), which displays a list of activities including "Cinema," "Cleaning," "Cooking," "Gardening," "Jogging," "Officework," "Relaxing," "Sleeping," "Study Group Session," "Swimming," and "Woodworking." (page changed from Edit to Manage)

wait_until_activity(d, "Manage")
d(textStartsWith="Jogging", resourceIdMatches=".*activity_background").click()
print("Touch on a button that has text 'Jogging': SUCCESS")
wait()
# Expected behaviour: By touching on the "Jogging" button, the screen has changed from the "Manage" page to the "Edit" page for the "Jogging" activity. The "Delete activity" and "Save" buttons are now visible, and the textfield for the activity name is focused. (page changed from Manage to Edit)

wait_until_activity(d, "Edit")
d(descriptionMatches=".*Navigate up").click()
print("Touch on a button that has content_desc 'Navigate up': SUCCESS")
wait()
# Expected behaviour: The action of touching the "Navigate up" button has taken the user from the "Edit" screen to the "Manage" screen. On the "Manage" screen, the user can now see a list of activities including "Cinema," "Cleaning," "Cooking," "Gardening," "Jogging," and more. (page changed from Edit to Manage)

wait_until_activity(d, "Manage")
d(descriptionMatches=".*Add Activity", resourceIdMatches=".*action_add_activity").click()
print("Touch on a button that has content_desc 'Add Activity': SUCCESS")
wait()
# Expected behaviour: The action of touching on the "Add Activity" button in the previous screen has opened a new screen called "Edit" where the user can add a new activity. The new screen contains options to delete and save the activity, a text field to enter the activity title, and a button to edit the activity color. (page changed from Manage to Edit)

wait_until_activity(d, "Edit")
d(resourceIdMatches=".*edit_activity_color").click()
print("Touch on a button that has resource_id 'edit_activity_color': SUCCESS")
wait()
# Expected behaviour: After touching on the "edit_activity_color" button, the color selector screen is opened where the user can enter or select a color for the activity. The previous textview showing the activity color is replaced with a "#" symbol and a focused textfield with the text "0097A7". A new button with the text "SELECT" is added.

wait_until_activity(d, "Edit")
d(textStartsWith="0097A7", resourceIdMatches=".*hexCode").set_text("FFA500")
print("Fill a focused textfield that has text '0097A7' with 'FFA500': SUCCESS")
wait()
# Expected behaviour: The focused textfield that previously had the text "0097A7" now has the text "FFA500".

wait_until_activity(d, "Edit")
d.press("back")
print("Press 'BACK' button to navigate back: SUCCESS")
wait()
"""
11. Change the color code of the activity.
"""
wait_until_activity(d, "Edit")
d(textStartsWith="FFA500", resourceIdMatches=".*hexCode").set_text("00FF00 (Jade Green wants to change the color code to green)")
print("Fill a focused textfield that has text 'FFA500' with '00FF00 (Jade Green wants to change the color code to green)': SUCCESS")
wait()
# Expected behaviour: The focused textfield that previously had the text "FFA500" has now been updated to "00FF00", as desired by Jade Green.

wait_until_activity(d, "Edit")
d(textStartsWith="SELECT", resourceIdMatches=".*okColorButton").click()
print("Touch on a button that has text 'SELECT': SUCCESS")
wait()
# Expected behaviour: After touching the "SELECT" button, the previous screen has been replaced with a new activity screen where the button has been replaced with a "Navigate up" button and new buttons for deleting and saving the activity. The text fields and text views have also changed to display new activity information.

wait_until_activity(d, "Edit")
d(descriptionMatches=".*Save", resourceIdMatches=".*action_edit_done").click()
print("Touch on a button that has content_desc 'Save': SUCCESS")
wait()
# Expected behaviour: The action of touching the "Save" button in the previous screen has transitioned the user to the "Manage" screen, where they can now see a list of activities with different buttons to add, show deleted, and change activity backgrounds. (page changed from Edit to Manage)

wait_until_activity(d, "Manage")
d(textStartsWith="Jogging", resourceIdMatches=".*activity_background").click()
print("Touch on a button that has text 'Jogging': SUCCESS")
wait()
# Expected behaviour: The action of touching the "Jogging" button has opened a new screen where the user can edit the details of the "Jogging" activity, including the activity name and color. (page changed from Manage to Edit)

"""
12. View the history and statistics of the "Jogging" activity.
"""
wait_until_activity(d, "Edit")
d(descriptionMatches=".*Save", resourceIdMatches=".*action_edit_done").click()
print("Touch on a button that has content_desc 'Save': SUCCESS")
wait()
# Expected behaviour: By touching the "Save" button, the user is taken from the "Edit" screen to the "Manage" screen. The "Manage" screen now displays a list of activities and additional options such as "Add Activity" and "Show Deleted". (page changed from Edit to Manage)

wait_until_activity(d, "Manage")
d(textStartsWith="Jogging", resourceIdMatches=".*activity_background").click()
print("Touch on a button that has text 'Jogging': SUCCESS")
wait()
# Expected behaviour: The action of touching the "Jogging" button on the previous screen has opened the "Edit" screen, where the user can now edit and manage the details of the "Jogging" activity. (page changed from Manage to Edit)

wait_until_activity(d, "Edit")
d(descriptionMatches=".*Save", resourceIdMatches=".*action_edit_done").click()
print("Touch on a button that has content_desc 'Save': SUCCESS")
wait()
# Expected behaviour: By touching the "Save" button, the user transitioned from the "Edit" screen to the "Manage" screen. The "Manage activities" textview and a list of activity buttons are now visible on the current screen. (page changed from Edit to Manage)

wait_until_activity(d, "Manage")
d(textStartsWith="Jogging", resourceIdMatches=".*activity_background").click()
print("Touch on a button that has text 'Jogging': SUCCESS")
wait()
# Expected behaviour: By touching the button with text "Jogging", the user is taken to the Edit screen where they can modify the details of the "Jogging" activity, such as its color and name. (page changed from Manage to Edit)

wait_until_activity(d, "Edit")
d(descriptionMatches=".*Navigate up").click()
print("Touch on a button that has content_desc 'Navigate up': SUCCESS")
wait()
# Expected behaviour: After touching the "Navigate up" button, the screen has changed from the previous "Edit" page to the current "Manage" page. The "Manage activities" textview and several buttons for different activities are now visible. (page changed from Edit to Manage)

wait_until_activity(d, "Manage")
d(descriptionMatches=".*Show Deleted", resourceIdMatches=".*action_show_hide_deleted").click()
print("Touch on a button that has content_desc 'Show Deleted': SUCCESS")
wait()
# Expected behaviour: After touching the "Show Deleted" button, it has changed to "Hide Deleted" on the current screen. Additionally, a new button labeled "Yoga Class" has been added to the list of activities.

wait_until_activity(d, "Manage")
d(descriptionMatches=".*Navigate up").click()
print("Touch on a button that has content_desc 'Navigate up': SUCCESS")
wait()
# Expected behaviour: The touch on the "Navigate up" button in the Manage screen has led to a transition to the Main screen, where the navigation button has been replaced with an "Open navigation" button and the text has changed to "Activity Diary Debug". Additionally, new tabs and buttons have appeared on the Main screen. (page changed from Manage to Main)

wait_until_activity(d, "Main")
d(textStartsWith="STATISTICS", descriptionMatches=".*Statistics").click()
print("Touch on a selected tab that has text 'STATISTICS': SUCCESS")
wait()
# Expected behaviour: The performed action of touching on the "STATISTICS" tab has caused an update in the displayed time values, with the previous values being "2' 39''" and the current values being "2' 49''". Additionally, a new button with the text "Jogging" and a button with the resource ID "select_card_view" have appeared on the current screen.

wait_until_activity(d, "Main")
d(textStartsWith="STATISTICS", descriptionMatches=".*Statistics").click()
print("Touch on a selected tab that has text 'STATISTICS': SUCCESS")
wait()
# Expected behaviour: The performed action on the "STATISTICS" tab has updated the displayed time values in the textviews from "2' 49''" to "3' 19''".

wait_until_activity(d, "Main")
d(textStartsWith="Jogging", resourceIdMatches=".*select_card_view").click()
print("Touch on a button that has text 'Jogging': SUCCESS")
wait()
# Expected behaviour: After touching the "Jogging" button, the screen updated to show the details of the jogging activity, including the duration and average duration. A popup message briefly appeared showing the updated duration.

wait_until_activity(d, "Main")
d(textStartsWith="NOTE", descriptionMatches=".*Note").click()
print("Touch on a tab that has text 'NOTE': SUCCESS")
wait()
# Expected behaviour: By touching on the "NOTE" tab, the selected tab changed to "NOTE" and the previous selected tab "STATISTICS" became unselected. Additionally, some popup messages briefly appeared and disappeared showing updated time durations for the activity.

wait_until_activity(d, "Main")
d(textStartsWith="Jogging", resourceIdMatches=".*activity_background").click()
print("Touch on a button that has text 'Jogging': SUCCESS")
wait()
# Expected behaviour: After touching the "Jogging" button, the button's text changes to "<No Activity>".

wait_until_activity(d, "Main")
d(descriptionMatches=".*Add Activity", resourceIdMatches=".*action_add_activity").click()
print("Touch on a button that has content_desc 'Add Activity': SUCCESS")
wait()
# Expected behaviour: After touching the "Add Activity" button, the previous main screen transitions to a new edit screen where the user can create a new activity. The edit screen includes options to delete the activity, save changes, and edit the activity's color. (page changed from Main to Edit)

"""
13. Create a new activity named "Study Group" with a color of her choice and then view its history and statistics.
"""
wait_until_activity(d, "Edit")
d(textStartsWith="Activity title", resourceIdMatches=".*edit_activity_name").set_text("Study Group")
print("Fill a focused textfield that has text 'Activity title' with 'Study Group': SUCCESS")
wait()
# Expected behaviour: The focused textfield with the text "Activity title" has been successfully filled with "Study Group". Additionally, a new textview with the text "New activity name similar to Study Group Session" has appeared.

wait_until_activity(d, "Edit")
d(resourceIdMatches=".*edit_activity_color").click()
print("Touch on a button that has resource_id 'edit_activity_color': SUCCESS")
wait()
# Expected behaviour: After touching on the button with resource_id "edit_activity_color", the text in the focused textfield changed from "F57C00" to "#", and a new button with text "SELECT" appeared.

wait_until_activity(d, "Edit")
d(textStartsWith="SELECT", resourceIdMatches=".*okColorButton").click()
print("Touch on a button that has text 'SELECT': SUCCESS")
wait()
# Expected behaviour: The action of touching the "SELECT" button has navigated the user to a new activity screen where they can edit and save a new activity with a specific name and color. The previous screen had a button with the text "SELECT" while the current screen has buttons with content descriptions "Navigate up", "Delete activity", and "Save", indicating new options for the user to interact with.

wait_until_activity(d, "Edit")
d(descriptionMatches=".*Save", resourceIdMatches=".*action_edit_done").click()
print("Touch on a button that has content_desc 'Save': SUCCESS")
wait()
# Expected behaviour: After touching the "Save" button, the screen has transitioned from the "Edit" page to the "Main" page. The previous buttons and textview related to editing activities have been replaced with buttons and tabs for navigating and adding activities. (page changed from Edit to Main)

wait_until_activity(d, "Main")
d(textStartsWith="Study Group", resourceIdMatches=".*activity_background").click()
print("Touch on a button that has text 'Study Group': SUCCESS")
wait()
# Expected behaviour: After touching the "Study Group" button, another button with the text "<No Activity>" appears in its place.

wait_until_activity(d, "Main")
d(textStartsWith="Study Group", resourceIdMatches=".*select_card_view").click()
print("Touch on a button that has text 'Study Group': SUCCESS")
wait()
# Expected behaviour: By touching on the "Study Group" button, a new button labeled "UNDO" and a textview labeled "Study Group" have been added to the main screen.

wait_until_activity(d, "Main")
d(textStartsWith="Study Group", resourceIdMatches=".*activity_background").click()
print("Touch on a button that has text 'Study Group': SUCCESS")
wait()
# Expected behaviour: After touching on the "Study Group" button, it has been replaced with "<No Activity>", and a new "Study Group" button has appeared in the scrollable area.

wait_until_activity(d, "Main")
d(textStartsWith="Study Group", resourceIdMatches=".*select_card_view").click()
print("Touch on a button that has text 'Study Group': SUCCESS")
wait()
# Expected behaviour: By touching on the "Study Group" button, a new button with the text "UNDO" and a new textview with the text "Study Group" have been added to the current screen.

wait_until_activity(d, "Main")
d(textStartsWith="STATISTICS", descriptionMatches=".*Statistics").click()
print("Touch on a tab that has text 'STATISTICS': SUCCESS")
wait()
# Expected behaviour: The performed action changed the selected tab from "NOTE" to "STATISTICS" in the main screen, and also added several new textviews and buttons related to statistics information.

wait_until_activity(d, "Main")
d(resourceIdMatches=".*detail_content").click()
print("Touch on a button that has text 'Since 45 sec, Average duration: 27 sec, Last start: 2023.10.17 07:50[...and more]': SUCCESS")
wait()
# Expected behaviour: After touching the button, the screen changed to the "HistoryDetail" page. The previous buttons and textviews were replaced with a new set of buttons and textviews related to a specific diary entry. Additionally, some popup messages briefly appeared and disappeared. (page changed from Main to HistoryDetail)

wait_until_activity(d, "HistoryDetail")
d(descriptionMatches=".*Save", resourceIdMatches=".*action_edit_done").click()
print("Touch on a button that has content_desc 'Save': SUCCESS")
wait()
# Expected behaviour: The previous screen, "HistoryDetail," is replaced by the current screen, "Main." The "Save" button in the previous screen is still present in the current screen. (page changed from HistoryDetail to Main)

wait_until_activity(d, "Main")
d(textStartsWith="Study Group", resourceIdMatches=".*activity_background").click()
print("Touch on a button that has text 'Study Group': SUCCESS")
wait()
# Expected behaviour: After touching the "Study Group" button, the button text changed to "<No Activity>". The duration displayed in the textviews "2023 Week 42: 2' 04''" and "October 2023: 2' 04''" also changed to "2' 24''". Additionally, two popup messages appeared briefly showing the durations "Tue, 10.17.23: 2' 24''" and "Since 90 sec".

wait_until_activity(d, "Main")
d(textStartsWith="STATISTICS", descriptionMatches=".*Statistics").click()
print("Touch on a selected tab that has text 'STATISTICS': SUCCESS")
wait()
# Expected behaviour: By touching on the "STATISTICS" tab, the previous "-" textview has been updated to "Since a few seconds" in the current screen.

"""
14. Check the historical data and statistics for the "Jogging" activity.
"""
wait_until_activity(d, "Main")
d(textStartsWith="Jogging", resourceIdMatches=".*select_card_view").click()
print("Touch on a button that has text 'Jogging': SUCCESS")
wait()
# Expected behaviour: After touching the "Jogging" button, the previous button with the text "<No Activity>" has been replaced with a new button with the text "Jogging" in the current screen. Additionally, a popup message briefly appeared and disappeared, showing the text "Since 75 sec".

wait_until_activity(d, "Main")
d(textStartsWith="STATISTICS", descriptionMatches=".*Statistics").click()
print("Touch on a selected tab that has text 'STATISTICS': SUCCESS")
wait()
# Expected behaviour: After touching on the "STATISTICS" tab, the "Since just now" text in the previous screen is updated to "Since a few seconds" in the current screen. Additionally, the displayed durations in the textviews are updated to "3' 56''" and the popup messages briefly show updated durations before disappearing.

wait_until_activity(d, "Main")
d(textStartsWith="NOTE", descriptionMatches=".*Note").click()
print("Touch on a tab that has text 'NOTE': SUCCESS")
wait()
# Expected behaviour: After touching on the "NOTE" tab, the selected tab is now "NOTE" and the previously selected tab "STATISTICS" is now unselected. The textviews showing time durations and dates have been updated with new values. Additionally, some popup messages briefly appeared and disappeared.

wait_until_activity(d, "Main")
d(textStartsWith="STATISTICS", descriptionMatches=".*Statistics").click()
print("Touch on a tab that has text 'STATISTICS': SUCCESS")
wait()
# Expected behaviour: By touching on the "STATISTICS" tab, it becomes the selected tab, and the "NOTE" tab becomes unselected. Additionally, several textviews and a button related to statistics information are added to the screen.

wait_until_activity(d, "Main")
d(textStartsWith="Jogging", resourceIdMatches=".*activity_background").click()
print("Touch on a button that has text 'Jogging': SUCCESS")
wait()
# Expected behaviour: After touching on the "Jogging" button, the button's text changed to "<No Activity>". The previous time and duration information for "Jogging" were replaced with dashes. Additionally, a popup message briefly appeared, showing the updated time and duration for the activity.

wait_until_activity(d, "Main")
d(textStartsWith="STATISTICS", descriptionMatches=".*Statistics").click()
print("Touch on a selected tab that has text 'STATISTICS': SUCCESS")
wait()
# Expected behaviour: By touching on the "STATISTICS" tab, the text in the textview has changed from "-" to "Since a few seconds".

wait_until_activity(d, "Main")
d(resourceIdMatches=".*detail_content").click()
print("Touch on a button that has text 'Since a few seconds, -, -[...and more]': SUCCESS")
wait()
# Expected behaviour: The textview displaying the time duration has been updated from "Since a few seconds" to "Since 30 sec".

wait_until_activity(d, "Main")
d(resourceIdMatches=".*detail_content").click()
print("Touch on a button that has text 'Since 30 sec, -, -[...and more]': SUCCESS")
wait()
# Expected behaviour: After touching the button, the text in the "Since" TextView has changed from "30 sec" to "60 sec" in the current screen.

wait_until_activity(d, "Main")
d(resourceIdMatches=".*detail_content").click()
print("Touch on a button that has text 'Since 60 sec, -, -[...and more]': SUCCESS")
wait()
# Expected behaviour: After touching the button, the textview displaying the time duration changed from "Since 60 sec" to "Since 2 min" on the main screen.

wait_until_activity(d, "Main")
d(resourceIdMatches=".*detail_content").click()
print("Touch on a button that has text 'Since 2 min, -, -[...and more]': SUCCESS")
wait()
wait_until_activity(d, "Main")
d(resourceIdMatches=".*detail_content").click()
print("Touch on a button that has text 'Since 2 min, -, -[...and more]': SUCCESS")
wait()
wait_until_activity(d, "Main")
d(resourceIdMatches=".*detail_content").click()
print("Touch on a button that has text 'Since 2 min, -, -[...and more]': SUCCESS")
wait()
# Expected behaviour: The text in the textview "Since 2 min" has been updated to "Since 3 min" after touching the button.

wait_until_activity(d, "Main")
d(descriptionMatches=".*Open navigation").click()
print("Touch on a button that has content_desc 'Open navigation': SUCCESS")
wait()
# Expected behaviour: After touching the button with content description "Open navigation", the button's content description changes to "Close navigation" and several new buttons appear on the screen, including "Select Activity", "Diary", "Statistics", "Map", "Add Activity", "Edit Activities", "Settings", "About", and "Privacy Policy".

"""
15. Check the overall statistics of all activities in the app.
"""
wait_until_activity(d, "Main")
d(textStartsWith="STATISTICS", descriptionMatches=".*Statistics").click()
print("Touch on a selected tab that has text 'STATISTICS': SUCCESS")
wait()
# Expected behaviour: By touching on the "STATISTICS" tab, the "Since 3 min" text in the previous screen has been updated to "Since 4 min" in the current screen.

wait_until_activity(d, "Main")
d(resourceIdMatches=".*viewpager").swipe(down)
print("Scroll down on a scrollable area that has text 'Since 4 min, -, -[...and more]': SUCCESS")
wait()
wait_until_activity(d, "Main")
d(resourceIdMatches=".*viewpager").swipe(down)
print("Scroll down on a scrollable area that has text 'Since 4 min, -, -[...and more]': SUCCESS")
wait()
# Expected behaviour: By scrolling down on the scrollable area, the textview displaying the time has been updated to "Since 5 min".

"""
16. Navigate to the Statistics page and view the overall statistics of all activities.
"""
wait_until_activity(d, "Main")
d(descriptionMatches=".*Close navigation").click()
print("Touch on a button that has content_desc 'Close navigation': SUCCESS")
wait()
# Expected behaviour: After touching the "Close navigation" button, the button changed to "Open navigation" on the current screen.

wait_until_activity(d, "Main")
d(textStartsWith="STATISTICS", descriptionMatches=".*Statistics").click()
print("Touch on a selected tab that has text 'STATISTICS': SUCCESS")
wait()
"""
17. Navigate to the History page and review the activity records.
"""
wait_until_activity(d, "Main")
d(descriptionMatches=".*Open navigation").click()
print("Touch on a button that has content_desc 'Open navigation': SUCCESS")
wait()
# Expected behaviour: The performed action changed the button with content_desc "Open navigation" to "Close navigation" on the main screen. Additionally, several new buttons and a checked button with text "Select Activity" were added to the screen. The textview displaying the time since the last activity was also updated from 6 minutes to 7 minutes.

wait_until_activity(d, "Main")
d.click(186, 464)
print("Touch on a button that has text 'Statistics': SUCCESS")
wait()
# Expected behaviour: After touching on the "Statistics" button, the screen has changed to the Statistics page. The previous buttons for navigation and the text views related to the main page have been replaced by a "Navigate up" button and a "Statistics" text view respectively. Additionally, a dropdown field with the text "All" has appeared. (page changed from Main to Statistics)

wait_until_activity(d, "Statistics")
d(descriptionMatches=".*Navigate up").click()
print("Touch on a button that has content_desc 'Navigate up': SUCCESS")
wait()
# Expected behaviour: The performed action opened the navigation drawer, resulting in a change from the "Statistics" screen to the "Main" screen. The "Navigate up" button is replaced with an "Open navigation" button, and additional widgets such as a "Search" button and "Add Activity" button are now visible. (page changed from Statistics to Main)

wait_until_activity(d, "Main")
d(descriptionMatches=".*Open navigation").click()
print("Touch on a button that has content_desc 'Open navigation': SUCCESS")
wait()
# Expected behaviour: After touching on the button with content_desc "Open navigation", the button changes to "Close navigation" and several new buttons appear, including "Select Activity", "Diary", "Statistics", "Map", "Add Activity", "Edit Activities", "Settings", "About", and "Privacy Policy".

wait_until_activity(d, "Main")
d(textStartsWith="Diary", resourceIdMatches=".*design_menu_item_text").click()
print("Touch on a button that has text 'Diary': SUCCESS")
wait()
# Expected behaviour: After touching the "Diary" button, the main screen changed to the history screen. The previous buttons for adding activities and selecting a card view were replaced with a list of activities in the history, including "Jogging," "Study Group," and "Statistics." Additionally, a popup message briefly appeared showing the time since the last activity. (page changed from Main to History)

wait_until_activity(d, "History")
d(resourceIdMatches=".*history_list").swipe(down)
print("Scroll down on a scrollable area that has text 'TODAY, Jogging, Start: 2023.10.17 07:53[...and more]': SUCCESS")
wait()
# Expected behaviour: After scrolling down on the history list, the previous entries are replaced with new entries including activities such as "Cinema" and "Yoga Class" with their respective start and end times. Additionally, there is a new button with the resource ID "detail_card_view" present.

wait_until_activity(d, "History")
d(resourceIdMatches=".*detail_card_view").click()
print("Touch on a button that has resource_id 'detail_card_view': SUCCESS")
wait()
# Expected behaviour: After touching the button with resource_id "detail_card_view", the previous screen with a scrollable area called "history_list" is replaced by a new screen with a listview called "resolver_list" which contains options like "Open with Photos", "JUST ONCE", "ALWAYS", and "Use a different app". (page changed from History to Resolver)

"""
18. Edit the "Yoga Class" activity to change its color and add a reminder.
"""
wait_until_activity(d, "Resolver")
d.press("back")
print("Press 'BACK' button to navigate back: SUCCESS")
wait()
# Expected behaviour: The action of pressing the "BACK" button navigated the user back to the "History" screen. The previous screen (Resolver) had a list of resolved actions, while the current screen (History) displays a list of past events and their details. (page changed from Resolver to History)

wait_until_activity(d, "History")
d.click(360, 420)
print("Touch on a button that has text 'Yoga Class, Start: 2023.10.17 07:32, End: 2023.10.17 07:37 (4' 58'')': SUCCESS")
wait()
# Expected behaviour: The action of touching on the "Yoga Class" button opens a new screen called "HistoryDetail" which displays the details of the yoga class entry, including the start and end times, and a "Save" button. (page changed from History to HistoryDetail)

wait_until_activity(d, "HistoryDetail")
d.press("back")
print("Press 'BACK' button to navigate back: SUCCESS")
wait()
wait_until_activity(d, "HistoryDetail")
d(textStartsWith="Note", resourceIdMatches=".*edit_activity_note").click()
print("Touch on a focused textfield that has text 'Note': SUCCESS")
wait()
wait_until_activity(d, "HistoryDetail")
d(descriptionMatches=".*Navigate up").click()
print("Touch on a button that has content_desc 'Navigate up': SUCCESS")
wait()
# Expected behaviour: The action of touching the "Navigate up" button has taken the user from the "HistoryDetail" screen to the "History" screen. The "Diary entry" textview and "Save" button are replaced with the "Diary" textview and "Search" button respectively. Additionally, there are new entries with details about different activities such as "Study Group Session" and "Yoga Class" displayed on the "History" screen. (page changed from HistoryDetail to History)

wait_until_activity(d, "History")
d.click(360, 420)
print("Touch on a button that has text 'Yoga Class, Start: 2023.10.17 07:32, End: 2023.10.17 07:37 (4' 58'')': SUCCESS")
wait()
# Expected behaviour: After touching on the button with the text "Yoga Class, Start: 2023.10.17 07:32, End: 2023.10.17 07:37 (4' 58'')", the screen changed to the HistoryDetail page where the previous widgets related to the history are replaced with a textview for the diary entry, a button to save the entry, and a focused textfield for adding notes. (page changed from History to HistoryDetail)

wait_until_activity(d, "HistoryDetail")
d.press("back")
print("Press 'BACK' button to navigate back: SUCCESS")
wait()
wait_until_activity(d, "HistoryDetail")
d(descriptionMatches=".*Navigate up").click()
print("Touch on a button that has content_desc 'Navigate up': SUCCESS")
wait()
# Expected behaviour: After touching the "Navigate up" button, the screen changes from the HistoryDetail page to the History page. The previous screen had a textview with the text "Diary entry" and a button with the content description "Save", while the current screen has a textview with the text "Diary" and a button with the content description "Search". Additionally, the current screen displays a list of different events with their start and end times. (page changed from HistoryDetail to History)

wait_until_activity(d, "History")
d.click(360, 420)
print("Touch on a button that has text 'Yoga Class, Start: 2023.10.17 07:32, End: 2023.10.17 07:37 (4' 58'')': SUCCESS")
wait()
# Expected behaviour: After touching the "Yoga Class" button, the screen changed to the "HistoryDetail" page, where the details of the yoga class entry are displayed, including the start and end times, as well as an option to save the entry. (page changed from History to HistoryDetail)

wait_until_activity(d, "HistoryDetail")
d(descriptionMatches=".*Save", resourceIdMatches=".*action_edit_done").click()
print("Touch on a button that has content_desc 'Save': SUCCESS")
wait()
# Expected behaviour: By touching the "Save" button, the screen has changed from the "HistoryDetail" page to the "History" page. The "Navigate up" button has replaced the "Save" button, and additional buttons for searching and creating new entries have been added. The details of previous diary entries are also displayed, including the start and end times, along with the option to adjust adjacent entries. (page changed from HistoryDetail to History)

wait_until_activity(d, "History")
d.click(360, 440)
print("Touch on a button that has text 'Yoga Class, Start: 2023.10.17 07:32, End: 2023.10.17 07:37 (4' 58'')': SUCCESS")
wait()
# Expected behaviour: The performed action opens a new screen called "HistoryDetail" where the user can view and edit the details of a diary entry for a Yoga Class that starts at 07:32 and ends at 07:37. The screen includes a textview displaying "Diary entry," a button to save changes, and a focused textfield for adding notes. (page changed from History to HistoryDetail)

"""
19. Adjust the start and end times of the "Yoga Class" activity on the HistoryDetail page.
"""
wait_until_activity(d, "HistoryDetail")
d(textStartsWith="07:32", descriptionMatches=".*Start time", resourceIdMatches=".*time_start").click()
print("Touch on a button that has text '07:32': SUCCESS")
wait()
# Expected behaviour: The action of touching the button with text "07:32" changed the previous time format into separate buttons for hour, minute, and AM/PM selection, allowing the user to edit the time more precisely.

wait_until_activity(d, "HistoryDetail")
d(textStartsWith="7", resourceIdMatches=".*hours").click()
print("Touch on a button that has text '7': SUCCESS")
wait()
wait_until_activity(d, "HistoryDetail")
d(textStartsWith="32", resourceIdMatches=".*minutes").click()
print("Touch on a button that has text '32': SUCCESS")
wait()
wait_until_activity(d, "HistoryDetail")
d(textStartsWith="PM", resourceIdMatches=".*pm_label").click()
print("Touch on a button that has text 'PM': SUCCESS")
wait()
# Expected behaviour: By touching the button with the text "PM", the button with the text "AM" is deselected and the button with the text "PM" is selected.

wait_until_activity(d, "HistoryDetail")
d(textStartsWith="OK", resourceIdMatches=".*button1").click()
print("Touch on a button that has text 'OK': SUCCESS")
wait()
# Expected behaviour: The previous screen, which displayed a history detail, has been replaced with a new screen showing a diary entry. The buttons and textviews have been updated accordingly, and a new focused textfield for entering notes is now present.

wait_until_activity(d, "HistoryDetail")
d(textStartsWith="07:37", descriptionMatches=".*End time", resourceIdMatches=".*time_end").click()
print("Touch on a button that has text '07:37': SUCCESS")
wait()
# Expected behaviour: The action of touching the button with text "07:37" changed the previous time display into separate buttons for the hour and minute, along with buttons for selecting AM or PM.

wait_until_activity(d, "HistoryDetail")
d(textStartsWith="37", resourceIdMatches=".*minutes").click()
print("Touch on a button that has text '37': SUCCESS")
wait()
wait_until_activity(d, "HistoryDetail")
d(textStartsWith="37", resourceIdMatches=".*minutes").click()
print("Touch on a button that has text '37': SUCCESS")
wait()
wait_until_activity(d, "HistoryDetail")
d(textStartsWith="7", resourceIdMatches=".*hours").click()
print("Touch on a button that has text '7': SUCCESS")
wait()
wait_until_activity(d, "HistoryDetail")
d(textStartsWith="7", resourceIdMatches=".*hours").click()
print("Touch on a button that has text '7': SUCCESS")
wait()
wait_until_activity(d, "HistoryDetail")
d(textStartsWith="7", resourceIdMatches=".*hours").click()
print("Touch on a button that has text '7': SUCCESS")
wait()
wait_until_activity(d, "HistoryDetail")
d(textStartsWith="37", resourceIdMatches=".*minutes").click()
print("Touch on a button that has text '37': SUCCESS")
wait()
wait_until_activity(d, "HistoryDetail")
d(textStartsWith="PM", resourceIdMatches=".*pm_label").click()
print("Touch on a button that has text 'PM': SUCCESS")
wait()
# Expected behaviour: The action of touching the "PM" button has successfully changed the state of the buttons, making the "PM" button checked and the "AM" button unchecked.

"""
20. Adjust the start and end times for the "Yoga Class" activity.
"""
wait_until_activity(d, "HistoryDetail")
d(textStartsWith="7", resourceIdMatches=".*hours").click()
print("Touch on a button that has text '7': SUCCESS")
wait()
wait_until_activity(d, "HistoryDetail")
d(textStartsWith="37", resourceIdMatches=".*minutes").click()
print("Touch on a button that has text '37': SUCCESS")
wait()
wait_until_activity(d, "HistoryDetail")
d(textStartsWith="AM", resourceIdMatches=".*am_label").click()
print("Touch on a button that has text 'AM': SUCCESS")
wait()
# Expected behaviour: The performed action changed the selected time from "PM" to "AM" in the HistoryDetail screen.

wait_until_activity(d, "HistoryDetail")
d(textStartsWith="OK", resourceIdMatches=".*button1").click()
print("Touch on a button that has text 'OK': SUCCESS")
wait()
# Expected behaviour: The performed action of touching the "OK" button has caused a change in the screen. The previous screen, "HistoryDetail", has been replaced with a new screen, also called "HistoryDetail", which displays different widgets such as a "Navigate up" button, a "Save" button, textviews for "Diary entry", "Start", "End", and "The activity shall always start before it ends", a checkbox for "Adjust adjacent diary entries", and a focused textfield for "Note".

wait_until_activity(d, "HistoryDetail")
d(textStartsWith="19:32", descriptionMatches=".*Start time", resourceIdMatches=".*time_start").click()
print("Touch on a button that has text '19:32': SUCCESS")
wait()
# Expected behaviour: The button with the text "19:32" has been replaced with separate buttons for the hour (7), minute (32), and AM/PM options. Additionally, there are new buttons for "CANCEL" and "OK".

wait_until_activity(d, "HistoryDetail")
d(textStartsWith="7", resourceIdMatches=".*hours").click()
print("Touch on a button that has text '7': SUCCESS")
wait()
wait_until_activity(d, "HistoryDetail")
d(textStartsWith="OK", resourceIdMatches=".*button1").click()
print("Touch on a button that has text 'OK': SUCCESS")
wait()
# Expected behaviour: After touching the "OK" button, the previous screen with buttons and textviews related to time and date is replaced by a new screen displaying a diary entry with details such as start and end times, a note field, and options for adjusting adjacent entries.

wait_until_activity(d, "HistoryDetail")
d(descriptionMatches=".*Save", resourceIdMatches=".*action_edit_done").click()
print("Touch on a button that has content_desc 'Save': SUCCESS")
wait()
"""
21. Edit the start and end times of the "Yoga Class" activity in the HistoryDetail page.
"""
wait_until_activity(d, "HistoryDetail")
d(textStartsWith="19:32", descriptionMatches=".*Start time", resourceIdMatches=".*time_start").click()
print("Touch on a button that has text '19:32': SUCCESS")
wait()
# Expected behaviour: The action changed the time displayed on the button from "19:32" to "7:32 AM".

wait_until_activity(d, "HistoryDetail")
d(textStartsWith="32", resourceIdMatches=".*minutes").click()
print("Touch on a button that has text '32': SUCCESS")
wait()
wait_until_activity(d, "HistoryDetail")
d(textStartsWith="32", resourceIdMatches=".*minutes").click()
print("Touch on a button that has text '32': SUCCESS")
wait()
wait_until_activity(d, "HistoryDetail")
d(textStartsWith="OK", resourceIdMatches=".*button1").click()
print("Touch on a button that has text 'OK': SUCCESS")
wait()
# Expected behaviour: The action of touching the "OK" button in the previous screen has brought the user to a different screen where they can view and edit a diary entry for a yoga class, including the start and end times, a note, and an option to adjust adjacent diary entries.

wait_until_activity(d, "HistoryDetail")
d(textStartsWith="07:37", descriptionMatches=".*End time", resourceIdMatches=".*time_end").click()
print("Touch on a button that has text '07:37': SUCCESS")
wait()
# Expected behaviour: The action of touching on the button with text "07:37" changed the previous time display into separate buttons for hour and minute, along with buttons for selecting AM/PM, and options to cancel or confirm the time selection.

wait_until_activity(d, "HistoryDetail")
d(textStartsWith="37", resourceIdMatches=".*minutes").click()
print("Touch on a button that has text '37': SUCCESS")
wait()
wait_until_activity(d, "HistoryDetail")
d(textStartsWith="PM", resourceIdMatches=".*pm_label").click()
print("Touch on a button that has text 'PM': SUCCESS")
wait()
# Expected behaviour: The action changed the state of the buttons from "AM" to "PM", and vice versa, indicating a toggle between AM and PM time options.

wait_until_activity(d, "HistoryDetail")
d(textStartsWith="AM", resourceIdMatches=".*am_label").click()
print("Touch on a button that has text 'AM': SUCCESS")
wait()
# Expected behaviour: By touching on the button with text "AM", the button becomes checked and the button with text "PM" becomes unchecked.

wait_until_activity(d, "HistoryDetail")
d(textStartsWith="AM", resourceIdMatches=".*am_label").click()
print("Touch on a checked button that has text 'AM': SUCCESS")
wait()
wait_until_activity(d, "HistoryDetail")
d(textStartsWith="OK", resourceIdMatches=".*button1").click()
print("Touch on a button that has text 'OK': SUCCESS")
wait()
# Expected behaviour: The performed action on the "OK" button in the previous screen has caused a change in the current screen where the previous buttons and textviews have been replaced with new buttons, textviews, a checkbox, and a focused textfield.

wait_until_activity(d, "HistoryDetail")
d(textStartsWith="07:37", descriptionMatches=".*End time", resourceIdMatches=".*time_end").click()
print("Touch on a button that has text '07:37': SUCCESS")
wait()
# Expected behaviour: The action of touching the button with text "07:37" has changed the time display format from a single button to separate buttons for hours and minutes, along with buttons for selecting AM or PM.

wait_until_activity(d, "HistoryDetail")
d(textStartsWith="37", resourceIdMatches=".*minutes").click()
print("Touch on a button that has text '37': SUCCESS")
wait()
wait_until_activity(d, "HistoryDetail")
d(textStartsWith="PM", resourceIdMatches=".*pm_label").click()
print("Touch on a button that has text 'PM': SUCCESS")
wait()
# Expected behaviour: By touching on the "PM" button, the button is checked and the "AM" button is unchecked, indicating that the time format has been changed from AM to PM.

"""
22. Change the color of the "Study Group" activity.
"""
wait_until_activity(d, "HistoryDetail")
d.press("back")
print("Press 'BACK' button to navigate back: SUCCESS")
wait()
# Expected behaviour: The action of pressing the "BACK" button navigated back to the previous screen, which is the HistoryDetail screen. The widgets on the screen have changed, including the presence of a button with the content description "Navigate up", a textview with the text "Diary entry", a button with the content description "Save", and various other widgets related to a diary entry.

wait_until_activity(d, "HistoryDetail")
d(descriptionMatches=".*Navigate up").click()
print("Touch on a button that has content_desc 'Navigate up': SUCCESS")
wait()
# Expected behaviour: The action of touching the "Navigate up" button in the HistoryDetail screen takes the user to the History screen, where they can view a list of previous activities, including their start and end times, and perform actions such as searching and navigating. (page changed from HistoryDetail to History)

wait_until_activity(d, "History")
d.click(360, 245)
print("Touch on a button that has text 'Study Group Session, Start: 2023.10.17 07:37, End: 2023.10.17 07:40 (3' 19'')': SUCCESS")
wait()
# Expected behaviour: The performed action updated the current screen to show the details of a study group session with the start and end times, along with options to save and make adjustments to adjacent diary entries. (page changed from History to HistoryDetail)

"""
23. Adjust the start and end times of the "Study Group" activity.
"""
wait_until_activity(d, "HistoryDetail")
d(textStartsWith="2023.10.17", descriptionMatches=".*Start date", resourceIdMatches=".*date_start").click()
print("Touch on a button that has text '2023.10.17': SUCCESS")
wait()
# Expected behaviour: After touching the button with the text "2023.10.17", the screen has changed to display a calendar view with the current month and year, along with buttons for previous and next month navigation, and options to cancel or confirm the selected date.

wait_until_activity(d, "HistoryDetail")
d(resourceIdMatches=".*day_picker_view_pager").swipe(right)
print("Scroll right on a scrollable area that has text '1, 2, 3[...and more]': SUCCESS")
wait()
# Expected behaviour: By scrolling right on the scrollable area, the checked widget with text "17" has been unchecked and a new widget with text "31" has appeared.

wait_until_activity(d, "HistoryDetail")
d(textStartsWith="Tue, Oct 17", resourceIdMatches=".*date_picker_header_date").click()
print("Touch on a button that has text 'Tue, Oct 17': SUCCESS")
wait()
# Expected behaviour: The button "Tue, Oct 17" was successfully selected and is now checked on the current screen.

wait_until_activity(d, "HistoryDetail")
d(resourceIdMatches=".*day_picker_view_pager").swipe(right)
print("Scroll right on a scrollable area that has text '1, 2, 3[...and more]': SUCCESS")
wait()
# Expected behaviour: By scrolling right on the scrollable area, the user has revealed more widgets with texts "17" and "31" and removed the check mark from the widget with text "17".

wait_until_activity(d, "HistoryDetail")
d(resourceIdMatches=".*day_picker_view_pager").swipe(right)
print("Scroll right on a scrollable area that has text '1, 2, 3[...and more]': SUCCESS")
wait()
# Expected behaviour: By scrolling right on the scrollable area, the screen has been updated to display an additional widget with the text "31".

wait_until_activity(d, "HistoryDetail")
d(textStartsWith="OK", resourceIdMatches=".*button1").click()
print("Touch on a button that has text 'OK': SUCCESS")
wait()
# Expected behaviour: After touching the "OK" button, the previous screen is replaced by a new screen with a navigation button, a textview displaying "Diary entry", a "Save" button, a textview displaying "Study Group Session", buttons showing the date and time of the session, a checkbox, and a textfield for adding notes.

wait_until_activity(d, "HistoryDetail")
d(descriptionMatches=".*Save", resourceIdMatches=".*action_edit_done").click()
print("Touch on a button that has content_desc 'Save': SUCCESS")
wait()
# Expected behaviour: The action of touching the "Save" button in the "HistoryDetail" screen changed the screen to the "History" screen, where the "Navigate up" button, "Search" button, and a list of diary entries are now visible. The previous "Diary entry" textview and "Save" button are no longer present. (page changed from HistoryDetail to History)

wait_until_activity(d, "History")
d.click(360, 265)
print("Touch on a button that has text 'Study Group Session, Start: 2023.10.17 07:37, End: 2023.10.17 07:40 (3' 19'')': SUCCESS")
wait()
# Expected behaviour: After touching the button "Study Group Session, Start: 2023.10.17 07:37, End: 2023.10.17 07:40 (3' 19'')", the screen changes to the "HistoryDetail" screen, where the previous textviews for the start and end times are replaced with buttons that display the corresponding dates and times. Additionally, a new textview for "Diary entry" and a button for "Save" are added. (page changed from History to HistoryDetail)

wait_until_activity(d, "HistoryDetail")
d(textStartsWith="07:37", descriptionMatches=".*Start time", resourceIdMatches=".*time_start").click()
print("Touch on a button that has text '07:37': SUCCESS")
wait()
# Expected behaviour: The performed action changed the button with text "07:37" into separate buttons for hour (7), colon (:), and minute (37), along with buttons for AM and PM, as well as buttons for canceling or confirming the selection.

wait_until_activity(d, "HistoryDetail")
d(textStartsWith="7", resourceIdMatches=".*hours").click()
print("Touch on a button that has text '7': SUCCESS")
wait()
wait_until_activity(d, "HistoryDetail")
d(textStartsWith="37", resourceIdMatches=".*minutes").click()
print("Touch on a button that has text '37': SUCCESS")
wait()
wait_until_activity(d, "HistoryDetail")
d(textStartsWith="37", resourceIdMatches=".*minutes").click()
print("Touch on a button that has text '37': SUCCESS")
wait()
wait_until_activity(d, "HistoryDetail")
d(textStartsWith="7", resourceIdMatches=".*hours").click()
print("Touch on a button that has text '7': SUCCESS")
wait()
"""
24. Adjust the start and end times of the current activity using the "Adjust adjacent diary entries" option.
"""
wait_until_activity(d, "HistoryDetail")
d(textStartsWith="OK", resourceIdMatches=".*button1").click()
print("Touch on a button that has text 'OK': SUCCESS")
wait()
# Expected behaviour: The action of touching the "OK" button on the previous screen led to changes on the current screen, including the addition of a "Navigate up" button, a "Save" button, and the modification of various textviews and buttons related to a diary entry.

wait_until_activity(d, "HistoryDetail")
d(textStartsWith="Adjust adjacent diary entries", resourceIdMatches=".*adjust_adjacent").click()
print("Touch on a checked checkbox that has text 'Adjust adjacent diary entries': SUCCESS")
wait()
# Expected behaviour: The checked checkbox with the text "Adjust adjacent diary entries" is now unchecked.

wait_until_activity(d, "HistoryDetail")
d(textStartsWith="2023.10.17", descriptionMatches=".*Start date", resourceIdMatches=".*date_start").click()
print("Touch on a button that has text '2023.10.17': SUCCESS")
wait()
# Expected behaviour: By touching on the button with the text "2023.10.17", the screen has changed to display a calendar with dates and buttons to navigate between months.

wait_until_activity(d, "HistoryDetail")
d(textStartsWith="Tue, Oct 17", resourceIdMatches=".*date_picker_header_date").click()
print("Touch on a button that has text 'Tue, Oct 17': SUCCESS")
wait()
wait_until_activity(d, "HistoryDetail")
d.press("back")
print("Press 'BACK' button to navigate back: SUCCESS")
wait()
# Expected behaviour: Navigating back from the HistoryDetail screen brings the user back to the previous screen, where they can see the "Navigate up" button, a "Save" button, the text "Diary entry", a "Study Group Session" textview, "Start" and "End" textviews with corresponding date and time buttons, a checkbox for adjusting adjacent diary entries, and a focused textfield for notes.

wait_until_activity(d, "HistoryDetail")
d(textStartsWith="Adjust adjacent diary entries", resourceIdMatches=".*adjust_adjacent").click()
print("Touch on a checkbox that has text 'Adjust adjacent diary entries': SUCCESS")
wait()
# Expected behaviour: The checkbox with the text "Adjust adjacent diary entries" has been checked.

wait_until_activity(d, "HistoryDetail")
d(textStartsWith="07:37", descriptionMatches=".*Start time", resourceIdMatches=".*time_start").click()
print("Touch on a button that has text '07:37': SUCCESS")
wait()
# Expected behaviour: The performed action changed the time displayed on the button from "07:37" to "7:37 AM".

wait_until_activity(d, "HistoryDetail")
d(textStartsWith="7", resourceIdMatches=".*hours").click()
print("Touch on a button that has text '7': SUCCESS")
wait()
wait_until_activity(d, "HistoryDetail")
d(textStartsWith="7", resourceIdMatches=".*hours").click()
print("Touch on a button that has text '7': SUCCESS")
wait()
wait_until_activity(d, "HistoryDetail")
d(textStartsWith="37", resourceIdMatches=".*minutes").click()
print("Touch on a button that has text '37': SUCCESS")
wait()
wait_until_activity(d, "HistoryDetail")
d(textStartsWith="7", resourceIdMatches=".*hours").click()
print("Touch on a button that has text '7': SUCCESS")
wait()
wait_until_activity(d, "HistoryDetail")
d(textStartsWith="PM", resourceIdMatches=".*pm_label").click()
print("Touch on a button that has text 'PM': SUCCESS")
wait()
# Expected behaviour: The action of touching on the "PM" button changed its state to checked, and the "AM" button changed its state to unchecked.

wait_until_activity(d, "HistoryDetail")
d(textStartsWith="OK", resourceIdMatches=".*button1").click()
print("Touch on a button that has text 'OK': SUCCESS")
wait()
# Expected behaviour: The action of touching the "OK" button on the previous screen led to a change in the current screen where the previous buttons and textviews were replaced with new buttons, textviews, and checkboxes related to a diary entry.

"""
25. Adjust the start time of the "Study Group" activity.
"""
wait_until_activity(d, "HistoryDetail")
d(textStartsWith="2023.10.17", descriptionMatches=".*Start date", resourceIdMatches=".*date_start").click()
print("Touch on a button that has text '2023.10.17': SUCCESS")
wait()
# Expected behaviour: After touching the button with the text "2023.10.17", the previous screen has been replaced with a new screen displaying a calendar with the month of October 2023 and the selected date highlighted.

wait_until_activity(d, "HistoryDetail")
d(textStartsWith="OK", resourceIdMatches=".*button1").click()
print("Touch on a button that has text 'OK': SUCCESS")
wait()
# Expected behaviour: After touching the "OK" button, the previous screen has been replaced with a new screen that displays a "Diary entry" with a "Save" button, study session details including start and end times, a note text field, and an option to adjust adjacent diary entries.

wait_until_activity(d, "HistoryDetail")
d(textStartsWith="07:40", descriptionMatches=".*End time", resourceIdMatches=".*time_end").click()
print("Touch on a button that has text '07:40': SUCCESS")
wait()
# Expected behaviour: By touching on the button with the text "07:40", the time selection for the diary entry has been changed to 7:40 AM, and the options to cancel or confirm the selection are now visible.

wait_until_activity(d, "HistoryDetail")
d(textStartsWith="OK", resourceIdMatches=".*button1").click()
print("Touch on a button that has text 'OK': SUCCESS")
wait()
# Expected behaviour: After touching the "OK" button, the previous screen changed to a screen with a different layout. The button with the text "OK" is replaced by a button with the content description "Navigate up" and a button with the content description "Save". The textviews and buttons also have different text values.

wait_until_activity(d, "HistoryDetail")
d(descriptionMatches=".*Save", resourceIdMatches=".*action_edit_done").click()
print("Touch on a button that has content_desc 'Save': SUCCESS")
wait()
"""
26. Add a note to the "Study Group" activity in the HistoryDetail page.
"""
wait_until_activity(d, "HistoryDetail")
d(textStartsWith="Note", resourceIdMatches=".*edit_activity_note").click()
print("Touch on a focused textfield that has text 'Note': SUCCESS")
wait()
wait_until_activity(d, "HistoryDetail")
d(descriptionMatches=".*Save", resourceIdMatches=".*action_edit_done").click()
print("Touch on a button that has content_desc 'Save': SUCCESS")
wait()
wait_until_activity(d, "HistoryDetail")
d(textStartsWith="Note", resourceIdMatches=".*edit_activity_note").set_text("Prepared for the study session and discussed chapter 4 of the textbook.")
print("Fill a focused textfield that has text 'Note' with 'Prepared for the study session and discussed chapter 4 of the textbook.': SUCCESS")
wait()
# Expected behaviour: The focused textfield that had the text "Note" has been filled with the text "Prepared for the study session and discussed chapter 4 of the textbook."

wait_until_activity(d, "HistoryDetail")
d(descriptionMatches=".*Save", resourceIdMatches=".*action_edit_done").click()
print("Touch on a button that has content_desc 'Save': SUCCESS")
wait()
"""
27. Edit the end time of the "Study Group" activity.
"""
wait_until_activity(d, "HistoryDetail")
d(textStartsWith="07:40", descriptionMatches=".*End time", resourceIdMatches=".*time_end").click()
print("Touch on a button that has text '07:40': SUCCESS")
wait()
# Expected behaviour: The action of touching the button with text "07:40" has changed the previous screen to a screen where the time can be adjusted, with buttons for selecting the hour, minute, and AM/PM, as well as buttons for canceling or confirming the selection.

wait_until_activity(d, "HistoryDetail")
d(textStartsWith="7", resourceIdMatches=".*hours").click()
print("Touch on a button that has text '7': SUCCESS")
wait()
wait_until_activity(d, "HistoryDetail")
d(textStartsWith="AM", resourceIdMatches=".*am_label").click()
print("Touch on a checked button that has text 'AM': SUCCESS")
wait()
wait_until_activity(d, "HistoryDetail")
d(textStartsWith="OK", resourceIdMatches=".*button1").click()
print("Touch on a button that has text 'OK': SUCCESS")
wait()
# Expected behaviour: After touching the "OK" button, the previous screen, "HistoryDetail," is replaced with the current screen, "HistoryDetail." The new screen shows information about a study group session, including the start and end times, along with a checkbox to adjust adjacent diary entries. There is also a focused text field for entering notes about the session.

wait_until_activity(d, "HistoryDetail")
d(textStartsWith="07:40", descriptionMatches=".*End time", resourceIdMatches=".*time_end").click()
print("Touch on a button that has text '07:40': SUCCESS")
wait()
# Expected behaviour: The action changed the time displayed on the button from "07:40" to "7:40 AM" with additional buttons to select between AM and PM, and options to cancel or confirm the time change.

wait_until_activity(d, "HistoryDetail")
d(textStartsWith="40", resourceIdMatches=".*minutes").click()
print("Touch on a button that has text '40': SUCCESS")
wait()
wait_until_activity(d, "HistoryDetail")
d(textStartsWith="40", resourceIdMatches=".*minutes").click()
print("Touch on a button that has text '40': SUCCESS")
wait()
wait_until_activity(d, "HistoryDetail")
d(textStartsWith="40", resourceIdMatches=".*minutes").click()
print("Touch on a button that has text '40': SUCCESS")
wait()
wait_until_activity(d, "HistoryDetail")
d(textStartsWith="40", resourceIdMatches=".*minutes").click()
print("Touch on a button that has text '40': SUCCESS")
wait()
wait_until_activity(d, "HistoryDetail")
d(textStartsWith="OK", resourceIdMatches=".*button1").click()
print("Touch on a button that has text 'OK': SUCCESS")
wait()
# Expected behaviour: After touching the "OK" button, the previous screen changed to a screen with a different layout. The button with text "OK" and other elements related to time and date were replaced with elements related to a diary entry, such as a textfield for notes and buttons for saving and navigating.

"""
28. Navigate to the Statistics page and review the detailed statistics of the "Jogging" activity.
"""
wait_until_activity(d, "History")
d(descriptionMatches=".*Navigate up").click()
print("Touch on a button that has content_desc 'Navigate up': SUCCESS")
wait()
# Expected behaviour: The touch on the "Navigate up" button caused the previous screen to transition to the current screen, where a new button with content description "Open navigation" appeared along with additional options for activities such as "Study Group," "Jogging," and "Sleeping." (page changed from History to Main)

wait_until_activity(d, "Main")
d(textStartsWith="Jogging", resourceIdMatches=".*select_card_view").click()
print("Touch on a button that has text 'Jogging': SUCCESS")
wait()
# Expected behaviour: By touching on the "Jogging" button, the previous screen's "<No Activity>" button is replaced with a "Jogging" button. Additionally, the textviews related to activity duration and statistics are updated with new values.

wait_until_activity(d, "Main")
d(textStartsWith="Jogging", resourceIdMatches=".*activity_background").click()
print("Touch on a button that has text 'Jogging': SUCCESS")
wait()
# Expected behaviour: After touching the "Jogging" button, the button text changed to "<No Activity>", and the displayed duration and last start time for jogging activity were updated to "5' 39''" and "Since a few seconds" respectively.

wait_until_activity(d, "Main")
d(textStartsWith="STATISTICS", descriptionMatches=".*Statistics").click()
print("Touch on a selected tab that has text 'STATISTICS': SUCCESS")
wait()
# Expected behaviour: By touching on the "STATISTICS" tab, the main screen now displays updated information in the textview, "Since a few seconds," instead of displaying a hyphen.

wait_until_activity(d, "Main")
d(resourceIdMatches=".*detail_content").click()
print("Touch on a button that has text 'Since a few seconds, -, -[...and more]': SUCCESS")
wait()
# Expected behaviour: After touching the button, the text in the "Since a few seconds" TextView has changed to "Since 60 sec" and a popup message appeared briefly displaying "Since 45 sec".

wait_until_activity(d, "Main")
d(resourceIdMatches=".*detail_content").click()
print("Touch on a button that has text 'Since 60 sec, -, -[...and more]': SUCCESS")
wait()
# Expected behaviour: After touching the button, the "Since 60 sec" textview on the main screen has been updated to "Since 75 sec".

"""
29. Check the detailed statistics of the "Cinema" activity.
"""
wait_until_activity(d, "Main")
d(textStartsWith="Cinema", resourceIdMatches=".*select_card_view").click()
print("Touch on a button that has text 'Cinema': SUCCESS")
wait()
# Expected behaviour: The performed action changed the text of a button from "<No Activity>" to "Cinema".

wait_until_activity(d, "Main")
d(textStartsWith="STATISTICS", descriptionMatches=".*Statistics").click()
print("Touch on a selected tab that has text 'STATISTICS': SUCCESS")
wait()
# Expected behaviour: After touching on the "STATISTICS" tab, the duration values displayed in the textviews have changed from "1' 05''" to "2' 22''".

wait_until_activity(d, "Main")
d(resourceIdMatches=".*detail_content").click()
print("Touch on a button that has text 'Since 75 sec, Average duration: 1' 06'', Last start: 2023.10.17 07:25[...and more]': SUCCESS")
wait()
# Expected behaviour: After touching on the button, the screen changed to the "HistoryDetail" page. The button "Open navigation" was replaced with the button "Navigate up", and additional widgets such as "Diary entry", "Save" button, and text fields for "Start" and "End" appeared. A popup message briefly displayed multiple updated duration values. (page changed from Main to HistoryDetail)

wait_until_activity(d, "HistoryDetail")
d.press("back")
print("Press 'BACK' button to navigate back: SUCCESS")
wait()
wait_until_activity(d, "HistoryDetail")
d(descriptionMatches=".*Navigate up").click()
print("Touch on a button that has content_desc 'Navigate up': SUCCESS")
wait()
# Expected behaviour: The performed action has taken the user from the HistoryDetail screen to the Main screen, where the navigation button has been replaced with a button to open the navigation drawer. (page changed from HistoryDetail to Main)

wait_until_activity(d, "Main")
d(textStartsWith="STATISTICS", descriptionMatches=".*Statistics").click()
print("Touch on a selected tab that has text 'STATISTICS': SUCCESS")
wait()
# Expected behaviour: By touching on the "STATISTICS" tab, the duration displayed in the textviews has increased by 20 seconds, indicating that the timer has been running for an additional minute since the previous screen.

"""
30. Add a new activity named "Gym Workout" to the Activity Diary Debug app.
"""
wait_until_activity(d, "Main")
d(descriptionMatches=".*Add Activity", resourceIdMatches=".*action_add_activity").click()
print("Touch on a button that has content_desc 'Add Activity': SUCCESS")
wait()
# Expected behaviour: By touching the "Add Activity" button, the user is taken to the "Edit" screen where they can create a new activity. The previous screen's buttons for navigation and search are replaced with buttons for deleting and saving the activity, and there is a text field for entering the activity title. A popup message briefly appears with updated activity duration information. (page changed from Main to Edit)

wait_until_activity(d, "Edit")
d(textStartsWith="Activity title", resourceIdMatches=".*edit_activity_name").set_text("Gym Workout")
print("Fill a focused textfield that has text 'Activity title' with 'Gym Workout': SUCCESS")
wait()
# Expected behaviour: The user successfully filled the focused textfield with the text "Gym Workout", replacing the previous text "Activity title".

wait_until_activity(d, "Edit")
d(resourceIdMatches=".*edit_activity_color").click()
print("Touch on a button that has resource_id 'edit_activity_color': SUCCESS")
wait()
# Expected behaviour: By touching on the "edit_activity_color" button, the color selection screen is opened where the user can input and select a new activity color using the text field and "SELECT" button.

wait_until_activity(d, "Edit")
d(textStartsWith="AFB42B", resourceIdMatches=".*hexCode").set_text("C4D8A2")
print("Fill a focused textfield that has text 'AFB42B' with 'C4D8A2': SUCCESS")
wait()
# Expected behaviour: The focused textfield that previously had the text "AFB42B" has now been filled with the text "C4D8A2".

wait_until_activity(d, "Edit")
d(textStartsWith="SELECT", resourceIdMatches=".*okColorButton").click()
print("Touch on a button that has text 'SELECT': SUCCESS")
wait()
# Expected behaviour: After touching the "SELECT" button, the previous screen with a focused textfield and a button has been replaced with a new screen that has a different layout, including a textview, buttons with content descriptions, and a focused textfield with different text.

wait_until_activity(d, "Edit")
d(descriptionMatches=".*Save", resourceIdMatches=".*action_edit_done").click()
print("Touch on a button that has content_desc 'Save': SUCCESS")
wait()
# Expected behaviour: The touch on the "Save" button in the previous screen navigated the user to the main screen, where they can see different tabs for statistics, notes, and pictures, along with various activity buttons and a scrollable area. (page changed from Edit to Main)

wait_until_activity(d, "Main")
d(resourceIdMatches=".*viewpager").swipe(down)
print("Scroll down on a scrollable area that has text 'Since 5 min, -, -[...and more]': SUCCESS")
wait()
# Expected behaviour: By scrolling down on the scrollable area, the text "Since 5 min" has been updated to "Since 75 sec" and the time durations in the three textviews below have increased from "0 sec" to "1' 19''".

"""
31. Explore the details and statistics of the newly added "Gym Workout" activity.
"""
wait_until_activity(d, "Main")
d(textStartsWith="Gym Workout", resourceIdMatches=".*select_card_view").click()
print("Touch on a button that has text 'Gym Workout': SUCCESS")
wait()
# Expected behaviour: The "Gym Workout" button on the main screen has been replaced with a "<No Activity>" button. Additionally, the displayed time duration has been updated to "2' 09''" and the date has changed to "Tue, 10.17.23".

"""
32. Search for a specific activity, "Gym Workout", using the search function.
"""
wait_until_activity(d, "Main")
d(descriptionMatches=".*Search", resourceIdMatches=".*search_button").click()
print("Touch on a button that has content_desc 'Search': SUCCESS")
wait()
# Expected behaviour: After touching on the "Search" button, the button is replaced by a focused textfield with the text "Search…" and a "Clear query" button appears.

wait_until_activity(d, "Main")
d(textStartsWith="Search…", resourceIdMatches=".*search_src_text").set_text("Gym Workout")
print("Fill a focused textfield that has text 'Search' with 'Gym Workout': SUCCESS")
wait()
# Expected behaviour: The focused textfield that previously had the text "Search…" is now filled with "Gym Workout". Additionally, the button that had the text "Jogging" is now replaced with a button that has the text "Gym Workout".

wait_until_activity(d, "Main")
d(textStartsWith="Gym Workout", resourceIdMatches=".*select_card_view").click()
print("Touch on a button that has text 'Gym Workout': SUCCESS")
wait()
# Expected behaviour: After touching the button "Gym Workout", the screen has changed to show statistics and details about the workout, such as average duration and last start time. The button "Gym Workout" is now selected and there are additional tabs for notes and pictures.

"""
33. Add a picture to the "Gym Workout" activity.
"""
wait_until_activity(d, "Main")
d(textStartsWith="Gym Workout", resourceIdMatches=".*select_card_view").click()
print("Touch on a button that has text 'Gym Workout': SUCCESS")
wait()
# Expected behaviour: After touching the "Gym Workout" button, the textview displaying the gym workout details is updated with the new duration of "3' 08''" and the previous undo button disappears.

wait_until_activity(d, "Main")
d(textStartsWith="PICTURES", descriptionMatches=".*Pictures").click()
print("Touch on a tab that has text 'PICTURES': SUCCESS")
wait()
# Expected behaviour: After touching on the "PICTURES" tab, the selected tab changed to "PICTURES" and the "STATISTICS" tab became unselected. Additionally, a popup message briefly appeared saying "Since a few seconds."

wait_until_activity(d, "Main")
d(resourceIdMatches=".*fab_attach_picture").click()
print("Touch on a button that has resource_id 'fab_attach_picture': SUCCESS")
wait()
# Expected behaviour: After touching on the "fab_attach_picture" button, the previous screen transitions to the Camera screen, where the "fab_attach_picture" button is replaced by a "Shutter button" and additional buttons with resource_ids "More setting controls", "indicator_control", and "btn_cancel" are added. (page changed from Main to Camera)

wait_until_activity(d, "Camera")
d(descriptionMatches=".*Shutter button", resourceIdMatches=".*shutter_button").click()
print("Touch on a button that has content_desc 'Shutter button': SUCCESS")
wait()
# Expected behaviour: After touching the "Shutter button", the "btn_cancel" button has been replaced with the "btn_retake" and "btn_done" buttons.

wait_until_activity(d, "Camera")
d(resourceIdMatches=".*btn_done").click()
print("Touch on a button that has resource_id 'btn_done': SUCCESS")
wait()
# Expected behaviour: After touching the "btn_done" button, the previous Camera screen is replaced with the Main screen. The Main screen now displays various buttons for activities, a scrollable area, tabs for different sections, and options to search and add activities. (page changed from Camera to Main)

wait_until_activity(d, "Main")
d(textStartsWith="Gym Workout", resourceIdMatches=".*select_card_view").click()
print("Touch on a button that has text 'Gym Workout': SUCCESS")
wait()
# Expected behaviour: By touching the "Gym Workout" button, the previous button "<No Activity>" was replaced with a new button "Gym Workout" and a new "UNDO" button appeared. Additionally, a new textview with the text "Gym Workout" was added.

"""
34. Start a "Relaxing" activity from the Main page.
"""
wait_until_activity(d, "Main")
d(textStartsWith="Relaxing", resourceIdMatches=".*select_card_view").click()
print("Touch on a button that has text 'Relaxing': SUCCESS")
wait()
# Expected behaviour: The button with the text "Relaxing" has replaced the button with the text "Gym Workout" on the current screen.

wait_until_activity(d, "Main")
d(resourceIdMatches=".*viewpager").swipe(down)
print("Scroll down on a scrollable area that has resource_id 'viewpager': SUCCESS")
wait()
# Expected behaviour: By scrolling down on the "viewpager" scrollable area, the "Relaxing" textview and the "UNDO" button have disappeared from the main screen.

wait_until_activity(d, "Main")
d(resourceIdMatches=".*viewpager").swipe(up)
print("Scroll up on a scrollable area that has resource_id 'viewpager': SUCCESS")
wait()
"""
35. Adjust the settings of the Activity Diary Debug app to personalize the user experience.
"""
wait_until_activity(d, "Main")
d(descriptionMatches=".*Open navigation").click()
print("Touch on a button that has content_desc 'Open navigation': SUCCESS")
wait()
# Expected behaviour: The performed action opens the navigation drawer, which changes the content_desc of the button from "Open navigation" to "Close navigation" and adds a list of buttons related to different activities and settings.

wait_until_activity(d, "Main")
d.click(186, 741)
print("Touch on a button that has text 'Settings': SUCCESS")
wait()
# Expected behaviour: After touching the "Settings" button, the screen changes to the Settings page where there are options to customize the app, such as changing the date and duration formats, enabling notifications, and managing location services. (page changed from Main to Settings)

wait_until_activity(d, "Settings")
d(resourceIdMatches=".*recycler_view").swipe(down)
print("Scroll down on a focused scrollable area that has text 'View, Date format, 2023.10.17 08:55[...and more]': SUCCESS")
wait()
# Expected behaviour: After scrolling down on the Settings page, the screen has changed to show additional options such as "Images", "Picture Storage Folder", "Metadata", "Conditions", "Activity sequence", "Activity interruptions", "Activity occurrence", "Daytime", "Backup", and "Import database".

wait_until_activity(d, "Settings")
d.click(360, 170)
print("Touch on a button that has text 'Picture Storage Folder, Store activity photos in directory ActivityDiary': SUCCESS")
wait()
# Expected behaviour: After touching the button "Picture Storage Folder", the screen changed to a new page where there is a textfield with the current directory "ActivityDiary" displayed, along with buttons "CANCEL" and "OK".

wait_until_activity(d, "Settings")
d(textStartsWith="ActivityDiary", resourceIdMatches=".*edit").set_text("/storage/emulated/0/ActivityDiary")
print("Fill a focused textfield that has text 'ActivityDiary' with '/storage/emulated/0/ActivityDiary': SUCCESS")
wait()
# Expected behaviour: The user successfully filled the focused textfield with the directory path "/storage/emulated/0/ActivityDiary" in the Settings screen.

wait_until_activity(d, "Settings")
d(textStartsWith="OK", resourceIdMatches=".*button1").click()
print("Touch on a button that has text 'OK': SUCCESS")
wait()
# Expected behaviour: After touching the "OK" button, the textview "Directory to store the activity photos" and the focused textfield with the directory path "/storage/emulated/0/ActivityDiary" are removed, and a new textview "Store activity photos in directory /storage/emulated/0/ActivityDiary" is added.

wait_until_activity(d, "Settings")
d(resourceIdMatches=".*recycler_view").swipe(down)
print("Scroll down on a focused scrollable area that has text 'Images, Picture Storage Folder, Store activity photos in directory /storage/emulat[...][...and more]': SUCCESS")
wait()
# Expected behaviour: After scrolling down on the focused scrollable area in the Settings page, the "Images" textview is no longer visible, but the rest of the widgets remain the same.

wait_until_activity(d, "Settings")
d.click(360, 417)
print("Touch on a button that has text 'Alphabetical sort, Alphabetical sorting has a weight of 3 on suggeste[...]': SUCCESS")
wait()
# Expected behaviour: The action of touching the button with the text "Alphabetical sort" has changed the state of the button from "ON" to "OFF".

wait_until_activity(d, "Settings")
d(textStartsWith="1", resourceIdMatches=".*text1").click()
print("Touch on a button that has text '1': SUCCESS")
wait()
# Expected behaviour: After touching the button with text "1", the button with text "1" is no longer visible on the current screen.

"""
36. Create a backup of the activity data in the Activity Diary Debug app.
"""
wait_until_activity(d, "Documents")
d(descriptionMatches=".*More options").click()
print("Touch on a button that has content_desc 'More options': SUCCESS")
wait()
# Expected behaviour: The action of touching the "More options" button in the previous screen has resulted in the appearance of a new button with the text "New folder" and two additional buttons labeled "Hide internal storage" and "More options" in the current screen.

wait_until_activity(d, "Documents")
d(textStartsWith="New folder", resourceIdMatches=".*title").click()
print("Touch on a button that has text 'New folder': SUCCESS")
wait()
wait_until_activity(d, "Documents")
d(textStartsWith="New folder", resourceIdMatches=".*title").click()
print("Touch on a button that has text 'New folder': SUCCESS")
wait()
wait_until_activity(d, "Documents")
d(textStartsWith="New folder", resourceIdMatches=".*title").click()
print("Touch on a button that has text 'New folder': SUCCESS")
wait()
wait_until_activity(d, "Documents")
d(textStartsWith="Hide internal storage", resourceIdMatches=".*title").click()
print("Touch on a button that has text 'Hide internal storage': SUCCESS")
wait()
wait_until_activity(d, "Documents")
go_back_until_inside_app(d)
print("Press the back button 2 times because you stayed on the pages not belonging to the target app for too long: SUCCESS")
wait()
# Expected behaviour: The action of touching the button "Hide internal storage" in the previous screen navigates the user to the "Settings" screen, where they can configure various settings related to the app's functionality, such as picture storage, metadata, sorting, backup, and more. (page changed from Documents to Settings)

wait_until_activity(d, "Settings")
d.click(360, 1069)
print("Touch on a button that has text 'Export database, Store a copy of the current database in a file for[...]': SUCCESS")
wait()
# Expected behaviour: After touching the "Export database" button, the screen has changed from the "Settings" page to the "Documents" page. The "Recent" section is now visible, and there is a focused textfield with the default filename "ActivityDiary_Export.sqlite3" for exporting the database. (page changed from Settings to Documents)

wait_until_activity(d, "Documents")
d(textStartsWith="ActivityDiary_Export.sqlite3", resourceIdMatches=".*title").set_text("ActivityDiary_Backup_JadeGreen.sqlite3")
print("Fill a focused textfield that has text 'ActivityDiary_Export.sqlite3' with 'ActivityDiary_Backup_JadeGreen.sqlite3': SUCCESS")
wait()
# Expected behaviour: The focused textfield that previously had the text "ActivityDiary_Export.sqlite3" now has the updated text "ActivityDiary_Backup_JadeGreen.sqlite3".

wait_until_activity(d, "Documents")
d(descriptionMatches=".*More options").click()
print("Touch on a button that has content_desc 'More options': SUCCESS")
wait()
# Expected behaviour: By touching on the "More options" button, a new button labeled "New folder" and a button labeled "Show internal storage" appeared on the screen, along with a new button. The previous button that had the content description "More options" is no longer present. Additionally, the textview that previously displayed "No items" has been replaced with a focused textfield displaying the text "ActivityDiary_Backup_JadeGreen.sqlite3".

wait_until_activity(d, "Documents")
d(textStartsWith="Show internal storage", resourceIdMatches=".*title").click()
print("Touch on a button that has text 'Show internal storage': SUCCESS")
wait()
# Expected behaviour: After touching the button "Show internal storage", the screen has changed to show additional options like "Show roots" and "More options", as well as a textview indicating that there are no items. Additionally, there is a focused textfield displaying the name "ActivityDiary_Backup_JadeGreen.sqlite3".

wait_until_activity(d, "Documents")
d(descriptionMatches=".*More options").click()
print("Touch on a button that has content_desc 'More options': SUCCESS")
wait()
# Expected behaviour: After touching the "More options" button, a new button labeled "New folder" and two additional buttons are added to the screen, while the "Show roots" button is removed. Additionally, the textview "Recent" is replaced with the textview "No items" and a focused textfield with the text "ActivityDiary_Backup_JadeGreen.sqlite3" is added.

wait_until_activity(d, "Documents")
d(textStartsWith="New folder", resourceIdMatches=".*title").click()
print("Touch on a button that has text 'New folder': SUCCESS")
wait()
wait_until_activity(d, "Documents")
go_back_until_inside_app(d)
print("Press the back button 3 times because you stayed on the pages not belonging to the target app for too long: SUCCESS")
wait()
# Expected behaviour: The action of touching the "New folder" button in the previous screen has taken the user to the "Settings" screen, where they can configure various settings related to the app. (page changed from Documents to Settings)

wait_until_activity(d, "Settings")
d.click(360, 1069)
print("Touch on a button that has text 'Export database, Store a copy of the current database in a file for[...]': SUCCESS")
wait()
# Expected behaviour: After touching the "Export database" button in the Settings screen, the current screen in the Documents section shows a button to show roots, a "Recent" text, a button for more options, and a focused textfield with the name "ActivityDiary_Export.sqlite3" for exporting the database. (page changed from Settings to Documents)

wait_until_activity(d, "Documents")
d(textStartsWith="ActivityDiary_Export.sqlite3", resourceIdMatches=".*title").set_text("ActivityDiary_Backup_JadeGreen.sqlite3")
print("Fill a focused textfield that has text 'ActivityDiary_Export.sqlite3' with 'ActivityDiary_Backup_JadeGreen.sqlite3': SUCCESS")
wait()
# Expected behaviour: The focused textfield in the Documents screen, which previously had the text "ActivityDiary_Export.sqlite3", now has the text "ActivityDiary_Backup_JadeGreen.sqlite3" after filling it with the new text.

"""
37. Save a backup of the activity data in the Activity Diary Debug app.
"""
wait_until_activity(d, "Documents")
d(descriptionMatches=".*Show roots").click()
print("Touch on a button that has content_desc 'Show roots': SUCCESS")
wait()
# Expected behaviour: After touching the "Show roots" button, the current screen shows additional options for saving files, including "Recent" and "Downloads". The available storage space is also displayed for both the internal and external storage.

wait_until_activity(d, "Documents")
d(textStartsWith="Recent", resourceIdMatches=".*title").click()
print("Touch on a button that has text 'Recent': SUCCESS")
wait()
# Expected behaviour: After touching the "Recent" button, the current screen shows additional buttons for "Downloads", "Android SDK built for x86", and "SDCARD" along with their respective free storage space. The "Save to" textview is no longer visible.

wait_until_activity(d, "Documents")
d(textStartsWith="ActivityDiary_Backup_JadeGreen.sqlite3", resourceIdMatches=".*title").click()
print("Touch on a focused textfield that has text 'ActivityDiary_Backup_JadeGreen.sqlite3': SUCCESS")
wait()
wait_until_activity(d, "Documents")
d(descriptionMatches=".*More options").click()
print("Touch on a button that has content_desc 'More options': SUCCESS")
wait()
wait_until_activity(d, "Documents")
go_back_until_inside_app(d)
print("Press the back button 3 times because you stayed on the pages not belonging to the target app for too long: SUCCESS")
wait()
# Expected behaviour: After touching the "More options" button, the screen transitions from the "Documents" page to the "Settings" page. The previous buttons and textviews are replaced with new ones related to settings, such as "Navigate up," "Picture Storage Folder," "Metadata," "Conditions," "Activity sequence," "Activity interruptions," "Activity occurrence," "Daytime," "Backup," and a scrollable area. (page changed from Documents to Settings)

wait_until_activity(d, "Settings")
d.click(360, 1069)
print("Touch on a button that has text 'Export database, Store a copy of the current database in a file for[...]': SUCCESS")
wait()
# Expected behaviour: After touching the "Export database" button in the Settings screen, the current screen in the Documents section shows a focused textfield with the default filename "ActivityDiary_Export.sqlite3" for exporting the current database. (page changed from Settings to Documents)

wait_until_activity(d, "Documents")
d(textStartsWith="ActivityDiary_Export.sqlite3", resourceIdMatches=".*title").set_text("JadeGreen_ActivityDiary_Backup.sqlite3")
print("Fill a focused textfield that has text 'ActivityDiary_Export.sqlite3' with 'JadeGreen_ActivityDiary_Backup.sqlite3': SUCCESS")
wait()
# Expected behaviour: The focused textfield in the Documents screen has been updated from "ActivityDiary_Export.sqlite3" to "JadeGreen_ActivityDiary_Backup.sqlite3".

wait_until_activity(d, "Documents")
d(descriptionMatches=".*More options").click()
print("Touch on a button that has content_desc 'More options': SUCCESS")
wait()
# Expected behaviour: After touching the "More options" button, a new button with the text "New folder" and two additional buttons appear on the screen. The "Show roots" button is removed and replaced with a textview that says "Recent". The screen also shows a textview with the text "No items" and a focused textfield with the text "JadeGreen_ActivityDiary_Backup.sqlite3".

wait_until_activity(d, "Documents")
d.press("back")
print("Press 'BACK' button to navigate back: SUCCESS")
wait()
# Expected behaviour: The "BACK" button was pressed, and the screen changed from the "Documents" page to the "Documents" page. The only visible change is the addition of a focused textfield with the text "JadeGreen_ActivityDiary_Backup.sqlite3".

wait_until_activity(d, "Documents")
d(descriptionMatches=".*More options").click()
print("Touch on a button that has content_desc 'More options': SUCCESS")
wait()
# Expected behaviour: After touching the "More options" button, the previous screen changed to the current screen. The "Show roots" button and the "No items" textview were removed, and new buttons for creating a new folder and hiding internal storage were added.

wait_until_activity(d, "Documents")
d(textStartsWith="New folder", resourceIdMatches=".*title").click()
print("Touch on a button that has text 'New folder': SUCCESS")
wait()
wait_until_activity(d, "Documents")
go_back_until_inside_app(d)
print("Press the back button 3 times because you stayed on the pages not belonging to the target app for too long: SUCCESS")
wait()
# Expected behaviour: The action of touching the "New folder" button has navigated the user from the "Documents" screen to the "Settings" screen, where various settings related to the app's functionality are displayed. (page changed from Documents to Settings)

wait_until_activity(d, "Settings")
d.click(360, 1069)
print("Touch on a button that has text 'Export database, Store a copy of the current database in a file for[...]': SUCCESS")
wait()
# Expected behaviour: The action of touching the "Export database" button in the Settings screen has taken the user to the Documents screen, where there is a focused textfield displaying the file name "ActivityDiary_Export.sqlite3" for exporting the current database. (page changed from Settings to Documents)

wait_until_activity(d, "Documents")
d(descriptionMatches=".*More options").click()
print("Touch on a button that has content_desc 'More options': SUCCESS")
wait()
# Expected behaviour: After touching on the "More options" button, a new button labeled "New folder" and two additional buttons appeared on the screen. Additionally, the previous textview "No items" was replaced with a focused textfield displaying the text "ActivityDiary_Export.sqlite3".

wait_until_activity(d, "Documents")
d(textStartsWith="New folder", resourceIdMatches=".*title").click()
print("Touch on a button that has text 'New folder': SUCCESS")
wait()
"""
38. Create a new folder in the Documents page.
"""
wait_until_activity(d, "Documents")
d(textStartsWith="New folder", resourceIdMatches=".*title").click()
print("Touch on a button that has text 'New folder': SUCCESS")
wait()
wait_until_activity(d, "Documents")
d(textStartsWith="New folder", resourceIdMatches=".*title").click()
print("Touch on a button that has text 'New folder': SUCCESS")
wait()
wait_until_activity(d, "Documents")
d(textStartsWith="New folder", resourceIdMatches=".*title").click()
print("Touch on a button that has text 'New folder': SUCCESS")
wait()
wait_until_activity(d, "Documents")
go_back_until_inside_app(d)
print("Press the back button 3 times because you stayed on the pages not belonging to the target app for too long: SUCCESS")
wait()
# Expected behaviour: By touching the "New folder" button, the screen has changed from the "Documents" screen to the "Settings" screen. The "New folder" button is no longer visible, and there are various new options and settings available in the "Settings" screen. (page changed from Documents to Settings)

wait_until_activity(d, "Settings")
d.press("back")
print("Press 'BACK' button to navigate back: SUCCESS")
wait()
# Expected behaviour: The action of pressing the "BACK" button navigates back from the Settings page to the Main page. The Main page displays a list of activity buttons, tabs for Statistics, Note, and Pictures, and buttons for adding activities, attaching pictures, and editing notes. (page changed from Settings to Main)

wait_until_activity(d, "Main")
d.press("back")
print("Press 'BACK' button to navigate back: SUCCESS")
wait()
wait_until_activity(d, "Main")
d.app_start("de.rampro.activitydiary.debug")
print("Open the app again because the previous action led to closing the app: SUCCESS")
wait()
# Expected behaviour: By pressing the "BACK" button, the selected tab changed from "PICTURES" to "STATISTICS" and additional information such as the time since the activity, a date, and workout duration were displayed. The "detail_content" button and a scrollable area with resource_id "nested_scrollview" were also added.

wait_until_activity(d, "Main")
d(textStartsWith="PICTURES", descriptionMatches=".*Pictures").click()
print("Touch on a tab that has text 'PICTURES': SUCCESS")
wait()
# Expected behaviour: After touching on the "PICTURES" tab, the selected tab changed to "PICTURES" and the previous statistics related information disappeared. Additionally, a popup message briefly appeared and disappeared, showing updated time information.

wait_until_activity(d, "Main")
d.press("back")
print("Press 'BACK' button to navigate back: SUCCESS")
wait()
wait_until_activity(d, "Main")
d.app_start("de.rampro.activitydiary.debug")
print("Open the app again because the previous action led to closing the app: SUCCESS")
wait()
# Expected behaviour: The action of pressing the "BACK" button navigated back to the previous screen. The "STATISTICS" tab is now selected, and there are additional textviews displaying time-related information.

wait_until_activity(d, "Main")
d(textStartsWith="PICTURES", descriptionMatches=".*Pictures").click()
print("Touch on a tab that has text 'PICTURES': SUCCESS")
wait()
# Expected behaviour: The action of touching on the "PICTURES" tab caused the tab to become selected, replacing the previous "STATISTICS" tab. The content in the viewpager also changed, showing buttons for "Gym Workout" and "Jogging" instead of the previous "Relaxing" button. Additionally, some popup messages appeared briefly and then disappeared.

wait_until_activity(d, "Main")
d(resourceIdMatches=".*fab_attach_picture").click()
print("Touch on a button that has resource_id 'fab_attach_picture': SUCCESS")
wait()
# Expected behaviour: After touching the "fab_attach_picture" button, the screen changed from the main page to the camera page. The "fab_attach_picture" button is replaced by a "Shutter button" and additional buttons "More setting controls", "indicator_control", and "btn_cancel" are now visible. (page changed from Main to Camera)

wait_until_activity(d, "Camera")
d.press("back")
print("Press 'BACK' button to navigate back: SUCCESS")
wait()
# Expected behaviour: Navigating back from the Camera screen to the Main screen, the "More setting controls" button, "indicator_control" button, "btn_cancel" button, and "Shutter button" are no longer visible. The Main screen now displays a "Open navigation" button, "Activity Diary Debug" textview, "What are you doing?" textview, "Search" button, "Add Activity" button, "STATISTICS" tab, "NOTE" tab, "PICTURES" tab (selected), a scrollable area with various activity buttons, "select_card_view" button, "fab_attach_picture" button, and "fab_edit_note" button. (page changed from Camera to Main)

wait_until_activity(d, "Main")
d(resourceIdMatches=".*select_card_view").click()
print("Touch on a button that has resource_id 'select_card_view': SUCCESS")
wait()
# Expected behaviour: By touching on the "select_card_view" button, new activity buttons such as "Gym Workout", "Relaxing", "Sleeping", "Study Group", and "Woodworking" are added to the main screen. Additionally, an "UNDO" button is also added.

wait_until_activity(d, "Main")
d.press("back")
print("Press 'BACK' button to navigate back: SUCCESS")
wait()
wait_until_activity(d, "Main")
d.app_start("de.rampro.activitydiary.debug")
print("Open the app again because the previous action led to closing the app: SUCCESS")
wait()
# Expected behaviour: Pressing the "BACK" button navigated back to the previous screen. The "STATISTICS" tab is now selected, and additional textviews and buttons have been added.

wait_until_activity(d, "Main")
d(resourceIdMatches=".*activity_background").click()
print("Touch on a button that has resource_id 'activity_background': SUCCESS")
wait()
# Expected behaviour: After touching the button with resource_id "activity_background", the text views "2023 Week 42: 4' 10''" and "October 2023: 4' 10''" have been updated to "2023 Week 42: 4' 50''", indicating a change in the duration of the activity. Additionally, two new text views with "-" have appeared.

