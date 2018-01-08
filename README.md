# flask_app

### To get a prediction on a row of data
```
curl -H "Content-type: application/json" -X POST http://localhost:5000/ -d '{"SCHWEISSZEIT_IST": 1, "DURCHDRINGUNG_IST": 1, "BOLZENUEBERSTAND_IST": 1, "SCHWEISSENERGIE_IST": 1, "UL_HAUPTSTROM_IST": 1, "SCHWEISSSTROM_IST": 1, "UL_VORSTROM_IST": 1, "ANZAHL_WIPWOP_PROG": 1, "ABFALLZEIT_SOLL": 1, "HUBHOEHE_IST": 1, "DISTANZNULLLINIE_IST": 1, "WIP": 1, "ABFALLZEIT_IST": 1, "date": "01.02.2016 11:38:24"}'
```
The data must be a jsonified dictionary, where keys are feature names and values are feature values. There has to be one entry for the date field, even if it isn't an x variable.