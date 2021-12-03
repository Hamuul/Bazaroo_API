Am ales proba de backend.

Pentru a rula aplicația trebuie să aveți instalat interpretorul de python și managerul de pachete pip, apoi să rulați. Pentru verificarea tabelelor din baza de date puteți folosi TablePlus sau alte tooluri similare.

```bash
pip install -r requirements.txt
```

Am implementat toate endpointurile conform specificatiilor cu excepția ```POST /tutoring-classes```  si </br> ```POST /tutoring-class/{id}/enroll```. Parolele sunt stocate în baza de date cu bcrypt.
