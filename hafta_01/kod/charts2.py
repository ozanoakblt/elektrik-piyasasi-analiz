exec(open("charts.py").read().split("# C1 mevsim")[0])
import statsmodels.formula.api as smf
df["net"]=df.tuketim_mwh-df.uretim_wind-df.uretim_solar
# N1 USD: 2026 / ayni ay 2023-25 ort
u=df.groupby(["y","m"]).ptf_usd.mean().unstack(0)
rt=(u[2026]/u[[2023,2024,2025]].mean(axis=1)).dropna()
fig,ax=plt.subplots(figsize=(9.6,6.2))
cols=[OR if v<.5 else G2 for v in rt.values]
ax.bar(rt.index,rt.values*100,color=cols,width=.65)
for x,v in rt.items(): ax.text(x,v*100+2,f"%{v*100:.0f}",ha="center",fontsize=12,color="#1f2937")
ax.axhline(100,color="#1f2937",ls="--",lw=1);ax.set_xticks(range(1,11));ax.set_xticklabels(ay[:10]);ax.set_ylim(0,115)
ax.set_ylabel("2026 PTF (USD) / 2023-2025 aynı ay ortalaması (%)");fig.tight_layout();save(fig,"n1")
# N2 arz eğrisi
s=df[df.m.isin([4,5,6])&df.y.isin([2025,2026])].copy();s["b"]=pd.cut(s.net/1000,[0,20,25,30,35,40,60],labels=["<20","20-25","25-30","30-35","35-40",">40"])
t=s.groupby(["b","y"],observed=True).ptf_usd.mean().unstack()
fig,ax=plt.subplots(figsize=(9.6,6.2));x=np.arange(len(t));w=.38
ax.bar(x-w/2,t[2025],w,color=G2,label="Nis-Haz 2025");ax.bar(x+w/2,t[2026],w,color=OR,label="Nis-Haz 2026")
for i,(a,b) in enumerate(zip(t[2025],t[2026])): ax.text(i-w/2,a+1,f"{a:.0f}",ha="center",fontsize=11);ax.text(i+w/2,b+1,f"{b:.0f}",ha="center",fontsize=11,color=OR)
ax.set_xticks(x);ax.set_xticklabels(t.index);ax.set_xlabel("Net yük (tüketim - rüzgâr - güneş), GW");ax.set_ylabel("Ortalama PTF (USD/MWh)");ax.legend(frameon=False,loc="upper left");fig.tight_layout();save(fig,"n2")
# N3 regresyon: katsayılar
d=df.dropna(subset=["ptf_usd"]).copy();d["hidro"]=(d.uretim_dammedHydro+d.uretim_river)/1000
d["wp"]=d.uretim_wind/1000;d["sp"]=d.uretim_solar/1000;d["tk"]=d.tuketim_mwh/1000
r=smf.ols("ptf_usd ~ hidro+wp+sp+tk+C(h)+C(m)+C(y)",d).fit(cov_type="HAC",cov_kwds={"maxlags":24})
names={"hidro":"Hidroelektrik","wp":"Rüzgâr","sp":"Güneş*","tk":"Tüketim"}
fig,ax=plt.subplots(figsize=(9.6,5.4))
ks=list(names);co=[r.params[k] for k in ks];se=[1.96*r.bse[k] for k in ks]
y=np.arange(len(ks))[::-1];ax.barh(y,co,color=[NV if c<0 else OR for c in co],height=.55);ax.errorbar(co,y,xerr=se,fmt="none",ecolor="#1f2937",capsize=4)
for yy,c in zip(y,co): ax.text(c+(-.6 if c<0 else .6),yy+.33,f"{c:+.1f}",ha="left" if c>0 else "right",fontsize=13)
ax.set_yticks(y);ax.set_yticklabels([names[k] for k in ks]);ax.axvline(0,color="#1f2937",lw=1);ax.set_xlabel("1 GW artışın saatlik PTF'ye etkisi (USD/MWh)");ax.grid(axis="y",visible=False)
fig.tight_layout();save(fig,"n3")
# N4 baraj gün içi
p=s.groupby(["y","h"])[["uretim_dammedHydro","uretim_river"]].mean()/1000
fig,ax=plt.subplots(figsize=(9.6,6.2))
for y_,c in [(2025,G2),(2026,OR)]:
    ax.plot(p.loc[y_].index,p.loc[y_].uretim_dammedHydro,color=c,lw=3,label=f"Barajlı {y_}")
    ax.plot(p.loc[y_].index,p.loc[y_].uretim_river,color=c,lw=2,ls="--",label=f"Akarsu {y_}")
ax.set_xticks(range(0,24,3));ax.set_xticklabels([f"{h:02d}:00" for h in range(0,24,3)]);ax.set_ylabel("Ortalama üretim (GW), Nis-Haz");ax.legend(frameon=False,ncol=2,loc="upper left");ax.set_ylim(0,18);fig.tight_layout();save(fig,"n4")
print({k:round(r.params[k],2) for k in ks})
gk=s.groupby(["y",s.h.between(6,16)]).ptf_usd.mean().unstack();print(gk.round(1));print("gündüz değişim",round(gk.loc[2026,True]/gk.loc[2025,True]-1,2),"diğer saatler",round(gk.loc[2026,False]/gk.loc[2025,False]-1,2))
a=s[s.h.between(17,21)].groupby("y").ptf_usd.mean();g=s[s.h.between(6,16)].groupby("y").ptf_usd.mean();print("akşam",a.round(1).to_dict(),"gündüz",g.round(1).to_dict())
