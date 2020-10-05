# -*- coding: utf-8 -*-
"""
Created on Tue Oct  1 11:00:00 2019

@author: ym-02
"""

import tkinter as tk
from tkinter import ttk
import requests
#import pprint
from tkinter import messagebox



class MainFrame(tk.Frame):
    def __init__(self,master):
        super().__init__(master)
        self.CreateWidgets()
        self.grid()
        self.path="log/SaveShopList.text"
        self.writeList=[]
        self.ReLord()


    #部品を作るメソッド------------------------------------------------------------
    def CreateWidgets(self):
        
        #------------フレームを作成------------#
        
        fmSearch=tk.Frame(self)
        fmCategory=tk.Frame(self)
        fmCheck=tk.LabelFrame(self)
        fmSearchList=tk.Frame(self)
        fmListBox=tk.Frame(self)
        fmButton=tk.Frame(self)
        fmVisitShops=tk.Frame(self)
        
        #-----------------------------------#

        
        #-----------fmSearchに格納-----------#
        #ラベル
        lblSe=tk.Label(fmSearch,text="フリーワード")
        lblSe.grid(row=0,column=0)
        
        #エントリー
        self.enS=tk.Entry(fmSearch,width=30)
        self.enS.grid(row=0,column=1)

        #ボタン

        btnS=tk.Button(fmSearch,text="検索",command=self.btnSClicked)
        btnS.grid(row=0,column=2)        

        #pack
        fmSearch.pack()

        #-----------------------------------#

        ##########インスタンス化###########
        self.app=Application(self)
        category_l_list=self.app.GetCategoryL()


        #----------fmCategoryに格納----------#

        #ラベル
        lbC=tk.Label(fmCategory,text="分類")
        lbC.grid(row=0,column=0)
        
        
        #コンボボックス
        self.cmbCR=ttk.Combobox(fmCategory,values=category_l_list)
        self.cmbCR.grid(row=0,column=1)
                
        #パックする
        fmCategory.pack()
        #-----------------------------------#

        #------------------fmCheckに格納-------------------#
        
        #チェックボックス
        datalist=["ランチ営業あり","モーニングあり","禁煙席あり","日曜営業",
                  "駐車場あり","個室あり","カード可","電子マネー利用可",
                  "wifiあり","電源あり","ペット同伴可","Web予約可"]
        
        self.var=[]
        count=0

        #チェックボックス12個を表示  
        for i in range(3):
            for j in range(4):  
                self.var.append(tk.StringVar())
                self.cbLu=ttk.Checkbutton(fmCheck,text=datalist[count],variable=self.var[count])
                self.var[count].set(False)
                self.cbLu.grid(row=i,column=j)   
                count+=1

        
        #パックする
        fmCheck.pack(pady=10,padx=10)

        #-------------------------------------------------#
        
        
        #----------------fmSearchListに格納----------------#
        #ラベル
        lblS=tk.Label(fmSearchList,text="検索店舗一覧")
        lblS.grid(row=0,column=0)
        
        btnUp=tk.Button(fmSearchList,text="↑",command=self.btnUpClicked)
        btnUp.grid(row=0,column=1)
        
        btnDwn=tk.Button(fmSearchList,text="↓",command=self.btnDwnClicked)
        btnDwn.grid(row=0,column=2,sticky=tk.S)
        
                
        lblH=tk.Label(fmSearchList,text="検索結果:")
        lblH.grid(row=0,column=3)
        
        ##検索件数を取得##
        
        self.var_count=tk.StringVar()
     
        lblHit=tk.Label(fmSearchList,textvariable=self.var_count)
        lblHit.grid(row=0,column=4)

        
        #パックする
        fmSearchList.pack(pady=10)  
        #-------------------------------------------------#
        
        #-----------------fmListBoxに格納-----------------#
        #リストボックス
        self.lbS=tk.Listbox(fmListBox,width=50,height=10,selectmode=tk.EXTENDED)
        self.lbS.config()
        self.lbS.grid(row=1,column=0,padx=10)

        #パックする
        fmListBox.pack()        
        
        #-------------------------------------------------#
        

        
        #------------------fmButtonに格納------------------#
        
        #ボタン
        btnDi=tk.Button(fmButton,text="表示",command=self.showWindow)
        btnDi.grid(row=0,column=0)
        
        btnAdd=tk.Button(fmButton,text="来店済み",command=self.btnVClicked)
        btnAdd.grid(row=0,column=1)
            
        #パックする
        fmButton.pack()
    
        #-------------------------------------------------#
        
        
        #----------------fmVisitShopsに格納----------------#
        #ラベル
        lblV=tk.Label(fmVisitShops,text="来店済み店舗一覧")
        lblV.grid(row=0,column=0)
        
        #リストボックス
        self.lbV=tk.Listbox(fmVisitShops,width=50,height=8)
        self.lbV.grid(row=1,column=0,padx=10)
        
        #ボタン
        btnV=tk.Button(fmVisitShops,text="削除",command=self.btnDeClicked)
        btnV.grid(row=2,column=0)
        
        #パックする
        fmVisitShops.pack(pady=10)
        
        #-------------------------------------------------#
    
    #新しいウィンドウを開かせるためのメソッド---------------------------------------------
    def showWindow(self):
        
        #選択されたデータを取得
        self.selection=self.lbS.curselection()
        
        result={}
                
        #なにも選択されていないとき
        if len(self.selection)==0:
            messagebox.showwarning("警告","リストボックスから表示したいデータを選択してください")
            return
        
        #いくつ選択されたかを代入
        count=int(len(self.selection))
        
        #選択されたデータの数だけループを回す
        for i in range(count):         
            
            #i番目の選択したデータの行数を代入
            index=self.selection[i] 
           
            #i番目の選択したデータの店名を取得
            shopname=self.lbS.get(index)
            
            #メソッドから店舗情報を取得
            result=self.app.getShopInfo(shopname)
            
            ########インスタンス化#########コンストラクタに店舗情報を渡す
            SubWindow(self,result)
              

    
    #検索ボタン押下時→APIに検索条件を渡し、返ってきたデータをリストボックスへ挿入--------------
    def btnSClicked(self):
           
        self.lbS.delete(0,tk.END)
        
        #エントリーからフリーワードを取得
        freeword=self.enS.get()   
        
        
        checklist=[]
        for i in range(12):   
            #チェックリストから値を取得
            checklist.append(self.var[i].get())
        
        
        category=self.cmbCR.get()
    
        #カテゴリーを何も選択していないとき
        if category=="":
            messagebox.showwarning("警告","分類を選択してください")
            return
        
        #APIを取得、店名のリストを取得
        self.shoplist=self.app.getAPI(freeword,checklist,category)
        
        #店が一軒も検索結果にないとき
        if self.shoplist is None:
            self.updateLabel()
            return
        
        #店名をリストからリストボックスへ挿入
        for i in range(len(self.shoplist)):
            text=self.shoplist[i]
            self.lbS.insert(tk.END,text)
            
        #検索件数を表示させるメソッドを呼び出す
        self.updateLabel()                
    
    
    #検索件数を表示させるメソッド----------------------------------------------------
    def updateLabel(self):
                
        #Applicationクラスから検索件数を引っ張てくる
        total_hit=str(self.app.getHitCount())+str("件")
    
        #ラベルの変数に代入し、表示    
        self.var_count.set(total_hit)
        
    
        
        
    #リストを昇順にするメソッド--------------------------------------------------------
    def btnUpClicked(self):
        
        #リストボックスをクリアする
        self.lbS.delete(0,tk.END)
        
        #店名のリストを昇順にする
        self.shoplist.sort(reverse=False)
        
        #降順にした店名のリストを挿入しなおす
        for i in range(len(self.shoplist)):
            text=self.shoplist[i]
            self.lbS.insert(tk.END,text)
        
        
    #リストを降順にするメソッド--------------------------------------------------------
    def btnDwnClicked(self):
        
        #リストボックスをクリアする
        self.lbS.delete(0,tk.END)
        
        #店名のリストを昇順にする
        self.shoplist.sort(reverse=True)
        
        #降順にした店名のリストを挿入しなおす
        for i in range(len(self.shoplist)):
            text=self.shoplist[i]
            self.lbS.insert(tk.END,text)
              
        
    #来店済みの店名をtextに保存し、リストボックスに表示させるメソッド------------------------
    def btnVClicked(self):
        
        point=0
        
        #何も選択していないとき、警告
        if len(self.lbS.curselection())==0:
            messagebox.showwarning("警告","店名を選択してください")
            return
        
     
        #選択されたデータの数だけループを回す
        for i in range(len(self.lbS.curselection())):
            
            #選択されたデータのインデクスを取得
            index=self.lbS.curselection()[i]
            
            
            #来店済み店舗のリストにデータがいくつあるか確認
            count=len(self.writeList)
            
            #来店済み店舗のリストボックスにデータがあるか確認
            if count>0:
                
                #来店済みデータがあった場合、そのデータ数だけループ
                for j in range(count):
                    #来店済み店名リストと、選択したリストの名前が重複していないか確認
                    if str(self.writeList[j])==str(self.lbS.get(index)):
                        point+=1
                
                #重複していないとき、リストに追加
                if point==0:
                    print("重複していないのでリストにデータを追加します")
                    self.writeList.append(self.lbS.get(index))
                    self.lbV.insert(tk.END,self.lbS.get(index))
                else:
                    print("重複しているデータがあるため除外")
                
            #来店済みデータが0のとき
            else:
                print("来店済みデータは0です")
                self.writeList.append(self.lbS.get(index))
                self.lbV.insert(tk.END,self.writeList[i])

        
        #ファイルに書き込み
        with open(self.path,mode="w") as f:
            f.write(str(",".join(self.writeList)))
  


          
            
    #ファイルと書き込み用リストからデータを削除-------------------------------------------
    def btnDeClicked(self):
        
        count=len(self.lbV.curselection())
        
        if len(self.writeList)==0:
            return
        
        #何も選択していないとき、警告
        if count==0:
            messagebox.showwarning("警告","選択をしてから削除してください")
        
       #削除する要素をリストから探し、削除する     
        for i in range(count):
            index=self.lbV.curselection()[i]
            
            for j in range(len(self.writeList)):
                if str(self.writeList[j])==str(self.lbV.get(index)):
                    del self.writeList[j]
                    break
        
        #リストボックスのデータを削除する
        self.lbV.delete(0,tk.END)
                    
        #リストボックスにデータを入れなおす
        for w in self.writeList:
            self.lbV.insert(tk.END,w)
        
        #ファイルに書き込み
        with open(self.path,mode="w") as f:
            f.write(str(",".join(self.writeList)))
            
        
        

    #ファイルからデータを取り出し、リストボックスに格納するメソッド-----------------------------
    def ReLord(self):
        
        datalist=[]
        
        #ファイルを開く
        with open(self.path,mode="r") as f:
          writer=f.read()
   
        if len(writer)==0:
            return
    
        #データをリスト型にする
        datalist=writer.split(',')  
        
        #リストをリストボックスに格納
        for d in datalist:
            self.lbV.insert(tk.END,d)
            self.writeList.append(d)



#----------------------------------------------------------------------------------------------------------------------------#

##新しいウィンドウを生成するクラス##
class SubWindow(tk.Toplevel):
            
    def __init__(self,master,result):
        super().__init__(master)
        self.newWindows=[]
        self.CreateWidgets(result)
    
    #部品を作るメソッド------------------------------------------------------------
    def CreateWidgets(self,result):
        
             
            #---------------フレーム---------------#
            fminfo=tk.LabelFrame(self,width=50)
            fmbutton=tk.Frame(self)
            #------------------------------------#
                        
            #----------------fminfoに格納---------------#
            #ラベル
            lblN=tk.Label(fminfo,text="店名：")
            lblN.grid(row=0,column=0,sticky=tk.W)
            
            lblNa=tk.Label(fminfo,text=result['name'])
            lblNa.grid(row=0,column=1)
            
            lblA=tk.Label(fminfo,text="住所：")
            lblA.grid(row=1,column=0,sticky=tk.W)
            
            lblAdrs=tk.Label(fminfo,text=result['address'])
            lblAdrs.grid(row=1,column=1)
            
            lblO=tk.Label(fminfo,text="開店時間：")
            lblO.grid(row=2,column=0,sticky=tk.W)
            
            lblOpn=tk.Label(fminfo,text=result['opentime'])
            lblOpn.grid(row=2,column=1)
            
            lblH=tk.Label(fminfo,text="定休日：",anchor='w')
            lblH.grid(row=3,column=0,sticky=tk.W)
            
            lblHldy=tk.Label(fminfo,text=result['holiday'])
            lblHldy.grid(row=3,column=1)
            
            lblB=tk.Label(fminfo,text="予算：",anchor='w')
            lblB.grid(row=4,column=0,sticky=tk.W)
            
            lblBgt=tk.Label(fminfo,text=str(result['budget'])+str("円"))
            lblBgt.grid(row=4,column=1)
            
 
            lblPR=tk.Label(fminfo,text=result['pr']['pr_long'])
            lblPR.grid(row=5,column=1)
    
            #パックする
            fminfo.pack(fill="x")
            
            #--------------------------------------------#
            
            #----------------fmbuttonに格納---------------#
            #ボタン
            btnClose=tk.Button(fmbutton,text="close",command=self.winDestroy)
            btnClose.focus_set()
            btnClose.pack()
            
            fmbutton.pack()
            
            #--------------------------------------------#

    def winDestroy(self):
        
        self.destroy()

        
#----------------------------------------------------------------------------------------------------------------------------#
class Application(tk.Frame):

    def __init__(self,master):
        super().__init__(master)
        self.key="YOUR ACCESSKEY"　##送られてきたアクセスキー##
        self.url="https://api.gnavi.co.jp/RestSearchAPI/v3/"
        self.lang="ja"     
        self.area="YOUR AREA"  ##好きな市町村エリア##
        #APIから取得したすべての店舗情報を格納するリスト
        self.backupList=[]
        

    def GetCategoryL(self):
            
        category_l_url="https://api.gnavi.co.jp/master/CategoryLargeSearchAPI/v3/"
        query={"keyid":self.key,"lang":self.lang}
        
        
        #カテゴリー情報を取得
        request_api=requests.get(category_l_url,params=query)
        result_api=request_api.json()
        
        self.category_l=[]
    
        #データからcategory_lの情報だけを取り出す
        self.category_l=result_api['category_l']
    
        #カテゴリーから名前だけを取得し、リストへ代入
        self.category_l_list=[d.get('category_l_name') for d in self.category_l]

        return self.category_l_list
    
    
    
    #渡された検索条件から、店を検索し、そのデータを返却する
    def getAPI(self,freeword,checklist,category):
        
        self.total_hit_count=0

        
        #リストからどの要素がチェックされたか調べる
        checkDict={0:"ランチ営業あり",1:"モーニングあり",2:"禁煙席あり",3:"日曜営業",
                  4:"駐車場あり",5:"個室あり",6:"カード可",7:"電子マネー利用可",
                  8:"wifiあり",9:"電源あり",10:"ペット同伴可",11:"Web予約可"}
        
        checkDict2={"ランチ営業あり":"lunch","モーニングあり":"breakfast","禁煙席あり":"no_smoking","日曜営業":"sunday_open",
                  "駐車場あり":"parking","個室あり":"private_room","カード可":"card","電子マネー利用可":"e_money",
                  "wifiあり":"wifi","電源あり":"outret","ペット同伴可":"with_pet","Web予約可":"web_reserve"}
        
        checkWlist=[]
        s_c_list=[]
        categoryCode=""
        count_one=0
        onelist=[]
        
        #渡されたチェックリストにチェックされた項目があるか確認
        for i in range(len(checklist)):
            if int(checklist[i])==1:
                count_one+=1
      
        #なにかチェックされていたとき  
        if count_one!=0:
            for i in range(len(checklist)):     
                #配列が1のとき、添え字をキーとしてCheckDictを検索
                if int(checklist[i])==1:
                    checkWlist.append(checkDict[i])
                    #checkDictから取り出した要素をキーとして、checkDict2から取り出す
                    for d in checkDict2:
                        for j in range(len(checkWlist)):
                            if str(checkWlist[j])==str(d):
                                s_c_list.append(checkDict2[d])
                          
        
           
        
            #queryに入れるために辞書を作る
            for i in range(len(s_c_list)):
                onelist.append(1)
        
            #辞書を作成
            items=dict(zip(s_c_list,onelist))    
    
        #どのカテゴリーが選択されたか調べ、カテゴリーコードを取得
        for d in self.category_l:
            if str(d['category_l_name'])==str(category):
                categoryCode=d['category_l_code']
                break
            
    
        ##基本のquery##
        query={"keyid":self.key,"category_l":categoryCode,"areacode_l":self.area}
            
        #フリーワードが入力されているとき、queryに追加
        if freeword !="":
              query['freeword']=freeword
            
        #チェックされた項目があるとき、項目を辞書に追加
        if count_one!=0:
            query.update(items)
                
        page_count=0 
        shoplist=[]

        #APIから得たデータをすべてリストに追加し、呼び出し元へ返す
        while(True):
            count_no=0
            
            #ページごとの表示件数
            query["hit_per_page"]=100
            #レコードの開始位置
            query['offset']=1+count_no
            #ページの開始位置
            query['offset_page']=1+page_count
            
            #APIからデータを取得
            request_api=requests.get(self.url,params=query)
            result_api=request_api.json()
            
            #エラーメッセージを代入
            error=int(request_api.status_code)
            
            #一件も見つからないとき
            if error==404: 
                #検索件数
                self.total_hit_count=0
                print("検索結果は0件でした")
                return
            
            #件数が0以上の時
            elif error==200:
                
                for i in range(len(result_api['rest'])):
                     self.backupList.append(result_api['rest'][i])
                page_count+=1
                
                hit=len(result_api['rest'])
                self.total_hit_count+=hit
    
                #1ページ分のデータを取得し、リストへ追加
                for i in range(hit):
                    count_no+=1
                    shoplist.append(result_api['rest'][i]["name"])
    
                #1ページの件数が100件を下回っていたとき、ループを抜ける
                if count_no<100:
                    break       
            #その他のエラーの時
            else:
                print(error)
                messagebox.showerror("警告","エラーが発生しました。中断します")
                return
                self.total_hit_count=0
        
        #店名のリストを返却
        return shoplist     
             
    #店舗情報を抜き出すメソッド
    def getShopInfo(self,shopname):
        
        getinfo={}
            
        #店名が同じだったとき、その店の情報を取り出す
        for d in self.backupList:
            if str(d['name'])==str(shopname):
                getinfo.update(d)
                    
        return getinfo
    
    #検索件数を返すメソッド
    def getHitCount(self):
        return self.total_hit_count


if __name__ == "__main__":
    root = tk.Tk()
    root.title("SaveList@yourtown")

     
  #フレーム生成
    mainfm = MainFrame(root)
    mainfm.mainloop()
