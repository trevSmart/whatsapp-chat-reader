# Real Example Test

Aquest directori conté un exemple real d'un xat de WhatsApp amb dades reals per testejar el sistema de manera robusta.

## Contingut

- **_chat.txt**: Fitxer de xat exportat amb 31.071 línies (2.1 MB)
- **3.430 fitxers adjunts**: Imatges, àudios, vídeos i documents
- **25.835 missatges**: Inclou missatges amb text, adjunts i missatges del sistema

## Característiques del Test

Aquest exemple permet validar:

- ✅ **Rendiment** amb xats reals molt grans
- ✅ **Virtual scrolling** amb desenes de milers de missatges
- ✅ **Lazy loading** d'adjunts amb centenars de fitxers
- ✅ **Parser robust** amb diferents formats de missatges
- ✅ **Gestió de memòria** en situacions extremes
- ✅ **API REST** amb chunks de missatges
- ✅ **Servei d'adjunts** sota demanda

## Com Executar els Tests

### Opció 1: Script Automàtic (Recomanat)

```bash
./test_real_example.sh
```

Aquest script et permet:
1. Executar tests automàtics amb pytest
2. Iniciar el servidor i provar manualment
3. Ambdues opcions

### Opció 2: Tests Automàtics amb pytest

```bash
# Instal·lar dependències si cal
pip install flask flask-cors pytest requests

# Executar tests
python3 -m pytest tests/test_real_example.py -v
```

### Opció 3: Servidor Manual

```bash
# Instal·lar dependències si cal
pip install flask flask-cors

# Executar servidor
python3 progressive_server.py \
    "tests/real-example-test/_chat.txt" \
    --attachments "tests/real-example-test" \
    --chat-name "Real Example Test Chat" \
    --port 8080

# Obrir navegador a http://localhost:8080
```

## Tests Inclosos

El test suite (`test_real_example.py`) valida:

1. ✅ **test_chat_file_exists**: Verifica que el fitxer de xat existeix i té contingut
2. ✅ **test_attachments_directory**: Comprova que hi ha adjunts disponibles
3. ✅ **test_api_stats**: Valida endpoint d'estadístiques
4. ✅ **test_api_messages_first_chunk**: Prova càrrega del primer chunk
5. ✅ **test_api_messages_middle_chunk**: Prova càrrega d'un chunk intermedi
6. ✅ **test_api_messages_last_chunk**: Prova càrrega de l'últim chunk
7. ✅ **test_message_structure**: Valida estructura dels missatges
8. ✅ **test_message_with_attachments**: Comprova missatges amb adjunts
9. ✅ **test_attachment_serving**: Valida servei de fitxers adjunts
10. ✅ **test_html_file_generated**: Verifica generació d'HTML
11. ✅ **test_root_endpoint**: Comprova servei del HTML

## Resultats Esperats

Tots els tests haurien de passar correctament:

```
================================================== 11 passed in ~3s ==================================================
```

## Estadístiques del Test

Quan executis els tests, veuràs estadístiques com:

```
📊 Chat file: 2.0 MB, 31071 lines
📎 Found 3430 attachment files
💬 Total messages: 25835
📝 First chunk: 50 messages
📎 Found 19 messages with attachments in first 100
✅ Successfully served attachment: 00000003-PHOTO-2021-05-08-16-38-19.jpg (102404 bytes)
📄 HTML file size: 28.4 KB
✅ HTML served from root endpoint (29085 bytes)
```

## Arquitectura del Test

El test utilitza:

1. **unittest**: Framework de testing de Python
2. **subprocess**: Per iniciar el servidor Flask
3. **requests**: Per fer peticions HTTP a l'API
4. **pytest**: Per executar els tests amb millor output

### Flux del Test

1. **setUpClass**: Inicia el servidor progressiu en background
2. **Tests individuals**: Validen diferents aspectes del sistema
3. **tearDownClass**: Atura el servidor

## Troubleshooting

### Port ja en ús
Si el port 8765 ja està en ús, canvia-lo a `test_real_example.py`:
```python
cls.port = 8888  # Canvia el port
```

### Servidor no s'inicia
Comprova que tens Flask instal·lat:
```bash
pip install flask flask-cors
```

### Tests fallen
Executa amb més verbositat per veure detalls:
```bash
python3 -m pytest tests/test_real_example.py -v -s
```

## Notes

Aquest exemple real és molt útil per:

- 🔍 Detectar problemes de rendiment
- 🐛 Trobar bugs amb dades reals
- 📊 Validar escalabilitat del sistema
- 🚀 Provar noves funcionalitats
- 📈 Fer benchmarking

## Privacitat

Les dades d'aquest test són reals però s'ha eliminat qualsevol informació sensible. Els noms i continguts són genèrics o simulats.
