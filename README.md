Projekt streamově zpracovává velký XML soubor z Retailys API (bez načítání do paměti) a poskytuje tři jednoduché REST endpointy pomocí Flasku. Součástí je Docker image a možnost nasazení na Render.

**Architektura**

•	Python + Flask – backend s endpointy:

o	/1 – počet produktů

o	/2 – názvy produktů (?limit=)

o	/3 – díly z categoriesWithParts (?limit=)

•	Stream XML parsování (iterparse)

Paměťově úsporné čtení XML, ukládání jen aktuální větve, průběžné elem.clear().

**Docker**

Image s Python 3.12, Flaskem a aplikací. Spouští se shodně lokálně i na Renderu.

**Render (deployment)**

Nasazení přímo z Docker Hub image → žádný build, nízké RAM nároky, stabilita.

**Popis projektu**

Aplikace:
1.	stáhne ZIP s XML,
2.	rozbalí ho v paměti,
3.	po částech zpracuje XML,
4.	poskytne data o produktech přes API.
   
Vhodné pro velmi velké XML soubory díky nízké spotřebě RAM.

🌍 **API Endpointy**

Endpoint	Popis	Parametry

/1	Počet produktů	–

/2	Názvy produktů (/items/item)	?limit=N

/3	Díly z /categoriesWithParts/.../item	?limit=N

N – počet vypsaných prvků (defaultně 100)

Example: https://retailys-app-latest.onrender.com/1  -> vypíše počet parametrů
