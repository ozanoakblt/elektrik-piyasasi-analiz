# Hafta 03: Bir MWh'nin yolculuğu

Soru: Türkiye'de elektriğin ne kadarı PTF'den fiyatlanıyor, bu pay mevsime ve yıllara göre nasıl değişiyor?

## Ana bulgular (Oca 2023 - Eki 2026, saatlik)

- Tüketimin yaklaşık %60'ı kadar enerji her saat GÖP'te, doğrudan PTF'den el değiştiriyor (%58-67 bandı).
- İkili anlaşma bildirimleri tüketimden büyük: %76 (2023) → %141 (2026). Artışın neredeyse tamamı özel anlaşmalardan.
- Yıl ve takvim ayı etkileri sabitlendiğinde bile, aylık PTF 10 USD/MWh düşükken ikili anlaşma oranı 3,5-4,6 puan yüksek. Mart-Haziran 2026 çıkarılınca da sonuç korunuyor.
- 2026'da GÖP oranı öğlen en düşük (%55), akşam en yüksek (%63).
- GİP, PTF'den ortalama 1 USD'den az sapıyor; SMF sistem yönüne göre PTF'nin üstüne ya da altına iniyor.
- "Yenilenebilir arttıkça GÖP büyür" hipotezi sağlamlık testini geçmedi.

## Tanım

EPİAŞ piyasa hacimleri alış ve satışı ayrı sayar (oran tam 2,00 doğrulandı). Analizde tek taraflı miktar kullanıldı.

## Sınırlar

- İkili anlaşmaların fiyatı, süresi ve tarafları yayınlanmıyor; artışın mekanizması bu veriyle bilinemez.
- YEKDEM üretim servisi boş döndü; vekil olarak yenilenebilir payı kullanıldı.

## İçerik

- `notebooks/01_veri_cekme.ipynb`: İA, GÖP, GİP, YAL/YAT, piyasa hacimleri (eptr2 ile; tamamlanan aylar önbelleğe alınır)
- `notebooks/02_analiz.ipynb`: oranlar, saatlik profil, sabit etkili testler, oynaklık, fiyat farkları
- `rapor/`: PDF rapor ve LinkedIn metni
