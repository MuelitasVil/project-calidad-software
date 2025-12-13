#!/bin/bash

# Crear carpeta de resultados si no existe
mkdir -p test-results

# Dar permisos de escritura completos
chmod 777 test-results

echo "==================================="
echo "Ejecutando pruebas K6 con Docker"
echo "==================================="
echo ""

# Obtener el UID y GID del usuario actual
USER_ID=$(id -u)
GROUP_ID=$(id -g)

# Ejecutar cada test
for test in tests/*.js; do
  test_name=$(basename "$test" .js)
  echo "📋 Running: $test"
  echo "-----------------------------------"
  
  docker run --rm -i \
    --network host \
    --user "$USER_ID:$GROUP_ID" \
    -v "$PWD:/work" \
    -w /work \
    -e K6_OUT=json=/work/test-results/${test_name}-raw.json \
    grafana/k6 run "/work/$test"
  
  echo ""
  echo "✅ Completado: $test"
  echo "📊 Resultados en: test-results/${test_name}-summary.html"
  echo "==================================="
  echo ""
done

# Asegurar que los archivos tengan permisos de lectura para todos
chmod -R 644 test-results/*.html test-results/*.json test-results/*.txt 2>/dev/null
chmod -R +r test-results/ 2>/dev/null

echo "🎉 Todas las pruebas completadas!"
echo "📁 Revisa los reportes en: test-results/"
echo ""
echo "Para ver reportes HTML en tu navegador:"
echo "  firefox test-results/create-users-summary.html"
echo "  firefox test-results/get-users-summary.html"
echo ""
echo "O simplemente abre el archivo haciendo doble clic en tu explorador de archivos"