# Système de gestion de salle


## Modèles
### Show (Spectacle)
```json
{
    "name": "String",
    "date": "String (Format ISO)",
    "description": "String"
}
```

### Ticket (Billet)
```json
{
    "uuid": "UUID4",
}
```


### Venue (Salle)
```json
{
    "name": "String",
    "address": "String",
    "capacity": "Int"
}
```

## Communication avec les sites de vente

### Payload de création
exemple: POST /spectacles

```json
{
    "name": "String",
    "date": "String (Format ISO)",
    "description": "String",
    "venue": {"Venue"},
    "tickets": [{"Tickets"}]
}
```

