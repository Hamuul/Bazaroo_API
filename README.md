Pentru a rula aplicația trebuie să aveți instalat interpretorul de python și managerul de pachete pip (și să le aveți în variabila PATH), apoi să rulați comenzile de mai jos. Pentru verificarea tabelelor din baza de date puteți folosi TablePlus sau alte tooluri similare.

```bash
pip install -r requirements.txt
uvicorn main:app
```
Serverul ruleaza implicit pe ```localhost:8000```, iar documentația APIului o găsiți la ```locahost:8000/docs```.
