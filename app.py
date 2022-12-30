# Toolbar, Navbar and list view all work
# Import from frontend.kv

from kivy.lang import Builder
from kivymd.app import MDApp
from kivy.core.window import Window
from kivymd.uix.list import OneLineListItem
from kivy.uix.screenmanager import Screen, ScreenManager
from kivy.uix.boxlayout import BoxLayout
from kivy.properties import ObjectProperty
from kivymd.uix.button import MDFlatButton
from kivymd.uix.dialog import MDDialog
import sqlite3

Window.size = (300, 500)


class ContentNavigationDrawer(BoxLayout):
    screen_manager = ObjectProperty()
    nav_drawer = ObjectProperty()


class Test(MDApp):
    dialog = None

    def build(self):
        return Builder.load_file('frontend.kv')

    def on_start(self):
        # Title list is going to be a query of all of the titles in the db
        titleList = ['Batman', 'Superman', 'Green Lantern', 'Daredevil', 'Fantastic Four']
        # Container is the id of the list on the home screen
        # It will loop through the query list and give all of the titles.
        for i in titleList:
            self.root.ids.container.add_widget(
                OneLineListItem(text=f"{i}", 
                on_release=self.home_click_me
                )
            )

        self.db_create()
            

    def home_click_me(self, onelinelistitem):
        # This method is called form the on start method
        # This method collects the information from the list click
        # and sends that to the list issue screen and builds a list for the 
        # issues.
        title = onelinelistitem.text

        # Changes the screen
        self.root.ids.screen_manager.current = 'ListScreen'

        # Builds the issue list on the list screen
        self.build_title_list(title)
    

    def build_title_list(self, title):
        # This list is the return of the query with the where clause is the title
        # from the home screen.
        # The range for loop is built for testing
        issueList = []
        for i in range(10):
            issueList.append("{0}: {1}".format(title, i))

        for i in issueList:
            self.root.ids.ListContainer.add_widget(OneLineListItem(
                text="{0}: {1}".format(title, i),
                on_release=self.issue_click_me))

    def issue_click_me(self, onelinelistitem):
        # This posts the information from the issue selected from the issues list screen
        self.root.ids.screen_manager.current = 'IssueScreen'
        self.root.ids.IssueTitle.text = '{0}'.format(onelinelistitem.text)

    def go_back(self):
        self.root.ids.screen_manager.current = 'ListScreen'

    def clear_title_list(self):
        # When the nav bar is selected it will clear the issues list
        self.root.ids.ListContainer.clear_widgets()

#############################################################################################
# DB methods

    def db_create(self):
        cmd = '''CREATE TABLE IF NOT EXISTS comics (
            title TEXT,
            publisher TEXT,
            volume_num INTEGER,
            issue_num INTEGER,
            subtitle TEXT,
            print_num INTGER,
            price REAL,
            purch_date TEXT)'''
        conn = sqlite3.connect('collection.db')
        cur = conn.cursor()
        cur.execute(cmd)
        conn.commit()
        conn.close()

    def db_insert(self, result):
        pass
        

#############################################################################################
# Action Screens

    def add_title(self):
        # Collect the information
        title = self.root.ids.AddIssueTitle.text
        title = self.scrub_title(title)
        print(title)

        publisher = self.root.ids.AddComicPublisher.text
        publisher = self.scrub_publisher(publisher)
        print(publisher)

        vol_num = self.root.ids.AddVolumeNumber.text
        issue_num = self.root.ids.AddIssueNumber.text

        issue_subtitle = self.root.ids.AddIssueSubtitle.text
        issue_subtitle = self.scrub_subtitle(issue_subtitle)
        print(issue_subtitle)

        print_num = self.root.ids.AddPrintNumber.text
        issue_price = self.root.ids.AddIssuePrice.text
        purch_date = self.root.ids.AddPurchaseDate.text

        # Load information into the database
        result = [title, publisher, vol_num, issue_num, issue_subtitle, print_num, issue_price, purch_date]
        self.db_insert(result)

        # Clear fields
        self.root.ids.AddIssueTitle.text = ''
        self.root.ids.AddComicPublisher.text = ''
        self.root.ids.AddVolumeNumber.text = ''
        self.root.ids.AddIssueNumber.text = ''
        self.root.ids.AddIssueSubtitle.text = ''
        self.root.ids.AddPrintNumber.text = ''
        self.root.ids.AddIssuePrice.text = ''
        self.root.ids.AddPurchaseDate.text = ''

        self.root.ids.screen_manager.current = 'AddConfirmation'
        self.root.ids.CardAddTitle.text = '{0}: {1}'.format(title, issue_num)



    def update_title(self):
        # Collect the information
        title = self.root.ids.UpdateIssueTitle.text
        title = self.scrub_title(title)

        publisher = self.root.ids.UpdateComicPublisher.text
        publisher = self.scrub_publisher(publisher)

        vol_num = self.root.ids.UpdateVolumeNumber.text
        issue_num = self.root.ids.UpdateIssueNumber.text

        issue_subtitle = self.root.ids.UpdateIssueSubtitle.text
        issue_subtitle = self.scrub_subtitle(issue_subtitle)

        print_num = self.root.ids.UpdatePrintNumber.text
        issue_price = self.root.ids.UpdateIssuePrice.text
        purch_date = self.root.ids.UpdatePurchaseDate.text

        # Load information into the database
        result = [title, publisher, vol_num, issue_num, issue_subtitle, print_num, issue_price, purch_date]

        # Clear fields
        self.root.ids.UpdateIssueTitle.text = ''
        self.root.ids.UpdateComicPublisher.text = ''
        self.root.ids.UpdateVolumeNumber.text = ''
        self.root.ids.UpdateIssueNumber.text = ''
        self.root.ids.UpdateIssueSubtitle.text = ''
        self.root.ids.UpdatePrintNumber.text = ''
        self.root.ids.UpdateIssuePrice.text = ''
        self.root.ids.UpdatePurchaseDate.text = ''

        self.root.ids.screen_manager.current = 'UpdateConfirmation'
        self.root.ids.CardUpdateTitle.text = '{0}: {1}'.format(title, issue_num)


    def delete_title(self):
        # Collect the information
        title = self.root.ids.DeleteIssueTitle.text
        title = self.scrub_title(title)

        publisher = self.root.ids.DeleteComicPublisher.text
        publisher = self.scrub_publisher(publisher)

        vol_num = self.root.ids.DeleteVolumeNumber.text
        issue_num = self.root.ids.DeleteIssueNumber.text

        issue_subtitle = self.root.ids.DeleteIssueSubtitle.text
        issue_subtitle = self.scrub_subtitle(issue_subtitle)

        print_num = self.root.ids.DeletePrintNumber.text
        issue_price = self.root.ids.DeleteIssuePrice.text
        purch_date = self.root.ids.DeletePurchaseDate.text

        # Load information into the database
        result = [title, publisher, vol_num, issue_num, issue_subtitle, print_num, issue_price, purch_date]

        # Clear fields
        self.root.ids.DeleteIssueTitle.text = ''
        self.root.ids.DeleteComicPublisher.text = ''
        self.root.ids.DeleteVolumeNumber.text = ''
        self.root.ids.DeleteIssueNumber.text = ''
        self.root.ids.DeleteIssueSubtitle.text = ''
        self.root.ids.DeletePrintNumber.text = ''
        self.root.ids.DeleteIssuePrice.text = ''
        self.root.ids.DeletePurchaseDate.text = ''

        self.root.ids.screen_manager.current = 'DeleteConfirmation'
        self.root.ids.CardDeleteTitle.text = '{0}: {1}'.format(title, issue_num)

    def scrub_title(self, title):
        return title.title()

    def scrub_publisher(self, publisher):
        publisher = publisher.lower()
        if publisher == 'dc':
            publisher = 'DC'
        else:
            publisher = publisher.title()
        return publisher

    def scrub_subtitle(self, issue_subtitle):
        return issue_subtitle.title()

    def go_back_to_action(self):
        # You can get the page ID's and work them into a conditional
        if self.root.ids.screen_manager.current == 'DeleteConfirmation':
            self.root.ids.screen_manager.current = 'DeleteIssueScreen'
        elif self.root.ids.screen_manager.current == 'UpdateConfirmation':
            self.root.ids.screen_manager.current = 'UpdateIssueScreen'
        else:
            self.root.ids.screen_manager.current = 'AddIssueScreen'


    
    

Test().run()



'''
    def actions(self):
        if self.root.ids.screen_manager.current == 'AddIssueScreen':
            action = 'Add'
        elif self.root.ids.screen_manager.current == 'UpdateIssueScreen':
            action == 'Update'
        else:
            action == 'Delete'
        title = self.root.ids.UpdateIssueTitle.text
        title = self.scrub_title(title)

        publisher = self.root.ids.UpdateComicPublisher.text
        publisher = self.scrub_publisher(publisher)
        
        vol_num = self.root.ids.UpdateVolumeNumber.text
        issue_num = self.root.ids.UpdateIssueNumber.text
        issue_subtitle = self.root.ids.UpdateIssueSubtitle.text
        print_num = self.root.ids.UpdatePrintNumber.text
        issue_price = self.root.ids.UpdateIssuePrice.text
        purch_date = self.root.ids.UpdatePurchaseDate.text

        # Load information into the database
        result = [title, publisher, vol_num, issue_num, issue_subtitle, print_num, issue_price, purch_date]

        # Clear fields
        self.root.ids.UpdateIssueTitle.text = ''
        self.root.ids.UpdateComicPublisher.text = ''
        self.root.ids.UpdateVolumeNumber.text = ''
        self.root.ids.UpdateIssueNumber.text = ''
        self.root.ids.UpdateIssueSubtitle.text = ''
        self.root.ids.UpdatePrintNumber.text = ''
        self.root.ids.UpdateIssuePrice.text = ''
        self.root.ids.UpdatePurchaseDate.text = ''

        self.root.ids.screen_manager.current = 'UpdateConfirmation'
        self.root.ids.CardUpdateTitle.text = '{0}: {1}'.format(title, issue_num)
'''