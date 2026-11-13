exec(open("charts.py").read().split("# C1 mevsim")[0])
d=df[df.m<=10].copy()
d["gun"]=np.where(d.h.between(10,15),"ogle",np.where(d.h.between(17,21),"aksam","diger"))
cols={2023:G1,2024:G2,2025:G3,2026:OR}
# N7 saatlik USD profil
p=d.groupby(["y","h"]).ptf_usd.mean().unstack(0)
fig,ax=plt.subplots(figsize=(9.6,6.2))
for y,c in cols.items(): ax.plot(p.index,p[y],color=c,lw=3.4 if y==2026 else 2.2,label=str(y))
ax.set_xticks(range(0,24,3));ax.set_xticklabels([f"{h:02d}:00" for h in range(0,24,3)]);ax.set_ylabel("Ortalama PTF (USD/MWh), Oca-Eki");ax.legend(frameon=False,ncol=4,loc="upper left");ax.set_ylim(0,None)
fig.tight_layout();save(fig,"n7")
t=d.groupby(["y","gun"]).ptf_usd.mean().unstack();t["ort"]=d.groupby("y").ptf_usd.mean();t["cukur"]=t.ogle/t.ort;t["aksam_ogle_fark"]=t.aksam-t.ogle;t["aksam_ogle_oran"]=t.aksam/t.ogle
print(t.round(2).to_string())
# N8 pay
d["gp"]=d.uretim_solar/d.uretim_total*100;d["rp"]=d.uretim_wind/d.uretim_total*100
gs=d.groupby(["y","h"]).gp.mean().unstack(0);rs=d.groupby(["y","h"]).rp.mean().unstack(0)
fig,axs=plt.subplots(1,2,figsize=(9.6,5.2),sharey=False)
for ax,s,tt in [(axs[0],gs,"Güneş*"),(axs[1],rs,"Rüzgâr")]:
    for y,c in cols.items(): ax.plot(s.index,s[y],color=c,lw=3.2 if y==2026 else 2,label=str(y))
    ax.set_title(tt,loc="left",fontsize=14,color="#1f2937");ax.set_xticks(range(0,24,6));ax.set_xticklabels([f"{h:02d}" for h in range(0,24,6)]);ax.set_xlabel("Saat")
axs[0].set_ylabel("Toplam üretimdeki pay (%)");axs[0].legend(frameon=False,ncol=2,loc="upper left");fig.tight_layout();save(fig,"n8")
print("ogle gunes payi",gs.loc[10:15].mean().round(1).to_dict(),"ogle ruzgar",rs.loc[10:15].mean().round(1).to_dict(),"toplam gun ruzgar",d.groupby("y").rp.mean().round(1).to_dict(),"gunes",d.groupby("y").gp.mean().round(1).to_dict())
print("max saat gunes payi",gs.max().round(1).to_dict())
# N9 öğle pay vs öğle fiyat yıllık+aylık
o=d[d.h.between(10,15)].groupby(["y","m"]).agg(pay=("gp","mean"),rp=("rp","mean"),fiyat=("ptf_usd","mean"))
o["yenil"]=o.pay+o.rp
fig,ax=plt.subplots(figsize=(9.6,6.2))
for y,c in cols.items():
    s=o.loc[y];ax.scatter(s.yenil,s.fiyat,color=c,s=75,edgecolor="white",lw=1,label=str(y),zorder=3)
ax.set_xlabel("Öğle (10-15) güneş + rüzgâr payı (%)");ax.set_ylabel("Öğle ortalama PTF (USD/MWh)");ax.legend(frameon=False,ncol=4,loc="upper right")
fig.tight_layout();save(fig,"n9")
print("korelasyon 2023-25 ay:",round(o.loc[2023:2025].yenil.corr(o.loc[2023:2025].fiyat),2),"tum",round(o.yenil.corr(o.fiyat),2))
# solar mevsim: Nis-Haz öğle güneş payı
print(d[d.m.isin([4,5,6])&d.h.between(10,15)].groupby("y").gp.mean().round(1).to_dict())
print(d.groupby("y").uretim_solar.mean().round(0).to_dict(),d[d.h.between(10,15)].groupby("y").uretim_solar.mean().round(0).to_dict())
