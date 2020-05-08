from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.uic import loadUiType
import urllib.request
import pafy
import humanize
import sys
import os
import os.path

ui, _ = loadUiType('Main.ui')


class MainApp(QMainWindow, ui):
    def __init__(self, parent=None):
        super(MainApp, self).__init__(parent)
        QMainWindow.__init__(self)
        self.setupUi(self)
        self.inItUI()
        self.handle_buttons()

    def inItUI(self):
        # contain all ui changes in loading
        self.tabWidget.tabBar().setVisible(False)
        style = open('themes/darkOrange.css', 'r')
        style = style.read()
        self.setStyleSheet(style)
        self.box1_animation()
        self.box2_animation()
        self.box3_animation()
        self.box4_animation()

    def handle_buttons(self):
        # handle all button in the app
        print("handle_buttons")
        self.pushButton.clicked.connect(self.download)
        self.pushButton_2.clicked.connect(self.handle_browse)
        self.pushButton_5.clicked.connect(self.Get_Video_Data)
        self.pushButton_4.clicked.connect(self.Download_Video)
        self.pushButton_8.clicked.connect(self.playlist_download)
        self.pushButton_7.clicked.connect(self.playlist_browse)
        self.pushButton_3.clicked.connect(self.Save_Browse)
        self.pushButton_9.clicked.connect(self.open_home)
        self.pushButton_10.clicked.connect(self.open_download)
        self.pushButton_11.clicked.connect(self.open_youtube)
        self.pushButton_12.clicked.connect(self.open_setting)
        self.pushButton_18.clicked.connect(self.apply_amoled)
        self.pushButton_17.clicked.connect(self.apply_aqua)
        self.pushButton_19.clicked.connect(self.apply_consoleStyle)
        self.pushButton_20.clicked.connect(self.apply_dark)
        self.pushButton_30.clicked.connect(self.apply_darkBlue)
        self.pushButton_32.clicked.connect(self.apply_darkGray)
        self.pushButton_31.clicked.connect(self.apply_darkOrange)
        self.pushButton_29.clicked.connect(self.apply_elegantDark)
        self.pushButton_34.clicked.connect(self.apply_light)
        self.pushButton_36.clicked.connect(self.apply_manjaroMix)
        self.pushButton_35.clicked.connect(self.apply_materialDark)
        self.pushButton_33.clicked.connect(self.apply_ubantu)

    def handel_progress(self, blocknum, blocksize, totalsize):
        # calculate the progress
        print("handel_progress")
        readed_data = blocknum * blocksize
        print(blocknum, blocksize, readed_data, totalsize)

        if totalsize > 0:
            download_percentage = readed_data * 100 / totalsize
            self.progressBar.setValue(download_percentage)
            QApplication.processEvents()

    def handle_browse(self):
        # enable browsing or our os , pick save location
        print("handle_browser")
        save_location = QFileDialog.getSaveFileName(caption="save as", directory=".", filter="All Files(*.*)")
        self.lineEdit_2.setText(save_location[0])

    def download(self):
        # download any file
        print("download")

        download_url = self.lineEdit.text()
        save_location = self.lineEdit_2.text()

        if download_url == '' or save_location == '':
            QMessageBox.warning(self, "Data Error", "Provide Valid URL or Save Location")
        else:
            try:
                urllib.request.urlretrieve(download_url, save_location, self.handel_progress)

            except Exception:
                QMessageBox.warning(self, "Download Error", "Provide valid URL Or save location")
                return

            QMessageBox.warning(self, "Download Completed", "The Download Completed successfully")
            self.lineEdit.setText('')
            self.lineEdit_2.setText('')
            self.progressBar.setValue(0)

    ##############################################
    ######## Download Youtube Single Video
    def Save_Browse(self):
        print("Save_Browse")
        # save location in the line edit
        save_location = QFileDialog.getSaveFileName(self, caption="Save as", directory=".", filter="All Files(*.*)")
        self.lineEdit_4.setText(str(save_location[0]))

    def Get_Video_Data(self):
        print("Get_Video_Data")
        video_url = self.lineEdit_3.text()
        print(video_url)

        if video_url == '':
            QMessageBox.warning(self, "Data Error", "Provide a valid Video URL")

        else:
            video = pafy.new(video_url)
            print(video.title)
            print(video.duration)
            print(video.author)
            print(video.length)
            print(video.viewcount)
            print(video.likes)
            print(video.dislikes)

            video_streams = video.streams
            for stream in video_streams:
                print(stream.get_filesize())
                size = humanize.naturalsize(stream.get_filesize())
                data = "{} {} {} {}".format(stream.mediatype, stream.extension, stream.quality, size)
                self.comboBox.addItem(data)

    def Download_Video(self):
        print("Download_Video")
        video_url = self.lineEdit_3.text()
        save_location = self.lineEdit_4.text()

        if video_url == '' or save_location == '':
            QMessageBox.warning(self, "Data Error", "Provide a valid Video URL or save location")

        else:
            video = pafy.new(video_url)
            video_stream = video.streams
            print(video_stream)
            video_quality = self.comboBox.currentIndex()
            print(video_quality, "video_quality")
            download = video_stream[video_quality].download(filepath=save_location, callback=self.Video_Progress)

    def Video_Progress(self, total, received, ratio, rate, time):
        read_data = received
        if total > 0:
            print("Video_progress", total, received, ratio, rate, time)
            download_percentage = read_data * 100 / total
            print(download_percentage, "download_percentage")
            self.progressBar_2.setValue(download_percentage)
            # remaining_time = round(time/60 , 2)
            # print(remaining_time ,"remaining_time")
            self.label_5.setText(str('transfer rate : {}   sec remaining : {}   '.format(rate, time)))
            QApplication.processEvents()

    # playlist_download
    def playlist_browse(self):
        playlist_save_location = QFileDialog.getExistingDirectory(self, "Select Download Directory")
        print(playlist_save_location)
        self.lineEdit_6.setText(str(playlist_save_location))

    def playlist_download(self):
        playlist_url = self.lineEdit_5.text()
        save_loation = self.lineEdit_6.text()
        print(playlist_url, save_loation)
        if playlist_url == '' or save_loation == '':
            QMessageBox.warning(self, "Data Error", "Provide a valid playlist url or save location")
        else:
            playlist = pafy.get_playlist(playlist_url)
            playlist_videos = playlist['items']

            self.lcdNumber_2.display(len(playlist_videos))
            print(playlist_videos)
            print(len(playlist_videos))

        os.chdir(save_loation)
        if os.path.exists(str(playlist['title'])):
            os.chdir(str(playlist['title']))
        else:
            os.mkdir(str(playlist['title']))
            os.chdir(str(playlist['title']))

        current_video_no = 1
        quality = self.comboBox_2.currentIndex()

        self.lcdNumber.display(current_video_no)

        for video in playlist_videos:
            current_video = video['pafy']
            current_video_stream = current_video.streams
            self.lcdNumber.display(current_video_no)
            download = current_video_stream[quality].download(callback=self.playlist_progress)
            QApplication.processEvents()

            current_video_no += 1

    def playlist_progress(self, total, received, ratio, rate, time):
        read_data = received
        if total > 0:
            download_percentage = read_data * 100 / total
            self.progressBar_3.setValue(download_percentage)
            # remaining_time = round(time / 60, 2)

            self.label_6.setText(
                str('transfer rate : {} kbps         Time  remaining : {} seconds'.format(int(rate), time)))
            QApplication.processEvents()

    # Ui changes

    def open_home(self):
        self.tabWidget.setCurrentIndex(0)
        QApplication.processEvents()

    def open_download(self):
        print("open DO")
        self.tabWidget.setCurrentIndex(1)
        QApplication.processEvents()

    def open_youtube(self):
        self.tabWidget.setCurrentIndex(2)
        QApplication.processEvents()

    def open_setting(self):
        self.tabWidget.setCurrentIndex(3)
        QApplication.processEvents()

    # App themes
    def apply_amoled(self):
        self.setStyleSheet(None)
        style = open('themes/amoled.css', 'r')
        style = style.read()
        self.setStyleSheet(style)

    def apply_aqua(self):
        self.setStyleSheet(None)
        style = open('themes/aqua.css', 'r')
        style = style.read()
        self.setStyleSheet(style)

    def apply_consoleStyle(self):
        self.setStyleSheet(None)
        style = open('themes/consoleStyle.css', 'r')
        style = style.read()
        self.setStyleSheet(style)

    def apply_dark(self):
        self.setStyleSheet(None)
        style = open('themes/dark.css', 'r')
        style = style.read()
        self.setStyleSheet(style)

    def apply_darkBlue(self):
        self.setStyleSheet(None)
        style = open('themes/darkBlue.css', 'r')
        style = style.read()
        self.setStyleSheet(style)

    def apply_darkGray(self):
        self.setStyleSheet(None)
        style = open('themes/darkGray.css', 'r')
        style = style.read()
        self.setStyleSheet(style)

    def apply_darkOrange(self):
        self.setStyleSheet(None)
        style = open('themes/darkOrange.css', 'r')
        style = style.read()
        self.setStyleSheet(style)

    def apply_elegantDark(self):
        self.setStyleSheet(None)
        style = open('themes/elegantDark.css', 'r')
        style = style.read()
        self.setStyleSheet(style)

    def apply_light(self):
        self.setStyleSheet(None)
        style = open('themes/light.css', 'r')
        style = style.read()
        self.setStyleSheet(style)

    def apply_manjaroMix(self):
        self.setStyleSheet(None)
        style = open('themes/manjaroMix.css', 'r')
        style = style.read()
        self.setStyleSheet(style)

    def apply_materialDark(self):
        self.setStyleSheet(None)
        style = open('themes/materialdark.css', 'r')
        style = style.read()
        self.setStyleSheet(style)

    def apply_ubantu(self):
        self.setStyleSheet(None)
        style = open('themes/ubantu.css', 'r')
        style = style.read()
        self.setStyleSheet(style)

    # App Animation
    def box1_animation(self):
        box_animation1 = QPropertyAnimation(self.groupBox, b"geometry")
        box_animation1.setDuration(2500)
        box_animation1.setStartValue(QRect(40, 100, 0, 0))
        box_animation1.setEndValue(QRect(40, 150, 331, 141))
        box_animation1.start()
        self.box_animation1 = box_animation1

    def box2_animation(self):
        box_animation2 = QPropertyAnimation(self.groupBox_2, b"geometry")
        box_animation2.setDuration(2500)
        box_animation2.setStartValue(QRect(40, 100, 0, 0))
        box_animation2.setEndValue(QRect(430, 150, 331, 141))
        box_animation2.start()
        self.box_animation2 = box_animation2

    def box3_animation(self):
        box_animation3 = QPropertyAnimation(self.groupBox_3, b"geometry")
        box_animation3.setDuration(2500)
        box_animation3.setStartValue(QRect(40, 100, 0, 0))
        box_animation3.setEndValue(QRect(40, 340, 331, 141))
        box_animation3.start()
        self.box_animation3 = box_animation3

    def box4_animation(self):
        box_animation4 = QPropertyAnimation(self.groupBox_4, b"geometry")
        box_animation4.setDuration(2500)
        box_animation4.setStartValue(QRect(40, 100, 0, 0))
        box_animation4.setEndValue(QRect(430, 340, 331, 141))
        box_animation4.start()
        self.box_animation4 = box_animation4


def main():
    app = QApplication(sys.argv)
    window = MainApp()
    window.show()
    app.exec_()


if __name__ == '__main__':
    main()
