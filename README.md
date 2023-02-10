# CalculatorBack

Projekt stworzony z pomocą [PyCharm](https://www.jetbrains.com/pycharm/).

## Zależności projektu
Wszystkie niezbędne moduły znajdują się w pliku *requirements.txt*. Instalacja:

    pip install -r requirements.txt

Po instalacji zależności projekt powinien być możliwy do uruchomienia
    
    python app.py

## Wykorzystanie
### Dostępne ścieżki
- POST /evaluate 
: Przyjmuje wyrażenie matematyczne w postaci json
```javascript
    {
        expression: string,
        options?: {
            radians?: boolean
        }
    }
```

- GET /history
: Zwraca historie obliczonych wyrażeń w formacie json
```javascript
    {
        expression: string,
        result: string
    }
```

### Interfejs graficzny użytkownika
Druga część projektu - [GUI](https://github.com/FunnyPaper/Calculator-Front)
### Curl
Wykonywanie operacji:
    
    curl -d "{\"expression\":\" <expression> \"}" -H "Content-Type: application/json" -X POST http://localhost:5000/evaluate
np.

    curl -d "{\"expression\":\"5!\"}" -H "Content-Type: application/json" -X POST http://localhost:5000/evaluate
Sprawdzanie historii:

    curl localhost:5000/history
    
### interface.bat
Wykonywanie operacji:

    interface -e <expression: string> <radians: boolean>
np.

    interface -e "2^5" false
Sprawdzanie historii:

    interface -h
## Uruchamianie testów
Testy wykonane z pomocą środowiska [Unittest](https://docs.python.org/3/library/unittest.html) i [Coverage](https://coverage.readthedocs.io/en/7.1.0/):

    coverage run -m unittest
    coverage report
