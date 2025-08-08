# 矩形土體傳遞邊界二維模擬之實務技術開發
本篇包含碩士論文中使用之 **OpenSeesPy數值驗證程式碼**、**外力歷時反應資料**以及 **Python所進行輸出資料繪製圖**。方便未來重現模擬、修改分析參數、重新繪製圖表。
## 資料夾說明
- '數值模擬/'：論文第三章數值驗證中所包含一維入射波與二維反彈波的OpenSeesPy程式碼，及外加力加載所使用的歷時反應文件（txt）檔案。第四章中雷力阻尼所進行的分析程式碼。
- 'data/'：包含數值模擬所輸出之資料。
- '結果'：繪圖與分析結果（含圖檔）。
## 軟體安裝
當需要下載最新版本OpenSeespy，需要至The OpenSeesPy官網（https://openseespydoc.readthedocs.io/en/latest )
確認所需Pyhton最新版本。並於Python中安裝OpenSeesPy
![image](https://github.com/wwe2323520/Distributed-load-at-soil-/blob/main/Version.png)pip install openseespy
## 使用方式

### 數值模擬/數值驗證
