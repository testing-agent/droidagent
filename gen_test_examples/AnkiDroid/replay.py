
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
        if current_app['package'] == "com.ichi2.anki" and activity_name in current_app['activity']:
            break
        time.sleep(1)
    
    # if the target activity is not launched, raise exception
    current_app = d.app_current()
    if current_app['package'] != "com.ichi2.anki" or activity_name not in current_app['activity']:
        raise Exception(f"Action precondition cannot be satisfied: %s is not launched" % activity_name)

def go_back_until_inside_app(d, max_backtrack=10):
    for i in range(0, max_backtrack):
        current_app = d.app_current()
        if current_app['package'] == "com.ichi2.anki":
            break
        d.press("back")
    
    raise Exception(f"Backtrack failed: com.ichi2.anki is not launched")


avd_serial = sys.argv[1]
d = u2.connect(avd_serial)
assert d.device_info['display']['width'] == 720 and d.device_info['display']['height'] == 1280, "Screen size is different from the original screen size"

d.app_start("com.ichi2.anki")
wait()

"""
1. Synchronize the existing AnkiDroid account with the app.
"""
wait_until_activity(d, "DeckPicker")
d(descriptionMatches=".*Synchronization", resourceIdMatches=".*action_sync").click()
print("Touch on a button that has content_desc 'Synchronization': SUCCESS")
wait()
# Expected behaviour: After touching on the "Synchronization" button, the previous screen displaying deck information is replaced with a screen prompting the user to log in to AnkiWeb for cloud sync service.

wait_until_activity(d, "DeckPicker")
d(textStartsWith="LOG IN", resourceIdMatches=".*md_buttonDefaultPositive").click()
print("Touch on a button that has text 'LOG IN': SUCCESS")
wait()
# Expected behaviour: After touching the "LOG IN" button, the previous screen (DeckPicker) is replaced with the current screen (MyAccount), which contains various widgets such as a "Navigate up" button, textfields for email address and password, a "LOG IN" button, and other informational buttons and textviews related to AnkiWeb account management. (page changed from DeckPicker to MyAccount)

wait_until_activity(d, "MyAccount")
d(textStartsWith="Email address", resourceIdMatches=".*username").set_text("anony1017mous@gmail.com")
print("Fill a focused textfield that has text 'Email address' with 'anony1017mous@gmail.com': SUCCESS")
wait()
# Expected behaviour: The focused textfield with the text "Email address" has been successfully filled with "anony1017mous@gmail.com".

wait_until_activity(d, "MyAccount")
d(textStartsWith="Password", resourceIdMatches=".*password").set_text("green1029*")
print("Fill a password textfield that has text 'Password' with 'green1029*': SUCCESS")
wait()
# Expected behaviour: The password textfield on the MyAccount screen is now focused and the previously displayed text "Password" has been replaced with dots indicating that the password has been entered.

wait_until_activity(d, "MyAccount")
d(textStartsWith="LOG IN", resourceIdMatches=".*login_button").click()
print("Touch on a button that has text 'LOG IN': SUCCESS")
wait()
# Expected behaviour: After touching the "LOG IN" button, the previous "MyAccount" screen has changed to the current "DeckPicker" screen. The previous buttons and text fields related to logging in have been replaced with a textview displaying "Synchronization" and a button showing "Downloading... Up: 0 kB, down: 0 kB". (page changed from MyAccount to DeckPicker)

wait_until_activity(d, "DeckPicker")
wait()
print("Wait for a loading state to finish: SUCCESS")
wait()
# Expected behaviour: The loading state has finished and the DeckPicker screen has been updated. The screen now shows information about the user's deck, including the number of cards due, the number of cards studied, and an option to add new cards.

wait_until_activity(d, "DeckPicker")
d(descriptionMatches=".*Synchronization", resourceIdMatches=".*action_sync").click()
print("Touch on a button that has content_desc 'Synchronization': SUCCESS")
wait()
# Expected behaviour: After touching the "Synchronization" button, a new textview with the text "No changes found" appears on the current screen.

"""
2. Create a new deck and add a few flashcards to it.
"""
wait_until_activity(d, "DeckPicker")
d(descriptionMatches=".*Add", resourceIdMatches=".*fab_expand_menu_button").click()
print("Touch on a button that has content_desc 'Add': SUCCESS")
wait()
# Expected behaviour: The touch on the "Add" button has added a new button with the content description "Add" to the current screen.

wait_until_activity(d, "DeckPicker")
d(descriptionMatches=".*Add", resourceIdMatches=".*fab_expand_menu_button").click()
print("Touch on a button that has content_desc 'Add': SUCCESS")
wait()
# Expected behaviour: The touch on the "Add" button has resulted in the addition of a new button with the content description "Add" to the current screen.

wait_until_activity(d, "DeckPicker")
d(descriptionMatches=".*Add", resourceIdMatches=".*fab_expand_menu_button").click()
print("Touch on a button that has content_desc 'Add': SUCCESS")
wait()
# Expected behaviour: The action of touching the "Add" button on the previous screen has added two new buttons with the content description "Add" on the current screen.

wait_until_activity(d, "DeckPicker")
d(descriptionMatches=".*Create deck", resourceIdMatches=".*add_deck_action").click()
print("Touch on a button that has content_desc 'Create deck': SUCCESS")
wait()
# Expected behaviour: After touching the "Create deck" button, the previous screen updated to the current screen with the addition of a focused textfield and two buttons labeled "CANCEL" and "OK".

wait_until_activity(d, "DeckPicker")
d.click(360, 623)
d.send_keys("My Deck")
print("Fill a focused textfield with 'My Deck': SUCCESS")
wait()
# Expected behaviour: The focused textfield in the DeckPicker screen now contains the text "My Deck" after filling it with the input "My Deck".

wait_until_activity(d, "DeckPicker")
d(textStartsWith="OK", resourceIdMatches=".*md_buttonDefaultPositive").click()
print("Touch on a button that has text 'OK': SUCCESS")
wait()
# Expected behaviour: After touching the "OK" button, the previous screen with a button labeled "OK" is replaced with a new screen that contains various widgets, including a button with the label "Navigate up", a textview with the text "AnkiDroid", and a button with the label "Synchronization".

wait_until_activity(d, "DeckPicker")
d(resourceIdMatches=".*DeckPickerHoriz").click()
print("Touch on a button that has text 'My Deck, 0, 0, 0': SUCCESS")
wait()
# Expected behaviour: After touching the "My Deck" button, the current screen shows a message indicating that the deck is empty and a "HELP" button has been added.

wait_until_activity(d, "DeckPicker")
d(textStartsWith="HELP", resourceIdMatches=".*snackbar_action").click()
print("Touch on a button that has text 'HELP': SUCCESS")
wait()
# Expected behaviour: After touching the "HELP" button, the textview "This deck is empty" is removed from the current screen.

wait_until_activity(d, "DeckPicker")
d(descriptionMatches=".*Add", resourceIdMatches=".*fab_expand_menu_button").click()
print("Touch on a button that has content_desc 'Add': SUCCESS")
wait()
# Expected behaviour: After touching on the "Add" button, a new button with the content description "Add" is added to the current screen.

wait_until_activity(d, "DeckPicker")
d(descriptionMatches=".*Add", resourceIdMatches=".*add_note_action").click()
print("Touch on a button that has content_desc 'Add': SUCCESS")
wait()
# Expected behaviour: After touching the "Add" button, the previous DeckPicker screen is replaced by the NoteEditor screen, where you can input and save a new note with fields for the front and back of the card, multimedia attachments, tags, and card options. (page changed from DeckPicker to NoteEditor)

wait_until_activity(d, "NoteEditor")
d(descriptionMatches=".*Save", resourceIdMatches=".*action_save").click()
print("Touch on a button that has content_desc 'Save': SUCCESS")
wait()
# Expected behaviour: After the action, the following popup message(s) were shown and soon disappeared: {'The first field is empty'}

wait_until_activity(d, "NoteEditor")
d(descriptionMatches=".*Front", resourceIdMatches=".*id_note_editText").set_text("What is the capital city of France?")
print("Fill a focused textfield that has content_desc 'Front' with 'What is the capital city of France?': SUCCESS")
wait()
# Expected behaviour: The focused textfield with content description "Front" has been filled with the text "What is the capital city of France?"

wait_until_activity(d, "NoteEditor")
d(descriptionMatches=".*Back", resourceIdMatches=".*id_note_editText").set_text("Paris")
print("Fill a textfield that has content_desc 'Back' with 'Paris': SUCCESS")
wait()
# Expected behaviour: The user successfully filled the textfield with the content description "Back" with the text "Paris".

"""
3. Create a new flashcard in the "My Deck" deck with the question "What is the capital city of France?" and the answer "Paris".
"""
wait_until_activity(d, "NoteEditor")
d(textStartsWith="What is the capital city of France?", descriptionMatches=".*Front", resourceIdMatches=".*id_note_editText").set_text("What is the capital city of France?")
print("Fill a textfield that has text 'What is the capital city of France?' with 'What is the capital city of France?': SUCCESS")
wait()
# Expected behaviour: The textfield with the initial text "What is the capital city of France?" is now focused and contains the entered text "FranceWhat is the capital city of France?". The textfield for the answer "Paris" remains unchanged.

wait_until_activity(d, "NoteEditor")
d(textStartsWith="Paris", descriptionMatches=".*Back", resourceIdMatches=".*id_note_editText").set_text("Paris")
print("Fill a textfield that has text 'Paris' with 'Paris': SUCCESS")
wait()
# Expected behaviour: The textfield that had the text "Paris" was filled with the text "Paris".

wait_until_activity(d, "NoteEditor")
d(descriptionMatches=".*Save", resourceIdMatches=".*action_save").click()
print("Touch on a button that has content_desc 'Save': SUCCESS")
wait()
# Expected behaviour: After touching the "Save" button, the focused text field for the "Front" of the note remains the same, but the focused text field for the "Back" of the note is now empty. Additionally, a popup message briefly appeared, indicating that 2 cards were added.

wait_until_activity(d, "NoteEditor")
d(textStartsWith="My Deck", resourceIdMatches=".*note_deck_spinner").click()
print("Touch on a dropdown field that has text 'My Deck': SUCCESS")
wait()
# Expected behaviour: The performed action changed the selected option in the dropdown field from "My Deck" to "Default".

wait_until_activity(d, "NoteEditor")
d(textStartsWith="My Deck", resourceIdMatches=".*text1").click()
print("Touch on a checked button that has text 'My Deck': SUCCESS")
wait()
# Expected behaviour: The performed action changed the checked button text to "My Deck" and added several new widgets, including a dropdown field for selecting the deck, a textfield for entering the front and back of the card, and buttons for attaching multimedia content.

wait_until_activity(d, "NoteEditor")
d(descriptionMatches=".*Front", resourceIdMatches=".*id_note_editText").set_text("What is the capital city of France?")
print("Fill a focused textfield that has content_desc 'Front' with 'What is the capital city of France?': SUCCESS")
wait()
# Expected behaviour: The focused textfield with content_desc "Front" has been filled with the text "What is the capital city of France?".

wait_until_activity(d, "NoteEditor")
d(descriptionMatches=".*Back", resourceIdMatches=".*id_note_editText").set_text("Paris")
print("Fill a textfield that has content_desc 'Back' with 'Paris': SUCCESS")
wait()
# Expected behaviour: The user filled the textfield with the content_desc "Back" with the text "Paris", replacing the previous text "What is the capital city of France?".

wait_until_activity(d, "NoteEditor")
d(descriptionMatches=".*Save", resourceIdMatches=".*action_save").click()
print("Touch on a button that has content_desc 'Save': SUCCESS")
wait()
# Expected behaviour: After touching the "Save" button, the popup message "2 cards added" appeared briefly and disappeared. The textfield for the "Front" field is now focused, and the textfield for the "Back" field is no longer focused.

wait_until_activity(d, "NoteEditor")
d(textStartsWith="My Deck", resourceIdMatches=".*note_deck_spinner").click()
print("Touch on a dropdown field that has text 'My Deck': SUCCESS")
wait()
# Expected behaviour: The performed action changed the selected option in the dropdown field from "My Deck" to "Default".

wait_until_activity(d, "NoteEditor")
d(textStartsWith="My Deck", resourceIdMatches=".*text1").click()
print("Touch on a checked button that has text 'My Deck': SUCCESS")
wait()
# Expected behaviour: After touching on the checked button "My Deck", the NoteEditor screen is updated with a dropdown field for selecting the deck, and the selected deck is now "My Deck".

wait_until_activity(d, "NoteEditor")
d(descriptionMatches=".*Save", resourceIdMatches=".*action_save").click()
print("Touch on a button that has content_desc 'Save': SUCCESS")
wait()
# Expected behaviour: After the action, the following popup message(s) were shown and soon disappeared: {'The first field is empty'}

wait_until_activity(d, "NoteEditor")
d(descriptionMatches=".*Save", resourceIdMatches=".*action_save").click()
print("Touch on a button that has content_desc 'Save': SUCCESS")
wait()
# Expected behaviour: After the action, the following popup message(s) were shown and soon disappeared: {'The first field is empty'}

wait_until_activity(d, "NoteEditor")
d(descriptionMatches=".*Save", resourceIdMatches=".*action_save").click()
print("Touch on a button that has content_desc 'Save': SUCCESS")
wait()
# Expected behaviour: After the action, the following popup message(s) were shown and soon disappeared: {'The first field is empty'}

"""
4. Attach a photo to the 'Front' field of the flashcard in the NoteEditor page.
"""
wait_until_activity(d, "NoteEditor")
d(descriptionMatches=".*Attach multimedia content to the Front field", resourceIdMatches=".*id_media_button").click()
print("Touch on a button that has content_desc 'Attach multimedia content to the Front field': SUCCESS")
wait()
# Expected behaviour: After touching on the button with the content description "Attach multimedia content to the Front field", the current screen now includes additional buttons for adding an image, adding an audio clip, recording audio, and accessing the advanced editor.

wait_until_activity(d, "NoteEditor")
d(textStartsWith="Add image").click()
print("Touch on a button that has text 'Add image': SUCCESS")
wait()
# Expected behaviour: After touching the "Add image" button, the previous NoteEditor screen is replaced with the MultimediaEditField screen, which now includes additional options such as adding audio clips, recording audio, and accessing advanced editing features. (page changed from NoteEditor to MultimediaEditField)

wait_until_activity(d, "MultimediaEditField")
d(textStartsWith="GALLERY").click()
print("Touch on a button that has text 'GALLERY': SUCCESS")
wait()
# Expected behaviour: After touching the "GALLERY" button, the previous screen with multimedia editing options is replaced with a new screen showing a list of apps to choose from, with "Photos" and "Gallery" options available. (page changed from MultimediaEditField to Resolver)

wait_until_activity(d, "Resolver")
d.click(359, 1011)
print("Touch on a button that has text 'Photos': SUCCESS")
wait()
# Expected behaviour: After touching on the "Photos" button, two additional buttons with text "JUST ONCE" and "ALWAYS" have appeared on the current screen, along with the existing "Gallery" textview, button, and focused listview.

wait_until_activity(d, "Resolver")
d.click(359, 1011)
print("Touch on a button that has text 'Photos': SUCCESS")
wait()
# Expected behaviour: After touching the "Photos" button, the screen changed to the "ExternalPicker" screen, where there are options to select a photo from different folders, including "Screenshots" and "Pictures". (page changed from Resolver to ExternalPicker)

wait_until_activity(d, "ExternalPicker")
d(textStartsWith="Pictures").click()
print("Touch on a button that has text 'Pictures': SUCCESS")
wait()
# Expected behaviour: After touching the "Pictures" button, the current screen shows a list of photos with their corresponding dates and times, allowing the user to select a photo. (page changed from ExternalPicker to LocalPhotos)

wait_until_activity(d, "LocalPhotos")
d(descriptionMatches=".*Photo taken on Oct 5, 2023 11:27:33 AM.").click()
print("Touch on a button that has content_desc 'Photo taken on Oct 5, 2023 11:27:33 AM.': SUCCESS")
wait()
# Expected behaviour: After touching the button with content description "Photo taken on Oct 5, 2023 11:27:33 AM", the screen has changed from the "LocalPhotos" screen to the "MultimediaEditField" screen. The previous buttons and text have been replaced with new buttons and a textview for editing multimedia content. (page changed from LocalPhotos to MultimediaEditField)

wait_until_activity(d, "MultimediaEditField")
d(descriptionMatches=".*Done", resourceIdMatches=".*multimedia_edit_field_done").click()
print("Touch on a button that has content_desc 'Done': SUCCESS")
wait()
# Expected behaviour: After touching the "Done" button, the previous MultimediaEditField screen is replaced with the current NoteEditor screen. The NoteEditor screen includes options to save the note, select note type and deck, add content to the front and back fields, and manage tags and cards. (page changed from MultimediaEditField to NoteEditor)

"""
5. Review the flashcards in the "My Deck" deck.
"""
wait_until_activity(d, "NoteEditor")
d(descriptionMatches=".*Save", resourceIdMatches=".*action_save").click()
print("Touch on a button that has content_desc 'Save': SUCCESS")
wait()
# Expected behaviour: After touching the "Save" button, the content description of the focused text field changed from "<img src="droidbot_utg.png">" to "Front". Additionally, a popup message briefly appeared and disappeared, indicating that one card was added.

wait_until_activity(d, "NoteEditor")
d(descriptionMatches=".*Navigate up").click()
print("Touch on a button that has content_desc 'Navigate up': SUCCESS")
wait()
# Expected behaviour: The previous NoteEditor screen is replaced by the DeckPicker screen, which shows different widgets such as a textview with the text "AnkiDroid" and buttons with content descriptions "Synchronization" and "More options". (page changed from NoteEditor to DeckPicker)

wait_until_activity(d, "DeckPicker")
d(resourceIdMatches=".*DeckPickerHoriz").click()
print("Touch on a button that has text 'My Deck, 5, 0, 0': SUCCESS")
wait()
# Expected behaviour: The button "My Deck, 5, 0, 0" was touched and the current screen shows the flashcard for the question "What is the capital city of France?" with options to show the answer. (page changed from DeckPicker to Reviewer)

wait_until_activity(d, "Reviewer")
d(textStartsWith="SHOW ANSWER", resourceIdMatches=".*flashcard_layout_flip").click()
print("Touch on a button that has text 'SHOW ANSWER': SUCCESS")
wait()
# Expected behaviour: After touching the "SHOW ANSWER" button, the answer to the flashcard is displayed as a widget with the text "Paris". Additionally, there are several new widgets related to reviewing the flashcard, such as buttons for different levels of ease and corresponding time intervals.

wait_until_activity(d, "Reviewer")
d(resourceIdMatches=".*flashcard_layout_ease1").click()
print("Touch on a button that has text '< 1 min, Again': SUCCESS")
wait()
# Expected behaviour: By touching on the button "< 1 min, Again", the textviews displaying the time left and the ease options have been updated. The time left has changed from "3 minutes" to "4 minutes" and the ease options have been updated to "Hard", "Good", "Easy".

wait_until_activity(d, "Reviewer")
d(textStartsWith="SHOW ANSWER", resourceIdMatches=".*flashcard_layout_flip").click()
print("Touch on a button that has text 'SHOW ANSWER': SUCCESS")
wait()
# Expected behaviour: After touching the "SHOW ANSWER" button, the answer "Paris" is displayed, along with additional options to rate the flashcard difficulty and a countdown timer indicating the time until the flashcard is shown again.

wait_until_activity(d, "Reviewer")
d(resourceIdMatches=".*flashcard_layout_ease1").click()
print("Touch on a button that has text '< 1 min, Again': SUCCESS")
wait()
# Expected behaviour: After touching on the button "< 1 min, Again", the previous textview with the text "< 1 min" has been changed to "3", and the previous button with the text "Again" has been changed to "SHOW ANSWER".

wait_until_activity(d, "Reviewer")
d(textStartsWith="AnkiDroid Flashcard").swipe(left)
print("Scroll left on a focused scrollable area that has text 'AnkiDroid Flashcard, droidbot_utg': SUCCESS")
wait()
wait_until_activity(d, "Reviewer")
d(textStartsWith="SHOW ANSWER", resourceIdMatches=".*flashcard_layout_flip").click()
print("Touch on a button that has text 'SHOW ANSWER': SUCCESS")
wait()
# Expected behaviour: After touching the "SHOW ANSWER" button, the previous button is replaced with a set of buttons labeled with different time intervals and difficulty levels. Additionally, there are new text views displaying the time intervals and difficulty levels.

wait_until_activity(d, "Reviewer")
d(resourceIdMatches=".*flashcard_layout_ease2").click()
print("Touch on a button that has text '< 6 min, Hard': SUCCESS")
wait()
# Expected behaviour: After touching on the button "< 6 min, Hard", the textview that displays the remaining time changed from "3 minutes left" to "2 minutes left". Additionally, the flashcard question changed from "droidbot_utg" to "FranceWhat is the capital city of France?".

wait_until_activity(d, "Reviewer")
d(textStartsWith="SHOW ANSWER", resourceIdMatches=".*flashcard_layout_flip").click()
print("Touch on a button that has text 'SHOW ANSWER': SUCCESS")
wait()
# Expected behaviour: After touching the "SHOW ANSWER" button, the previous button disappears and is replaced by the answer "Paris". Additionally, new widgets such as a textview with the text "< 1 min", a textview with the text "Again", and buttons with resource IDs "flashcard_layout_ease1", "flashcard_layout_ease2", "flashcard_layout_ease3", and "flashcard_layout_ease4" are displayed.

wait_until_activity(d, "Reviewer")
d(resourceIdMatches=".*flashcard_layout_ease3").click()
print("Touch on a button that has text '< 10 min, Good': SUCCESS")
wait()
# Expected behaviour: After touching the button "< 10 min, Good", the text of the button changed to "SHOW ANSWER".

wait_until_activity(d, "Reviewer")
d(textStartsWith="AnkiDroid Flashcard").swipe(down)
print("Scroll down on a focused scrollable area that has text 'AnkiDroid Flashcard, What is the capital city of France?': SUCCESS")
wait()
"""
6. Review the flashcard "What is the capital city of France?" and rate its difficulty.
"""
wait_until_activity(d, "Reviewer")
d(textStartsWith="SHOW ANSWER", resourceIdMatches=".*flashcard_layout_flip").click()
print("Touch on a button that has text 'SHOW ANSWER': SUCCESS")
wait()
# Expected behaviour: After touching the "SHOW ANSWER" button, the answer "Paris" is displayed on the screen along with additional options to rate the flashcard.

wait_until_activity(d, "Reviewer")
d(resourceIdMatches=".*flashcard_layout_ease3").click()
print("Touch on a button that has text '< 10 min, Good': SUCCESS")
wait()
# Expected behaviour: The action of touching on the button "< 10 min, Good" has changed the text of the button to "SHOW ANSWER".

"""
7. Flag the currently reviewed flashcard.
"""
wait_until_activity(d, "Reviewer")
d(descriptionMatches=".*Flag card", resourceIdMatches=".*action_flag").click()
print("Touch on a button that has content_desc 'Flag card': SUCCESS")
wait()
# Expected behaviour: By touching on the "Flag card" button, new flag options have appeared on the current screen, allowing the user to flag the card with different colors.

wait_until_activity(d, "Reviewer")
d(textStartsWith="Red flag").click()
print("Touch on a button that has text 'Red flag': SUCCESS")
wait()
# Expected behaviour: By touching on the "Red flag" button, the previous screen has been replaced with a new screen that includes additional buttons and widgets such as "Navigate up", "My Deck", "2 minutes left", "Undo", "Flag card", "Edit note", "More options", as well as new textviews displaying numbers and a framelayout with a resource_id "touch_layer". The new screen also includes a widget with the text "Paris" and a focused scrollable area with the text "AnkiDroid Flashcard".

"""
8. Edit the note of the current flashcard.
"""
wait_until_activity(d, "Reviewer")
d(descriptionMatches=".*Edit note", resourceIdMatches=".*action_edit").click()
print("Touch on a button that has content_desc 'Edit note': SUCCESS")
wait()
# Expected behaviour: After touching the "Edit note" button, the previous screen with the reviewer's information is replaced with the Note Editor screen, where the user can edit the note's content and save it. (page changed from Reviewer to NoteEditor)

wait_until_activity(d, "NoteEditor")
d(textStartsWith="FranceWhat is the capital city of France?", descriptionMatches=".*Front", resourceIdMatches=".*id_note_editText").click()
print("Touch on a textfield that has text 'FranceWhat is the capital city of France?': SUCCESS")
wait()
# Expected behaviour: The performed action focused on the textfield and updated the text to "FranceWhat is the capital city of France?"

wait_until_activity(d, "NoteEditor")
d(textStartsWith="Paris", descriptionMatches=".*Back", resourceIdMatches=".*id_note_editText").click()
print("Touch on a textfield that has text 'Paris': SUCCESS")
wait()
# Expected behaviour: The performed action focuses on the textfield with the text "Paris" in the NoteEditor screen, allowing the user to edit the content of the textfield.

wait_until_activity(d, "NoteEditor")
d(descriptionMatches=".*Save", resourceIdMatches=".*action_save").click()
print("Touch on a button that has content_desc 'Save': SUCCESS")
wait()
# Expected behaviour: After touching the "Save" button, the previous NoteEditor screen is replaced with the current Reviewer screen, which shows the flashcard "France: What is the capital city of France?" with the answer "Paris" and additional options such as "Undo" and "Flag card". (page changed from NoteEditor to Reviewer)

wait_until_activity(d, "Reviewer")
d.press("back")
print("Press 'BACK' button to navigate back: SUCCESS")
wait()
# Expected behaviour: Navigating back from the "DeckPicker" page to the "Reviewer" page, the following changes are observed: a button with content_desc "Navigate up" is removed, and the textviews and buttons related to deck statistics and options are also removed. (page changed from Reviewer to DeckPicker)

wait_until_activity(d, "DeckPicker")
d(descriptionMatches=".*Synchronization", resourceIdMatches=".*action_sync").click()
print("Touch on a button that has content_desc 'Synchronization': SUCCESS")
wait()
# Expected behaviour: By touching on the "Synchronization" button, the previous screen, which displayed deck information, has been replaced with a screen showing the progress of writing changes into the database.

wait_until_activity(d, "DeckPicker")
d.press("back")
print("Press 'BACK' button to navigate back: SUCCESS")
wait()
wait_until_activity(d, "DeckPicker")
d.app_start("com.ichi2.anki")
print("Open the app again because the previous action led to closing the app: SUCCESS")
wait()
# Expected behaviour: Pressing the "BACK" button navigates back to the previous screen, which displays the "DeckPicker" with different widgets, including a new button for navigation, updated textviews for deck information, and a button to add new cards.

wait_until_activity(d, "DeckPicker")
d(resourceIdMatches=".*DeckPickerHoriz").click()
print("Touch on a button that has text 'My Deck, 2, 3, 0': SUCCESS")
wait()
# Expected behaviour: After touching on the button with text "My Deck, 2, 3, 0", the previous DeckPicker screen is replaced by the current Reviewer screen. The Reviewer screen displays the deck name "My Deck", a timer with "2 minutes left", and buttons to flag the card and edit the note. (page changed from DeckPicker to Reviewer)

wait_until_activity(d, "Reviewer")
d(textStartsWith="AnkiDroid Flashcard").swipe(down)
print("Scroll down on a focused scrollable area that has text 'AnkiDroid Flashcard, Paris': SUCCESS")
wait()
wait_until_activity(d, "Reviewer")
d(descriptionMatches=".*Edit note", resourceIdMatches=".*action_edit").click()
print("Touch on a button that has content_desc 'Edit note': SUCCESS")
wait()
# Expected behaviour: After touching the "Edit note" button, the previous reviewer screen has transitioned to the NoteEditor screen where the "Edit note" button has been replaced with a "Save" button, and new text and input fields for editing the note have been added. (page changed from Reviewer to NoteEditor)

wait_until_activity(d, "NoteEditor")
d(textStartsWith="FranceWhat is the capital city of France?", descriptionMatches=".*Front", resourceIdMatches=".*id_note_editText").click()
print("Touch on a textfield that has text 'FranceWhat is the capital city of France?': SUCCESS")
wait()
# Expected behaviour: The performed action focused on the textfield and updated the text to "FranceWhat is the capital city of France?".

wait_until_activity(d, "NoteEditor")
d(textStartsWith="FranceWhat is the capital city of France?", descriptionMatches=".*Front", resourceIdMatches=".*id_note_editText").set_text("What is the capital city of France?")
print("Fill a focused textfield that has text 'FranceWhat is the capital city of France?' with 'What is the capital city of France?': SUCCESS")
wait()
# Expected behaviour: The focused textfield now has the correct text "What is the capital city of France?" instead of "FranceWhat is the capital city of France?"

wait_until_activity(d, "NoteEditor")
d(descriptionMatches=".*Save", resourceIdMatches=".*action_save").click()
print("Touch on a button that has content_desc 'Save': SUCCESS")
wait()
# Expected behaviour: After touching the "Save" button, the previous NoteEditor screen is replaced with the current Reviewer screen. The Reviewer screen displays the text "My Deck" and "2 minutes left", along with buttons for flagging the card and editing the note. The content of the note, including the front and back fields, is also displayed on the screen. (page changed from NoteEditor to Reviewer)

"""
9. Obtain statistics about the flashcards in the "My Deck" deck.
"""
wait_until_activity(d, "Reviewer")
d(descriptionMatches=".*More options").click()
print("Touch on a button that has content_desc 'More options': SUCCESS")
wait()
# Expected behaviour: After touching on the "More options" button, the screen has changed to show additional buttons such as "Replay audio", "Bury", "Suspend", "Delete note", "Mark note", "Reschedule", "Enable whiteboard", and "Options".

wait_until_activity(d, "Reviewer")
d(textStartsWith="Options").click()
print("Touch on a button that has text 'Options': SUCCESS")
wait()
# Expected behaviour: The touch on the "Options" button has opened a new screen called "DeckOptions" where various options related to the current deck are displayed, such as deck group options, group management, new cards, reviews, lapses, general settings, reminders, and deck description. (page changed from Reviewer to DeckOptions)

wait_until_activity(d, "DeckOptions")
d(textStartsWith="Reviews").click()
print("Touch on a button that has text 'Reviews': SUCCESS")
wait()
# Expected behaviour: After touching the "Reviews" button, the current screen shows additional options related to reviews, such as "Maximum reviews/day" and "Easy bonus".

wait_until_activity(d, "DeckOptions")
d.press("back")
print("Press 'BACK' button to navigate back: SUCCESS")
wait()
# Expected behaviour: Pressing the "BACK" button navigates back to the previous screen, "DeckOptions", which displays options for the user's deck. The previous screen shows various options related to deck settings, while the current screen shows buttons to navigate to different sections of the deck management.

wait_until_activity(d, "DeckOptions")
d(descriptionMatches=".*Navigate up").click()
print("Touch on a button that has content_desc 'Navigate up': SUCCESS")
wait()
# Expected behaviour: After touching the "Navigate up" button, the previous screen "DeckOptions" is replaced by the current screen "Reviewer". The current screen displays the title "My Deck", a countdown timer "2 minutes left", buttons to flag and edit the card, more options, and the flashcard content. (page changed from DeckOptions to Reviewer)

wait_until_activity(d, "Reviewer")
d(descriptionMatches=".*More options").click()
print("Touch on a button that has content_desc 'More options': SUCCESS")
wait()
# Expected behaviour: By touching on the "More options" button, additional options such as "Replay audio," "Bury," "Suspend," "Delete note," "Mark note," "Reschedule," "Enable whiteboard," and "Options" are now available on the screen.

wait_until_activity(d, "Reviewer")
d(textStartsWith="Options").click()
print("Touch on a button that has text 'Options': SUCCESS")
wait()
# Expected behaviour: The touch on the "Options" button opened a new screen called "DeckOptions" where various options for the deck are displayed, including options for group management, new cards, reviews, lapses, reminders, and deck description. (page changed from Reviewer to DeckOptions)

wait_until_activity(d, "DeckOptions")
d.click(360, 260)
print("Touch on a button that has text 'Options group, Default 2 decks use this group': SUCCESS")
wait()
# Expected behaviour: The performed action checked the "Default" button in the "Options group" section of the DeckOptions screen and added a "CANCEL" button.

wait_until_activity(d, "DeckOptions")
d.press("back")
print("Press 'BACK' button to navigate back: SUCCESS")
wait()
# Expected behaviour: Navigating back from the DeckOptions screen takes the user back to the previous screen, where they can continue with their previous actions or navigate to other sections of the app.

wait_until_activity(d, "DeckOptions")
d.press("back")
print("Press 'BACK' button to navigate back: SUCCESS")
wait()
# Expected behaviour: The "BACK" button press navigated the user back from the "DeckOptions" screen to the "Reviewer" screen. The "Reviewer" screen now displays the flashcard with the question "Paris" and the options to flag the card, edit the note, and access more options. (page changed from DeckOptions to Reviewer)

wait_until_activity(d, "Reviewer")
d(descriptionMatches=".*More options").click()
print("Touch on a button that has content_desc 'More options': SUCCESS")
wait()
# Expected behaviour: After touching on the "More options" button, additional options such as "Replay audio", "Bury", "Suspend", "Delete note", "Mark note", "Reschedule", "Enable whiteboard", and "Options" are now visible on the screen.

wait_until_activity(d, "Reviewer")
d(textStartsWith="Options").click()
print("Touch on a button that has text 'Options': SUCCESS")
wait()
# Expected behaviour: After touching the "Options" button, the previous screen is replaced with the "DeckOptions" screen, which displays various options and settings related to the current deck. (page changed from Reviewer to DeckOptions)

wait_until_activity(d, "DeckOptions")
d(descriptionMatches=".*Navigate up").click()
print("Touch on a button that has content_desc 'Navigate up': SUCCESS")
wait()
# Expected behaviour: The action of touching the "Navigate up" button has taken the user from the "DeckOptions" screen to the "Reviewer" screen. The "DeckOptions" screen had options for managing decks, while the "Reviewer" screen displays specific details about a deck, such as the deck name, time remaining, and options for flagging, editing, and more. (page changed from DeckOptions to Reviewer)

"""
10. Create a filtered deck from the "My Deck" deck.
"""
wait_until_activity(d, "Reviewer")
d(descriptionMatches=".*Navigate up").click()
print("Touch on a button that has content_desc 'Navigate up': SUCCESS")
wait()
# Expected behaviour: After touching the "Navigate up" button, the screen has changed to a new page with additional buttons for "Decks", "Card browser", "Statistics", "Settings", "Help", and "Send feedback". There is also a "Night mode" toggle button and information about the current deck and remaining time.

wait_until_activity(d, "Reviewer")
d(textStartsWith="Decks", resourceIdMatches=".*design_menu_item_text").click()
print("Touch on a button that has text 'Decks': SUCCESS")
wait()
# Expected behaviour: After touching the "Decks" button, the screen transitions to the DeckPicker screen, where there are additional buttons for "Card browser", "Statistics", "Settings", "Help", and "Send feedback". The previous "Decks" button is replaced with a textview displaying "AnkiDroid" and a button for synchronization. Additionally, there is a textview indicating the number of cards due and a button for more options. (page changed from Reviewer to DeckPicker)

wait_until_activity(d, "DeckPicker")
d(resourceIdMatches=".*DeckPickerHoriz").click()
print("Touch on a button that has text 'My Deck, 2, 3, 0': SUCCESS")
wait()
# Expected behaviour: After touching the button with the text "My Deck, 2, 3, 0", the screen changed from the DeckPicker to the Reviewer screen. The previous textviews and buttons were replaced with new ones, such as "My Deck", "2 minutes left", "Flag card", and "Edit note". A new widget with the text "droidbot_utg" and a scrollable area with the text "AnkiDroid Flashcard" also appeared. (page changed from DeckPicker to Reviewer)

wait_until_activity(d, "Reviewer")
d(descriptionMatches=".*More options").click()
print("Touch on a button that has content_desc 'More options': SUCCESS")
wait()
# Expected behaviour: After touching the "More options" button, several new buttons and options have appeared on the screen, including options to replay audio, bury card, suspend card, delete note, mark note, reschedule, enable whiteboard, and access additional options.

wait_until_activity(d, "Reviewer")
d.press("back")
print("Press 'BACK' button to navigate back: SUCCESS")
wait()
# Expected behaviour: Pressing the "BACK" button navigated back to the previous screen, where the buttons "Replay audio", "Bury card", "Suspend card", "Delete note", "Mark note", "Reschedule", "Enable whiteboard", and "Options" are no longer visible. Instead, the current screen displays a button with the content description "Navigate up", a textview with the text "My Deck", a textview with the text "2 minutes left", buttons with content descriptions "Flag card", "Edit note", and "More options", as well as several textviews with the texts "2", "3", and "0", and a widget with the text "droidbot_utg". Additionally, a focused scrollable area with the text "AnkiDroid Flashcard" and a button with the text "SHOW ANSWER" are also visible.

wait_until_activity(d, "Reviewer")
d(descriptionMatches=".*Navigate up").click()
print("Touch on a button that has content_desc 'Navigate up': SUCCESS")
wait()
# Expected behaviour: The performed action of touching the "Navigate up" button has taken the user back to the previous screen, where they can see a list of buttons for different options such as "Decks", "Card browser", "Statistics", "Settings", "Help", and "Send feedback". The "Night mode" is displayed with an "OFF" button. The user can also see the "My Deck" textview and a countdown of "2 minutes left".

wait_until_activity(d, "Reviewer")
d(textStartsWith="Decks", resourceIdMatches=".*design_menu_item_text").click()
print("Touch on a button that has text 'Decks': SUCCESS")
wait()
# Expected behaviour: After touching the "Decks" button, the previous screen transitions to the "DeckPicker" screen. The new screen displays information about the user's deck, including the deck name, the number of cards due, a synchronization button, and additional options. (page changed from Reviewer to DeckPicker)

wait_until_activity(d, "DeckPicker")
d(resourceIdMatches=".*DeckPickerHoriz").click()
print("Touch on a button that has text 'My Deck, 2, 3, 0': SUCCESS")
wait()
# Expected behaviour: The performed action has changed the screen from the DeckPicker to the Reviewer screen. The previous buttons for navigating up and synchronizing are replaced with buttons for flagging cards and editing notes. The text "My Deck" is now displayed as a title, and there is a countdown timer showing "2 minutes left". Additionally, there is a new widget displaying the text "droidbot_utg". (page changed from DeckPicker to Reviewer)

wait_until_activity(d, "Reviewer")
d.press("back")
print("Press 'BACK' button to navigate back: SUCCESS")
wait()
# Expected behaviour: Pressing the "BACK" button navigated back to the previous screen, where the "My Deck" textview, "Flag card" button, "Edit note" button, "More options" button, "2 minutes left" textview, "droidbot_utg" widget, and "SHOW ANSWER" button are now visible again. (page changed from Reviewer to DeckPicker)

wait_until_activity(d, "DeckPicker")
d(descriptionMatches=".*More options").click()
print("Touch on a button that has content_desc 'More options': SUCCESS")
wait()
# Expected behaviour: After touching on the button with content description "More options", the previous screen (DeckPicker) is replaced with the current screen (DeckPicker) where additional options are displayed as buttons, such as "Create filtered deck", "Check database", "Check media", etc.

wait_until_activity(d, "DeckPicker")
d(textStartsWith="Create filtered deck").click()
print("Touch on a button that has text 'Create filtered deck': SUCCESS")
wait()
# Expected behaviour: The action of touching the "Create filtered deck" button on the previous screen has opened a new screen where the user can create a deck. The new screen includes a text field for the deck name, as well as "CANCEL" and "CREATE" buttons.

wait_until_activity(d, "DeckPicker")
d(textStartsWith="Filtered Deck 1").set_text("My Filtered Deck")
print("Fill a focused textfield that has text 'Filtered Deck 1' with 'My Filtered Deck': SUCCESS")
wait()
# Expected behaviour: The focused textfield in the DeckPicker screen that previously had the text "Filtered Deck 1" now has the text "My Filtered Deck" after the action.

wait_until_activity(d, "DeckPicker")
d(textStartsWith="CREATE", resourceIdMatches=".*md_buttonDefaultPositive").click()
print("Touch on a button that has text 'CREATE': SUCCESS")
wait()
# Expected behaviour: After touching the "CREATE" button, the previous "DeckPicker" screen is replaced with the "FilteredDeckOptions" screen, which includes various options for creating a filtered deck. (page changed from DeckPicker to FilteredDeckOptions)

"""
11. Change the "Limit to" option for the filtered deck.
"""
wait_until_activity(d, "FilteredDeckOptions")
d.click(360, 277)
print("Touch on a button that has text 'Limit to, 100': SUCCESS")
wait()
# Expected behaviour: The action of touching the button that says "Limit to, 100" has replaced the text view with a focused text field containing "100", and added two buttons with text "CANCEL" and "OK".

wait_until_activity(d, "FilteredDeckOptions")
d(textStartsWith="100", resourceIdMatches=".*edit").set_text("50")
print("Fill a focused textfield that has text '100' with '50': SUCCESS")
wait()
# Expected behaviour: The focused textfield that previously had the text "100" is now updated with the text "50".

wait_until_activity(d, "FilteredDeckOptions")
d(textStartsWith="OK", resourceIdMatches=".*button1").click()
print("Touch on a button that has text 'OK': SUCCESS")
wait()
# Expected behaviour: After touching the "OK" button, the "50" limit is confirmed and there are additional options displayed such as "cards selected by", "Oldest seen first", "Reschedule", "Reschedule cards based on my answers in this deck", "Define custom steps", and checkboxes.

wait_until_activity(d, "FilteredDeckOptions")
d.click(360, 376)
print("Touch on a button that has text 'cards selected by, Oldest seen first': SUCCESS")
wait()
# Expected behaviour: By touching on the button with the text "cards selected by, Oldest seen first", the button is now checked and the previous button with the text "Oldest seen first" is now a checked button, indicating that the sorting option has been selected as "Oldest seen first".

wait_until_activity(d, "FilteredDeckOptions")
d(textStartsWith="CANCEL", resourceIdMatches=".*button2").click()
print("Touch on a button that has text 'CANCEL': SUCCESS")
wait()
# Expected behaviour: The action of touching the "CANCEL" button in the FilteredDeckOptions screen has resulted in the appearance of additional widgets, including a button with the content description "Navigate up," a textview with the text "Options for My Filtered Deck," a button with the text "Search," and various other buttons and textviews related to rescheduling and custom steps.

wait_until_activity(d, "FilteredDeckOptions")
d(descriptionMatches=".*Navigate up").click()
print("Touch on a button that has content_desc 'Navigate up': SUCCESS")
wait()
# Expected behaviour: The button with content description "Navigate up" has been replaced with buttons with content descriptions "Rebuild", "Empty", and "More options". Additionally, new textviews have appeared displaying information about the "My Filtered Deck". (page changed from FilteredDeckOptions to StudyOptions)

"""
12. View all the cards in the "My Filtered Deck" on the CardBrowser page.
"""
wait_until_activity(d, "StudyOptions")
d.press("back")
print("Press 'BACK' button to navigate back: SUCCESS")
wait()
# Expected behaviour: Pressing the "BACK" button navigates back to the previous screen, StudyOptions, where there is a button with the content description "Rebuild" and a button with the content description "Empty". (page changed from StudyOptions to DeckPicker)

wait_until_activity(d, "DeckPicker")
d(resourceIdMatches=".*DeckPickerHoriz").click()
print("Touch on a button that has text 'My Filtered Deck, 2, 3, 0': SUCCESS")
wait()
# Expected behaviour: The performed action has changed the screen from the "DeckPicker" to the "Reviewer" screen. The "My Filtered Deck" is now displayed with the details "2 minutes left" and there are additional buttons for flagging and editing the card. (page changed from DeckPicker to Reviewer)

wait_until_activity(d, "Reviewer")
d(descriptionMatches=".*Navigate up").click()
print("Touch on a button that has content_desc 'Navigate up': SUCCESS")
wait()
# Expected behaviour: After touching on the "Navigate up" button, the previous screen is replaced with a new screen that shows a list of buttons including "Decks," "Card browser," "Statistics," and "Settings" as well as a textview displaying "My Filtered Deck" and "2 minutes left."

wait_until_activity(d, "Reviewer")
d(textStartsWith="Card browser", resourceIdMatches=".*design_menu_item_text").click()
print("Touch on a button that has text 'Card browser': SUCCESS")
wait()
# Expected behaviour: The action of touching on the "Card browser" button has opened the CardBrowser screen, which displays a list of flashcards with their questions and answers. (page changed from Reviewer to CardBrowser)

wait_until_activity(d, "CardBrowser")
d(resourceIdMatches=".*toolbar_spinner").click()
print("Touch on a dropdown field that has text 'My Filtered Deck, 5 cards shown': SUCCESS")
wait()
# Expected behaviour: The performed action on the dropdown field changed the visible buttons in the current screen. The "My Filtered Deck" button became checked while the "All decks", "Default", and "My Deck" buttons became visible.

wait_until_activity(d, "CardBrowser")
d(textStartsWith="My Filtered Deck", resourceIdMatches=".*dropdown_deck_name").click()
print("Touch on a checked button that has text 'My Filtered Deck': SUCCESS")
wait()
# Expected behaviour: The checked button with the text "My Filtered Deck" has been selected. Additionally, new widgets have appeared, including a textview displaying "My Filtered Deck" and a textview showing "5 cards shown".

wait_until_activity(d, "CardBrowser")
d(resourceIdMatches=".*toolbar_spinner").swipe(down)
print("Scroll down on a dropdown field that has text 'My Filtered Deck, 5 cards shown': SUCCESS")
wait()
# Expected behaviour: After scrolling down on the dropdown field, the current screen shows additional buttons for "All decks", "Default", and "My Deck", as well as a checked button for "My Filtered Deck".

wait_until_activity(d, "CardBrowser")
d(textStartsWith="My Filtered Deck", resourceIdMatches=".*dropdown_deck_name").click()
print("Touch on a checked button that has text 'My Filtered Deck': SUCCESS")
wait()
# Expected behaviour: The performed action selected the "My Filtered Deck" button, which caused the screen to update with a new list of cards displayed in the "CardBrowser" screen.

"""
13. Access and view the Statistics of the "My Filtered Deck".
"""
wait_until_activity(d, "CardBrowser")
d(descriptionMatches=".*More options").click()
print("Touch on a button that has content_desc 'More options': SUCCESS")
wait()
# Expected behaviour: After touching the "More options" button, several new buttons have appeared on the current screen, including "Change display order", "Filter marked", "Filter suspended", "Filter by tag", "Preview", and "Select all".

wait_until_activity(d, "CardBrowser")
d(textStartsWith="Change display order").click()
print("Touch on a button that has text 'Change display order': SUCCESS")
wait()
# Expected behaviour: The "Change display order" button has been replaced with a "Choose display order" textview and a series of buttons representing different sorting options.

wait_until_activity(d, "CardBrowser")
d(textStartsWith="Select a field twice to reverse", resourceIdMatches=".*md_content").click()
print("Touch on a button that has text 'Select a field twice to reverse': SUCCESS")
wait()
wait_until_activity(d, "CardBrowser")
d(resourceIdMatches=".*md_control").click()
print("Touch on a checked button that has resource_id 'md_control': SUCCESS")
wait()
# Expected behaviour: The checked button with resource_id "md_control" is touched, causing the listview to become focused. Additionally, several widgets related to card browsing and filtering are added, such as a textview displaying the filtered deck name and the number of cards shown, dropdown fields for selecting question and answer types, and buttons for adding notes, searching, and accessing more options.

wait_until_activity(d, "CardBrowser")
d(descriptionMatches=".*Navigate up").click()
print("Touch on a button that has content_desc 'Navigate up': SUCCESS")
wait()
# Expected behaviour: After touching the "Navigate up" button, the current screen shows additional buttons for "Decks", "Card browser", "Statistics", "Settings", "Help", and "Send feedback", as well as a textview displaying "My Filtered Deck" and "5 cards shown".

wait_until_activity(d, "CardBrowser")
d(textStartsWith="Statistics", resourceIdMatches=".*design_menu_item_text").click()
print("Touch on a button that has text 'Statistics': SUCCESS")
wait()
# Expected behaviour: The action of touching the "Statistics" button has transitioned the previous screen (CardBrowser) to the current screen (Statistics), which displays various statistics and metrics related to card studying. (page changed from CardBrowser to Statistics)

wait_until_activity(d, "Statistics")
d(resourceIdMatches=".*toolbar_spinner").click()
print("Touch on a dropdown field that has text 'My Filtered Deck, Statistics': SUCCESS")
wait()
# Expected behaviour: The dropdown field was touched and the selected option changed from "My Deck" to "My Filtered Deck".

wait_until_activity(d, "Statistics")
d(textStartsWith="My Filtered Deck", resourceIdMatches=".*dropdown_deck_name").click()
print("Touch on a checked button that has text 'My Filtered Deck': SUCCESS")
wait()
# Expected behaviour: After touching the checked button "My Filtered Deck", the previous screen with buttons for different decks is replaced by a new screen displaying statistics related to the "My Filtered Deck" deck. The new screen includes various widgets such as textviews, buttons, and scrollable areas with information about the deck's statistics and performance.

"""
14. Modify the 'New Card Position' setting in the Preferences page.
"""
wait_until_activity(d, "Statistics")
d(descriptionMatches=".*Navigate up").click()
print("Touch on a button that has content_desc 'Navigate up': SUCCESS")
wait()
# Expected behaviour: After touching the "Navigate up" button, the screen changes to the "Statistics" page, which includes various buttons and a textview displaying the title "My Filtered Deck" and "Statistics".

wait_until_activity(d, "Statistics")
d(textStartsWith="Settings").click()
print("Touch on a button that has text 'Settings': SUCCESS")
wait()
# Expected behaviour: The action of touching the "Settings" button has brought the user to a new screen called "Preferences". The previous screen, "Statistics", has been replaced by a screen with various preferences related to the app. (page changed from Statistics to Preferences)

wait_until_activity(d, "Preferences")
d.click(360, 143)
print("Touch on a button that has text 'AnkiDroid, General settings': SUCCESS")
wait()
# Expected behaviour: After touching the button "AnkiDroid, General settings", the "Preferences" screen is updated to include new options such as "AnkiWeb account", "Fetch media on sync", "Automatic synchronization", "Deck for new cards", "Language", "Share feature usage", "Error reporting mode", "Notify when", "Vibrate", and "Blink light".

wait_until_activity(d, "Preferences")
d(resourceIdMatches=".*list").swipe(down)
print("Scroll down on a focused scrollable area that has text 'AnkiWeb account, anony1017mous@gmail.com, Fetch media on sync, Automatically fetch missing media when syncing, Automatic synchronization, Sync automatically on app start/exit if the last s[...], Deck for new cards, Use current deck, Language, System language, Share feature usage, You can contribute to AnkiDroid by helping the dev[...], Error reporting mode, Never report, Notify when, Pending messages available, Vibrate, Blink light': SUCCESS")
wait()
wait_until_activity(d, "Preferences")
d(resourceIdMatches=".*list").swipe(down)
print("Scroll down on a focused scrollable area that has text 'AnkiWeb account, anony1017mous@gmail.com, Fetch media on sync, Automatically fetch missing media when syncing, Automatic synchronization, Sync automatically on app start/exit if the last s[...], Deck for new cards, Use current deck, Language, System language, Share feature usage, You can contribute to AnkiDroid by helping the dev[...], Error reporting mode, Never report, Notify when, Pending messages available, Vibrate, Blink light': SUCCESS")
wait()
wait_until_activity(d, "Preferences")
d(resourceIdMatches=".*list").swipe(down)
print("Scroll down on a focused scrollable area that has text 'AnkiWeb account, anony1017mous@gmail.com, Fetch media on sync, Automatically fetch missing media when syncing, Automatic synchronization, Sync automatically on app start/exit if the last s[...], Deck for new cards, Use current deck, Language, System language, Share feature usage, You can contribute to AnkiDroid by helping the dev[...], Error reporting mode, Never report, Notify when, Pending messages available, Vibrate, Blink light': SUCCESS")
wait()
wait_until_activity(d, "Preferences")
d(resourceIdMatches=".*list").swipe(down)
print("Scroll down on a focused scrollable area that has text 'AnkiWeb account, anony1017mous@gmail.com, Fetch media on sync, Automatically fetch missing media when syncing, Automatic synchronization, Sync automatically on app start/exit if the last s[...], Deck for new cards, Use current deck, Language, System language, Share feature usage, You can contribute to AnkiDroid by helping the dev[...], Error reporting mode, Never report, Notify when, Pending messages available, Vibrate, Blink light': SUCCESS")
wait()
wait_until_activity(d, "Preferences")
d(resourceIdMatches=".*list").swipe(down)
print("Scroll down on a focused scrollable area that has text 'AnkiWeb account, anony1017mous@gmail.com, Fetch media on sync, Automatically fetch missing media when syncing, Automatic synchronization, Sync automatically on app start/exit if the last s[...], Deck for new cards, Use current deck, Language, System language, Share feature usage, You can contribute to AnkiDroid by helping the dev[...], Error reporting mode, Never report, Notify when, Pending messages available, Vibrate, Blink light': SUCCESS")
wait()
wait_until_activity(d, "Preferences")
d(resourceIdMatches=".*list").swipe(down)
print("Scroll down on a focused scrollable area that has text 'AnkiWeb account, anony1017mous@gmail.com, Fetch media on sync, Automatically fetch missing media when syncing, Automatic synchronization, Sync automatically on app start/exit if the last s[...], Deck for new cards, Use current deck, Language, System language, Share feature usage, You can contribute to AnkiDroid by helping the dev[...], Error reporting mode, Never report, Notify when, Pending messages available, Vibrate, Blink light': SUCCESS")
wait()
wait_until_activity(d, "Preferences")
d.click(360, 555)
print("Touch on a button that has text 'Deck for new cards, Use current deck': SUCCESS")
wait()
# Expected behaviour: After touching the button with the text "Deck for new cards, Use current deck", the button's text is changed to "Use current deck" and a new button with the text "Decide by note type" is added. Additionally, a button with the text "CANCEL" is also visible on the current screen.

wait_until_activity(d, "Preferences")
d(textStartsWith="Decide by note type", resourceIdMatches=".*text1").click()
print("Touch on a button that has text 'Decide by note type': SUCCESS")
wait()
# Expected behaviour: By touching on the button "Decide by note type", the screen has not changed significantly. However, the textview "Decide by note type" is now focused in a scrollable area.

wait_until_activity(d, "Preferences")
d.click(360, 555)
print("Touch on a button that has text 'Deck for new cards, Decide by note type': SUCCESS")
wait()
# Expected behaviour: After touching the button with text "Deck for new cards, Decide by note type", the "Decide by note type" option is selected and the "Use current deck" option is unselected. Additionally, a "CANCEL" button is now visible.

wait_until_activity(d, "Preferences")
d.press("back")
print("Press 'BACK' button to navigate back: SUCCESS")
wait()
# Expected behaviour: Pressing the "BACK" button navigates back to the previous screen, which is the Preferences screen. There are no visible changes in the widgets between the previous and current screens.

"""
15. Modify the fields of a note type using the ModelFieldEditor page.
"""
wait_until_activity(d, "DeckPicker")
d(descriptionMatches=".*More options").click()
print("Touch on a button that has content_desc 'More options': SUCCESS")
wait()
# Expected behaviour: After touching the "More options" button, the previous screen "DeckPicker" has been changed to the current screen "DeckPicker" with additional buttons such as "Create filtered deck", "Check database", "Check media", "Empty cards", "Restore from backup", "Manage note types", "Import", and "Export collection".

wait_until_activity(d, "DeckPicker")
d(textStartsWith="Manage note types").click()
print("Touch on a button that has text 'Manage note types': SUCCESS")
wait()
# Expected behaviour: After touching the "Manage note types" button, the current screen now displays a list of available note types, along with options to add new note types and the number of notes associated with each type. (page changed from DeckPicker to ModelBrowser)

wait_until_activity(d, "ModelBrowser")
d.click(360, 143)
print("Touch on a button that has text 'Basic, 0 notes': SUCCESS")
wait()
# Expected behaviour: After touching on the button with the text "Basic, 0 notes", the screen changed from the ModelBrowser to the ModelFieldEditor. The previous textviews related to note types and notes have been replaced with new textviews related to editing fields, and new buttons for adding fields are now visible. (page changed from ModelBrowser to ModelFieldEditor)

wait_until_activity(d, "ModelFieldEditor")
d(textStartsWith="Front", resourceIdMatches=".*model_editor_list_display").click()
print("Touch on a button that has text 'Front': SUCCESS")
wait()
# Expected behaviour: After touching the "Front" button, the previous button with the text "Front" has been replaced with a textview that now displays "Front" on the current screen. Additionally, new buttons with the options to reposition, sort, rename, and delete the field have been added.

wait_until_activity(d, "ModelFieldEditor")
d(textStartsWith="Reposition field").click()
print("Touch on a button that has text 'Reposition field': SUCCESS")
wait()
# Expected behaviour: By touching the "Reposition field" button, the previous screen with the button and other options is replaced with a new screen where the button is replaced with a text field for entering a value, along with "CANCEL" and "OK" buttons.

wait_until_activity(d, "ModelFieldEditor")
d.click(360, 639)
d.send_keys("1")
print("Fill a focused textfield with '1': SUCCESS")
wait()
# Expected behaviour: The focused textfield in the ModelFieldEditor screen now contains the value "1" that was entered by the user.

wait_until_activity(d, "ModelFieldEditor")
d(textStartsWith="OK", resourceIdMatches=".*md_buttonDefaultPositive").click()
print("Touch on a button that has text 'OK': SUCCESS")
wait()
# Expected behaviour: After touching the "OK" button, the previous screen with a text field and instructions is replaced by a new screen with the app's name "AnkiDroid" and a confirmation message with "CANCEL" and "OK" buttons.

wait_until_activity(d, "ModelFieldEditor")
d(textStartsWith="OK", resourceIdMatches=".*md_buttonDefaultPositive").click()
print("Touch on a button that has text 'OK': SUCCESS")
wait()
# Expected behaviour: After touching the "OK" button, the previous screen with a button for canceling the action and a textview with information about uploading the database has been replaced with a new screen that has buttons for navigating and adding fields for editing.

wait_until_activity(d, "ModelFieldEditor")
d(textStartsWith="Back", resourceIdMatches=".*model_editor_list_display").click()
print("Touch on a button that has text 'Back': SUCCESS")
wait()
# Expected behaviour: The action of touching the "Back" button has changed the previous screen from a field editor with navigation buttons to a field editor with additional options for repositioning, sorting, renaming, and deleting fields.

"""
16. Create a new card template in the CardTemplateEditor page.
"""
wait_until_activity(d, "Preferences")
d(descriptionMatches=".*Navigate up").click()
print("Touch on a button that has content_desc 'Navigate up': SUCCESS")
wait()
# Expected behaviour: After touching the "Navigate up" button, the screen changes to the Preferences screen, which includes various settings options such as General settings, Reviewing, Appearance, Gestures, and Advanced.

wait_until_activity(d, "Preferences")
d.click(360, 431)
print("Touch on a button that has text 'Advanced, Optimization and experimental features': SUCCESS")
wait()
# Expected behaviour: By touching on the button "Advanced, Optimization and experimental features", the screen has changed to the "Advanced" section in the Preferences menu, displaying various advanced settings and options such as AnkiDroid directory, force full sync, custom sync server, gestures, and more.

wait_until_activity(d, "Preferences")
d(resourceIdMatches=".*list").swipe(down)
print("Scroll down on a focused scrollable area that has text 'AnkiDroid directory, /storage/emulated/0/AnkiDroid, Force full sync, On next sync, force changes in one direction, Custom sync server, Disabled, Max number of backups, 8, Safe display mode, Disable all animations and use safer method for dr[...], Type answer into the card, Use a text input box inside the card to type in th[...], Disable Single-Field Edit Mode, Allows 'Cloze Deletion' context menu when in lands[...], Enable AnkiDroid API, Let other apps connect to AnkiDroid and read / wri[...], Third-party API apps, See a list of applications which make use of the A[...]': SUCCESS")
wait()
# Expected behaviour: After scrolling down on the Preferences screen, the text "AnkiDroid directory" and its corresponding path "/storage/emulated/0/AnkiDroid" are no longer visible, but new options such as "Reads out question and answer if no sound file is included" and "Lookup dictionary" have appeared.

wait_until_activity(d, "Preferences")
d(resourceIdMatches=".*list").swipe(down)
print("Scroll down on a focused scrollable area that has text 'Reads out question and answer if no sound file is [...], Lookup dictionary, None, Reset languages, Reset language assignments (for text to speech and[...], Chess notation support, Draw chessboard from ForsythEdwards Notation. The[...], Advanced statistics, Disabled, HTML / Javascript Debugging, Enable remote WebView connections, and save card H[...], Experimental V2 scheduler, Enable the experimental scheduler. Forces changes [...], About AnkiDroid, Version: 2.10beta3, Trigger test crash, Touch here for an immediate test crash, Switch Analytics to dev mode, Touch here to use Analytics dev tag and 100% sampl[...], Lock Database, Touch here to lock the database (all threads block[...]': SUCCESS")
wait()
wait_until_activity(d, "Preferences")
d(descriptionMatches=".*Navigate up").click()
print("Touch on a button that has content_desc 'Navigate up': SUCCESS")
wait()
# Expected behaviour: After touching the "Navigate up" button, the screen transitioned to the "Preferences" screen. The "Preferences" screen now displays various settings options such as "General settings," "Reviewing," "Appearance," "Gestures," and more.

wait_until_activity(d, "Preferences")
d.click(360, 143)
print("Touch on a button that has text 'AnkiDroid, General settings': SUCCESS")
wait()
# Expected behaviour: After touching the button with the text "AnkiDroid, General settings," the current screen shows additional options such as "AnkiWeb account," "Fetch media on sync," "Automatic synchronization," "Deck for new cards," "Language," "Share feature usage," "Error reporting mode," "Notify when," "Vibrate," and "Blink light." Additionally, a focused scrollable area is present.

wait_until_activity(d, "Preferences")
d(descriptionMatches=".*Navigate up").click()
print("Touch on a button that has content_desc 'Navigate up': SUCCESS")
wait()
# Expected behaviour: By touching on the "Navigate up" button, the screen has changed to the "Preferences" page, where various settings options are displayed such as "General settings," "Reviewing," "Appearance," "Gestures," "Advanced," and more.

wait_until_activity(d, "Preferences")
d.press("back")
print("Press 'BACK' button to navigate back: SUCCESS")
wait()
# Expected behaviour: The action of pressing the "BACK" button navigated the user back from the "Preferences" screen to the "Statistics" screen. The "Preferences" screen with various settings and options has been replaced by the "Statistics" screen, which displays statistics and information about the user's study progress. (page changed from Preferences to Statistics)

wait_until_activity(d, "Statistics")
d(descriptionMatches=".*Navigate up").click()
print("Touch on a button that has content_desc 'Navigate up': SUCCESS")
wait()
# Expected behaviour: The action of touching the "Navigate up" button has taken the user from the "Statistics" screen to a new screen that displays a filtered deck's statistics.

wait_until_activity(d, "Statistics")
d(descriptionMatches=".*Navigate up").click()
print("Touch on a button that has content_desc 'Navigate up': SUCCESS")
wait()
wait_until_activity(d, "Statistics")
d(textStartsWith="Decks", resourceIdMatches=".*design_menu_item_text").click()
print("Touch on a button that has text 'Decks': SUCCESS")
wait()
# Expected behaviour: After touching the "Decks" button, the current screen shows additional information about the user's deck, including the number of cards studied and the time taken to study them. (page changed from Statistics to DeckPicker)

wait_until_activity(d, "DeckPicker")
d.press("back")
print("Press 'BACK' button to navigate back: SUCCESS")
wait()
wait_until_activity(d, "DeckPicker")
d.app_start("com.ichi2.anki")
print("Open the app again because the previous action led to closing the app: SUCCESS")
wait()
wait_until_activity(d, "DeckPicker")
d(resourceIdMatches=".*DeckPickerHoriz").click()
print("Touch on a button that has text 'My Deck, 0, 0, 0': SUCCESS")
wait()
# Expected behaviour: After touching the button "My Deck, 0, 0, 0", the current screen shows that the deck is empty with a message "This deck is empty" and a button "HELP" is added.

"""
17. Rename a field in the note type.
"""
wait_until_activity(d, "ModelFieldEditor")
d(textStartsWith="Rename field").click()
print("Touch on a button that has text 'Rename field': SUCCESS")
wait()
# Expected behaviour: The action of touching on the "Rename field" button has opened a new screen called "Rename note type" with a focused textfield for renaming, along with buttons for canceling and confirming the rename.

wait_until_activity(d, "ModelFieldEditor")
d(textStartsWith="Back").set_text("NewField")
print("Fill a focused textfield that has text 'Back' with 'NewField': SUCCESS")
wait()
# Expected behaviour: The focused textfield in the ModelFieldEditor screen that previously had the text "Back" has now been filled with the text "NewField".

wait_until_activity(d, "ModelFieldEditor")
d(textStartsWith="RENAME", resourceIdMatches=".*md_buttonDefaultPositive").click()
print("Touch on a button that has text 'RENAME': SUCCESS")
wait()
# Expected behaviour: The action of touching the "RENAME" button has caused the previous screen, which displayed a field editor for renaming a note type, to transition to a new screen titled "Edit fields" with additional buttons for adding new fields.

"""
18. Create a new field in the note type using the ModelFieldEditor page.
"""
wait_until_activity(d, "ModelFieldEditor")
d(descriptionMatches=".*Add field", resourceIdMatches=".*action_add_new_model").click()
print("Touch on a button that has content_desc 'Add field': SUCCESS")
wait()
# Expected behaviour: After touching the "Add field" button, the previous screen is replaced with a new screen that allows the user to add a new field. The new screen includes a focused textfield and buttons for canceling or confirming the action.

wait_until_activity(d, "ModelFieldEditor")
d.click(360, 623)
d.send_keys("Field1")
print("Fill a focused textfield with 'Field1': SUCCESS")
wait()
# Expected behaviour: The focused textfield on the ModelFieldEditor screen is now filled with the text "Field1".

wait_until_activity(d, "ModelFieldEditor")
d(textStartsWith="OK", resourceIdMatches=".*md_buttonDefaultPositive").click()
print("Touch on a button that has text 'OK': SUCCESS")
wait()
# Expected behaviour: The action of touching the "OK" button has transitioned the user from the previous "ModelFieldEditor" screen to the current "ModelFieldEditor" screen, where additional buttons and textviews related to editing fields are now visible.

wait_until_activity(d, "ModelFieldEditor")
d(textStartsWith="NewField", resourceIdMatches=".*model_editor_list_display").click()
print("Touch on a button that has text 'NewField': SUCCESS")
wait()
# Expected behaviour: The action of touching the "NewField" button in the previous screen has resulted in the appearance of additional buttons in the current screen, such as "Reposition field", "Sort by this field", "Rename field", and "Delete field", as well as a new text view displaying "NewField".

wait_until_activity(d, "ModelFieldEditor")
d(textStartsWith="Rename field").click()
print("Touch on a button that has text 'Rename field': SUCCESS")
wait()
# Expected behaviour: The performed action opens a screen for renaming a field. The previous screen displayed a button with the text "Rename field", while the current screen shows a text field for entering a new field name, along with buttons for canceling or renaming the field.

wait_until_activity(d, "ModelFieldEditor")
d(textStartsWith="NewField").set_text("CustomField")
print("Fill a focused textfield that has text 'NewField' with 'CustomField': SUCCESS")
wait()
# Expected behaviour: The focused textfield with the text "NewField" has been updated to have the text "CustomField".

wait_until_activity(d, "ModelFieldEditor")
d(textStartsWith="RENAME", resourceIdMatches=".*md_buttonDefaultPositive").click()
print("Touch on a button that has text 'RENAME': SUCCESS")
wait()
# Expected behaviour: After touching the "RENAME" button, the previous screen is replaced with a new screen that shows options to edit fields, including buttons for adding fields and selecting different field types.

wait_until_activity(d, "ModelFieldEditor")
d(descriptionMatches=".*Add field", resourceIdMatches=".*action_add_new_model").click()
print("Touch on a button that has content_desc 'Add field': SUCCESS")
wait()
# Expected behaviour: The touch on the "Add field" button in the ModelFieldEditor screen resulted in the appearance of a new screen with a focused textfield, along with the addition of "CANCEL" and "OK" buttons.

wait_until_activity(d, "ModelFieldEditor")
d(textStartsWith="OK", resourceIdMatches=".*md_buttonDefaultPositive").click()
print("Touch on a button that has text 'OK': SUCCESS")
wait()
# Expected behaviour: After touching the "OK" button, the previous screen is replaced with a new screen that shows a different layout. The new screen displays options to edit fields and add different types of fields. Additionally, a popup message briefly appears and disappears, stating that a name must be entered.

wait_until_activity(d, "ModelFieldEditor")
d(textStartsWith="Field1", resourceIdMatches=".*model_editor_list_display").click()
print("Touch on a button that has text 'Field1': SUCCESS")
wait()
# Expected behaviour: By touching on the button with text "Field1", the previous screen has been updated to show options to reposition, sort, rename, and delete the field.

wait_until_activity(d, "ModelFieldEditor")
d.press("back")
print("Press 'BACK' button to navigate back: SUCCESS")
wait()
# Expected behaviour: Pressing the "BACK" button navigated back to the previous screen, where the "ModelFieldEditor" view was displayed with the options to reposition, sort, rename, and delete fields.

wait_until_activity(d, "ModelFieldEditor")
d(textStartsWith="Field1", resourceIdMatches=".*model_editor_list_display").click()
print("Touch on a button that has text 'Field1': SUCCESS")
wait()
# Expected behaviour: After touching the button with text "Field1", the button has been replaced with a textview displaying "Field1" and additional buttons for repositioning, sorting, renaming, and deleting the field have appeared.

wait_until_activity(d, "ModelFieldEditor")
d(textStartsWith="Reposition field").click()
print("Touch on a button that has text 'Reposition field': SUCCESS")
wait()
# Expected behaviour: After touching on the "Reposition field" button, the screen has changed to a new page where there is a text field with a prompt to enter a value between 1 and 3, along with buttons for "CANCEL" and "OK".

"""
19. Reposition a field in a note type on the ModelFieldEditor page.
"""
wait_until_activity(d, "ModelFieldEditor")
d.click(360, 639)
d.send_keys("2")
print("Fill a focused textfield with '2': SUCCESS")
wait()
# Expected behaviour: The focused textfield in the ModelFieldEditor screen now contains the text "2" that was entered by the user.

wait_until_activity(d, "ModelFieldEditor")
d(textStartsWith="OK", resourceIdMatches=".*md_buttonDefaultPositive").click()
print("Touch on a button that has text 'OK': SUCCESS")
wait()
# Expected behaviour: The performed action of touching the "OK" button resulted in a change of the previous screen to the current screen, where the previous widgets related to field editing were replaced with new widgets related to field navigation and editing options.

wait_until_activity(d, "ModelFieldEditor")
d(textStartsWith="Field1", resourceIdMatches=".*model_editor_list_display").click()
print("Touch on a button that has text 'Field1': SUCCESS")
wait()
# Expected behaviour: After touching on the button with the text "Field1", the previous screen transformed to the current screen where the button with the text "Field1" was replaced by a textview with the text "Field1". Additionally, new buttons labeled "Reposition field", "Sort by this field", "Rename field", "Delete field", and "Remember last input when adding" were added.

"""
20. Sort flashcards by a specific field in the "My Deck" deck.
"""
wait_until_activity(d, "ModelFieldEditor")
d(textStartsWith="Sort by this field").click()
print("Touch on a button that has text 'Sort by this field': SUCCESS")
wait()
# Expected behaviour: The action of touching the "Sort by this field" button on the previous screen has navigated the user to a new screen where they can edit and manage fields. The current screen displays options to add, edit, and delete fields, as well as options to sort and reposition fields.

wait_until_activity(d, "ModelFieldEditor")
d(textStartsWith="Front", resourceIdMatches=".*model_editor_list_display").click()
print("Touch on a button that has text 'Front': SUCCESS")
wait()
# Expected behaviour: After touching on the "Front" button, the previous screen is replaced with a new screen called "ModelFieldEditor" where the button with text "Front" is now a textview with the text "Front". Additionally, there are new buttons available for repositioning, sorting, renaming, and deleting the field, as well as an option to remember the last input when adding a field.

wait_until_activity(d, "ModelFieldEditor")
d(textStartsWith="Sort by this field").click()
print("Touch on a button that has text 'Sort by this field': SUCCESS")
wait()
# Expected behaviour: The action of touching the "Sort by this field" button has changed the previous screen to the current screen, where the button "Sort by this field" is replaced by a button with content description "Navigate up" and additional buttons for adding and editing fields.

wait_until_activity(d, "ModelFieldEditor")
d(descriptionMatches=".*Navigate up").click()
print("Touch on a button that has content_desc 'Navigate up': SUCCESS")
wait()
# Expected behaviour: By touching on the "Navigate up" button, the previous screen (ModelFieldEditor) has changed to the current screen (ModelBrowser), where there are new options for managing note types, including the ability to add new note types and view existing notes. (page changed from ModelFieldEditor to ModelBrowser)

wait_until_activity(d, "ModelBrowser")
d.press("back")
print("Press 'BACK' button to navigate back: SUCCESS")
wait()
# Expected behaviour: Pressing the "BACK" button navigates back to the previous screen (ModelBrowser) from the current screen (DeckPicker), where the previous screen displays a button with the content description "Navigate up" and various text views related to note types, while the current screen displays a button for synchronization, more options, and different deck information. (page changed from ModelBrowser to DeckPicker)

wait_until_activity(d, "DeckPicker")
d(resourceIdMatches=".*DeckPickerHoriz").click()
print("Touch on a button that has text 'My Deck, 0, 0, 0': SUCCESS")
wait()
# Expected behaviour: After touching the button "My Deck, 0, 0, 0", the current screen shows a message "This deck is empty" and a button "HELP" has been added.

wait_until_activity(d, "DeckPicker")
d(textStartsWith="HELP", resourceIdMatches=".*snackbar_action").click()
print("Touch on a button that has text 'HELP': SUCCESS")
wait()
# Expected behaviour: After touching the "HELP" button, the textview "This deck is empty" is no longer visible on the current screen.

wait_until_activity(d, "DeckPicker")
d(descriptionMatches=".*Add", resourceIdMatches=".*fab_expand_menu_button").click()
print("Touch on a button that has content_desc 'Add': SUCCESS")
wait()
# Expected behaviour: After touching the "Add" button, a new button with the same content description "Add" is added to the current screen.

wait_until_activity(d, "DeckPicker")
d(resourceIdMatches=".*DeckPickerHoriz").click()
print("Touch on a button that has text 'My Deck, 0, 0, 0': SUCCESS")
wait()
# Expected behaviour: After touching the button with the text "My Deck, 0, 0, 0", the previous screen is replaced with a current screen where the text "This deck is empty" is displayed instead of the options to create or get shared decks.

wait_until_activity(d, "DeckPicker")
d(descriptionMatches=".*Add", resourceIdMatches=".*fab_expand_menu_button").click()
print("Touch on a button that has content_desc 'Add': SUCCESS")
wait()
# Expected behaviour: After touching the "Add" button, a new button with the content description "Add" has been added to the current screen.

wait_until_activity(d, "DeckPicker")
d(resourceIdMatches=".*DeckPickerHoriz").click()
print("Touch on a button that has text 'My Deck, 0, 0, 0': SUCCESS")
wait()
# Expected behaviour: After touching on the "My Deck" button, the previous screen's "Create deck" and "Get shared decks" options are replaced with a message indicating that the deck is empty and a "HELP" button.

wait_until_activity(d, "DeckPicker")
d(descriptionMatches=".*Add", resourceIdMatches=".*fab_expand_menu_button").click()
print("Touch on a button that has content_desc 'Add': SUCCESS")
wait()
# Expected behaviour: After touching the "Add" button, a new button with the content description "Add" has appeared on the current screen.

wait_until_activity(d, "DeckPicker")
d(resourceIdMatches=".*DeckPickerHoriz").click()
print("Touch on a button that has text 'My Deck, 0, 0, 0': SUCCESS")
wait()
# Expected behaviour: After touching the button with the text "My Deck, 0, 0, 0", the previous screen is replaced with a new screen in which the "Create deck" and "Get shared decks" options are no longer available, and instead, the text "This deck is empty" is displayed along with a "HELP" button.

"""
21. Translate a flashcard's content from English to French.
"""
wait_until_activity(d, "DeckPicker")
d(resourceIdMatches=".*DeckPickerHoriz").click()
print("Touch on a button that has text 'My Deck, 0, 0, 0': SUCCESS")
wait()
wait_until_activity(d, "DeckPicker")
d(resourceIdMatches=".*counts_layout").click()
print("Touch on a button that has text '0, 0, 0': SUCCESS")
wait()
wait_until_activity(d, "DeckPicker")
d(descriptionMatches=".*Add", resourceIdMatches=".*fab_expand_menu_button").click()
print("Touch on a button that has content_desc 'Add': SUCCESS")
wait()
# Expected behaviour: After touching the "Add" button, a new button with the content description "Add" has been added to the current screen.

wait_until_activity(d, "DeckPicker")
d(resourceIdMatches=".*DeckPickerHoriz").click()
print("Touch on a button that has text 'My Deck, 0, 0, 0': SUCCESS")
wait()
# Expected behaviour: After touching the button with the text "My Deck, 0, 0, 0", the screen has changed. The "Create deck" and "Get shared decks" options are no longer visible, and instead, it shows that the deck is empty. There is also a new "HELP" button available.

wait_until_activity(d, "DeckPicker")
d(textStartsWith="HELP", resourceIdMatches=".*snackbar_action").click()
print("Touch on a button that has text 'HELP': SUCCESS")
wait()
# Expected behaviour: After touching the "HELP" button, the previous textview with the text "This deck is empty" is no longer visible on the current screen.

wait_until_activity(d, "DeckPicker")
d(descriptionMatches=".*Add", resourceIdMatches=".*fab_expand_menu_button").click()
print("Touch on a button that has content_desc 'Add': SUCCESS")
wait()
# Expected behaviour: By touching the "Add" button, a new button with the same content description "Add" has been added to the current screen.

wait_until_activity(d, "DeckPicker")
d(descriptionMatches=".*Add", resourceIdMatches=".*add_note_action").click()
print("Touch on a button that has content_desc 'Add': SUCCESS")
wait()
# Expected behaviour: After touching the "Add" button, the previous "DeckPicker" screen has changed to the "NoteEditor" screen where you can create a new note by filling in the fields for front and back contents. (page changed from DeckPicker to NoteEditor)

wait_until_activity(d, "NoteEditor")
d(descriptionMatches=".*Save", resourceIdMatches=".*action_save").click()
print("Touch on a button that has content_desc 'Save': SUCCESS")
wait()
# Expected behaviour: After the action, the following popup message(s) were shown and soon disappeared: {'The first field is empty'}

wait_until_activity(d, "NoteEditor")
d(descriptionMatches=".*Front", resourceIdMatches=".*id_note_editText").click()
print("Touch on a focused textfield that has content_desc 'Front': SUCCESS")
wait()
wait_until_activity(d, "NoteEditor")
d(descriptionMatches=".*Front", resourceIdMatches=".*id_note_editText").set_text("Hello World")
print("Fill a focused textfield that has content_desc 'Front' with 'Hello World': SUCCESS")
wait()
# Expected behaviour: The focused textfield with content description "Front" has been successfully filled with the text "Hello World".

wait_until_activity(d, "NoteEditor")
d(descriptionMatches=".*Back", resourceIdMatches=".*id_note_editText").click()
print("Touch on a textfield that has content_desc 'Back': SUCCESS")
wait()
# Expected behaviour: By touching on the "Back" textfield, the textfield becomes focused and the keyboard is displayed for text input.

wait_until_activity(d, "NoteEditor")
d(descriptionMatches=".*Back", resourceIdMatches=".*id_note_editText").set_text("Bonjour le monde")
print("Fill a focused textfield that has content_desc 'Back' with 'Bonjour le monde': SUCCESS")
wait()
# Expected behaviour: The focused textfield with content_desc "Back" in the previous screen now has the text "Bonjour le monde" in the current screen.

wait_until_activity(d, "NoteEditor")
d(descriptionMatches=".*Save", resourceIdMatches=".*action_save").click()
print("Touch on a button that has content_desc 'Save': SUCCESS")
wait()
# Expected behaviour: After touching the "Save" button, the focused text fields for the "Front" and "Back" of the note have been updated with their corresponding content descriptions, and a popup message saying "2 cards added" briefly appeared and disappeared.

"""
22. Add a tag to the flashcard in the NoteEditor page.
"""
wait_until_activity(d, "NoteEditor")
d(textStartsWith="Tags: ", resourceIdMatches=".*CardEditorTagButton").click()
print("Touch on a button that has text 'Tags: ': SUCCESS")
wait()
# Expected behaviour: After touching the button with the text "Tags: ", the previous screen, NoteEditor, has been updated to display a new set of widgets related to managing tags, including a textview for "Tags", buttons for filtering, adding, and checking/unchecking tags, and a message indicating that no tags have been added yet.

wait_until_activity(d, "NoteEditor")
d(descriptionMatches=".*Add tag", resourceIdMatches=".*tags_dialog_action_add").click()
print("Touch on a button that has content_desc 'Add tag': SUCCESS")
wait()
# Expected behaviour: The touch on the "Add tag" button in the previous screen opened a new screen where a text field for entering a tag name is displayed along with buttons to cancel or save the tag.

wait_until_activity(d, "NoteEditor")
d(textStartsWith="Tag name", resourceIdMatches=".*input").set_text("Study Tips")
print("Fill a focused textfield that has text 'Tag name' with 'Study Tips': SUCCESS")
wait()
wait_until_activity(d, "NoteEditor")
d(textStartsWith="OK", resourceIdMatches=".*md_buttonDefaultPositive").click()
print("Touch on a button that has text 'OK': SUCCESS")
wait()
# Expected behaviour: After touching the "OK" button, the screen has changed to show the "Tags" section with buttons for filtering, adding tags, and checking/unchecking all tags. The previous "Add tag" section is now replaced with a message indicating that no tags have been added yet.

wait_until_activity(d, "NoteEditor")
d(descriptionMatches=".*Add tag", resourceIdMatches=".*tags_dialog_action_add").click()
print("Touch on a button that has content_desc 'Add tag': SUCCESS")
wait()
# Expected behaviour: By touching the "Add tag" button, the previous screen with a list of tags is replaced with a new screen that allows the user to add a new tag by entering a tag name in the focused text field.

wait_until_activity(d, "NoteEditor")
d(textStartsWith="Tag name", resourceIdMatches=".*input").set_text("Study Tips")
print("Fill a focused textfield that has text 'Tag name' with 'Study Tips': SUCCESS")
wait()
wait_until_activity(d, "NoteEditor")
d(textStartsWith="OK", resourceIdMatches=".*md_buttonDefaultPositive").click()
print("Touch on a button that has text 'OK': SUCCESS")
wait()
# Expected behaviour: By touching on the "OK" button, the screen changed to a note editor page with additional buttons for filtering and adding tags, as well as a message indicating that no tags have been added yet.

wait_until_activity(d, "NoteEditor")
d(textStartsWith="OK", resourceIdMatches=".*md_buttonDefaultPositive").click()
print("Touch on a button that has text 'OK': SUCCESS")
wait()
# Expected behaviour: After touching the "OK" button, the previous screen is replaced with a current screen where the user can add a note. The previous buttons and textviews related to tags are replaced with buttons and textviews related to note creation.

wait_until_activity(d, "NoteEditor")
d(descriptionMatches=".*Save", resourceIdMatches=".*action_save").click()
print("Touch on a button that has content_desc 'Save': SUCCESS")
wait()
# Expected behaviour: After the action, the following popup message(s) were shown and soon disappeared: {'The first field is empty'}

wait_until_activity(d, "NoteEditor")
d(descriptionMatches=".*Save", resourceIdMatches=".*action_save").click()
print("Touch on a button that has content_desc 'Save': SUCCESS")
wait()
# Expected behaviour: After the action, the following popup message(s) were shown and soon disappeared: {'The first field is empty'}

wait_until_activity(d, "NoteEditor")
d(descriptionMatches=".*Front", resourceIdMatches=".*id_note_editText").set_text("The front side of the flashcard contains a question about the topic.")
print("Fill a focused textfield that has content_desc 'Front' with 'The front side of the flashcard contains a question about the topic.': SUCCESS")
wait()
# Expected behaviour: The focused textfield with content_desc "Front" has been filled with the text "The front side of the flashcard contains a question about the topic."

wait_until_activity(d, "NoteEditor")
d(descriptionMatches=".*Back", resourceIdMatches=".*id_note_editText").set_text("The answer to the flashcard question is XYZ.")
print("Fill a textfield that has content_desc 'Back' with 'The answer to the flashcard question is XYZ.': SUCCESS")
wait()
# Expected behaviour: The textfield with content description "Back" has been filled with the text "The answer to the flashcard question is XYZ."

wait_until_activity(d, "NoteEditor")
d(textStartsWith="Tags: ", resourceIdMatches=".*CardEditorTagButton").click()
print("Touch on a button that has text 'Tags: ': SUCCESS")
wait()
# Expected behaviour: The button "Tags: " has been replaced with a textview "Tags". Additionally, new buttons "Filter tags", "Add tag", and "Check/uncheck all tags" have appeared, along with a textview indicating that no tags have been added yet.

"""
23. Add a tag to the current flashcard in the NoteEditor page.
"""
wait_until_activity(d, "NoteEditor")
d(descriptionMatches=".*Add tag", resourceIdMatches=".*tags_dialog_action_add").click()
print("Touch on a button that has content_desc 'Add tag': SUCCESS")
wait()
# Expected behaviour: After touching the "Add tag" button, the previous screen is replaced with a new screen where a textfield for adding a new tag is displayed along with "CANCEL" and "OK" buttons. The previous buttons related to tags are no longer visible.

wait_until_activity(d, "NoteEditor")
d(textStartsWith="Tag name", resourceIdMatches=".*input").set_text("Study Tips")
print("Fill a focused textfield that has text 'Tag name' with 'Study Tips': SUCCESS")
wait()
wait_until_activity(d, "NoteEditor")
d(textStartsWith="OK", resourceIdMatches=".*md_buttonDefaultPositive").click()
print("Touch on a button that has text 'OK': SUCCESS")
wait()
# Expected behaviour: After touching the "OK" button, the previous screen was replaced with a new screen that includes additional buttons for filtering and adding tags, as well as a new textview indicating that no tags have been added yet.

"""
24. Add a tag "Study Tips" to a flashcard.
"""
wait_until_activity(d, "NoteEditor")
d(descriptionMatches=".*Add tag", resourceIdMatches=".*tags_dialog_action_add").click()
print("Touch on a button that has content_desc 'Add tag': SUCCESS")
wait()
# Expected behaviour: The action of touching on the "Add tag" button in the previous screen has opened a new screen in the current state where the user can add a new tag by entering a tag name in the focused textfield.

wait_until_activity(d, "NoteEditor")
d(textStartsWith="Tag name", resourceIdMatches=".*input").set_text("Study Tips")
print("Fill a focused textfield that has text 'Tag name' with 'Study Tips': SUCCESS")
wait()
wait_until_activity(d, "NoteEditor")
d(textStartsWith="OK", resourceIdMatches=".*md_buttonDefaultPositive").click()
print("Touch on a button that has text 'OK': SUCCESS")
wait()
# Expected behaviour: After touching the "OK" button, the screen has changed to display tags, along with buttons for filtering, adding tags, and checking/unchecking all tags. The previous "Add tag" text field has been replaced with a message indicating that no tags have been added yet.

wait_until_activity(d, "NoteEditor")
d(textStartsWith="OK", resourceIdMatches=".*md_buttonDefaultPositive").click()
print("Touch on a button that has text 'OK': SUCCESS")
wait()
# Expected behaviour: After touching the "OK" button, the previous NoteEditor screen has been updated with a new "Save" button, dropdown fields for "Type" and "Deck", textfields for "Front" and "Back" flashcard content, and buttons for attaching multimedia content. Additionally, the "Tags" section now displays the selected cards.

wait_until_activity(d, "NoteEditor")
d(textStartsWith="Cards: Card 1, Card 2", resourceIdMatches=".*CardEditorCardsText").click()
print("Touch on a button that has text 'Cards: Card 1, Card 2': SUCCESS")
wait()
# Expected behaviour: The action of touching the button "Cards: Card 1, Card 2" in the previous screen has opened the CardTemplateEditor screen, where the user can edit the content of the flashcards. The screen now displays options to edit the front and back templates, styling, and allows the user to switch between different cards. (page changed from NoteEditor to CardTemplateEditor)

wait_until_activity(d, "CardTemplateEditor")
d(textStartsWith="CARD 1").click()
print("Touch on a button that has text 'CARD 1': SUCCESS")
wait()
wait_until_activity(d, "CardTemplateEditor")
d(textStartsWith="{{Front}}", descriptionMatches=".*Front template", resourceIdMatches=".*front_edit").set_text("Study Tips: {{Front}}")
print("Fill a focused textfield that has text '{{Front}}' with 'Study Tips: {{Front}}': SUCCESS")
wait()
# Expected behaviour: The focused textfield that previously had the text "{{Front}}" is now filled with "Study Tips: {{Front}}".

wait_until_activity(d, "CardTemplateEditor")
d(descriptionMatches=".*Save", resourceIdMatches=".*action_confirm").click()
print("Touch on a button that has content_desc 'Save': SUCCESS")
wait()
# Expected behaviour: After touching the "Save" button, the screen changed from the "CardTemplateEditor" to the "DeckPicker" screen. The previous screen had options for editing card templates, while the current screen displays information about the AnkiDroid app and the user's deck. (page changed from CardTemplateEditor to DeckPicker)

wait_until_activity(d, "DeckPicker")
d(descriptionMatches=".*Navigate up").click()
print("Touch on a button that has content_desc 'Navigate up': SUCCESS")
wait()
# Expected behaviour: The performed action takes the user back to the previous screen, the DeckPicker screen, where they can see a list of buttons for navigating to different sections of the app, including "Decks", "Card browser", "Statistics", and "Settings".

wait_until_activity(d, "DeckPicker")
d(textStartsWith="Decks", resourceIdMatches=".*design_menu_item_text").click()
print("Touch on a checked button that has text 'Decks': SUCCESS")
wait()
wait_until_activity(d, "DeckPicker")
d(descriptionMatches=".*Navigate up").click()
print("Touch on a button that has content_desc 'Navigate up': SUCCESS")
wait()
wait_until_activity(d, "DeckPicker")
d(descriptionMatches=".*Navigate up").click()
print("Touch on a button that has content_desc 'Navigate up': SUCCESS")
wait()
wait_until_activity(d, "DeckPicker")
d(descriptionMatches=".*Navigate up").click()
print("Touch on a button that has content_desc 'Navigate up': SUCCESS")
wait()
"""
25. Add an image to a flashcard in the MultimediaEditField page.
"""
wait_until_activity(d, "DeckPicker")
d(resourceIdMatches=".*DeckPickerHoriz").click()
print("Touch on a button that has text 'My Deck, 2, 0, 0': SUCCESS")
wait()
wait_until_activity(d, "DeckPicker")
d(textStartsWith="Decks", resourceIdMatches=".*design_menu_item_text").click()
print("Touch on a checked button that has text 'Decks': SUCCESS")
wait()
wait_until_activity(d, "DeckPicker")
d(textStartsWith="Card browser", resourceIdMatches=".*design_menu_item_text").click()
print("Touch on a button that has text 'Card browser': SUCCESS")
wait()
# Expected behaviour: By touching on the button with the text "Card browser", the screen has changed to the CardBrowser page, where there is a dropdown field for selecting the card type, a list of study tips with corresponding translations, and a focused listview for browsing the cards. (page changed from DeckPicker to CardBrowser)

wait_until_activity(d, "CardBrowser")
d(resourceIdMatches=".*card_item_browser").click()
print("Touch on a button that has text 'Study Tips:  droidbot_utg.png': SUCCESS")
wait()
# Expected behaviour: The previous CardBrowser screen has been replaced by the current NoteEditor screen, which allows the user to edit a note. The textview has changed to "Edit note" and a "Save" button has been added, indicating that the user can now make changes to the note and save it. (page changed from CardBrowser to NoteEditor)

wait_until_activity(d, "NoteEditor")
d(descriptionMatches=".*Attach multimedia content to the Back field", resourceIdMatches=".*id_media_button").click()
print("Touch on a button that has content_desc 'Attach multimedia content to the Back field': SUCCESS")
wait()
# Expected behaviour: After touching the button that has the content description "Attach multimedia content to the Back field", the current screen now shows additional buttons for adding an image, audio clip, and recording audio, as well as an option for accessing the advanced editor.

wait_until_activity(d, "NoteEditor")
d(textStartsWith="Add image").click()
print("Touch on a button that has text 'Add image': SUCCESS")
wait()
# Expected behaviour: The action of touching on the "Add image" button in the previous screen has opened a new screen called "MultimediaEditField" where several new buttons and a textview are displayed, including options to add audio clips, record audio, access advanced editing features, and navigate back. (page changed from NoteEditor to MultimediaEditField)

wait_until_activity(d, "MultimediaEditField")
d(textStartsWith="GALLERY").click()
print("Touch on a button that has text 'GALLERY': SUCCESS")
wait()
# Expected behaviour: After touching the "GALLERY" button, the screen now shows a selection of options for completing the action using the Photos app, including "JUST ONCE", "ALWAYS", and "Use a different app". The listview with resource_id "resolver_list" is also now in focus. (page changed from MultimediaEditField to Resolver)

wait_until_activity(d, "Resolver")
d(textStartsWith="JUST ONCE", resourceIdMatches=".*button_once").click()
print("Touch on a button that has text 'JUST ONCE': SUCCESS")
wait()
# Expected behaviour: After touching the button with text "JUST ONCE", the previous screen (Resolver) is replaced with the current screen (ExternalPicker) which shows different options for selecting a photo, such as "Screenshots", "ActivityDiary", and "Pictures". (page changed from Resolver to ExternalPicker)

wait_until_activity(d, "ExternalPicker")
d(textStartsWith="Pictures").click()
print("Touch on a button that has text 'Pictures': SUCCESS")
wait()
# Expected behaviour: After touching on the "Pictures" button, the current screen shows a list of photos with the date "Thursday, Oct 5" and their corresponding content descriptions. (page changed from ExternalPicker to LocalPhotos)

wait_until_activity(d, "LocalPhotos")
d(descriptionMatches=".*Photo taken on Oct 5, 2023 11:27:33 AM.").click()
print("Touch on a button that has content_desc 'Photo taken on Oct 5, 2023 11:27:33 AM.': SUCCESS")
wait()
# Expected behaviour: The action of touching on the button with content description "Photo taken on Oct 5, 2023 11:27:33 AM" has transitioned the screen from the "LocalPhotos" page to the "MultimediaEditField" page, where the user can now edit multimedia content such as text, audio recordings, and images. (page changed from LocalPhotos to MultimediaEditField)

wait_until_activity(d, "MultimediaEditField")
d(descriptionMatches=".*Done", resourceIdMatches=".*multimedia_edit_field_done").click()
print("Touch on a button that has content_desc 'Done': SUCCESS")
wait()
# Expected behaviour: The "Done" button was touched, and the previous MultimediaEditField screen changed to the NoteEditor screen. The "Navigate up" button was added, and the "Editing field" textview was replaced with the "Edit note" textview. The "Save" button was added, and the "More options" button was removed. The "Type" dropdown field and "Card deck" dropdown field were added, along with the "Front" and "Back" textviews and corresponding textfields. The "Attach multimedia content" buttons were added for both the front and back fields. The "Tags" and "Cards" buttons were also added. (page changed from MultimediaEditField to NoteEditor)

wait_until_activity(d, "NoteEditor")
d(descriptionMatches=".*Attach multimedia content to the Back field", resourceIdMatches=".*id_media_button").click()
print("Touch on a button that has content_desc 'Attach multimedia content to the Back field': SUCCESS")
wait()
# Expected behaviour: After touching the "Attach multimedia content to the Back field" button, the previous screen has been updated to include additional buttons such as "Add image," "Add audio clip," "Record audio," and "Advanced editor" in the NoteEditor.

"""
26. Add an audio clip to a flashcard.
"""
wait_until_activity(d, "NoteEditor")
d(textStartsWith="Add image").click()
print("Touch on a button that has text 'Add image': SUCCESS")
wait()
# Expected behaviour: After touching on the "Add image" button, the previous NoteEditor screen is replaced with the MultimediaEditField screen, which now includes additional buttons for adding audio clips, recording audio, an advanced editor, options to navigate up, and buttons for selecting text, audio recording, gallery, and camera. The screen also displays a textview indicating that it is the editing field, and buttons for "Done" and "More options". (page changed from NoteEditor to MultimediaEditField)

wait_until_activity(d, "MultimediaEditField")
d(textStartsWith="AUDIO RECORDING", resourceIdMatches=".*multimedia_edit_field_to_audio").click()
print("Touch on a button that has text 'AUDIO RECORDING': SUCCESS")
wait()
# Expected behaviour: After touching on the "AUDIO RECORDING" button, the button is replaced with two new buttons labeled "IMAGE" and "AUDIO CLIP" in the current screen.

wait_until_activity(d, "MultimediaEditField")
d(textStartsWith="AUDIO CLIP", resourceIdMatches=".*multimedia_edit_field_to_audio_clip").click()
print("Touch on a button that has text 'AUDIO CLIP': SUCCESS")
wait()
# Expected behaviour: After touching the "AUDIO CLIP" button, it is replaced by a "More options" button and a "LIBRARY" button is added. The "Done" button is still present.

wait_until_activity(d, "MultimediaEditField")
d(textStartsWith="LIBRARY").click()
print("Touch on a button that has text 'LIBRARY': SUCCESS")
wait()
# Expected behaviour: After touching the "LIBRARY" button, the previous MultimediaEditField screen is replaced with the Documents screen, which displays various options for opening files such as Recent, Audio, Downloads, SDCARD, and Drive, along with the information about available storage space. (page changed from MultimediaEditField to Documents)

wait_until_activity(d, "Documents")
d(textStartsWith="Audio", resourceIdMatches=".*title").click()
print("Touch on a button that has text 'Audio': SUCCESS")
wait()
# Expected behaviour: By touching the "Audio" button, the content of the screen has changed to show a list of audio files, with options to view them in either a grid or list format, sort them, and access more options.

wait_until_activity(d, "Documents")
d(textStartsWith="Unknown", resourceIdMatches=".*title").click()
print("Touch on a button that has text 'Unknown': SUCCESS")
wait()
# Expected behaviour: After touching the button with text "Unknown", the previous button with text "Unknown" has been replaced with a new button with the same text.

wait_until_activity(d, "Documents")
d(textStartsWith="Music", resourceIdMatches=".*title").click()
print("Touch on a button that has text 'Music': SUCCESS")
wait()
# Expected behaviour: After touching the "Music" button, the previous "Unknown" button is replaced with a "Heartbeat" button, and a new "intermission" button and a textview with the text "Oct 5" are added to the current screen.

wait_until_activity(d, "Documents")
d(textStartsWith="Heartbeat", resourceIdMatches=".*title").click()
print("Touch on a button that has text 'Heartbeat': SUCCESS")
wait()
# Expected behaviour: After touching the "Heartbeat" button, the previous "Documents" screen has changed to the "MultimediaEditField" screen, where there is a new button "LIBRARY" and a textview showing the sound of a heartbeat. (page changed from Documents to MultimediaEditField)

wait_until_activity(d, "MultimediaEditField")
d(descriptionMatches=".*Done", resourceIdMatches=".*multimedia_edit_field_done").click()
print("Touch on a button that has content_desc 'Done': SUCCESS")
wait()
# Expected behaviour: After touching the "Done" button, the previous MultimediaEditField screen is replaced with the current NoteEditor screen, which includes options to save the note, a dropdown field for selecting the card type, a textfield for editing the front and back of the card, and buttons for attaching multimedia content and managing tags and cards. (page changed from MultimediaEditField to NoteEditor)

wait_until_activity(d, "NoteEditor")
d(descriptionMatches=".*Save", resourceIdMatches=".*action_save").click()
print("Touch on a button that has content_desc 'Save': SUCCESS")
wait()
# Expected behaviour: After touching the "Save" button, the previous NoteEditor screen is replaced with the current CardBrowser screen. The CardBrowser screen displays a listview with cards and their corresponding study tips. (page changed from NoteEditor to CardBrowser)

wait_until_activity(d, "CardBrowser")
d(resourceIdMatches=".*card_item_browser").click()
print("Touch on a button that has text 'Study Tips:  droidbot_utg.png, droidbot_utg.png  ankidroid_audioclip_Heartbeat372[...]': SUCCESS")
wait()
# Expected behaviour: The action opens the NoteEditor screen where the user can edit the content of a note. The previous CardBrowser screen is replaced with a screen that allows the user to modify the note's front and back content, add multimedia attachments, and assign tags and cards to the note. (page changed from CardBrowser to NoteEditor)

wait_until_activity(d, "NoteEditor")
d(descriptionMatches=".*Attach multimedia content to the Back field", resourceIdMatches=".*id_media_button").click()
print("Touch on a button that has content_desc 'Attach multimedia content to the Back field': SUCCESS")
wait()
# Expected behaviour: After touching the "Attach multimedia content to the Back field" button, the previous screen in the NoteEditor has changed to the current screen in the MultimediaEditField. The button options have been updated to include "TEXT" and "AUDIO RECORDING" buttons for attaching multimedia content to the editing field. (page changed from NoteEditor to MultimediaEditField)

wait_until_activity(d, "MultimediaEditField")
d(descriptionMatches=".*Navigate up").click()
print("Touch on a button that has content_desc 'Navigate up': SUCCESS")
wait()
# Expected behaviour: After touching the "Navigate up" button, the previous MultimediaEditField screen is replaced with the current NoteEditor screen. The new screen allows the user to edit a note, with options to save, attach multimedia content, and select card decks. (page changed from MultimediaEditField to NoteEditor)

"""
27. Preview a created flashcard on the "Previewer" page.
"""
wait_until_activity(d, "NoteEditor")
d(textStartsWith="Cards: Card 1, Card 2", resourceIdMatches=".*CardEditorCardsText").click()
print("Touch on a button that has text 'Cards: Card 1, Card 2': SUCCESS")
wait()
# Expected behaviour: The action of touching on the button "Cards: Card 1, Card 2" in the previous screen has brought the user to the CardTemplateEditor screen where they can edit the templates for the front and back of the cards. (page changed from NoteEditor to CardTemplateEditor)

wait_until_activity(d, "CardTemplateEditor")
d(descriptionMatches=".*Preview", resourceIdMatches=".*action_preview").click()
print("Touch on a button that has content_desc 'Preview': SUCCESS")
wait()
# Expected behaviour: After touching the "Preview" button, the screen changes to the "Previewer" page. The previous buttons and text views are replaced with a new "Preview" text view, a "Study Tips: droidbot_utg" widget, and a "SHOW ANSWER" button. (page changed from CardTemplateEditor to Previewer)

wait_until_activity(d, "Previewer")
d(textStartsWith="SHOW ANSWER", resourceIdMatches=".*flashcard_layout_flip").click()
print("Touch on a button that has text 'SHOW ANSWER': SUCCESS")
wait()
# Expected behaviour: After touching the "SHOW ANSWER" button, a new button with text "ankidroid_audioclip_Heartbeat372766725" appeared on the current screen.

"""
28. Access the "Translation" page and attempt to translate a foreign language word.
"""
wait_until_activity(d, "Previewer")
d.press("back")
print("Press 'BACK' button to navigate back: SUCCESS")
wait()
# Expected behaviour: Pressing the "BACK" button navigates back to the previous screen, CardTemplateEditor. The screen now displays various buttons for preview, saving, and more options, as well as textfields for front and back templates. (page changed from Previewer to CardTemplateEditor)

wait_until_activity(d, "CardTemplateEditor")
d(descriptionMatches=".*More options").click()
print("Touch on a button that has content_desc 'More options': SUCCESS")
wait()
# Expected behaviour: After touching the "More options" button, two new buttons labeled "Add" and "Delete" are now visible on the current screen.

wait_until_activity(d, "CardTemplateEditor")
d.press("back")
print("Press 'BACK' button to navigate back: SUCCESS")
wait()
# Expected behaviour: Pressing the "BACK" button navigated the user back to the previous screen, which is the CardTemplateEditor. The screen now displays various buttons, textviews, and textfields related to card templates and styling.

wait_until_activity(d, "CardTemplateEditor")
d(textStartsWith="CARD 1").click()
print("Touch on a button that has text 'CARD 1': SUCCESS")
wait()
wait_until_activity(d, "CardTemplateEditor")
d(descriptionMatches=".*More options").click()
print("Touch on a button that has content_desc 'More options': SUCCESS")
wait()
# Expected behaviour: After touching on the "More options" button, two new buttons labeled "Add" and "Delete" have appeared on the screen.

wait_until_activity(d, "CardTemplateEditor")
d(textStartsWith="Add").click()
print("Touch on a button that has text 'Add': SUCCESS")
wait()
# Expected behaviour: After touching the "Add" button, the screen has changed to include additional buttons for navigation, preview, saving, and more options. There are also new buttons for each card, as well as text fields for the front and back templates. The screen now also includes a scrollable area.

wait_until_activity(d, "CardTemplateEditor")
d(descriptionMatches=".*Navigate up").click()
print("Touch on a button that has content_desc 'Navigate up': SUCCESS")
wait()
# Expected behaviour: The performed action displays a confirmation dialog with the options to cancel or close and lose the current input.

wait_until_activity(d, "CardTemplateEditor")
d(textStartsWith="OK", resourceIdMatches=".*md_buttonDefaultPositive").click()
print("Touch on a button that has text 'OK': SUCCESS")
wait()
# Expected behaviour: After touching the "OK" button, the previous CardTemplateEditor screen is replaced with the current NoteEditor screen, which includes various widgets such as a dropdown field for card type, textfields for front and back content, buttons for saving and attaching multimedia content, and information about tags and cards. (page changed from CardTemplateEditor to NoteEditor)

wait_until_activity(d, "NoteEditor")
d(descriptionMatches=".*Navigate up").click()
print("Touch on a button that has content_desc 'Navigate up': SUCCESS")
wait()
# Expected behaviour: After touching the "Navigate up" button, the previous NoteEditor screen is replaced by the current CardBrowser screen. The current screen displays a different set of widgets, including a dropdown field with options for "Question" and "Answer", a textview with the title "My Deck" and the number of cards shown, and a listview with card items for studying. (page changed from NoteEditor to CardBrowser)

wait_until_activity(d, "CardBrowser")
d(descriptionMatches=".*More options").click()
print("Touch on a button that has content_desc 'More options': SUCCESS")
wait()
# Expected behaviour: After touching on the "More options" button, several new buttons have appeared on the screen, including "Change display order", "Filter marked", "Filter suspended", "Filter by tag", "Preview", and "Select all".

"""
29. Filter cards by the tag "Study Tips" on the CardBrowser page.
"""
wait_until_activity(d, "CardBrowser")
d(textStartsWith="Filter by tag").click()
print("Touch on a button that has text 'Filter by tag': SUCCESS")
wait()
# Expected behaviour: After touching the "Filter by tag" button, the previous buttons related to filtering are replaced with new buttons for selecting tags and filtering by tags. Additionally, a message is displayed indicating that no tags have been added yet.

wait_until_activity(d, "CardBrowser")
d(textStartsWith="SELECT", resourceIdMatches=".*md_buttonDefaultPositive").click()
print("Touch on a button that has text 'SELECT': SUCCESS")
wait()
# Expected behaviour: After touching the "SELECT" button, the previous CardBrowser screen is replaced by a new CardBrowser screen with different content. The new screen displays a list of cards with their corresponding study tips and translations.

wait_until_activity(d, "CardBrowser")
d(resourceIdMatches=".*card_item_browser").click()
print("Touch on a button that has text 'Study Tips:  droidbot_utg.png, droidbot_utg.png  ankidroid_audioclip_Heartbeat372[...]': SUCCESS")
wait()
# Expected behaviour: After touching the button with text "Study Tips:  droidbot_utg.png, droidbot_utg.png  ankidroid_audioclip_Heartbeat372[...]", the previous CardBrowser screen is replaced with the current NoteEditor screen. The NoteEditor screen displays an editable note with a dropdown field for selecting the card type, a dropdown field for selecting the card deck, text fields for the front and back of the card, and buttons for attaching multimedia content and managing tags and cards. (page changed from CardBrowser to NoteEditor)

wait_until_activity(d, "NoteEditor")
d(descriptionMatches=".*Navigate up").click()
print("Touch on a button that has content_desc 'Navigate up': SUCCESS")
wait()
# Expected behaviour: By touching the "Navigate up" button, the user has navigated from the NoteEditor screen to the CardBrowser screen. The CardBrowser screen now displays a list of cards with their associated study tips. (page changed from NoteEditor to CardBrowser)

wait_until_activity(d, "CardBrowser")
d(resourceIdMatches=".*toolbar_spinner").click()
print("Touch on a dropdown field that has text 'My Deck, 8 cards shown': SUCCESS")
wait()
# Expected behaviour: The dropdown field "My Deck, 8 cards shown" is replaced by a button "My Deck" that is checked. Additionally, two new buttons "All decks" and "Default" are added.

wait_until_activity(d, "CardBrowser")
d(textStartsWith="My Filtered Deck", resourceIdMatches=".*dropdown_deck_name").click()
print("Touch on a button that has text 'My Filtered Deck': SUCCESS")
wait()
# Expected behaviour: After touching on the button "My Filtered Deck", the CardBrowser screen has changed. The previous buttons "All decks", "Default", and "My Deck" have been replaced with a new button "Navigate up" and a textview displaying "My Filtered Deck". Additionally, there are new elements such as a dropdown field, buttons for adding notes and searching, and a listview for browsing cards.

wait_until_activity(d, "CardBrowser")
d(resourceIdMatches=".*toolbar_spinner").click()
print("Touch on a dropdown field that has text 'My Filtered Deck, 5 cards shown': SUCCESS")
wait()
# Expected behaviour: The performed action on the dropdown field in the CardBrowser screen has updated the list of decks displayed in the current screen. The "My Filtered Deck" option is now checked, indicating that it is selected.

wait_until_activity(d, "CardBrowser")
d(textStartsWith="My Filtered Deck", resourceIdMatches=".*dropdown_deck_name").click()
print("Touch on a checked button that has text 'My Filtered Deck': SUCCESS")
wait()
# Expected behaviour: The performed action updated the CardBrowser screen by adding a checked button with the text "My Filtered Deck" and displaying various textviews and buttons related to the deck's content.

wait_until_activity(d, "CardBrowser")
d(descriptionMatches=".*Navigate up").click()
print("Touch on a button that has content_desc 'Navigate up': SUCCESS")
wait()
# Expected behaviour: After touching the "Navigate up" button, the current screen shows additional buttons for "Decks", "Statistics", "Settings", "Help", and "Send feedback", as well as a textview displaying "My Filtered Deck" and "5 cards shown".

wait_until_activity(d, "CardBrowser")
d(descriptionMatches=".*More options").click()
print("Touch on a button that has content_desc 'More options': SUCCESS")
wait()
# Expected behaviour: By touching the "More options" button, additional options are displayed in the CardBrowser screen, including options such as "Decks", "Statistics", "Settings", "Help", and "Send feedback".

wait_until_activity(d, "CardBrowser")
d(descriptionMatches=".*Add note", resourceIdMatches=".*action_add_note_from_card_browser").click()
print("Touch on a button that has content_desc 'Add note': SUCCESS")
wait()
# Expected behaviour: The action of touching on the "Add note" button has opened the NoteEditor screen where the user can input and save note information. The previous CardBrowser screen is replaced by the NoteEditor screen, which contains fields for the user to input note details such as the type, deck, front, and back. (page changed from CardBrowser to NoteEditor)

wait_until_activity(d, "NoteEditor")
d(textStartsWith="My Deck", resourceIdMatches=".*note_deck_spinner").click()
print("Touch on a dropdown field that has text 'My Deck': SUCCESS")
wait()
# Expected behaviour: The performed action selected the "My Deck" option in the dropdown field for the "Deck" property, replacing the previous selection of "Default".

wait_until_activity(d, "NoteEditor")
d.press("back")
print("Press 'BACK' button to navigate back: SUCCESS")
wait()
# Expected behaviour: The "BACK" button was pressed to navigate back, and the previous screen displayed a button with the text "Default" and a checked button with the text "My Deck". The current screen shows a button with the content description "Navigate up", a text view with the text "Add note", a button with the content description "Save", and other widgets related to note editing.

"""
30. Change the note type of a flashcard from "Basic (and reversed card)" to another type in the NoteEditor page.
"""
wait_until_activity(d, "NoteEditor")
d(textStartsWith="Basic (and reversed card)", resourceIdMatches=".*note_type_spinner").click()
print("Touch on a dropdown field that has text 'Basic (and reversed card)': SUCCESS")
wait()
# Expected behaviour: The dropdown field has been expanded and now shows different options for selecting a card type, including "Basic", "Basic (and reversed card)", "Basic (optional reversed card)", "Basic (type in the answer)", and "Cloze".

wait_until_activity(d, "NoteEditor")
d(textStartsWith="Basic", resourceIdMatches=".*text1").click()
print("Touch on a button that has text 'Basic': SUCCESS")
wait()
# Expected behaviour: The touch on the "Basic" button in the previous screen has changed the current screen to a note editor with various options and fields for creating a new note.

wait_until_activity(d, "NoteEditor")
d(descriptionMatches=".*Save", resourceIdMatches=".*action_save").click()
print("Touch on a button that has content_desc 'Save': SUCCESS")
wait()
# Expected behaviour: After touching the "Save" button in the NoteEditor screen, the "Front" textfield became focused and a popup message briefly appeared and disappeared, indicating that the first field is empty.

wait_until_activity(d, "NoteEditor")
d(descriptionMatches=".*Front", resourceIdMatches=".*id_note_editText").set_text("Hello world!")
print("Fill a focused textfield that has content_desc 'Front' with 'Hello world!': SUCCESS")
wait()
# Expected behaviour: The focused textfield with content_desc "Front" has been filled with "Hello world!"

wait_until_activity(d, "NoteEditor")
d(descriptionMatches=".*Field1", resourceIdMatches=".*id_note_editText").set_text("Jade Green is a 25-year-old graduate student studying computer science.")
print("Fill a textfield that has content_desc 'Field1' with 'Jade Green is a 25-year-old graduate student studying computer science.': SUCCESS")
wait()
# Expected behaviour: The performed action successfully filled the textfield labeled "Field1" with the text "Jade Green is a 25-year-old graduate student studying computer science."

wait_until_activity(d, "NoteEditor")
d(descriptionMatches=".*Save", resourceIdMatches=".*action_save").click()
print("Touch on a button that has content_desc 'Save': SUCCESS")
wait()
# Expected behaviour: After touching the "Save" button, the focus shifted from the "Hello world!" textfield to the "Front" textfield, and the "Field1" textfield lost focus. Additionally, a popup message briefly appeared and disappeared, indicating that 1 card was added.

wait_until_activity(d, "NoteEditor")
d(descriptionMatches=".*Save", resourceIdMatches=".*action_save").click()
print("Touch on a button that has content_desc 'Save': SUCCESS")
wait()
# Expected behaviour: After the action, the following popup message(s) were shown and soon disappeared: {'The first field is empty'}

wait_until_activity(d, "NoteEditor")
d(descriptionMatches=".*Front", resourceIdMatches=".*id_note_editText").set_text("Hello everyone! Today, I want to share an interesting fact about computer science.")
print("Fill a focused textfield that has content_desc 'Front' with 'Hello everyone! Today, I want to share an interesting fact about computer science.': SUCCESS")
wait()
# Expected behaviour: The focused textfield with content_desc "Front" has been filled with the text "Hello everyone! Today, I want to share an interesting fact about computer science."

wait_until_activity(d, "NoteEditor")
d(textStartsWith="Cards: Card 1", resourceIdMatches=".*CardEditorCardsText").click()
print("Touch on a button that has text 'Cards: Card 1': SUCCESS")
wait()
# Expected behaviour: After touching the "Cards: Card 1" button, the screen has changed from the NoteEditor to the CardTemplateEditor. The CardTemplateEditor screen displays the card template details, including the front template, styling, and back template. (page changed from NoteEditor to CardTemplateEditor)

wait_until_activity(d, "CardTemplateEditor")
d(descriptionMatches=".*Save", resourceIdMatches=".*action_confirm").click()
print("Touch on a button that has content_desc 'Save': SUCCESS")
wait()
# Expected behaviour: After touching the "Save" button, the previous screen (CardTemplateEditor) has been replaced by the current screen (CardBrowser) which shows a list of cards and their corresponding templates. (page changed from CardTemplateEditor to CardBrowser)

wait_until_activity(d, "CardBrowser")
d(resourceIdMatches=".*card_item_browser").click()
print("Touch on a button that has text 'Study Tips:  droidbot_utg.png, droidbot_utg.png  ankidroid_audioclip_Heartbeat372[...]': SUCCESS")
wait()
# Expected behaviour: The action of touching the button with the text "Study Tips: droidbot_utg.png, droidbot_utg.png ankidroid_audioclip_Heartbeat372[...]" in the previous screen opened the NoteEditor screen in the current screen, where the user can edit a note with multimedia content attached to the front and back fields. (page changed from CardBrowser to NoteEditor)

wait_until_activity(d, "NoteEditor")
d(textStartsWith="Basic (and reversed card)", resourceIdMatches=".*note_type_spinner").click()
print("Touch on a dropdown field that has text 'Basic (and reversed card)': SUCCESS")
wait()
# Expected behaviour: The performed action on the dropdown field changed the available options for the card deck to "Basic", "Basic (optional reversed card)", "Basic (type in the answer)", and "Cloze".

wait_until_activity(d, "NoteEditor")
d(textStartsWith="Basic", resourceIdMatches=".*text1").click()
print("Touch on a button that has text 'Basic': SUCCESS")
wait()
# Expected behaviour: After touching the "Basic" button, the previous NoteEditor screen is replaced with a new NoteEditor screen that includes additional buttons and text fields for editing notes, as well as a dropdown field to select the note type.

"""
31. Explore the additional options available on the NoteEditor page by interacting with the "More options" widget.
"""
wait_until_activity(d, "NoteEditor")
d(descriptionMatches=".*More options").click()
print("Touch on a button that has content_desc 'More options': SUCCESS")
wait()
# Expected behaviour: The performed action on the "More options" button in the NoteEditor screen has added two new buttons to the current screen, "Add note" and "Copy note".

wait_until_activity(d, "NoteEditor")
d(textStartsWith="Add note").click()
print("Touch on a button that has text 'Add note': SUCCESS")
wait()
# Expected behaviour: After touching the "Add note" button, the NoteEditor screen is updated with additional widgets including a textfield for the "Front" field, a textfield for "Field1", a textfield for "CustomField", and buttons for attaching multimedia content to each field.

wait_until_activity(d, "NoteEditor")
d(descriptionMatches=".*Field1", resourceIdMatches=".*id_note_editText").click()
print("Touch on a textfield that has content_desc 'Field1': SUCCESS")
wait()
# Expected behaviour: The performed action caused the textfield with content description "Field1" to become focused, indicated by the change from "a textfield that has content_desc 'Field1'" to "a focused textfield that has content_desc 'Field1'".

wait_until_activity(d, "NoteEditor")
d(descriptionMatches=".*Save", resourceIdMatches=".*action_save").click()
print("Touch on a button that has content_desc 'Save': SUCCESS")
wait()
# Expected behaviour: After touching the "Save" button in the NoteEditor screen, the "Edit note" text is displayed instead of "Add note" and a "More options" button is added. A popup message briefly appeared and disappeared, stating "The first field is empty."

wait_until_activity(d, "NoteEditor")
d(textStartsWith="Basic", resourceIdMatches=".*note_type_spinner").click()
print("Touch on a dropdown field that has text 'Basic': SUCCESS")
wait()
# Expected behaviour: The performed action on the dropdown field changed the options available in the dropdown. The dropdown now shows multiple options related to different card types, including Basic, Basic (and reversed card), Basic (optional reversed card), Basic (type in the answer), and Cloze.

wait_until_activity(d, "NoteEditor")
d(textStartsWith="Basic (and reversed card)", resourceIdMatches=".*text1").click()
print("Touch on a button that has text 'Basic (and reversed card)': SUCCESS")
wait()
# Expected behaviour: After touching the button with text "Basic (and reversed card)", the screen changed to the NoteEditor screen, where the button with text "Basic (and reversed card)" is selected and there are additional buttons and fields for editing the note.

wait_until_activity(d, "NoteEditor")
d(textStartsWith="<img src=", descriptionMatches=".*Back", resourceIdMatches=".*id_note_editText").set_text("The mitochondria are the powerhouse of the cell.")
print("Fill a textfield that has text '<img src='droidbot_utg.png'>[sound:ankidroid_audio[...]' with 'The mitochondria are the powerhouse of the cell.': SUCCESS")
wait()
# Expected behaviour: The performed action successfully filled the textfield with "The mitochondria are the powerhouse of the cell." The previous audio clip text is replaced with the new text.

wait_until_activity(d, "NoteEditor")
d(textStartsWith="sound:ankidroid_audioclip_Heartbeat372766725The mitochondria are the powerhouse of the cell.", descriptionMatches=".*Back", resourceIdMatches=".*id_note_editText").click()
print("Touch on a focused textfield that has text 'sound:ankidroid_audioclip_Heartbeat372766725The mi[...]': SUCCESS")
wait()
wait_until_activity(d, "NoteEditor")
d(textStartsWith="<img src=", descriptionMatches=".*Front", resourceIdMatches=".*id_note_editText").set_text("What is the difference between a linked list and an array?")
print("Fill a textfield that has text '<img src='droidbot_utg.png'>' with 'What is the difference between a linked list and an array?': SUCCESS")
wait()
# Expected behaviour: The user filled the textfield with the question "What is the difference between a linked list and an array?" and the textfield now shows the entered question with a ">" symbol at the beginning.

wait_until_activity(d, "NoteEditor")
d(descriptionMatches=".*Attach multimedia content to the Front field", resourceIdMatches=".*id_media_button").click()
print("Touch on a button that has content_desc 'Attach multimedia content to the Front field': SUCCESS")
wait()
# Expected behaviour: After touching the button with content description "Attach multimedia content to the Front field", the previous NoteEditor screen transitioned to the MultimediaEditField screen. The MultimediaEditField screen now displays options to attach image and audio recordings to the editing field. (page changed from NoteEditor to MultimediaEditField)

wait_until_activity(d, "MultimediaEditField")
d(textStartsWith="IMAGE", resourceIdMatches=".*multimedia_edit_field_to_image").click()
print("Touch on a button that has text 'IMAGE': SUCCESS")
wait()
# Expected behaviour: The button with the text "IMAGE" has been changed to a button with the text "TEXT" on the current screen. Additionally, new buttons with the text "GALLERY" and "CAMERA" have been added.

wait_until_activity(d, "MultimediaEditField")
d(textStartsWith="AUDIO RECORDING", resourceIdMatches=".*multimedia_edit_field_to_audio").click()
print("Touch on a button that has text 'AUDIO RECORDING': SUCCESS")
wait()
# Expected behaviour: After touching the "AUDIO RECORDING" button, it is replaced with buttons for "IMAGE" and "AUDIO CLIP" on the current screen.

wait_until_activity(d, "MultimediaEditField")
d(descriptionMatches=".*Navigate up").click()
print("Touch on a button that has content_desc 'Navigate up': SUCCESS")
wait()
# Expected behaviour: The button with content description "Navigate up" was pressed, causing the previous MultimediaEditField screen to transition to the current NoteEditor screen. The NoteEditor screen now displays various buttons and text fields for editing a note, including options for attaching multimedia content and managing tags and cards. (page changed from MultimediaEditField to NoteEditor)

"""
32. Attach a video clip to a flashcard.
"""
wait_until_activity(d, "NoteEditor")
d(descriptionMatches=".*Attach multimedia content to the Front field", resourceIdMatches=".*id_media_button").click()
print("Touch on a button that has content_desc 'Attach multimedia content to the Front field': SUCCESS")
wait()
# Expected behaviour: After touching on the "Attach multimedia content to the Front field" button, the previous NoteEditor screen transitions to the MultimediaEditField screen. The MultimediaEditField screen now contains buttons for adding an image and audio recording, and the focused textfield is for editing the Front field. (page changed from NoteEditor to MultimediaEditField)

wait_until_activity(d, "MultimediaEditField")
d(textStartsWith="IMAGE", resourceIdMatches=".*multimedia_edit_field_to_image").click()
print("Touch on a button that has text 'IMAGE': SUCCESS")
wait()
# Expected behaviour: After touching the button with text "IMAGE", it changed to a button with text "TEXT". Additionally, a button with text "GALLERY" and a button with text "CAMERA" appeared on the current screen.

wait_until_activity(d, "MultimediaEditField")
d(textStartsWith="GALLERY").click()
print("Touch on a button that has text 'GALLERY': SUCCESS")
wait()
# Expected behaviour: The performed action opened the Gallery app, showing the options to complete the action using Photos, with the choices of "Just Once", "Always", and "Use a different app". The screen also displays a list of options in the Gallery app. (page changed from MultimediaEditField to Resolver)

wait_until_activity(d, "Resolver")
d.click(359, 1179)
print("Touch on a button that has text 'Gallery': SUCCESS")
wait()
# Expected behaviour: The action of touching the "Gallery" button has successfully opened the Gallery app. The previous screen, which displayed options for completing the action using different apps, has been replaced by the current screen, which allows the user to select a photo. (page changed from Resolver to Gallery)

wait_until_activity(d, "Gallery")
d.press("back")
print("Press 'BACK' button to navigate back: SUCCESS")
wait()
# Expected behaviour: The action successfully navigated back to the previous screen, which is the Multimedia Edit Field. The previous screen had a "Select photo" textview and a "CANCEL" button, while the current screen has additional buttons and textviews for editing multimedia. (page changed from Gallery to MultimediaEditField)

wait_until_activity(d, "MultimediaEditField")
d(textStartsWith="CAMERA").click()
print("Touch on a button that has text 'CAMERA': SUCCESS")
wait()
# Expected behaviour: The action of touching the "CAMERA" button has changed the screen from the previous MultimediaEditField to the current Camera screen, where additional buttons and controls related to camera functions are displayed. (page changed from MultimediaEditField to Camera)

wait_until_activity(d, "Camera")
d(descriptionMatches=".*Shutter button", resourceIdMatches=".*shutter_button").click()
print("Touch on a button that has content_desc 'Shutter button': SUCCESS")
wait()
# Expected behaviour: After touching the "Shutter button", the previous screen in the Camera app has changed. The button with the resource_id "btn_cancel" has been replaced by two new buttons with resource_ids "btn_retake" and "btn_done".

wait_until_activity(d, "Camera")
d(resourceIdMatches=".*btn_done").click()
print("Touch on a button that has resource_id 'btn_done': SUCCESS")
wait()
# Expected behaviour: The previous Camera screen has been replaced with the MultimediaEditField screen, which includes options for editing text and audio recordings, as well as buttons for navigating, accessing more options, and selecting from the gallery or camera. (page changed from Camera to MultimediaEditField)

wait_until_activity(d, "MultimediaEditField")
d(textStartsWith="TEXT", resourceIdMatches=".*multimedia_edit_field_to_text").click()
print("Touch on a button that has text 'TEXT': SUCCESS")
wait()
# Expected behaviour: After touching the button with the text "TEXT", the button's text has changed to "IMAGE". Additionally, new buttons with the text "CLONE FROM" and "CLEAR" have appeared, and the buttons with the text "GALLERY" and "CAMERA" are no longer present.

wait_until_activity(d, "MultimediaEditField")
d.press("back")
print("Press 'BACK' button to navigate back: SUCCESS")
wait()
# Expected behaviour: Navigating back from the MultimediaEditField screen to the NoteEditor screen, the "Navigate up" button is now present at the top left corner of the screen, and the "Editing field" textview has been replaced with "Edit note". The buttons for adding multimedia content, saving, and more options have also been adjusted. (page changed from MultimediaEditField to NoteEditor)

wait_until_activity(d, "NoteEditor")
d(descriptionMatches=".*Attach multimedia content to the Back field", resourceIdMatches=".*id_media_button").click()
print("Touch on a button that has content_desc 'Attach multimedia content to the Back field': SUCCESS")
wait()
# Expected behaviour: The touch on the "Attach multimedia content to the Back field" button in the NoteEditor screen opens the MultimediaEditField screen, which displays options to attach multimedia content such as images and audio recordings to the editing field. (page changed from NoteEditor to MultimediaEditField)

wait_until_activity(d, "MultimediaEditField")
d.press("back")
print("Press 'BACK' button to navigate back: SUCCESS")
wait()
# Expected behaviour: The "BACK" button press navigated back to the previous screen, which is the Note Editor screen. The screen contains a "Save" button instead of a "Done" button, and the textview now displays "Edit note" instead of "Editing field". Other changes include the presence of dropdown fields for card type and card deck selection, as well as different textfields for front and back card content. (page changed from MultimediaEditField to NoteEditor)

wait_until_activity(d, "NoteEditor")
d(descriptionMatches=".*Attach multimedia content to the Front field", resourceIdMatches=".*id_media_button").click()
print("Touch on a button that has content_desc 'Attach multimedia content to the Front field': SUCCESS")
wait()
# Expected behaviour: After touching the button with the content description "Attach multimedia content to the Front field", the current screen now displays options to attach images and audio recordings to the editing field, along with buttons for translation and pronunciation. (page changed from NoteEditor to MultimediaEditField)

"""
33. Translate a word or phrase in the editable field.
"""
wait_until_activity(d, "MultimediaEditField")
d(textStartsWith=">What is the difference between a linked list and an array?").set_text(">What is the difference between a linked list and an array?")
print("Fill a focused textfield that has text '>What is the difference between a linked list and [...]' with '>What is the difference between a linked list and an array?': SUCCESS")
wait()
# Expected behaviour: The performed action successfully filled the focused textfield with the text ">What is the difference between a linked list and an array?", replacing the previous text "a>What is the difference between a linked list and an array?".

wait_until_activity(d, "MultimediaEditField")
d(textStartsWith="TRANSLATION").click()
print("Touch on a button that has text 'TRANSLATION': SUCCESS")
wait()
# Expected behaviour: After touching the "TRANSLATION" button, a popup message briefly appeared and disappeared, showing the message "Dictionary usually expects one word". The current screen now displays a "Pick dictionary" textview and buttons for "Glosbe.com" and "ColorDict".

wait_until_activity(d, "MultimediaEditField")
d(textStartsWith="Glosbe.com", resourceIdMatches=".*text1").click()
print("Touch on a button that has text 'Glosbe.com': SUCCESS")
wait()
# Expected behaviour: After touching the button with text "Glosbe.com", the previous screen, which had a button with text "Glosbe.com", has been replaced with a new screen that displays a translation interface with options to select the source and target languages, and a button to perform the translation. (page changed from MultimediaEditField to Translation)

wait_until_activity(d, "Translation")
d(textStartsWith="Arabic").click()
print("Touch on a dropdown field that has text 'Arabic': SUCCESS")
wait()
# Expected behaviour: By touching on the dropdown field with the text "Arabic", the dropdown expands and displays a list of buttons with different language options to choose from.

wait_until_activity(d, "Translation")
d(textStartsWith="Arabic", resourceIdMatches=".*text1").click()
print("Touch on a checked button that has text 'Arabic': SUCCESS")
wait()
# Expected behaviour: After touching on the checked button with the text "Arabic", the previous screen with multiple language buttons has been replaced with a translation screen that includes dropdown fields for selecting the translation language and a button for translation.

wait_until_activity(d, "Translation")
d(textStartsWith="TRANSLATE").click()
print("Touch on a button that has text 'TRANSLATE': SUCCESS")
wait()
# Expected behaviour: The "Translation" screen is replaced with the "MultimediaEditField" screen, which includes options for editing and adding multimedia content to the translation. (page changed from Translation to MultimediaEditField)

wait_until_activity(d, "MultimediaEditField")
d(textStartsWith="a>What is the difference between a linked list and an array?").set_text("array")
print("Fill a focused textfield that has text 'a>What is the difference between a linked list and[...]' with 'array': SUCCESS")
wait()
# Expected behaviour: The focused textfield that previously contained the text "a>What is the difference between a linked list and an array?" is now updated with the word "betweenarray".

wait_until_activity(d, "MultimediaEditField")
d(textStartsWith="betweenarray").set_text("array")
print("Fill a focused textfield that has text 'betweenarray' with 'array': SUCCESS")
wait()
# Expected behaviour: The focused textfield that had the text "betweenarray" has been updated to now have the text "array".

wait_until_activity(d, "MultimediaEditField")
d(textStartsWith="TRANSLATION").click()
print("Touch on a button that has text 'TRANSLATION': SUCCESS")
wait()
# Expected behaviour: After touching the "TRANSLATION" button, the previous screen with various editing options has changed to a new screen with options for picking a dictionary, including "Glosbe.com" and "ColorDict".

wait_until_activity(d, "MultimediaEditField")
d(textStartsWith="Glosbe.com", resourceIdMatches=".*text1").click()
print("Touch on a button that has text 'Glosbe.com': SUCCESS")
wait()
# Expected behaviour: By touching on the button with text "Glosbe.com", the previous screen with a button for selecting a dictionary has been replaced with a new screen for translation. The new screen includes options for selecting the source and target languages, as well as a button for initiating the translation. (page changed from MultimediaEditField to Translation)

wait_until_activity(d, "Translation")
d(textStartsWith="TRANSLATE").click()
print("Touch on a button that has text 'TRANSLATE': SUCCESS")
wait()
# Expected behaviour: After touching the "TRANSLATE" button, the previous translation screen is replaced with a new multimedia editing field screen, which includes options for image and audio recording, as well as buttons for cloning, clearing, and searching for translation and pronunciation. (page changed from Translation to MultimediaEditField)

wait_until_activity(d, "MultimediaEditField")
d(textStartsWith="array").set_text("algorithm")
print("Fill a focused textfield that has text 'array' with 'algorithm': SUCCESS")
wait()
# Expected behaviour: The focused textfield that previously had the text "array" now has the text "algorithm".

wait_until_activity(d, "MultimediaEditField")
d(textStartsWith="CLEAR").click()
print("Touch on a button that has text 'CLEAR': SUCCESS")
wait()
# Expected behaviour: After touching the "CLEAR" button, the focused textfield that had the text "algorithm" in the previous screen is now empty.

"""
34. Translate a single word using the translation function on the MultimediaEditField page.
"""
wait_until_activity(d, "MultimediaEditField")
d.click(360, 165)
d.send_keys("<Please provide the single word that Jade Green wants to translate>")
print("Fill a focused textfield with '<Please provide the single word that Jade Green wants to translate>': SUCCESS")
wait()
# Expected behaviour: The focused textfield has been successfully filled with the word "<Please provide the single word that Jade Green wants to translate>".

wait_until_activity(d, "MultimediaEditField")
d(textStartsWith="TRANSLATION").click()
print("Touch on a button that has text 'TRANSLATION': SUCCESS")
wait()
# Expected behaviour: After touching the "TRANSLATION" button, a new screen appeared with options to pick a dictionary, including "Glosbe.com" and "ColorDict". A popup message briefly appeared and disappeared, stating that the dictionary usually expects one word.

wait_until_activity(d, "MultimediaEditField")
d(textStartsWith="Glosbe.com", resourceIdMatches=".*text1").click()
print("Touch on a button that has text 'Glosbe.com': SUCCESS")
wait()
# Expected behaviour: After touching the button labeled "Glosbe.com", the previous screen with a MultimediaEditField widget is replaced with a new screen displaying a Translation widget. The new screen includes options to select the source and target languages, and a button to translate the text. Additionally, there is a "Powered by glosbe.com" message displayed. (page changed from MultimediaEditField to Translation)

wait_until_activity(d, "Translation")
d(textStartsWith="Arabic").click()
print("Touch on a dropdown field that has text 'Arabic': SUCCESS")
wait()
# Expected behaviour: After touching on the dropdown field with the text "Arabic", the dropdown expands and shows a list of language options to choose from. The selected language "Arabic" is now checked.

wait_until_activity(d, "Translation")
d.press("back")
print("Press 'BACK' button to navigate back: SUCCESS")
wait()
# Expected behaviour: After pressing the "BACK" button, the previous page with a checked button and multiple language buttons has been replaced with a translation page that includes textviews, dropdown fields, and a "TRANSLATE" button.

"""
35. Translate a phrase from English to French.
"""
wait_until_activity(d, "Translation")
d(textStartsWith="Arabic").click()
print("Touch on a dropdown field that has text 'Arabic': SUCCESS")
wait()
# Expected behaviour: The dropdown field that previously had the text "Arabic" has been replaced with a checked button that also displays "Arabic", and a list of language options has appeared below it.

wait_until_activity(d, "Translation")
d(textStartsWith="English", resourceIdMatches=".*text1").click()
print("Touch on a button that has text 'English': SUCCESS")
wait()
# Expected behaviour: By touching the "English" button, the translation page is updated with a dropdown field that has "English" selected as the source language and "Arabic" selected as the target language, along with other translation-related elements.

"""
36. Change the target language from Arabic to French on the Translation page.
"""
wait_until_activity(d, "Translation")
d(textStartsWith="Arabic").click()
print("Touch on a dropdown field that has text 'Arabic': SUCCESS")
wait()
# Expected behaviour: After touching on the dropdown field, the selected language changed to "Arabic" and additional language options are displayed as buttons.

wait_until_activity(d, "Translation")
d(textStartsWith="French", resourceIdMatches=".*text1").click()
print("Touch on a button that has text 'French': SUCCESS")
wait()
# Expected behaviour: After touching on the "French" button, the previous translation screen is updated with a new dropdown field that has "French" selected as the target language, along with other textviews and a button for translation.

"""
37. Translate a simple English phrase to French.
"""
wait_until_activity(d, "Translation")
d(textStartsWith="French").click()
print("Touch on a dropdown field that has text 'French': SUCCESS")
wait()
# Expected behaviour: After touching on the dropdown field with the text "French," the dropdown expands and shows a list of other language options, including Croatian, Czech, Dutch, English, French (selected), German, Hindi, Hungarian, Italian, Japanese, Polish, Portuguese, Russian, Spanish, Swedish, Turkish, and Vietnamese.

"""
38. Translate an English phrase to French using the translation functionality of the app.
"""
wait_until_activity(d, "Translation")
d(textStartsWith="English", resourceIdMatches=".*text1").click()
print("Touch on a button that has text 'English': SUCCESS")
wait()
# Expected behaviour: After touching on the "English" button, the previous screen with a list of language options has been replaced with a translation screen, where there are dropdown fields to select the source and target languages, a "TRANSLATE" button, and some informational text.

wait_until_activity(d, "Translation")
d(textStartsWith="English").click()
print("Touch on a dropdown field that has text 'English': SUCCESS")
wait()
# Expected behaviour: After touching on the dropdown field with the text "English", the previous dropdown field is replaced with a scrollable list of buttons containing different language options.

wait_until_activity(d, "Translation")
d(textStartsWith="French", resourceIdMatches=".*text1").click()
print("Touch on a button that has text 'French': SUCCESS")
wait()
# Expected behaviour: After touching on the button with the text "French", the previous screen, which displayed a list of language buttons, has been replaced with a new screen that includes dropdown fields for selecting the translation languages and a "TRANSLATE" button.

wait_until_activity(d, "Translation")
d(textStartsWith="TRANSLATE").click()
print("Touch on a button that has text 'TRANSLATE': SUCCESS")
wait()
# Expected behaviour: After touching on the "TRANSLATE" button, the previous Translation screen is replaced with the MultimediaEditField screen, which provides various options for editing and multimedia input. (page changed from Translation to MultimediaEditField)

wait_until_activity(d, "MultimediaEditField")
d.press("back")
print("Press 'BACK' button to navigate back: SUCCESS")
wait()
# Expected behaviour: The previous screen was a MultimediaEditField where the user was editing a field with the text "Editing field". After pressing the "BACK" button, the current screen is a NoteEditor where the user can edit a note with the text "Edit note". (page changed from MultimediaEditField to NoteEditor)

wait_until_activity(d, "NoteEditor")
d(textStartsWith=">What is the difference between a linked list and an array?", descriptionMatches=".*Front", resourceIdMatches=".*id_note_editText").set_text(">What is the difference between a linked list and an array?")
print("Fill a focused textfield that has text '>What is the difference between a linked list and [...]' with '>What is the difference between a linked list and an array?': SUCCESS")
wait()
# Expected behaviour: The focused textfield in the NoteEditor screen now contains the text "between>What is the difference between a linked list and an array?", replacing the previous text.

wait_until_activity(d, "NoteEditor")
d(textStartsWith="between>What is the difference between a linked list and an array?", descriptionMatches=".*Front", resourceIdMatches=".*id_note_editText").set_text("What is the difference between a linked list and an array?")
print("Fill a focused textfield that has text 'between>What is the difference between a linked li[...]' with 'What is the difference between a linked list and an array?': SUCCESS")
wait()
# Expected behaviour: The text "between>What is the difference between a linked list and an array?" in the focused textfield has been replaced with "differenceWhat is the difference between a linked list and an array?".

wait_until_activity(d, "NoteEditor")
d(textStartsWith="differenceWhat is the difference between a linked list and an array?", descriptionMatches=".*Front", resourceIdMatches=".*id_note_editText").set_text("What is the difference between a linked list and an array?")
print("Fill a focused textfield that has text 'differenceWhat is the difference between a linked [...]' with 'What is the difference between a linked list and an array?': SUCCESS")
wait()
wait_until_activity(d, "NoteEditor")
d(descriptionMatches=".*Navigate up").click()
print("Touch on a button that has content_desc 'Navigate up': SUCCESS")
wait()
# Expected behaviour: The action of touching the "Navigate up" button in the NoteEditor screen has changed the buttons on the current screen to "Close and lose current input?", "CANCEL", and "OK".

wait_until_activity(d, "NoteEditor")
d(textStartsWith="CANCEL", resourceIdMatches=".*md_buttonDefaultNegative").click()
print("Touch on a button that has text 'CANCEL': SUCCESS")
wait()
# Expected behaviour: The touch on the "CANCEL" button in the NoteEditor screen has resulted in the appearance of additional buttons, a dropdown field, and textfields related to editing and saving notes.

wait_until_activity(d, "NoteEditor")
d(textStartsWith="differenceWhat is the difference between a linked list and an array?", descriptionMatches=".*Front", resourceIdMatches=".*id_note_editText").set_text("What is the difference between a linked list and an array?")
print("Fill a focused textfield that has text 'differenceWhat is the difference between a linked [...]' with 'What is the difference between a linked list and an array?': SUCCESS")
wait()
wait_until_activity(d, "NoteEditor")
d(descriptionMatches=".*Navigate up").click()
print("Touch on a button that has content_desc 'Navigate up': SUCCESS")
wait()
# Expected behaviour: After touching the "Navigate up" button, the current screen shows a confirmation prompt with the options "CANCEL" and "OK" to close and lose the current input.

wait_until_activity(d, "NoteEditor")
d(textStartsWith="CANCEL", resourceIdMatches=".*md_buttonDefaultNegative").click()
print("Touch on a button that has text 'CANCEL': SUCCESS")
wait()
# Expected behaviour: After touching on the "CANCEL" button, the screen changed to a NoteEditor screen with additional widgets such as a dropdown field for "Type" and "Card deck," a focused textfield for editing the note, and buttons for attaching multimedia content.

"""
39. Attach a video to a flashcard and preview it in the VideoPlayer page.
"""
wait_until_activity(d, "NoteEditor")
d(descriptionMatches=".*Attach multimedia content to the Front field", resourceIdMatches=".*id_media_button").click()
print("Touch on a button that has content_desc 'Attach multimedia content to the Front field': SUCCESS")
wait()
# Expected behaviour: After touching the button with content description "Attach multimedia content to the Front field", the previous NoteEditor screen has changed to the MultimediaEditField screen. The new screen includes buttons for adding images and audio recordings to the editing field. (page changed from NoteEditor to MultimediaEditField)

wait_until_activity(d, "MultimediaEditField")
d(textStartsWith="IMAGE", resourceIdMatches=".*multimedia_edit_field_to_image").click()
print("Touch on a button that has text 'IMAGE': SUCCESS")
wait()
# Expected behaviour: The button with the text "IMAGE" has been changed to a button with the text "TEXT" on the current screen.

wait_until_activity(d, "MultimediaEditField")
d.press("back")
print("Press 'BACK' button to navigate back: SUCCESS")
wait()
# Expected behaviour: The "BACK" button press navigated the user back to the NoteEditor screen, where they can edit and save their note. The previous MultimediaEditField screen had options for text and audio recording, while the current NoteEditor screen has options for saving and attaching multimedia content to the note. (page changed from MultimediaEditField to NoteEditor)

wait_until_activity(d, "NoteEditor")
d(descriptionMatches=".*Attach multimedia content to the Back field", resourceIdMatches=".*id_media_button").click()
print("Touch on a button that has content_desc 'Attach multimedia content to the Back field': SUCCESS")
wait()
# Expected behaviour: After touching the "Attach multimedia content to the Back field" button, the current screen shows additional options for attaching multimedia content to the editing field, such as "IMAGE" and "AUDIO RECORDING". (page changed from NoteEditor to MultimediaEditField)

wait_until_activity(d, "MultimediaEditField")
d(descriptionMatches=".*More options").click()
print("Touch on a button that has content_desc 'More options': SUCCESS")
wait()
# Expected behaviour: After touching on the "More options" button, a new button labeled "Audio Clip" is added to the current screen in the MultimediaEditField.

wait_until_activity(d, "MultimediaEditField")
d.press("back")
print("Press 'BACK' button to navigate back: SUCCESS")
wait()
# Expected behaviour: Pressing the "BACK" button navigates back to the previous screen, which is a Multimedia edit field. The current screen shows various buttons for different multimedia options, a search field, and options for cloning and clearing the field.

wait_until_activity(d, "MultimediaEditField")
d(descriptionMatches=".*More options").click()
print("Touch on a button that has content_desc 'More options': SUCCESS")
wait()
# Expected behaviour: After touching on the "More options" button, a new button labeled "Audio Clip" has been added to the current screen.

wait_until_activity(d, "MultimediaEditField")
d(textStartsWith="Audio Clip").click()
print("Touch on a button that has text 'Audio Clip': SUCCESS")
wait()
# Expected behaviour: After touching the "Audio Clip" button, the previous MultimediaEditField screen is replaced with a new MultimediaEditField screen that has additional buttons and a textview, as well as a different button with the text "Audio Clip" being replaced with a button with the content description "Navigate up".

wait_until_activity(d, "MultimediaEditField")
d(descriptionMatches=".*More options").click()
print("Touch on a button that has content_desc 'More options': SUCCESS")
wait()
# Expected behaviour: After touching the "More options" button, a new button labeled "Audio recording" is added to the current screen, along with other existing elements.

wait_until_activity(d, "MultimediaEditField")
d(textStartsWith="Audio recording").click()
print("Touch on a button that has text 'Audio recording': SUCCESS")
wait()
# Expected behaviour: After touching the "Audio recording" button, the previous screen, which only had the "Audio recording" button, is replaced with a current screen that has additional buttons and a textview, as well as a button with the text "Navigate up" replacing the "Audio recording" button.

wait_until_activity(d, "MultimediaEditField")
d.press("back")
print("Press 'BACK' button to navigate back: SUCCESS")
wait()
# Expected behaviour: The "BACK" button press navigates back to the previous screen, changing the widgets displayed from a MultimediaEditField to a NoteEditor. The NoteEditor screen now includes options to save, access more options, and edit the note's content and attributes. (page changed from MultimediaEditField to NoteEditor)

wait_until_activity(d, "NoteEditor")
d(descriptionMatches=".*More options").click()
print("Touch on a button that has content_desc 'More options': SUCCESS")
wait()
# Expected behaviour: After touching on the "More options" button, a new button labeled "Add note" and a button labeled "Copy note" appeared on the current screen.

wait_until_activity(d, "NoteEditor")
d(textStartsWith="Add note").click()
print("Touch on a button that has text 'Add note': SUCCESS")
wait()
# Expected behaviour: After touching the "Add note" button, the NoteEditor screen is updated to include additional fields such as "Type", "Deck", "Front", "Field1", "CustomField", "Tags", and "Cards".

"""
40. Navigate to the Info page by clicking on the "Navigate up" button from the current NoteEditor page, and then explore the Info page.
"""
wait_until_activity(d, "NoteEditor")
d(descriptionMatches=".*Navigate up").click()
print("Touch on a button that has content_desc 'Navigate up': SUCCESS")
wait()
# Expected behaviour: By touching on the "Navigate up" button, the user has changed the screen from "NoteEditor" to "NoteEditor". The textview displaying "Add note" has been changed to "Edit note" and a new button with content_desc "More options" has been added. The dropdown field for "Deck" has been changed to "Basic (and reversed card)" and the dropdown field for "Card deck" has been changed to "My Filtered Deck". The focused textfield for "Front" has been changed to "differenceWhat is the difference between a linked list and an array?". The button for attaching multimedia content to the "Back" field has been added and the button for "Cards" now displays "Card 1, Card 2".

wait_until_activity(d, "NoteEditor")
d(descriptionMatches=".*More options").click()
print("Touch on a button that has content_desc 'More options': SUCCESS")
wait()
# Expected behaviour: The action of touching the "More options" button in the NoteEditor screen resulted in the addition of two new buttons, "Add note" and "Copy note", to the current screen.

wait_until_activity(d, "NoteEditor")
d.press("back")
print("Press 'BACK' button to navigate back: SUCCESS")
wait()
# Expected behaviour: The "BACK" button successfully navigated back to the previous screen, which is the NoteEditor screen. The previous screen contains buttons such as "Add note" and "Copy note" along with various text views and dropdown fields for editing a note.

wait_until_activity(d, "NoteEditor")
d(descriptionMatches=".*More options").click()
print("Touch on a button that has content_desc 'More options': SUCCESS")
wait()
# Expected behaviour: The button "Add note" has been added to the current screen, along with the existing buttons "Copy note" and "More options".

wait_until_activity(d, "NoteEditor")
d(textStartsWith="Copy note").click()
print("Touch on a button that has text 'Copy note': SUCCESS")
wait()
# Expected behaviour: The action of touching the "Copy note" button in the NoteEditor screen has resulted in several changes. The "Add note" button has been replaced with a "Navigate up" button, and additional elements such as a "Save" button, dropdown fields for "Type" and "Deck," and textfields for "Front" and "CustomField" have been added.

wait_until_activity(d, "NoteEditor")
d(descriptionMatches=".*Navigate up").click()
print("Touch on a button that has content_desc 'Navigate up': SUCCESS")
wait()
# Expected behaviour: After touching the "Navigate up" button, the current screen shows a dialog box with the options to close and lose the current input or cancel and keep the input.

wait_until_activity(d, "NoteEditor")
d(textStartsWith="CANCEL", resourceIdMatches=".*md_buttonDefaultNegative").click()
print("Touch on a button that has text 'CANCEL': SUCCESS")
wait()
# Expected behaviour: The action of touching the "CANCEL" button in the NoteEditor screen resulted in the appearance of additional widgets such as a button with content description "Navigate up" and a textview with the text "Add note". Additionally, the "Close and lose current input?" button and the "OK" button were replaced by the "CANCEL" button.

wait_until_activity(d, "NoteEditor")
d(descriptionMatches=".*Navigate up").click()
print("Touch on a button that has content_desc 'Navigate up': SUCCESS")
wait()
# Expected behaviour: After touching on the "Navigate up" button, the previous NoteEditor screen is replaced by a new NoteEditor screen with additional buttons for closing and saving the current input.

wait_until_activity(d, "NoteEditor")
d(textStartsWith="OK", resourceIdMatches=".*md_buttonDefaultPositive").click()
print("Touch on a button that has text 'OK': SUCCESS")
wait()
# Expected behaviour: After touching on the "OK" button, the previous screen of NoteEditor is replaced with the current screen of NoteEditor, which includes various widgets such as a textview for editing notes, dropdown fields for selecting card types and decks, and textfields for inputting front and back content of the cards.

wait_until_activity(d, "NoteEditor")
d(descriptionMatches=".*More options").click()
print("Touch on a button that has content_desc 'More options': SUCCESS")
wait()
# Expected behaviour: After touching the "More options" button, a new button with the text "Add note" and another button with the text "Copy note" appeared on the current screen.

wait_until_activity(d, "NoteEditor")
d(textStartsWith="Add note").click()
print("Touch on a button that has text 'Add note': SUCCESS")
wait()
# Expected behaviour: After touching the "Add note" button, the NoteEditor screen has changed. The button "Add note" has been replaced with a button with content description "Navigate up", and several new widgets have appeared, including a textview for "Add note", a button for "Save", dropdown fields for "Type" and "Deck", and textfields for "Front", "Field1", and "CustomField".

wait_until_activity(d, "NoteEditor")
d(descriptionMatches=".*Navigate up").click()
print("Touch on a button that has content_desc 'Navigate up': SUCCESS")
wait()
# Expected behaviour: The performed action of touching the "Navigate up" button on the previous screen has changed the text of the "Add note" TextView to "Edit note" on the current screen. Additionally, a new button with content description "More options" has been added. The dropdown field for "Deck" has been changed to "Basic (and reversed card)" and the dropdown field for "Card deck" has been changed to "My Filtered Deck". The focused textfield for the "Front" field now has the text "What is the difference between a linked list and an array?". The "Back" textfield has been changed to "sound:ankidroid_audioclip_Heartbeat372766725The mitochondria are the powerhouse of the cell." The "Cards" button now displays "Card 1, Card 2".

wait_until_activity(d, "NoteEditor")
d(resourceIdMatches=".*CardEditorCardsButton").click()
print("Touch on a button that has text 'Cards: Card 1, Card 2': SUCCESS")
wait()
# Expected behaviour: After touching the "Cards: Card 1, Card 2" button, the current screen shows a new section with two buttons labeled "CARD 1" and "CARD 2" for selecting different card templates. (page changed from NoteEditor to CardTemplateEditor)

"""
41. Navigate to the Info page and read the information about the app.
"""
wait_until_activity(d, "CardTemplateEditor")
d(descriptionMatches=".*Navigate up").click()
print("Touch on a button that has content_desc 'Navigate up': SUCCESS")
wait()
# Expected behaviour: After touching the "Navigate up" button, the screen transitions from the CardTemplateEditor to the NoteEditor. The previous screen had a textview with the text "Card types" and buttons with the text "CARD 1" and "CARD 2", while the current screen displays a textview with the text "Edit note" and a dropdown field with the text "Basic (and reversed card)". The current screen also includes a textfield for the front and back templates, as well as options to attach multimedia content. (page changed from CardTemplateEditor to NoteEditor)

wait_until_activity(d, "NoteEditor")
d(descriptionMatches=".*Navigate up").click()
print("Touch on a button that has content_desc 'Navigate up': SUCCESS")
wait()
# Expected behaviour: After touching the "Navigate up" button, the NoteEditor screen has changed. The previous buttons and textfields have been replaced with buttons for closing the current input and cancelling or confirming the action.

wait_until_activity(d, "NoteEditor")
d.press("back")
print("Press 'BACK' button to navigate back: SUCCESS")
wait()
# Expected behaviour: The "BACK" button press navigated back to the previous screen, which is the NoteEditor screen. The screen has changed and now displays options for saving the note, navigating up, and more options, as well as fields for editing the note's type, card deck, front, and back.

wait_until_activity(d, "NoteEditor")
d(descriptionMatches=".*More options").click()
print("Touch on a button that has content_desc 'More options': SUCCESS")
wait()
# Expected behaviour: The touch on the "More options" button in the NoteEditor screen has added two new buttons to the screen - "Add note" and "Copy note".

wait_until_activity(d, "NoteEditor")
d.press("back")
print("Press 'BACK' button to navigate back: SUCCESS")
wait()
# Expected behaviour: The "BACK" button was pressed and the user was navigated back to the previous screen, where the NoteEditor is displayed with the previous note details and options for editing and saving the note.

wait_until_activity(d, "NoteEditor")
d(descriptionMatches=".*More options").click()
print("Touch on a button that has content_desc 'More options': SUCCESS")
wait()
# Expected behaviour: After touching the "More options" button, a new button labeled "Add note" and another button labeled "Copy note" appeared on the screen.

wait_until_activity(d, "NoteEditor")
d.press("back")
print("Press 'BACK' button to navigate back: SUCCESS")
wait()
# Expected behaviour: The "Add note" and "Copy note" buttons have been replaced with a "Navigate up" button, an "Edit note" textview, a "Save" button, a "More options" button, and various dropdown fields and textfields for editing the note. The "Tags" and "Cards" buttons also display the specific cards associated with the note.

wait_until_activity(d, "NoteEditor")
d(descriptionMatches=".*More options").click()
print("Touch on a button that has content_desc 'More options': SUCCESS")
wait()
# Expected behaviour: After touching on the "More options" button, a new button with text "Add note" and another button with text "Copy note" appeared on the current screen.

wait_until_activity(d, "NoteEditor")
d.press("back")
print("Press 'BACK' button to navigate back: SUCCESS")
wait()
# Expected behaviour: Pressing the "BACK" button navigated back to the NoteEditor screen, where the "Add note" and "Copy note" buttons were replaced with a "Navigate up" button, an "Edit note" textview, a "Save" button, a "More options" button, dropdown fields for "Type" and "Card deck," a "Front" textview with a focused textfield, a "Back" textview with a textfield, and buttons for attaching multimedia content, tags, and cards.

wait_until_activity(d, "NoteEditor")
d(descriptionMatches=".*Navigate up").click()
print("Touch on a button that has content_desc 'Navigate up': SUCCESS")
wait()
# Expected behaviour: The touch on the "Navigate up" button in the NoteEditor screen resulted in the appearance of three new buttons: "Close and lose current input?", "CANCEL", and "OK".

wait_until_activity(d, "NoteEditor")
d(textStartsWith="OK", resourceIdMatches=".*md_buttonDefaultPositive").click()
print("Touch on a button that has text 'OK': SUCCESS")
wait()
# Expected behaviour: After touching the "OK" button, the previous NoteEditor screen is replaced with the current CardBrowser screen. The CardBrowser screen displays a list of study cards with their corresponding questions and answers. (page changed from NoteEditor to CardBrowser)

wait_until_activity(d, "CardBrowser")
d(descriptionMatches=".*More options").click()
print("Touch on a button that has content_desc 'More options': SUCCESS")
wait()
# Expected behaviour: After touching the "More options" button, several new buttons have appeared on the screen, including "Change display order", "Filter marked", "Filter suspended", "Filter by tag", "Preview", and "Select all".

wait_until_activity(d, "CardBrowser")
d(textStartsWith="Change display order").click()
print("Touch on a button that has text 'Change display order': SUCCESS")
wait()
# Expected behaviour: After touching the "Change display order" button, the previous screen with a button is replaced by a current screen with a textview and multiple buttons representing different sorting options.

"""
42. Navigate to the Info page to learn more about the app's functionalities and usage.
"""
wait_until_activity(d, "CardBrowser")
d.press("back")
print("Press 'BACK' button to navigate back: SUCCESS")
wait()
# Expected behaviour: After pressing the "BACK" button, the current screen shows the previous CardBrowser screen with a focused listview displaying the cards.

wait_until_activity(d, "CardBrowser")
d(descriptionMatches=".*Navigate up").click()
print("Touch on a button that has content_desc 'Navigate up': SUCCESS")
wait()
# Expected behaviour: After touching the "Navigate up" button, the current screen shows additional buttons for "Decks", "Statistics", "Settings", "Help", and "Send feedback". The previous screen displayed a button for "Card browser" which is now checked.

wait_until_activity(d, "CardBrowser")
d(textStartsWith="Help").click()
print("Touch on a button that has text 'Help': SUCCESS")
wait()
wait_until_activity(d, "CardBrowser")
d.app_start("com.ichi2.anki")
print("Open the app again because the previous action led to closing the app: SUCCESS")
wait()
# Expected behaviour: After touching the "Help" button, the screen remains the same with no visible changes.

wait_until_activity(d, "CardBrowser")
d(descriptionMatches=".*More options").click()
print("Touch on a button that has content_desc 'More options': SUCCESS")
wait()
# Expected behaviour: By touching on the "More options" button, additional options such as "Change display order," "Filter marked," "Filter suspended," "Filter by tag," "Preview," and "Select all" are now visible on the screen.

wait_until_activity(d, "CardBrowser")
d.press("back")
print("Press 'BACK' button to navigate back: SUCCESS")
wait()
# Expected behaviour: The "BACK" button press navigated back to the previous screen, where the "Change display order", "Filter marked", "Filter suspended", "Filter by tag", "Preview", and "Select all" buttons are visible again, along with the card items in the listview.

wait_until_activity(d, "CardBrowser")
d(descriptionMatches=".*More options").click()
print("Touch on a button that has content_desc 'More options': SUCCESS")
wait()
# Expected behaviour: After touching on the "More options" button, several new buttons have appeared on the current screen, including "Change display order," "Filter marked," "Filter suspended," "Filter by tag," "Preview," and "Select all."

wait_until_activity(d, "CardBrowser")
d(textStartsWith="Filter by tag").click()
print("Touch on a button that has text 'Filter by tag': SUCCESS")
wait()
# Expected behaviour: The button "Filter by tag" has been replaced with a textview "Select tags" and buttons with content descriptions "Filter tags" and "Check/uncheck all tags". Additionally, a textview "You haven't added any tags yet" and buttons with text "All cards", "New", "Due", "CANCEL", and "SELECT" have been added.

wait_until_activity(d, "CardBrowser")
d(textStartsWith="SELECT", resourceIdMatches=".*md_buttonDefaultPositive").click()
print("Touch on a button that has text 'SELECT': SUCCESS")
wait()
# Expected behaviour: After touching the "SELECT" button, the screen changed to a different view called "CardBrowser" where a list of flashcards is displayed along with their corresponding questions and answers.

wait_until_activity(d, "CardBrowser")
d.press("back")
print("Press 'BACK' button to navigate back: SUCCESS")
wait()
# Expected behaviour: After pressing the "BACK" button, the user navigated back from the CardBrowser screen to the DeckPicker screen. The current screen now displays the deck "My Filtered Deck" with a text showing that 5 cards were studied in 3 minutes today. (page changed from CardBrowser to DeckPicker)

wait_until_activity(d, "DeckPicker")
d(descriptionMatches=".*More options").click()
print("Touch on a button that has content_desc 'More options': SUCCESS")
wait()
# Expected behaviour: After touching on the "More options" button, the previous screen (DeckPicker) is replaced with a current screen (DeckPicker) that now includes additional buttons for creating a filtered deck, checking the database and media, emptying cards, restoring from backup, managing note types, importing, and exporting the collection.

wait_until_activity(d, "DeckPicker")
d(textStartsWith="Create filtered deck").click()
print("Touch on a button that has text 'Create filtered deck': SUCCESS")
wait()
# Expected behaviour: After touching on the button "Create filtered deck", the previous screen with multiple buttons is replaced by a current screen with a textview showing "Create deck", a focused textfield for entering a deck name, and two buttons labeled "CANCEL" and "CREATE".

wait_until_activity(d, "DeckPicker")
d(textStartsWith="Filtered Deck 1").set_text("Jade's Custom Deck")
print("Fill a focused textfield that has text 'Filtered Deck 1' with 'Jade's Custom Deck': SUCCESS")
wait()
# Expected behaviour: The focused textfield in the DeckPicker screen has been updated from "Filtered Deck 1" to "Jade's Custom Deck" after filling it with the new text.

wait_until_activity(d, "DeckPicker")
d.press("back")
print("Press 'BACK' button to navigate back: SUCCESS")
wait()
"""
43. Create a custom deck named "Computer Science Quiz".
"""
wait_until_activity(d, "DeckPicker")
d(textStartsWith="Jade's Custom Deck").set_text("Computer Science Quiz")
print("Fill a focused textfield that has text 'Jade's Custom Deck' with 'Computer Science Quiz': SUCCESS")
wait()
# Expected behaviour: The focused textfield in the DeckPicker screen was updated from "Jade's Custom Deck" to "DeckComputer Science Quiz" after filling it with "Computer Science Quiz".

wait_until_activity(d, "DeckPicker")
d(textStartsWith="CREATE", resourceIdMatches=".*md_buttonDefaultPositive").click()
print("Touch on a button that has text 'CREATE': SUCCESS")
wait()
# Expected behaviour: By touching on the "CREATE" button, the previous screen (DeckPicker) has been replaced with the current screen (FilteredDeckOptions), which displays various options for creating a new deck, such as search, limit, rescheduling, and defining custom steps. (page changed from DeckPicker to FilteredDeckOptions)

"""
44. Define custom steps for the "Computer Science Quiz" deck.
"""
wait_until_activity(d, "FilteredDeckOptions")
d.click(360, 609)
print("Touch on a button that has text 'Define custom steps': SUCCESS")
wait()
# Expected behaviour: After touching the "Define custom steps" button, the screen has been updated to include additional elements such as a textview displaying "Custom steps (in minutes)", another textview displaying "1 10", and a button. The checkbox has also changed to a checked state.

wait_until_activity(d, "FilteredDeckOptions")
d.click(360, 695)
print("Touch on a button that has text 'Custom steps (in minutes), 1 10': SUCCESS")
wait()
# Expected behaviour: By touching on the "Custom steps (in minutes), 1 10" button, a focused textfield with the text "1 10" appears, along with the "CANCEL" and "OK" buttons.

wait_until_activity(d, "FilteredDeckOptions")
d(textStartsWith="OK", resourceIdMatches=".*button1").click()
print("Touch on a button that has text 'OK': SUCCESS")
wait()
# Expected behaviour: After touching the "OK" button, the previous focused textfield with the text "1 10" is replaced by a non-focused textview with the same text "1 10".

wait_until_activity(d, "FilteredDeckOptions")
d.click(360, 695)
print("Touch on a button that has text 'Custom steps (in minutes), 1 10': SUCCESS")
wait()
# Expected behaviour: The performed action on the "Custom steps (in minutes), 1 10" button has replaced the button with a focused textfield containing the text "1 10" and added two buttons labeled "CANCEL" and "OK".

wait_until_activity(d, "FilteredDeckOptions")
d(textStartsWith="1 10", resourceIdMatches=".*edit").set_text("3 15")
print("Fill a focused textfield that has text '1 10' with '3 15': SUCCESS")
wait()
# Expected behaviour: The focused textfield in the FilteredDeckOptions screen was updated from "1 10" to "3 15" after filling it with the new values.

wait_until_activity(d, "FilteredDeckOptions")
d(textStartsWith="OK", resourceIdMatches=".*button1").click()
print("Touch on a button that has text 'OK': SUCCESS")
wait()
# Expected behaviour: The action of touching the "OK" button on the FilteredDeckOptions screen resulted in the removal of a focused textfield with the text "3 15" and the addition of a new button on the current screen.

wait_until_activity(d, "FilteredDeckOptions")
d(descriptionMatches=".*Navigate up").click()
print("Touch on a button that has content_desc 'Navigate up': SUCCESS")
wait()
# Expected behaviour: After touching the "Navigate up" button in the previous screen (FilteredDeckOptions), the current screen (StudyOptions) shows additional buttons with content descriptions "Rebuild", "Empty", and "More options", along with various textviews displaying deck information and study statistics. (page changed from FilteredDeckOptions to StudyOptions)

