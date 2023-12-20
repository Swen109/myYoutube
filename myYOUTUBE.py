import sys
from PyQt5.QtCore import Qt, QUrl, QSize
from PyQt5.QtGui import QPixmap, QIcon, QFont
from PyQt5.QtWidgets import QApplication, QMainWindow, QSizePolicy, QWidget, QHBoxLayout, QVBoxLayout, QPushButton, QLabel, QStackedWidget, QLineEdit, QSpacerItem, QSizePolicy, QScrollArea
from PyQt5.QtWebEngineWidgets import QWebEngineView
from googleapiclient.discovery import build
import requests
from PyQt5.QtCore import Qt
from PyQt5 import QtWidgets

class YouTubeViewer(QMainWindow):
    def __init__(self):
        super(YouTubeViewer, self).__init__()

        # 視窗標題、位置大小
        self.setWindowTitle("YouTube Viewer")
        self.setGeometry(100, 100, 800, 600)

        self.init_ui()
        self.Ui_home_page()

    def init_ui(self):
        
        # 創建中央小部件
        self.central_widget = QWidget(self)
        self.setCentralWidget(self.central_widget)

        # 設置背景色為黑色
        self.setStyleSheet("background-color: black;")

        # 創建 QStackedWidget 用於顯示不同的頁面
        self.stacked_widget = QStackedWidget()

        # 創建 Web 檢視。QWebEngineView是Qt的Web引擎視圖元件，通常用於顯示Web內容。
        self.web_view = QWebEngineView()
        self.web_view.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        # 創建一個字體對象
        self.font = QFont()
        self.font.setFamily("Arial")  # 設置字型

    def make_thumbnail_and_title(self, nextPageToken, layoutType, keyword, mainLayout):

        # 建立 YouTube API 的服務物件
        api_key = "AIzaSyBZQYb6v1_U1-E8gkavifckIJzAz5-0tHM"
        youtube = build('youtube', 'v3', developerKey=api_key)
        # 指定取得snippet（標題、描述、發佈時間、頻道資訊等）
        request = youtube.videos().list(part='snippet', chart='mostPopular', regionCode='TW', maxResults=3, pageToken=nextPageToken)
        # 回傳一個字典
        response = request.execute()
    
        if keyword :
            # 將搜尋欄的文字丟給keyword
            keyword = self.search_bar.text()
            request = youtube.search().list(q=keyword, part='snippet', type='video', maxResults=10, regionCode='TW', pageToken=nextPageToken)
            response = request.execute()
        else:
            pass

        # 為每個影片創建帶縮圖的按鈕
        for item in response['items']:

        # 從字典取得需要的資訊(用搜尋欄找的影片中 id內的videoId才是影片id
            if keyword :
                video_id = item['id']['videoId']
            else:
                video_id = item['id']

            title = item['snippet']['title']
            thumbnail_url = item['snippet']['thumbnails']['medium']['url']
        
        # 創建縮圖按紐
            # QPixmap() => Qt框架中的一個類別，用來處理圖像
            pixmap = QPixmap()
            # 將YouTube影片的縮圖從網路下載到程序中，以便在應用程式中顯示
            pixmap.loadFromData(requests.get(thumbnail_url).content)
            self.thumbnail_button = QPushButton()
            self.thumbnail_button.setIcon(QIcon(pixmap))
            self.thumbnail_button.setIconSize(QSize(260, 150))
            # 不要顯示選擇框(點擊後的虛線)
            self.thumbnail_button.setFocusPolicy(Qt.NoFocus)

        # 創建帶標題文字的標籤
            self.thumbnail_title = QLabel(title)
            self.thumbnail_title.setAlignment(Qt.AlignCenter)
            self.thumbnail_title.setStyleSheet("color: white")
            # 文字自動換行
            self.thumbnail_title.setWordWrap(True)
            # 設置標題範圍的長寬
            self.thumbnail_title.setFixedWidth(260)
            self.thumbnail_title.setFixedHeight(60)

        # 功能
            # 點擊縮圖後執行self.play_video(video_id)
            self.thumbnail_button.clicked.connect(lambda _, vid=video_id: self.show_video_page(vid))
            # 鼠標移至縮圖按鈕上時會顯示完整標題
            self.thumbnail_button.setToolTip(title)

        # 排版
            #在主佈局內加入 thumbnail_button
            mainLayout.addWidget(self.thumbnail_button)
            # 創建垂直佈局，將縮圖和標題放入
            video_and_title_layout = layoutType()
            video_and_title_layout.addStretch(1)
            video_and_title_layout.addWidget(self.thumbnail_button)
            video_and_title_layout.addWidget(self.thumbnail_title)
            video_and_title_layout.addStretch(1)
            # 將video_and_title_layout添加到主佈局
            mainLayout.addLayout(video_and_title_layout)
        
    def Ui_home_page(self):
        # 創建home page佈局
        self.home_page_layout = QVBoxLayout(self.central_widget)

        # 創建首頁頁面
        self.home_page = QWidget()
        self.thumbnails_layout = QHBoxLayout(self.home_page)
        self.home_page_layout.addLayout(self.thumbnails_layout)
        
        # 建立myYoutube標籤
        self.myYoutube_label = QLabel("<a style='text-decoration: none; color: red;' href='#'>myYoutube</a>")
        # 設定字體
        self.myYoutube_label.setFont(self.font)
        self.myYoutube_label.setStyleSheet("font-size: 55px")

    #創建物件
        # 添加返回按鈕和設定樣式
        self.back_button = QPushButton("⇦")
        self.back_button.setStyleSheet("font-size: 50px; color: white;") # 字體大小、顏色
        self.back_button.setFixedWidth(50)  # 設定按鈕的寬度
        self.back_button.setFixedHeight(40)  # 設定按鈕的高度
        self.back_button.setFocusPolicy(Qt.NoFocus)  # 不要顯示聚焦框
        self.back_button.setVisible(False)  # 在home page時 返回鍵設置為不可見

        # 新增搜尋欄位
        self.search_bar = QtWidgets.QLineEdit()
        self.search_bar.setStyleSheet("font-size: 25px; color: white; background-color: Black;")
        self.search_bar.setFixedWidth(400)  # 設定寬度
        self.search_bar.setFixedHeight(40)  # 設定高度

        # 新增搜尋按鈕
        search_button = QPushButton("🔍")
        search_button.setStyleSheet("font-size: 30px; color: white; background-color: black;")
        search_button.setFixedWidth(40)  # 設定按鈕的寬度
        search_button.setFixedHeight(40)  # 設定按鈕的高度
        search_button.setFocusPolicy(Qt.NoFocus)

    #排版
        # 新增搜尋欄和搜尋按鈕的佈局
        search_layout = QHBoxLayout()
        # 將 QStackedWidget 添加到主佈局中
        self.home_page_layout.addWidget(self.stacked_widget)
        # 將home_page加入QStackedWidget
        self.stacked_widget.addWidget(self.home_page)
        # 將標myYoutube籤置中
        self.home_page_layout.addWidget(self.myYoutube_label, alignment=Qt.AlignCenter)
        # 添加彈簧
        search_layout.addStretch(1) 
        # 將返回鍵加入search_layout
        search_layout.addWidget(self.back_button, alignment=Qt.AlignLeft | Qt.AlignTop)
        # 添加彈簧
        search_layout.addStretch(3)
        # 將搜尋欄位和搜尋紐加入水平佈局
        search_layout.addWidget(self.search_bar, alignment=Qt.AlignCenter)
        search_layout.addWidget(search_button)
        # 添加彈簧
        search_layout.addStretch(5)
        # 將搜尋欄位和搜尋按鈕的水平佈局添加到主佈局
        self.home_page_layout.addLayout(search_layout)
        # 製作縮圖和標題
        self.make_thumbnail_and_title(None, QVBoxLayout, False, self.thumbnails_layout)
    

    #功能
        # myYoutube連結到show_thumbnails_page
        self.myYoutube_label.linkActivated.connect(self.show_home_page)
        # 點擊後回到首頁 （之後要改成上一頁）
        self.back_button.clicked.connect(self.show_home_page) 
        # 點擊後切換到search_videos頁面
        search_button.clicked.connect(self.search_videos) 



    def show_video_page(self, video_id):
        video_url = f"https://www.youtube.com/embed/{video_id}"
        
        # web_view 會載入並顯示指定YouTube影片的內容
        self.web_view.setUrl(QUrl(video_url))

        # 創建QWidget 並將play_page設置為垂直佈局
        play_page = QWidget()
        play_layout = QVBoxLayout(play_page)

        # 將web_view加入主佈局
        play_layout.addWidget(self.web_view)
        # 將play_page加入QStackedWidget
        self.stacked_widget.addWidget(play_page)
        # 切換到播放頁面
        self.stacked_widget.setCurrentWidget(play_page)

        # 顯示返回按鈕
        self.back_button.setVisible(True)

    def show_home_page(self):
        # 將 QWebEngineView 的內容設置為空白頁面
        self.web_view.setHtml('')

        # 將 QStackedWidget 添加到 home_page_layout 中
        self.home_page_layout.addWidget(self.stacked_widget)
        # 切換到 home_page
        self.stacked_widget.setCurrentWidget(self.home_page)

        self.back_button.setVisible(False)  # 返回按鈕設置為不可見

    
    def search_videos(self):
        # 創建顯示列表頁面
        list_page = QWidget()
        # 創建主佈局(垂直)
        list_layout = QVBoxLayout(list_page)

        # 創建 QScrollArea
        scroll_area = QScrollArea()
        # 指定scroll_area內的Widget應該被視為可調整大小的
        scroll_area.setWidgetResizable(True)
        
        # 創建一個容器窗口，放進主佈局
        container = QWidget()
        container.setLayout(list_layout)

        # 設置容器窗口為滾動條區域的內容
        scroll_area.setWidget(container)

        # 將滾動條區域設置為主窗口的佈局
        list_page.layout = QVBoxLayout(list_page)
        list_page.layout.addWidget(scroll_area)

        scroll_area.setStyleSheet("color: black; border: none;")
        scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

        self.make_thumbnail_and_title(None, QHBoxLayout, True, list_layout)

            # # 如果有下一頁，取得 nextPageToken
            # nextPageToken = response.get('nextPageToken')

            # # 如果沒有下一頁，跳出迴圈
            # if not nextPageToken:
            #     break


        # 將 list_page 添加到 QStackedWidget
        self.stacked_widget.addWidget(list_page)
        
        # 切換頁面到list page
        self.stacked_widget.setCurrentWidget(list_page)

        self.back_button.setVisible(True)  # 顯示返回按鈕


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = YouTubeViewer()
    window.show()
    sys.exit(app.exec_())