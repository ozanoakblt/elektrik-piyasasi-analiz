import base64,asyncio,html
from playwright.async_api import async_playwright
def img(n): return "data:image/png;base64,"+base64.b64encode(open(f"g/{n}.png","rb").read()).decode()
BOLT='<svg width="22" height="22" viewBox="0 0 22 22"><polygon points="12,1 4,12 10,12 8,21 18,8 12,8" fill="#ffd400" stroke="#6b5200" stroke-width="1"/></svg>'
CSS="""
@page{size:1080px 1350px;margin:0}*{box-sizing:border-box}body{margin:0}
.p{width:1080px;height:1350px;padding:34px 36px 30px;display:flex;flex-direction:column;gap:12px;page-break-after:always;overflow:hidden;
 background-color:#1c5ad0;background-image:linear-gradient(45deg,rgba(255,255,255,.07) 25%,transparent 25%,transparent 75%,rgba(255,255,255,.07) 75%),linear-gradient(45deg,rgba(255,255,255,.07) 25%,transparent 25%,transparent 75%,rgba(255,255,255,.07) 75%);background-size:8px 8px;background-position:0 0,4px 4px;
 font-family:'Liberation Sans',Arial,sans-serif;color:#0b0b0b}
.win{background:#c0c0c0;border:3px solid;border-color:#fff #404040 #404040 #fff;box-shadow:4px 4px 0 rgba(0,0,40,.45);padding:3px;display:flex;flex-direction:column}
.tb{height:42px;background:linear-gradient(90deg,#0a1f6b,#3a74dc);display:flex;align-items:center;justify-content:space-between;padding:0 8px;color:#fff;font-family:'DejaVu Sans Mono',monospace;font-weight:700;font-size:19px;letter-spacing:.02em}
.tb .l{display:flex;gap:10px;align-items:center}
.tb .bt{display:flex;gap:4px}.tb .bt i{display:block;width:28px;height:26px;background:#c0c0c0;border:2px solid;border-color:#fff #404040 #404040 #fff;color:#000;font-style:normal;font-size:17px;line-height:20px;text-align:center}
.main{flex:1;min-height:0}.body{flex:1;min-height:0;background:#fff;margin-top:3px;border:2px solid;border-color:#404040 #fff #fff #404040;padding:20px 34px 12px;display:flex;flex-direction:column;overflow:hidden}
h1,h2{font-family:'DejaVu Sans Mono',monospace;font-weight:700;color:#0a2a8a;text-shadow:3px 3px 0 #9fc2f5;margin:0 0 14px;line-height:1.12}
h1{font-size:60px}h2{font-size:40px}
p{font-size:28px;line-height:1.42;margin:0 0 12px;color:#111}
.cap{font-size:19px;line-height:1.35;color:#444;margin:8px 0 12px}
.fig{border:3px solid;border-color:#808080 #fff #fff #808080;background:#fff;padding:4px;margin-top:4px}.fig img{width:100%;display:block}
.tiles{display:flex;gap:14px;margin:6px 0 14px}.tile{flex:1;background:#020a3a;border:3px solid;border-color:#404040 #c0c0c0 #c0c0c0 #404040;padding:10px 14px;color:#7fe4ff;font-family:'DejaVu Sans Mono',monospace}
.tile b{display:block;font-size:46px;line-height:1.05;color:#fff;text-shadow:0 0 12px #3ac8ff}.tile span{font-size:17px;line-height:1.25;display:block;margin-top:4px}
.tick{background:#020a3a;border:3px solid;border-color:#404040 #c0c0c0 #c0c0c0 #404040;color:#7fe4ff;font-family:'DejaVu Sans Mono',monospace;font-size:21px;padding:11px 14px;white-space:nowrap;overflow:hidden;text-shadow:0 0 6px #3ac8ff}
.st{display:flex;gap:6px}.st div{flex:1;background:#c0c0c0;border:2px solid;border-color:#808080 #fff #fff #808080;font-size:17px;padding:6px 10px;color:#111;white-space:nowrap;overflow:hidden}
.nav{display:flex;gap:4px;background:#c0c0c0;border:3px solid;border-color:#fff #404040 #404040 #fff;padding:6px}
.nav i{flex:1;font-style:normal;text-align:center;font-family:'DejaVu Sans Mono',monospace;font-size:17px;font-weight:700;padding:6px 0;background:#c0c0c0;border:2px solid;border-color:#fff #404040 #404040 #fff;color:#000}
.nav i.on{background:#0a1f6b;color:#fff;border-color:#404040 #fff #fff #404040}
ul{margin:0;padding-left:34px}li{font-size:32px;line-height:1.42;margin-bottom:18px}
.row{display:flex;gap:24px}.art{width:340px;flex:none;border:3px solid;border-color:#808080 #fff #fff #808080}
"""
PYLON='''<svg viewBox="0 0 340 400" width="340" height="400"><defs><linearGradient id="sk" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#6fb4f2"/><stop offset="1" stop-color="#cfe8ff"/></linearGradient></defs>
<rect width="340" height="400" fill="url(#sk)"/><rect x="0" y="352" width="340" height="48" fill="#3f9a38"/><rect x="0" y="346" width="340" height="8" fill="#2d7a2a"/>
<g fill="#fff"><rect x="30" y="50" width="56" height="14"/><rect x="44" y="38" width="30" height="14"/><rect x="230" y="84" width="64" height="14"/><rect x="246" y="72" width="34" height="14"/></g>
<g stroke="#1b2a5a" stroke-width="5" fill="none" stroke-linejoin="miter"><polyline points="120,350 150,70 170,40 190,70 220,350"/>
<line x1="132" y1="270" x2="208" y2="270"/><line x1="140" y1="200" x2="200" y2="200"/><line x1="146" y1="140" x2="194" y2="140"/>
<line x1="120" y1="350" x2="208" y2="270"/><line x1="220" y1="350" x2="132" y2="270"/><line x1="132" y1="270" x2="200" y2="200"/><line x1="208" y1="270" x2="140" y2="200"/><line x1="140" y1="200" x2="194" y2="140"/><line x1="200" y1="200" x2="146" y2="140"/>
<line x1="60" y1="96" x2="280" y2="96"/><line x1="82" y1="128" x2="258" y2="128"/></g>
<g stroke="#1b2a5a" stroke-width="2.5" fill="none"><path d="M0,120 Q60,150 60,96"/><path d="M60,96 Q160,126 280,96"/><path d="M280,96 Q310,150 340,126"/><path d="M0,150 Q40,170 82,128"/><path d="M82,128 Q170,156 258,128"/><path d="M258,128 Q300,170 340,160"/></g>
<g fill="#ddd" stroke="#1b2a5a" stroke-width="2"><rect x="56" y="96" width="8" height="14"/><rect x="276" y="96" width="8" height="14"/><rect x="78" y="128" width="8" height="14"/><rect x="254" y="128" width="8" height="14"/></g>
<polygon points="276,176 244,236 264,236 252,292 300,218 278,218 292,176" fill="#ffd400" stroke="#7a5d00" stroke-width="3"/></svg>'''
MERIT='''<svg viewBox="0 0 900 330" width="100%"><rect x="2" y="2" width="896" height="326" fill="#fff" stroke="#808080" stroke-width="2"/>
<g font-family="DejaVu Sans Mono,monospace" font-size="17" fill="#0a1f6b">
<rect x="70" y="236" width="110" height="64" fill="#7fb4ff" stroke="#0a1f6b" stroke-width="2"/><text x="82" y="224">GÜNEŞ</text>
<rect x="180" y="226" width="110" height="74" fill="#7fb4ff" stroke="#0a1f6b" stroke-width="2"/><text x="188" y="214">RÜZGÂR</text>
<rect x="290" y="208" width="110" height="92" fill="#4f86e8" stroke="#0a1f6b" stroke-width="2"/><text x="324" y="196">SU</text>
<rect x="400" y="170" width="110" height="130" fill="#9aa3b5" stroke="#0a1f6b" stroke-width="2"/><text x="418" y="158">KÖMÜR</text>
<rect x="510" y="118" width="110" height="182" fill="#e8590c" stroke="#0a1f6b" stroke-width="2"/><text x="510" y="106">DOĞALGAZ</text>
<rect x="620" y="56" width="110" height="244" fill="#d8dce6" stroke="#0a1f6b" stroke-width="2" stroke-dasharray="6 4"/><text x="632" y="44" fill="#666">PAHALI</text>
<line x1="70" y1="300" x2="740" y2="300" stroke="#0a1f6b" stroke-width="3"/>
<line x1="612" y1="20" x2="612" y2="300" stroke="#d11" stroke-width="3" stroke-dasharray="8 5"/><text x="618" y="20" fill="#d11">TALEP</text>
<line x1="70" y1="118" x2="612" y2="118" stroke="#111" stroke-width="2.5"/><text x="74" y="106" fill="#111" font-weight="700">PTF = son kabul edilen teklif</text>
<text x="70" y="324" font-size="15" fill="#444">ucuz  ----------------------------------------------------------&gt;  pahalı</text></g></svg>'''
PAGES=[]
def page(slug,title_path,content,ticker,units,period="Oca 2023 - Eki 2026"):
    PAGES.append(dict(path=title_path,content=content,ticker=ticker,units=units,period=period))
def win(path,body):
    return f'<div class="win main"><div class="tb"><div class="l">{BOLT}<span>{path}</span></div><div class="bt"><i>_</i><i>□</i><i>×</i></div></div><div class="body">{body}</div></div>'
def chart(kick,title,imgn,cap,text,tiles=None):
    t=""
    if tiles: t='<div class="tiles">'+"".join(f'<div class="tile"><b>{a}</b><span>{b}</span></div>' for a,b in tiles)+'</div>'
    return f'<h2>{title}</h2>{t}<div class="fig"><img src="{img(imgn)}"></div><div class="cap">{cap}</div><p>{text}</p>'
# 1 cover
page("ozet","C:\\ELEKTRIK\\HAFTA01\\01_OZET.HTM",
 f'<div class="row"><div style="flex:1"><h1 style="margin-top:20px">Elektriğin saati ve mevsimi</h1><p>EPİAŞ Şeffaflık Platformu verisiyle 2023-2026 arası <b>33.600 saatlik</b> PTF analizi: günün saati, yılın ayı, güneş, rüzgâr ve su.</p></div><div class="art">{PYLON}</div></div>'
 '<div class="tiles" style="margin-top:70px"><div class="tile"><b>%17</b><span>Mayıs 2026 PTF (USD), önceki 3 yılın Mayıs ortalamasının yüzdesi</span></div><div class="tile"><b>%50</b><span>Mayıs 2026\'da hidroelektriğin üretimdeki payı (önceki yıllar %29-33)</span></div><div class="tile"><b>244</b><span>Mayıs 2026\'da PTF\'nin 100 TL/MWh altında kaldığı saat</span></div></div>'
 '<p style="margin-top:30px;font-size:34px">Öğle çukuru her yıl derinleşiyor. 2026 baharı ise bu eğilimin de dışına çıktı ve bu kopuşa hidrolojik olarak bol bir bahar eşlik ediyor.</p>',
 "*** Mayıs 2026 PTF, önceki üç yılın Mayıs ortalamasının %17'si ***",["Veri: EPİAŞ Şeffaflık","Dönem: Oca 2023-Eki 2026","Birim: USD/MWh"])
# 2 mechanism
page("mekanizma","C:\\ELEKTRIK\\HAFTA01\\02_MEKANIZMA.HTM",
 f'<h2>PTF nasıl oluşuyor?</h2><p>Gün öncesi piyasasında her saat için satış teklifleri <b>ucuzdan pahalıya</b> dizilir. Talep miktarı dolana kadar tekliflerin üzerinden yukarı çıkılır.</p><div class="fig" style="margin:6px 0 16px">{MERIT}</div><div style="border-left:8px solid #e8590c;padding:4px 0 4px 18px;margin:6px 0 14px"><p style="font-weight:700;color:#0a2a8a;margin:0">Talebi karşılayan son teklif, o saatin fiyatını belirler. Bu fiyata PTF denir.</p></div><p>Güneş, rüzgâr ve su gibi düşük maliyetli kaynaklar sıranın başında yer alır. Bunlar talebi büyük ölçüde karşılarsa pahalı santrallere ihtiyaç kalmaz ve fiyat düşer. Bu seride fiyatın saate, aya ve üretim karışımına göre nasıl değiştiğine bakıyoruz.</p>'.replace('<p>','<p style="font-size:31px">'),
 "*** Talebi karşılayan son teklif = PTF ***",["Kaynak: EPİAŞ GÖP işleyişi","Şema: temsili","Birim: -"],"-")
# 3 mevsim
page("mevsim","C:\\ELEKTRIK\\HAFTA01\\03_MEVSIM.HTM",chart("","Elektrik fiyatının mevsimi var mı?","c1","Her ay, o yılın Oca-Eki ortalamasına oranlanmıştır (1,0 = ortalama). 2026'da Kasım-Aralık olmadığından tüm yıllarda aynı 10 aylık referans kullanıldı.","2023-2025'te Nisan ve Haziran en ucuz, Temmuz-Ağustos en pahalı aylar. 2026 baharı bu desenin dışında. 2026 Temmuz-Ekim'in \"yüksek\" görünmesi hesap yönteminden gelen bir yanlılıktır, ilerleyen sayfada düzeltiyoruz."),
 "*** Nisan-Haziran en ucuz, Temmuz-Ağustos en pahalı ***",["Veri: EPİAŞ Şeffaflık","Dönem: Oca 2023-Eki 2026","Birim: oran (1,0=ort.)"])
# 4 saat
page("saat","C:\\ELEKTRIK\\HAFTA01\\04_SAAT.HTM",chart("","Gün içinde en ucuz saat öğle, en pahalı saat akşam","c2","2023-2025 ortalaması, saat x ay. Mavi: yıl ortalamasının altı, kırmızı: üstü.","Nisan-Haziran öğle saatleri belirgin biçimde ucuz. 17-21 arası akşam saatleri ise yılın hemen her ayında pahalı."),
 "*** Öğle ucuz, 17-21 akşam pahalı ***",["Veri: EPİAŞ Şeffaflık","Dönem: 2023-2025 ort.","Birim: PTF/yıl ort."])
# 5 yıllara göre
page("yillar","C:\\ELEKTRIK\\HAFTA01\\05_YILLAR.HTM",chart("","Öğle çukuru her yıl derinleşti","n7","Saatlik ortalama PTF, her yılın Oca-Eki dönemi. 2023 fiyat düzeyi yüksek olduğundan eğrileri düzeyden çok şekil olarak oku.","2026 rakamlarına bahar hidrolojisi de dahil, ama 2023-2025 arasındaki eğilim ondan bağımsız.",[("0,93 → 0,67","Öğle fiyatı / yıl ortalaması, 2023 → 2026"),("1,29 → 2,22","Akşam fiyatı / öğle fiyatı, 2023 → 2026")]),
 "*** Öğle fiyatı / yıl ortalaması: 0,93 (2023) → 0,67 (2026) ***",["Veri: EPİAŞ Şeffaflık","Dönem: Oca-Eki, her yıl","Birim: USD/MWh"])
# 6 ucuz saatler
page("ucuz","C:\\ELEKTRIK\\HAFTA01\\06_UCUZ.HTM",chart("","Mayıs 2026'da 244 saat PTF 100 TL/MWh altında","c4","PTF=0 olan 469 saatin 413'ü 2026'da görüldü; çoğu öğle saatlerinde.","Fiyat tavanları yıllar içinde değiştiği için burada TL düzeyi yerine sıfıra yakın saat sayısına bakıyoruz.",[("244","Mayıs 2026'da PTF < 100 TL/MWh saat sayısı"),("413 / 469","PTF=0 saatlerinin 2026'daki payı")]),
 "*** PTF=0 olan 469 saatin 413'ü 2026'da ***",["Veri: EPİAŞ Şeffaflık","Dönem: Oca 2023-Eki 2026","Birim: saat (TL eşiği)"])
# 7 gün içi
page("gunici","C:\\ELEKTRIK\\HAFTA01\\07_GUNICI.HTM",chart("","Düşüş her saatte aynı değil","n5","Nisan-Haziran ortalaması, USD/MWh. Etiketler 2025'e göre değişim.","Fark açılınca akşam saatlerini karşılayabilen esnek kaynakların değeri öne çıkıyor.",[("−%88","gündüz (06-16)"),("−%38","akşam (17-21)"),("−%70","gece (22-05)")]),
 "*** Gündüz -%88, akşam -%38 (Nis-Haz 2026 / 2025, USD) ***",["Veri: EPİAŞ Şeffaflık","Dönem: Nis-Haz 2025/2026","Birim: USD/MWh"])
# 8 duzeltme
page("duzeltme","C:\\ELEKTRIK\\HAFTA01\\08_DUZELTME.HTM",chart("","Dolar bazında 2026 yazı normalin üstünde değil","n1","2026 aylık ortalama PTF (USD), 2023-2025 aynı ay ortalamasına oran. Turuncu: %50 altı.","Temmuz-Ekim, geçmiş yılların aynı aylarının %76-83'ü seviyesinde. Yıl ortalaması yöntemi bunu olduğundan yüksek gösteriyordu.",[("%17","Mayıs 2026"),("%76-83","Temmuz-Ekim 2026")]),
 "*** USD bazında Tem-Ekim 2026, geçmiş yılların %76-83'ü ***",["Veri: EPİAŞ Şeffaflık","Dönem: Oca-Eki 2026","Birim: % (2023-25 aynı ay)"])
# 9 gunes ruzgar
page("pay","C:\\ELEKTRIK\\HAFTA01\\09_GUNES_RUZGAR.HTM",chart("","Güneş ve rüzgârın payı yıllar içinde büyüdü","n8","Saatlik ortalama pay, toplam üretim içinde, Oca-Eki. * EPİAŞ gerçek zamanlı üretimdeki güneş; lisanssız üretimin önemli bölümünü kapsamayabilir, gerçek güneş payı bundan yüksek olabilir.","Ortalama güneş üretimi 467 MW'tan 1.024 MW'a yükseldi.",[("%3,5 → %8,1","Güneşin öğle (10-15) payı, 2023 → 2026"),("%10,3 → %13,2","Rüzgârın öğle payı, 2023 → 2026")]),
 "*** Öğle saatlerinde güneş payı %3,5'ten %8,1'e çıktı ***",["Veri: EPİAŞ gerçek zamanlı","Dönem: Oca-Eki, her yıl","Birim: % (toplam üretim)"])
# 10 cukur
page("cukur","C:\\ELEKTRIK\\HAFTA01\\10_CUKUR.HTM",chart("","Öğlen yenilenebilir payı arttıkça öğle fiyatı düşüyor","n9","Her nokta bir ay (40 ay). Öğle: 10-15. Korelasyon -0,56; nedensellik iddiası değildir.","Bu, güneşin öğle çukurunu açan bir etken olduğuyla uyumlu. Tek başına açıklama değil: hidroloji, talep ve yakıt maliyeti de etkili. 2026'nın en düşük iki noktası hidro kaynaklı.",[("-0,56","aylık öğle güneş+rüzgâr payı ile öğle fiyatı korelasyonu")]),
 "*** Öğle yenilenebilir payı ile öğle fiyatı: korelasyon -0,56 ***",["Veri: EPİAŞ Şeffaflık","Dönem: Oca 2023-Eki 2026","Birim: USD/MWh, %"])
# 11 mix
page("karisim","C:\\ELEKTRIK\\HAFTA01\\11_KARISIM.HTM",chart("","Üretim karışımı değişti: su geldi, kömür ve gaz çekildi","c6","* EPİAŞ gerçek zamanlı üretim verisindeki güneş. Lisanssız üretimin tamamını kapsamayabilir.","Nisan-Haziran 2025 ile 2026 arasında güneş neredeyse aynı kaldı.",[("+6,6 GW","hidroelektrik"),("−3,5 GW","ithal kömür"),("−2,2 GW","doğal gaz")]),
 "*** Nis-Haz 2026: hidro +6,6 GW, ithal kömür -3,5 GW, gaz -2,2 GW ***",["Veri: EPİAŞ gerçek zamanlı","Dönem: Nis-Haz 2025/2026","Birim: GW (saatlik ort.)"])
# 12 net yuk
page("netyuk","C:\\ELEKTRIK\\HAFTA01\\12_NETYUK.HTM",chart("","Aynı talepte fiyat çok daha düşük","n2","Net yük = tüketim - rüzgâr - güneş. Nisan-Haziran, USD/MWh.","Eğri aşağı kaydı: aynı talebi karşılamak için daha ucuz teklifler yeterli oldu.",[("63 → 17","30-35 GW net yükte ortalama PTF, USD/MWh (2025 → 2026)")]),
 "*** Aynı net yükte fiyat: 63 USD/MWh → 17 USD/MWh ***",["Veri: EPİAŞ Şeffaflık","Dönem: Nis-Haz 2025/2026","Birim: USD/MWh"])
# 13 regresyon
page("regresyon","C:\\ELEKTRIK\\HAFTA01\\13_REGRESYON.HTM",chart("","Regresyon da aynı yöne işaret ediyor","n3","Saat, ay ve yıl etkileri sabit; 33.600 saatlik regresyon, %95 güven aralığı. Katsayılar saat bazında ortalama etkidir, kaynaklar arasında birebir kıyas değildir.","Hidro, rüzgâr ve güneş arttıkça fiyat düşüyor, tüketim arttıkça yükseliyor. Ancak doğal gaz ve kömür fiyatı modelde yok; katsayıların büyüklüğü nihai kabul edilmemeli. Yakıt maliyeti Hafta 3'te eklenecek."),
 "*** Yönler tutarlı; büyüklükler yakıt maliyeti eklenince doğrulanacak ***",["Model: OLS + saat/ay/yıl FE","Hata: Newey-West (24)","Birim: USD/MWh per GW"])
# 14 baraj
page("baraj","C:\\ELEKTRIK\\HAFTA01\\14_BARAJ.HTM",chart("","Barajlı hidro akşama kaydırılıyor","n4","Nisan-Haziran saatlik ortalama üretim, GW.","2026'da barajlı üretim her saatte arttı ama akşam saatlerinde 15-16 GW'a çıkıyor. Akarsu üretimi gün içinde neredeyse sabit. Barajlı hidro, akşam fiyatının gündüze göre çok daha az düşmesini kısmen açıklayabilir."),
 "*** 2026'da barajlı hidro akşam saatlerinde 15-16 GW'a çıkıyor ***",["Veri: EPİAŞ gerçek zamanlı","Dönem: Nis-Haz 2025/2026","Birim: GW (saatlik ort.)"])
# 15 yagis
page("yagis","C:\\ELEKTRIK\\HAFTA01\\15_YAGIS.HTM",chart("","Zincirin başı: yağış, iki ay sonra hidro","n6","Yağış: Elazığ, Şanlıurfa, Artvin, Sivas, Erzurum, Diyarbakır noktalarının ortalaması (Open-Meteo). Havza ağırlıkları temsili değildir.","Oca-May toplam yağışı 2026'da 539 mm ile dört yılın en yükseği; 2025'te 291 mm idi.",[("0,65","yağış-hidro korelasyonu, 2 ay gecikmeli (gecikmesiz 0,32)"),("8,9 → 15,5","Nis-Haz hidro, GW (2025 → 2026)")]),
 "*** Yağış, hidro üretimini yaklaşık 2 ay gecikmeyle izliyor ***",["Veri: Open-Meteo + EPİAŞ","Dönem: Oca 2023-Eki 2026","Birim: mm/ay, GW"])
# 16 cikarimlar
page("cikarim","C:\\ELEKTRIK\\HAFTA01\\16_CIKARIM.HTM",
 '<h2>Portföy yönetimi için çıkarımlar</h2><ul><li>Yıl ortalaması tek başına yanıltıcı. Aylık ve saatlik profil ayrı izlenmeli.</li><li>Öğle çukuru 2023\'ten beri her yıl derinleşiyor ve güneş ile rüzgârın payı büyüyor. Bu eğilim, bol sulu bir bahardan bağımsız olarak, öğle üretimi satan portföyler için yapısal bir risk.</li><li>Bol sulu baharda öğle fiyatı sıfıra yaklaşıyor. Öğle saatlerinde üretim satan portföyler için gelir riski büyüyor.</li><li>Akşam fiyatı gündüze göre çok daha az düşüyor. Akşam saatlerini karşılayabilen esnek kaynakların (depolama, talep yönetimi, barajlı hidro) değeri artıyor.</li><li>Hidroloji, fiyat tahmininde güneş ve rüzgârdan en az o kadar önemli bir girdi.</li></ul>',
 "*** Esneklik akşam saatlerinde değer kazanıyor ***",["Sonuç sayfası","Dönem: 2023-2026","Birim: -"],"2023-2026")
# 17 yontem
page("yontem","C:\\ELEKTRIK\\HAFTA01\\17_YONTEM.HTM",
 '<h2>Nasıl hesapladım?</h2><ul style="padding-left:30px"><li style="font-size:29px;margin-bottom:14px">Veri: EPİAŞ Şeffaflık Platformu. PTF, gerçek zamanlı üretim ve tüketim; 33.600 saat, Oca 2023 - Eki 2026.</li><li style="font-size:29px;margin-bottom:14px">Fiyat karşılaştırmaları USD bazında, aynı ay karşılaştırmasıyla yapıldı. Nominal TL düzeyleri yıllar arasında doğrudan kıyaslanmadı.</li><li style="font-size:29px;margin-bottom:14px">Regresyon: saatlik USD PTF, hidro + rüzgâr + güneş + tüketim, saat/ay/yıl sabit etkili, Newey-West standart hataları (24 gecikme).</li><li style="font-size:29px;margin-bottom:14px">Doğal gaz ve ithal kömür fiyatları ve fiyat tavanı modelde yok; katsayıların büyüklüğü kesin kabul edilmemeli. Sonuçlar nedensellik değil, ilişkidir.</li><li style="font-size:29px;margin-bottom:14px">Güneş, EPİAŞ gerçek zamanlı üretimdeki "sun" alanıdır; lisanssız üretimi tam yansıtmayabilir.</li><li style="font-size:29px;margin-bottom:14px">Yağış: Open-Meteo, 6 nokta ortalaması; kar erimesi ve baraj rezervi gecikme yaratır. Sıradaki adım: yakıt maliyetini ekleyerek nicel payları yeniden hesaplamak.</li><li style="font-size:29px;margin-bottom:14px">Paylaşımlar kişisel çalışmamdır.</li></ul>',
 "*** Bunlar ilişkilerdir, nedensellik iddiası değildir ***",["Yöntem sayfası","Kod: Python (pandas, statsmodels)","Birim: -"],"2023-2026")
N=len(PAGES)
out=[]
for k,pg in enumerate(PAGES,1):
    nav='<div class="nav">'+"".join(f'<i class="{"on" if j==k else ""}">{j}</i>' for j in range(1,N+1))+'</div>'
    st='<div class="st">'+"".join(f'<div>{html.escape(u)}</div>' for u in pg["units"])+'</div>'
    out.append(f'<div class="p">{win(pg["path"],pg["content"])}<div class="tick">{html.escape(pg["ticker"])}</div>{st}{nav}</div>')
H=f"<html><head><meta charset=utf-8><style>{CSS}</style></head><body>{''.join(out)}</body></html>"
open("k.html","w").write(H)
async def main():
    async with async_playwright() as p:
        b=await p.chromium.launch();pg=await b.new_page(viewport={"width":1080,"height":1350})
        await pg.set_content(H);await pg.wait_for_timeout(600)
        ov=await pg.evaluate("[...document.querySelectorAll('.body')].map((e,i)=>[i+1,e.scrollHeight-e.clientHeight])")
        print("overflow:",[o for o in ov if o[1]>0])
        await pg.pdf(path="Hafta01_Carousel_v5_retro.pdf",width="1080px",height="1350px",print_background=True)
        await b.close()
asyncio.run(main())
