exec(open("charts.py").read().split("# C1 mevsim")[0])
s=df[df.m.isin([4,5,6])&df.y.isin([2025,2026])]
a=s[s.h.between(17,21)].groupby("y").ptf_usd.mean();g=s[s.h.between(6,16)].groupby("y").ptf_usd.mean();n=s[~s.h.between(6,21)].groupby("y").ptf_usd.mean()
fig,ax=plt.subplots(figsize=(9.6,6.2));lab=["Gündüz\n06-16","Akşam\n17-21","Gece\n22-05"];x=np.arange(3);w=.38
v25=[g[2025],a[2025],n[2025]];v26=[g[2026],a[2026],n[2026]]
ax.bar(x-w/2,v25,w,color=G2,label="Nis-Haz 2025");ax.bar(x+w/2,v26,w,color=OR,label="Nis-Haz 2026")
for i in range(3):
    ax.text(i-w/2,v25[i]+1.5,f"{v25[i]:.0f}",ha="center",fontsize=12);ax.text(i+w/2,v26[i]+1.5,f"{v26[i]:.0f}",ha="center",fontsize=12,color=OR)
    ax.text(i+w/2,v26[i]+9,f"\u2212%{abs(v26[i]/v25[i]-1)*100:.0f}",ha="center",fontsize=13,color=OR,fontweight="bold")
ax.set_xticks(x);ax.set_xticklabels(lab);ax.set_ylabel("Ortalama PTF (USD/MWh)");ax.legend(frameon=False,loc="upper right");ax.set_ylim(0,105);fig.tight_layout();save(fig,"n5")
print(v25,v26)
