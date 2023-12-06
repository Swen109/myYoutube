import sys
from PyQt5.QtCore import Qt, QUrl, QSize
from PyQt5.QtGui import QPixmap, QIcon, QFont
from PyQt5.QtWidgets import QApplication, QMainWindow, QSizePolicy, QWidget, QHBoxLayout, QVBoxLayout, QPushButton, QLabel, QStackedWidget, QLineEdit, QSpacerItem, QSizePolicy, QScrollArea
from PyQt5.QtWebEngineWidgets import QWebEngineView
from googleapiclient.discovery import build
import requests
from PyQt5.QtCore import Qt
from PyQt5 import QtWidgets

count = 0

class YouTubeViewer(QMainWindow):
    def __init__(self):
        super(YouTubeViewer, self).__init__()

        self.setWindowTitle("YouTube Viewer")
        self.setGeometry(100, 100, 800, 600)

        self.init_ui()
        self.Ui_home_page()
        # self.play_video() 重複到的變數要改或是整合在一起
        # self.show_thumbnails_page()
        # self.search_videos() 會顯示在一打開的頁面

    def init_ui(self):
        
        # 創建中央小部件
        self.central_widget = QWidget(self)
        self.setCentralWidget(self.central_widget)

        # 設置背景色為黑色
        self.setStyleSheet("background-color: black;")

        # 創建 QStackedWidget 用於顯示不同的頁面
        self.stacked_widget = QStackedWidget()

        # 創建 Web 檢視
        self.web_view = QWebEngineView()
        self.web_view.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        # 創建一個字體對象
        self.font = QFont()
        self.font.setFamily("Arial")  # 設置字型

        
    def Ui_home_page(self):
        # 創建home page佈局
        self.home_page_layout = QVBoxLayout(self.central_widget)

        # 創建顯示縮圖的頁面
        home_page = QWidget()
        self.thumbnails_layout = QHBoxLayout(home_page)
        self.home_page_layout.addLayout(self.thumbnails_layout)
        
        # 建立myYoutube標籤
        self.myYoutube_label = QLabel("<a style='text-decoration: none; color: red;' href='#'>myYoutube</a>")
        self.myYoutube_label.linkActivated.connect(self.show_thumbnails_page)
        self.myYoutube_label.setFont(self.font)
        self.myYoutube_label.setStyleSheet("font-size: 55px")
        self.home_page_layout.addWidget(self.myYoutube_label, alignment=Qt.AlignCenter)
        
        #搜尋欄和搜尋按鈕的佈局
        search_layout = QHBoxLayout()
        search_layout.addStretch(1) # 添加彈簧

        # 添加返回按鈕和設定樣式
        self.back_button = QPushButton("⇦")
        self.back_button.setStyleSheet("font-size: 50px; color: white;") # 字體大小、顏色
        self.back_button.setFixedWidth(50)  # 設定按鈕的寬度
        self.back_button.setFixedHeight(40)  # 設定按鈕的高度
        #點擊後回到首頁 （之後要改成上一頁）
        self.back_button.clicked.connect(self.show_thumbnails_page)
        #不要選取框
        self.back_button.setFocusPolicy(Qt.NoFocus)  
        #將返回鍵加入search_layout
        search_layout.addWidget(self.back_button, alignment=Qt.AlignLeft | Qt.AlignTop)

        self.back_button.setVisible(False)  # 在home page時 返回鍵設置為不可見

        # 添加彈簧
        search_layout.addStretch(3)

        # 新增搜尋欄位
        self.search_bar = QtWidgets.QLineEdit()
        self.search_bar.setStyleSheet("font-size: 25px; color: white; background-color: Black;")
        self.search_bar.setFixedWidth(400)  # 設定寬度
        self.search_bar.setFixedHeight(40)  # 設定高度
        search_layout.addWidget(self.search_bar, alignment=Qt.AlignCenter)

        # 新增搜尋按鈕
        search_button = QPushButton("🔍")
        search_button.setStyleSheet("font-size: 30px; color: white; background-color: black;")
        search_button.clicked.connect(self.search_videos)
        search_button.setFixedWidth(40)  # 設定按鈕的寬度
        search_button.setFixedHeight(40)  # 設定按鈕的高度
        search_button.setFocusPolicy(Qt.NoFocus)
        search_layout.addWidget(search_button)

        # 添加彈簧
        search_layout.addStretch(5)


        # 將搜尋欄位和搜尋按鈕的水平佈局添加到主佈局
        self.home_page_layout.addLayout(search_layout)

        # 將 QStackedWidget 添加到其中
        self.home_page_layout.addWidget(self.stacked_widget)

        self.stacked_widget.addWidget(home_page)

        # 獲取前 3 個熱門影片
        api_key = "AIzaSyBZQYb6v1_U1-E8gkavifckIJzAz5-0tHM"
        youtube = build('youtube', 'v3', developerKey=api_key)
        request = youtube.videos().list(part='snippet', chart='mostPopular', regionCode='TW', maxResults=3)
        response = request.execute()


        # 為每個影片創建帶縮圖的按鈕
        for item in response['items']:
            video_id = item['id']
            title = item['snippet']['title']
            thumbnail_url = item['snippet']['thumbnails']['medium']['url']

            self.thumbnail_button = QPushButton()
            pixmap = QPixmap()
            pixmap.loadFromData(requests.get(thumbnail_url).content)
            self.thumbnail_button.setIcon(QIcon(pixmap))
            self.thumbnail_button.setIconSize(QSize(200, 150))
            # button.setStyleSheet("border: 1px solid white;") # 框起來看一下範圍
            self.thumbnail_button.clicked.connect(lambda _, vid=video_id: self.play_video(vid))
            self.thumbnail_button.setFocusPolicy(Qt.NoFocus)
            self.thumbnails_layout.addWidget(self.thumbnail_button)

            # 創建帶標題的標籤
            label = QLabel(title)
            label.setAlignment(Qt.AlignCenter)
            label.setStyleSheet("color: white")
            # label.setStyleSheet("color: white; border: 1px solid red;") # 框起來看一下範圍
            label.setFixedWidth(200)
            label.setFixedHeight(15)
            label.setWordWrap(True)  # 啟用自動換行


            # 將按鈕和標籤添加到垂直佈局
            video_layout = QVBoxLayout()
            video_layout.addStretch(1)
            video_layout.addWidget(self.thumbnail_button)
            video_layout.addWidget(label)
            video_layout.addStretch(1)
            
            self.thumbnail_button.setToolTip(title)

            # 將垂直佈局添加到水平佈局
            self.thumbnails_layout.addLayout(video_layout)




    def play_video(self, video_id):
        video_url = f"https://www.youtube.com/embed/{video_id}"
        self.web_view.setUrl(QUrl(video_url))

        # 創建顯示播放頁面
        play_page = QWidget()
        play_layout = QVBoxLayout(play_page)
        
        # 添加水平佈局
        noname_layout = QHBoxLayout()

        # 將水平佈局添加到播放頁面的主佈局
        play_layout.addLayout(noname_layout)

        # 添加 Web 檢視
        play_layout.addWidget(self.web_view)

        # 顯示play page
        self.stacked_widget.addWidget(play_page)

        # 切換到播放頁面
        self.stacked_widget.setCurrentWidget(play_page)

        # 顯示返回按鈕
        self.back_button.setVisible(True) 


    def show_thumbnails_page(self):
        # 切換回顯示縮圖的頁面
        self.stacked_widget.setCurrentIndex(0)

        self.back_button.setVisible(False)  # 返回按鈕設置為不可見

    
    def search_videos(self):

        # 使用 global 關鍵字宣告使用全局變數
        global count

        query = self.search_bar.text()

        # 建立 YouTube API 的服務物件
        youtube = build('youtube', 'v3', developerKey="AIzaSyBZQYb6v1_U1-E8gkavifckIJzAz5-0tHM")
        
        # 初始化變數
        videos = []
        nextPageToken = None  # 將 nextPageToken 初始化為 None
       
       # 處理每一頁的搜尋結果
        for page in range(1):
            print(f"Processing page {page + 1} for query '{query}'...")
            # 設定 API 請求的參數，包含 regionCode 和 pageToken
            request = youtube.search().list(
                part='snippet',
                q=query,
                type='video',
                maxResults=10,
                regionCode='TW',  # 台灣的代碼是 'TW'
                pageToken=nextPageToken  # 使用上一頁的 nextPageToken
            )

            # 發送 API 請求並取得回應
            try:
                response = request.execute()
                print(response)
                print('-'*170)
            except Exception as e:
                print(f"An error occurred: {e}")
                response = None

            # 檢查回應是否正確
            if response and 'items' in response:
                # 解析回應，提取有用的資訊
                for item in response['items']:
                    count += 1
                    videos.append({
                        'title': item['snippet']['title'],  # 影片標題
                        'video_id': item['id']['videoId'],  # 影片 ID
                        'thumbnail': item['snippet']['thumbnails']['default']['url']  # 影片縮圖 URL
                    })

            # 如果有下一頁，取得 nextPageToken
            nextPageToken = response.get('nextPageToken')

            # 如果沒有下一頁，跳出迴圈
            if not nextPageToken:
                break


        # 創建顯示列表頁面
        list_page = QWidget()
        list_layout = QVBoxLayout(list_page)

        # 創建 QScrollArea 並設置它的內容
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        
        # 創建一個容器窗口，放入垂直佈局
        container = QWidget()
        container.setLayout(list_layout)

        # 設置容器窗口為滾動條區域的內容
        scroll_area.setWidget(container)

        # 將滾動條區域設置為主窗口的佈局
        list_page.layout = QVBoxLayout(list_page)
        list_page.layout.addWidget(scroll_area)

        scroll_area.setStyleSheet("color: black; border: none;")
        scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

            # 輸出搜尋結果
        for video in videos:

            video_id = item['id']['videoId']
            title = video['title']
            thumbnail_url = video['thumbnail']
            
            thumbnail_button = QPushButton()
            pixmap = QPixmap()
            pixmap.loadFromData(requests.get(thumbnail_url).content)
            thumbnail_button.setIcon(QIcon(pixmap))
            thumbnail_button.setIconSize(QSize(200, 150))
            # button.setStyleSheet("border: 1px solid white;") # 框起來看一下範圍
            thumbnail_button.clicked.connect(lambda _, vid=video_id: self.play_video(vid))
            thumbnail_button.setFocusPolicy(Qt.NoFocus)
            list_layout.addWidget(thumbnail_button)

            # 創建帶標題的標籤
            label = QLabel(title)
            label.setAlignment(Qt.AlignLeft)
            label.setStyleSheet("color: white")
            # label.setStyleSheet("color: white; border: 1px solid red;") # 框起來看一下範圍
            label.setFixedWidth(200)
            label.setFixedHeight(15)
            label.setWordWrap(True)  # 啟用自動換行

            # 將按鈕和標籤添加到水平佈局
            video_layout = QHBoxLayout()
            video_layout.addStretch(1)
            video_layout.addWidget(thumbnail_button)
            video_layout.addWidget(label)
            video_layout.addStretch(1)

            list_layout.addLayout(video_layout)

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