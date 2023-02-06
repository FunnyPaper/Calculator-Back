# CalculatorBack
## Zależności projektu
Wszystkie niezbędne moduły znajdują się w pliku *requirements.txt*. Instalacja:

    pip install -r requirements.txt

Po instalacji zależności projekt powinien być możliwy do uruchomienia
    
    python app.py

## Wykorzystanie
### Dostępne ścieżki
- POST /evaluate 
: Przyjmuje wyrażenie matematyczne w postaci string

- GET /history
: Zwraca historie obliczonych wyrażeń w formacie json

### Interfejs graficzny użytkownika
Druga część projektu - [GUI](https://github.com/FunnyPaper/Calculator-Front)
### Curl
Wykonywanie operacji:

    curl -d "{\"expression\":\"5!\"}" -H "Content-Type: application/json" -X POST http://localhost:5000/evaluate
Sprawdzanie historii:

    curl localhost:5000/history