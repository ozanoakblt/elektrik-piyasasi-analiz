import pandas as pd, numpy as np, matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib import font_manager as fm
import logging; logging.getLogger("matplotlib.font_manager").setLevel(logging.ERROR)

plt.rcParams.update({"font.family":"DejaVu Sans Mono","font.size":10.5,"axes.spines.top":False,"axes.spines.right":False,"axes.edgecolor":"#0a1f6b","axes.linewidth":1.5,"axes.labelcolor":"#0a1f6b","xtick.color":"#0a1f6b","ytick.color":"#0a1f6b","axes.grid":True,"grid.color":"#c9d4ee","grid.linewidth":1,"grid.linestyle":":","axes.axisbelow":True})
NV,OR,G1,G2,G3="#0a1f6b","#e8590c","#c3d0ee","#7f9bd6","#2f4fb0"
import os
DATA=os.environ.get("H01_DATA","../../02_islenmis")
os.makedirs("g",exist_ok=True)
P=f"{DATA}/ana_tablo_saatlik.csv"
df=pd.read_csv(P,parse_dates=["zaman"]).set_index("zaman")
df["y"]=df.index.year;df["m"]=df.index.month;df["h"]=df.index.hour
df["hidro"]=df.uretim_dammedHydro+df.uretim_river
ay=["Oca","Şub","Mar","Nis","May","Haz","Tem","Ağu","Eyl","Eki","Kas","Ara"]
ref=df[df.m<=10].groupby("y").ptf.mean()
mm=df.groupby(["y","m"]).ptf.mean().unstack(0)/ref  # oran
def save(fig,n): fig.savefig(f"g/{n}.png",dpi=200,facecolor="white"); plt.close(fig)

# C1 mevsim
fig,ax=plt.subplots(figsize=(9.6,6.2))
for y,c,lw in [(2023,G1,2),(2024,G2,2),(2025,G3,2.2),(2026,OR,3.4)]:
    s=mm[y].dropna(); ax.plot(s.index,s.values,color=c,lw=lw,marker="o",ms=5)
    ax.text(s.index[-1]+.2,s.values[-1],str(y),color=c if y==2026 else G3,va="center",fontsize=12)
ax.axhline(1,color="#1f2937",ls="--",lw=1)
ax.set_xticks(range(1,13));ax.set_xticklabels(ay);ax.set_xlim(.7,12.8)
ax.set_ylabel("Aylık PTF / yıl ortalaması (Oca-Eki)")
fig.tight_layout();save(fig,"c1")

# C2 heatmap (2023-2025 ort, saat x ay, yıl ort oranı)
d=df[df.y<=2025].copy(); d["r"]=d.ptf/d.y.map(ref)
hm=d.pivot_table(index="h",columns="m",values="r",aggfunc="mean")
fig,ax=plt.subplots(figsize=(9.6,6.6))
im=ax.imshow(hm.values,aspect="auto",cmap="RdYlBu_r",vmin=.4,vmax=1.5,origin="upper")
ax.set_xticks(range(12));ax.set_xticklabels(ay);ax.set_yticks(range(0,24,3));ax.set_yticklabels([f"{h:02d}:00" for h in range(0,24,3)])
ax.grid(False);[s.set_visible(False) for s in ax.spines.values()]
cb=fig.colorbar(im,ax=ax,pad=.02);cb.set_label("PTF / yıl ortalaması");cb.outline.set_visible(False)
fig.tight_layout();save(fig,"c2")

# C3 akşam-gündüz farkı (yıl ort %)
G=df[df.h.between(6,16)].groupby(["y","m"]).ptf.mean();A=df[df.h.between(17,21)].groupby(["y","m"]).ptf.mean()
gap=((A-G).unstack(0)/ref*100)
fig,ax=plt.subplots(figsize=(9.6,6.2))
base=gap[[2023,2024,2025]].mean(axis=1)
w=.38;x=np.arange(1,13)
ax.bar(x-w/2,base.values,w,color=G2,label="2023-2025 ortalaması")
s=gap[2026].dropna();ax.bar(s.index+w/2,s.values,w,color=OR,label="2026")
ax.set_xticks(x);ax.set_xticklabels(ay);ax.set_ylabel("Akşam - gündüz fiyat farkı (yıl ortalamasının %'si)")
ax.legend(frameon=False,loc="upper left");fig.tight_layout();save(fig,"c3")

# C4 düşük fiyatlı saat (<100 TL/MWh) yıl x ay Nis-Haz
low=df[df.ptf<100].groupby(["y","m"]).size().unstack(0).reindex(range(1,11)).fillna(0)
fig,ax=plt.subplots(figsize=(9.6,6.2))
x=np.arange(1,11);w=.2
for i,(y,c) in enumerate([(2023,G1),(2024,G2),(2025,G3),(2026,OR)]):
    ax.bar(x+(i-1.5)*w,low[y].values,w,color=c,label=str(y))
ax.set_xticks(x);ax.set_xticklabels(ay[:10]);ax.set_ylabel("PTF < 100 TL/MWh olan saat sayısı")
ax.legend(frameon=False,ncol=4,loc="upper right");fig.tight_layout();save(fig,"c4")

# C5 hidro payı vs fiyat oranı
pay=(df.hidro/df.uretim_total).groupby([df.y,df.m]).mean().unstack(0)*100
fig,ax=plt.subplots(figsize=(9.6,6.2))
xs=[];ys=[]
for y,c in [(2023,G1),(2024,G2),(2025,G3),(2026,OR)]:
    s=pay[y].dropna();o=mm[y].dropna()
    ax.scatter(s.values,o.values,color=c,s=70,edgecolor="white",lw=1,label=str(y),zorder=3)
    xs+=list(s.values);ys+=list(o.values)
k=np.polyfit(xs,ys,1);xx=np.array([min(xs),max(xs)]);ax.plot(xx,k[0]*xx+k[1],"--",color="#1f2937",lw=1.5)
for m_ in (4,5):
    ax.annotate(f"{ay[m_-1]} 2026",(pay[2026][m_],mm[2026][m_]),xytext=(8,8),textcoords="offset points",color=OR,fontsize=11)
ax.set_xlabel("Hidroelektriğin üretimdeki payı (%, aylık ortalama)");ax.set_ylabel("Aylık PTF / yıl ortalaması")
ax.legend(frameon=False,ncol=4,loc="upper right");fig.tight_layout();save(fig,"c5")
r=np.corrcoef(xs,ys)[0,1];print("r",round(r,2),"n",len(xs))

# C6 mix 2025 vs 2026 Nis-Haz
rows=[("Hidroelektrik","hidro"),("Doğal gaz","uretim_naturalGas"),("İthal kömür","uretim_importCoal"),("Linyit","uretim_lignite"),("Rüzgâr","uretim_wind"),("Güneş*","uretim_solar")]
s=df[df.m.isin([4,5,6])]
a=s[s.y==2025][[c for _,c in rows]].mean();b=s[s.y==2026][[c for _,c in rows]].mean()
fig,ax=plt.subplots(figsize=(9.6,6.2));y=np.arange(len(rows))[::-1]
ax.barh(y+.2,a.values/1000,.38,color=G2,label="Nis-Haz 2025");ax.barh(y-.2,b.values/1000,.38,color=OR,label="Nis-Haz 2026")
ax.set_yticks(y);ax.set_yticklabels([n for n,_ in rows]);ax.set_xlabel("Saatlik ortalama üretim (GW)");ax.grid(axis="y",visible=False)
ax.legend(frameon=False,loc="lower right");fig.tight_layout();save(fig,"c6")
print((b-a).round(0).to_string())
print("kış-yaz:",mm[[2023,2024,2025]].mean(axis=1).round(2).to_dict())
print("0 saat 2026:",(df[df.y==2026].ptf==0).sum(),"toplam:",(df.ptf==0).sum())
print("gap Mayis 2026 %",round(gap[2026][5]),"base",round(base[5]))
