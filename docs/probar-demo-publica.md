# Probar la candidata de demo pública

Estado: candidata local; no está publicada online. La futura persona visitante sólo necesitará un navegador conJavaScript y accesoHTTPS. Estos pasos son para el mantenedor, no para el visitante.

Desde la raíz del código, con dependenciascore existentes:

```text
python public_demo/build.py
python public_demo/serve.py
```

Abrir http://127.0.0.1:8768/ en este computador. El servidor sirve sólo dist/public-demo y nunca debe exponerse aInternet. Un dobleclicfile:// no es una prueba equivalente: WebCrypto y fetch requieren origen compatible.

Prueba «¿Qué campos registra una observación de terreno?», abre su fuente y confirma que enumera fecha, sector, responsable y descripción. Después consulta imágenes o retirada documental. Una consulta sin evidencia debe abstenerse. Filtrar documentos no equivale a identidad.

Para validar:

```text
python -m pytest -q tests/test_public_demo.py
python public_demo/build.py
node --test public_demo/test_engine.mjs
```

En Linux/Python3.12, los paquetes de build/prueba están en requirements-lab-linux-py312.lock y se instalan con --require-hashes antes de ejecutar. Ese lock no es portátil aWindows sin resolver/verificar sus wheels. Ver instruccionescore enREADME; no esnecesario instalarStreamlit, ONNX ni pesos paraesta candidata.

Publicación y reversión: FORESTRAG_VERSIONING_STRATEGY.md. No sustituir el directorio público por la raíz delrepo. Mientras noexistaURLreal, no sepublica unbotón de demo falsa.
