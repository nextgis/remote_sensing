
set -e

# Поля:
# =====
# Sostav состав пород
# Pl площадь
# Eks экспозиция склона
# Poll крутизна склона
# Vmr преобладающая порода
# Bon бонитет (1 - лучше, ... 5, 5а, 5б - хуже)
# Kf1 доля первой по значимости породы
# Mr1 первая по значимости порода
# Amz1 возраст первой по значимости породы
# H1 выста первой по значимосит породы
# D1 диаметр первой по значимосит породы
# Psp1 запас первой по значимосит породы

# Преобладающие породы:
# =====================
# Д дуб 
# К кедр
# ЛИП липа
# Я ясень

v.to.rast type=area input=vud_all output=forest_spec_dub where="mr1=\"Д\"" use=attr attribute=kf1 --o
v.to.rast type=area input=vud_all output=forest_dub_d1 where="mr1=\"Д\"" use=attr attribute=d1 --o
v.to.rast type=area input=vud_all output=forest_dub_h1 where="mr1=\"Д\"" use=attr attribute=h1 --o
v.to.rast type=area input=vud_all output=forest_dub_amz1 where="mr1=\"Д\"" use=attr attribute=amz1 --o
v.to.rast type=area input=vud_all output=forest_dub_bon where="mr1=\"Д\"" use=attr attribute=bonitet --o

v.to.rast type=area input=vud_all output=forest_spec_kedr where="mr1=\"К\"" use=attr attribute=kf1 --o
v.to.rast type=area input=vud_all output=forest_kedr_d1 where="mr1=\"К\"" use=attr attribute=d1 --o
v.to.rast type=area input=vud_all output=forest_kedr_h1 where="mr1=\"К\"" use=attr attribute=h1 --o
v.to.rast type=area input=vud_all output=forest_kedr_amz1 where="mr1=\"К\"" use=attr attribute=amz1 --o
v.to.rast type=area input=vud_all output=forest_kedr_bon where="mr1=\"К\"" use=attr attribute=bonitet --o


v.to.rast type=area input=vud_all output=forest_spec_lipa where="mr1=\"ЛИП\"" use=attr attribute=kf1 --o
v.to.rast type=area input=vud_all output=forest_lipa_d1 where="mr1=\"ЛИП\"" use=attr attribute=d1 --o
v.to.rast type=area input=vud_all output=forest_lipa_h1 where="mr1=\"ЛИП\"" use=attr attribute=h1 --o
v.to.rast type=area input=vud_all output=forest_lipa_amz1 where="mr1=\"ЛИП\"" use=attr attribute=amz1 --o
v.to.rast type=area input=vud_all output=forest_lipa_bon where="mr1=\"ЛИП\"" use=attr attribute=bonitet --o


v.to.rast type=area input=vud_all output=forest_spec_jasen where="mr1=\"Я\"" use=attr attribute=kf1 --o
v.to.rast type=area input=vud_all output=forest_jasen_d1 where="mr1=\"Я\"" use=attr attribute=d1 --o
v.to.rast type=area input=vud_all output=forest_jasen_h1 where="mr1=\"Я\"" use=attr attribute=h1 --o
v.to.rast type=area input=vud_all output=forest_jasen_amz1 where="mr1=\"Я\"" use=attr attribute=amz1 --o
v.to.rast type=area input=vud_all output=forest_jasen_bon where="mr1=\"Я\"" use=attr attribute=bonitet --o

v.to.rast type=area input=vud_all output=forest_psp1 use=attr attribute=psp1 --o

