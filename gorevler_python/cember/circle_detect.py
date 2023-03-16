from math import radians, cos, sin, pi, sqrt, pow # kontrol trigonometrik fonksiyonlar ilk 16 basamaga kadar hesaplar. bu kod değiştirilmelidir.
import cv2
import numpy as np
import time

roi = None
kaideli_diziler = []
prev_frame_time = 0
new_frame_time = 0
kaydedilmis_cember_value = []
onay_alan = 0
onay_oran = 0

def kamera_islem(goruntu):
    global roi
    roi = goruntu
    color_g = np.array([25,50,50]), np.array([80,255,255])
    return main_islem(color_g)

def main_islem(color_g):
    global roi
    lower_color_HSV, upper_color_HSV = color_g
    hsv = cv2.cvtColor(roi, cv2.COLOR_BGR2HSV)
    islencek_goruntu = cv2.inRange(hsv, lower_color_HSV, upper_color_HSV)
    contours, hiyerarsi = cv2.findContours(islencek_goruntu, cv2.RETR_CCOMP,cv2.CHAIN_APPROX_NONE)
    resim_yukseklik, resim_genislik, _ = roi.shape
    cam_orta_nokta_x, cam_orta_nokta_y = int(resim_genislik/2), int(resim_yukseklik/2)
    motor_hareket = None
    if len(contours) > 0:
        odak = cember_tarama(resim_yukseklik, resim_genislik, contours, hiyerarsi)
        if odak is not None:
            x, y = kalibrasyon(odak, cam_orta_nokta_x, cam_orta_nokta_y)
            return roi, x, y
    return roi, None, None

def kalibrasyon(odak, cam_orta_nokta_x, cam_orta_nokta_y):
    global roi
    global onay_alan
    global onay_oran
    resim_yukseklik,resim_genislik,_ = roi.shape
    artanpay = resim_genislik-resim_yukseklik
    a = int(resim_yukseklik/2 + resim_yukseklik*0.3 + artanpay / 2)
    b = int(resim_yukseklik/2 + resim_yukseklik*0.3)
    c = int(resim_yukseklik/2 - resim_yukseklik*0.3 + artanpay / 2)
    d = int(resim_yukseklik/2 - resim_yukseklik*0.3)
    (nesne_yukseklik, nesne_genislik, angle_rect, nesne_orta_nokta_x, nesne_orta_nokta_y, bnd_x, bnd_y, bnd_w, bnd_h, nesne_box, rect) = odak
    cemberi_ciz(odak,(0,0,255), "")
    xuzaklik = nesne_orta_nokta_x - cam_orta_nokta_x
    yuzaklik = cam_orta_nokta_y - nesne_orta_nokta_y
    cv2.putText(roi,"x: " + str(xuzaklik) + " y: " + str(yuzaklik), (cam_orta_nokta_x + 10, cam_orta_nokta_y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,0,0), 1, cv2.LINE_AA)
    
    onay_alan = bnd_w*bnd_h*4
    onay_oran = int((kisaolan(bnd_w,bnd_h)/uzun_olan(bnd_w,bnd_h))*100)
    if onay_alan < a*a:
        cv2.rectangle(roi,(a , b),(c, d),(0,0,0),3)
    elif onay_alan > a*a and onay_oran > 80:
        cv2.rectangle(roi,(a , b),(c, d),(0,0,255),3)
        #duz ileriye gidecek kapali akil ile 85 85 80 80 85 85
    
    if()

    return xuzaklik,yuzaklik

def cember_tarama(resim_yukseklik, resim_genislik, contours, hiyerarsi):
    global roi
    tum_dizi = []
    parent_diziler = []
    for hiyer_sayi in range(0,len(hiyerarsi[0])): #kaideli parentler bulunur.
        Next =        hiyerarsi[0][hiyer_sayi][0]
        Previous =    hiyerarsi[0][hiyer_sayi][1]
        First_Child = hiyerarsi[0][hiyer_sayi][2]
        Parent =      hiyerarsi[0][hiyer_sayi][3]        
        if Parent == -1 and First_Child != -1:
            nesne_yukseklik, nesne_genislik, angle_rect, nesne_orta_nokta_x, nesne_orta_nokta_y, bnd_x, bnd_y, bnd_w, bnd_h, nesne_box, rect = size_data(contours[hiyer_sayi])
            if nesne_yukseklik > resim_yukseklik * 0.05 and nesne_genislik > resim_genislik * 0.05: #burada contours size da iş görebilir.
                parent_diziler.append(hiyer_sayi)

    for parent_kontur in range(0,len(parent_diziler)): #kaideli parentlerin kaideli childlerini bulur        
        gruplama_dizi = []
        Parent_ilk_cocuk = hiyerarsi[0][parent_diziler[parent_kontur]][2]
        while Parent_ilk_cocuk != -1:
            nesne_yukseklik, nesne_genislik, angle_rect, nesne_orta_nokta_x, nesne_orta_nokta_y, bnd_x, bnd_y, bnd_w, bnd_h, nesne_box, rect = size_data(contours[Parent_ilk_cocuk])
            if nesne_yukseklik > resim_yukseklik * 0.01 and nesne_genislik > resim_genislik * 0.01: #burada contours size da iş görebilir.
                gruplama_dizi.append(Parent_ilk_cocuk)
            Parent_ilk_cocuk = hiyerarsi[0][Parent_ilk_cocuk][0]
        if len(gruplama_dizi) > 0:
            tum_dizi.append(gruplama_dizi)

    for teker_ in tum_dizi:
        if len(teker_) > 1:
            sonuc, kritik_degerler = sekil_arastirma(resim_yukseklik, resim_genislik, contours[en_buyuk_child_konturu_bul(teker_,contours)])
            if sonuc < 85:
                sonuc, kritik_degerler = sekil_arastirma(resim_yukseklik, resim_genislik,
                birlestirme_kodu(buyukten_kucuge_2_li_sirala(teker_,contours,en_buyuk_child_konturu_bul(teker_,contours)), contours))
                if sonuc > 55:
                    cemberi_ciz(kritik_degerler,(255,0,0),sonuc)
                    kaydedilmis_cember_value.append(kritik_degerler)
            elif sonuc > 85:
                cemberi_ciz(kritik_degerler,(0,255,0),sonuc)
                kaydedilmis_cember_value.append(kritik_degerler)
        elif len(teker_) == 1:
            sonuc, kritik_degerler = sekil_arastirma(resim_yukseklik, resim_genislik, contours[teker_[0]])
            if sonuc > 85:
                cemberi_ciz(kritik_degerler,(0,255,0),sonuc)
                kaydedilmis_cember_value.append(kritik_degerler)

    kabuledilmiscircle = []
    grup_cember = []
    gidecekveri = None
    enbuyukcemberno = None
    if len(kaydedilmis_cember_value) > 0: #cemberleri dikey olarak gruplar
        for cember1 in range(0,len(kaydedilmis_cember_value)):
            for cember2 in range(0,len(kaydedilmis_cember_value)):
                (_, _, _, _, _, bnd_x1, bnd_y1, bnd_w1, bnd_h1, _, _) = kaydedilmis_cember_value[cember1]
                (_, _, _, _, _, bnd_x2, bnd_y2, bnd_w2, bnd_h2, _, _) = kaydedilmis_cember_value[cember2]
                if (cember1 != cember2) and dizide_deger_true_false(kabuledilmiscircle, cember1, cember2) and ((bnd_x1 < bnd_x2 < bnd_x1 + bnd_w1) or (bnd_x1 < bnd_x2 + bnd_w2 < bnd_x1 + bnd_w1)):
                    grup_cember.append([cember1,cember2])
                    kabuledilmiscircle.append(cember1)
                    kabuledilmiscircle.append(cember2)
                    
        for cembera in range(0,len(kaydedilmis_cember_value)): #gruplanmayan cemberleri gruplar
            if dizide_deger_true_falseso(kabuledilmiscircle,cembera):
                grup_cember.append([cembera,cembera])
                kabuledilmiscircle.append(cembera)

        enbuyukcemberno = enbuyukcemberibul(kaydedilmis_cember_value) #en buyuk alanli cemberi bulur
        bubm = dizide_deger_true_falsesonedo(grup_cember, enbuyukcemberno)
        (_, _, _, _, _, bnd_x9, bnd_y9, bnd_w9, bnd_h9, _, _) = kaydedilmis_cember_value[bubm[0]]
        (_, _, _, _, _, bnd_x8, bnd_y8, bnd_w8, bnd_h8, _, _) = kaydedilmis_cember_value[bubm[1]]
        if bubm[0] == bubm[1]:
            gidecekveri = kaydedilmis_cember_value[bubm[1]] #bubm1i baz al
        else:
            if bnd_y8 > bnd_y9:
                gidecekveri = kaydedilmis_cember_value[bubm[1]]
            elif bnd_y8 < bnd_y9:
                gidecekveri = kaydedilmis_cember_value[bubm[0]]
    return gidecekveri

def enbuyukcemberibul(kaydedilmis_cember_value):
    enbuyukalan = 0
    secili_cember = None
    for i in range(0,len(kaydedilmis_cember_value)):
        (_, _, _, _, _, bnd_xa, bnd_ya, bnd_wa, bnd_ha, _, _) = kaydedilmis_cember_value[i]
        if bnd_wa * bnd_ha > enbuyukalan:
            enbuyukalan = bnd_wa * bnd_ha
            secili_cember = i
    return secili_cember

def sekil_arastirma(resim_yukseklik, resim_genislik, gelen_kontur):
    ust_sinir = 400
    nesne_yukseklik, nesne_genislik, angle_rect, nesne_orta_nokta_x, nesne_orta_nokta_y, bnd_x, bnd_y, bnd_w, bnd_h, nesne_box, rect = size_data(gelen_kontur)            
    if bnd_x-5 > 0 and bnd_x+ bnd_w+5 < resim_genislik and bnd_y-5 > 0 and bnd_h+bnd_y+5 < resim_yukseklik:
        if nesne_genislik > resim_genislik*0.01 and nesne_yukseklik > resim_yukseklik*0.01:
            if nesne_genislik > ust_sinir and nesne_yukseklik > ust_sinir:
                contourse = kontur_kucult(gelen_kontur, ust_sinir,nesne_genislik,nesne_yukseklik)
                nesne_yukseklik, nesne_genislik, angle_rect, nesne_orta_nokta_x, nesne_orta_nokta_y, bnd_x, bnd_y, bnd_w, bnd_h, nesne_box, rect = size_data(contourse)
                sonuc = drawing_ellipse(nesne_orta_nokta_x, nesne_orta_nokta_y, angle_rect,nesne_yukseklik, nesne_genislik,contourse)
            else:
                contourse = np.vstack(list(set(tuple(row[0]) for row in gelen_kontur)))
                sonuc = drawing_ellipse(nesne_orta_nokta_x, nesne_orta_nokta_y, angle_rect,nesne_yukseklik, nesne_genislik,contourse)
            kr = (nesne_yukseklik, nesne_genislik, angle_rect, nesne_orta_nokta_x, nesne_orta_nokta_y, bnd_x, bnd_y, bnd_w, bnd_h, nesne_box, rect)
            return sonuc, kr

def drawing_ellipse(nesne_orta_nokta_x, nesne_orta_nokta_y, angle_rect,nesne_yukseklik, nesne_genislik,ctr):
    cizilen_elips_tam = []
    angle = radians(180-angle_rect)
    kabulx = int(nesne_genislik*0.07)
    kabuly = int(nesne_yukseklik*0.07)
    if kabulx < 3:
        kabulx=3
    if kabuly < 3:
        kabuly=3
    steps_jump = int(kabulx/3)
    if(steps_jump > 1):
        pass
    else:
        steps_jump = 1
    steps = int(360 * ((uzun_olan(nesne_genislik, nesne_yukseklik)/57)))
    
    for t in range(steps):
        x_orj = int(nesne_genislik * cos(2 * pi * t/steps))
        y_orj = int(nesne_yukseklik * sin(2 * pi * t/steps))
        y = int(x_orj*cos(angle) - y_orj*sin(angle))
        x = int(x_orj*sin(angle) + y_orj*cos(angle))
        cizilen_elips_tam.append([x,y])
    cizilen_elips_tam_plus = np.vstack(list(set(tuple(row) for row in cizilen_elips_tam)))
    veriler = nesne_orta_nokta_x, nesne_orta_nokta_y,cizilen_elips_tam_plus,kabulx,kabuly
    sonuc = hesaplama(ctr,veriler)
    return sonuc

def hesaplama(ctr,veriler):
    sayac = 0
    nesne_orta_nokta_x, nesne_orta_nokta_y,cizilen_elips_tam,kabulx,kabuly = veriler
    for a in ctr:
        x,y = a[0],a[1]
        dogruluk = True
        for i in cizilen_elips_tam:
            if dogruluk == True and nesne_orta_nokta_x+kabulx > x+i[0] > nesne_orta_nokta_x-kabulx and nesne_orta_nokta_y+kabuly > y+i[1] > nesne_orta_nokta_y-kabuly:
                sayac += 1
                dogruluk = False
    return int((sayac/len(ctr))*100)

def size_data(ctr):
    rect = cv2.minAreaRect(ctr)
    nesne_yukseklik, nesne_genislik = int(rect[1][0]/2),int(rect[1][1]/2)
    angle_rect = int(rect[2])
    nesne_orta_nokta_x, nesne_orta_nokta_y = int(rect[0][0]),int(rect[0][1])
    (bnd_x, bnd_y, bnd_w, bnd_h) = cv2.boundingRect(ctr)
    box = cv2.boxPoints(rect)
    nesne_box = np.int0(box)
    return nesne_yukseklik,nesne_genislik,angle_rect,nesne_orta_nokta_x,nesne_orta_nokta_y,bnd_x,bnd_y,bnd_w,bnd_h,nesne_box, rect

def kamera_xy_cizgi(ior):
    resim_yukseklik,resim_genislik,_ = ior.shape
    for i in range(0, resim_yukseklik ):
        ior[i, int(resim_genislik/2)] = [0,150,150]
    for i in range(0, resim_genislik ):
        ior[int(resim_yukseklik/2), i] = [0,150,150]
    return ior

def uzaklik_hesaplayici(ana_govde_x, ana_govde_y, secilen_govde_x,secilen_govde_y):
    return sqrt(pow((ana_govde_x-secilen_govde_x),2) + pow((ana_govde_y-secilen_govde_y),2))

def uzun_olan(k,l):
    if k > l:
        return k
    else:
        return l
    
def kisaolan(k,l):
    if k > l:
        return l
    else:
        return k

def ebob(i,k):
    if i >= k:
        return k/i
    else:
        return i/k

def fps_func(prev_frame_time,new_frame_time):
    new_frame_time = time.time()
    fps = 1/(new_frame_time-prev_frame_time)
    prev_frame_time = new_frame_time
    fps = str(int(fps))
    return fps, prev_frame_time, new_frame_time

def kontur_kucult(kontur, ust, nesne_genislik,nesne_yukseklik):
    M = cv2.moments(kontur)
    cx = int(M['m10']/M['m00'])
    cy = int(M['m01']/M['m00'])
    cnt_norm = kontur - [cx, cy]
    scaled = ((100 / (uzun_olan(nesne_genislik,nesne_yukseklik)/ust))/100)
    cnt_scaled = cnt_norm * scaled
    cnt_scaled = cnt_scaled + [cx, cy]
    cnt_scaled = cnt_scaled.astype(np.int32)
    data = np.vstack(list(set(tuple(row[0]) for row in cnt_scaled)))
    return data

def en_buyuk_child_konturu_bul(tum_nesneler,contours):
    en_buyuku = None
    buyukluk_sayi = 0
    for za in tum_nesneler:
        kontur_size = contours[za].size
        if kontur_size > buyukluk_sayi:
            en_buyuku = za
            buyukluk_sayi = kontur_size    
    return en_buyuku

def buyukten_kucuge_2_li_sirala(tum_nesneler,contours,buyuk_nesne):
    fav_yakinlik = 9999999999999
    secilen_nesne = None
    nesne_yukseklik, nesne_genislik, angle_rect, nesne_orta_nokta_x, nesne_orta_nokta_y, bnd_x, bnd_y, bnd_w, bnd_h, nesne_box, rect = size_data(contours[buyuk_nesne])
    for fus in tum_nesneler:
        if buyuk_nesne != fus:
            nesne_yukseklika, nesne_genislika, angle_recta, nesne_orta_nokta_xa, nesne_orta_nokta_ya, bnd_xa, bnd_ya, bnd_wa, bnd_ha, nesne_boxa, recta = size_data(contours[fus])
            uzaklik = uzaklik_hesaplayici(nesne_orta_nokta_x,nesne_orta_nokta_y,nesne_orta_nokta_xa,nesne_orta_nokta_ya)
            if uzaklik < fav_yakinlik:
                fav_yakinlik = uzaklik
                secilen_nesne = fus
    return [buyuk_nesne, secilen_nesne]

def birlestirme_kodu(ta_dizi, contours):
    tamame = np.concatenate((contours[ta_dizi[0]],contours[ta_dizi[1]]), axis=0)
    return tamame

def cemberi_ciz(kritik_degerler,renk,sonuc):
    global roi
    (nesne_yukseklik, nesne_genislik, angle_rect, nesne_orta_nokta_x, nesne_orta_nokta_y, bnd_x, bnd_y, bnd_w, bnd_h, nesne_box, rect) = kritik_degerler
    cv2.ellipse(roi, (nesne_orta_nokta_x,nesne_orta_nokta_y), (nesne_genislik,nesne_yukseklik), 270+angle_rect, 0, 360, renk, 2)
    if sonuc != "":
        cv2.putText(roi, "%"+ str(sonuc) + "e - %"+ str(int(ebob(nesne_yukseklik,nesne_genislik)*100)) + "c", (nesne_orta_nokta_x,nesne_orta_nokta_y), cv2.FONT_HERSHEY_SIMPLEX,0.5, renk, 1, cv2.LINE_AA)


def dizide_deger_true_false(dizi, aranendeger1, aranendeger2):
    if len(dizi) == 0:
        return True
    for a in dizi:
        if a == aranendeger1 or a == aranendeger2:
            return False
    return True

def dizide_deger_true_falsesonedo(dizi, aranendeger):
    if len(dizi) == 0:
        return True
    for a in dizi:
        if a[0] == aranendeger or a[1] == aranendeger:
            return [a[0],a[1]]
    return None

def dizide_deger_true_falseso(dizi, aranendeger):
    if len(dizi) == 0:
        return True
    for a in dizi:
        if a == aranendeger:
            return False
    return True

def baslangic():
    global prev_frame_time, new_frame_time
    roi = cv2.imread("a.png")
    resim_yukseklik, resim_genislik, _ = roi.shape
    roi, x, y = kamera_islem(roi)  
    roi = kamera_xy_cizgi(roi)  
    fps, prev_frame_time, new_frame_time = fps_func(prev_frame_time,new_frame_time)

    cv2.putText(roi, fps + " FPS", (15,15), cv2.FONT_HERSHEY_SIMPLEX,0.5, (0,0,255), 1, cv2.LINE_AA)

    cv2.imshow('tespit',roi)
    cv2.imwrite('cikti.png',roi)
    cv2.waitKey()

if __name__ == '__main__':
    baslangic()