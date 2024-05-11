<?php
// Configuración de cabecera para JSON
header('Content-Type: application/json');

// Recibir datos JSON de la solicitud POST
$json_data = file_get_contents('php://input');
$data = json_decode($json_data, true);

// Conectar a la base de datos
$db_connection = mysqli_connect("localhost", "root", "", "flujometro");

// Verificar la conexión
if (!$db_connection) {
    die(json_encode(['error' => 'La conexión a la base de datos falló: ' . mysqli_connect_error()]));
}

// Consultar total_liters_accumulated por sesión
$sql = "SELECT total_liters_accumulated FROM flow_data WHERE sesion = ?";
$stmt = mysqli_prepare($db_connection, $sql);
mysqli_stmt_bind_param($stmt, "i", $data['sesion']);
mysqli_stmt_execute($stmt);
$result = mysqli_stmt_get_result($stmt);

if ($row = mysqli_fetch_assoc($result)) {
    echo json_encode(['total_liters_accumulated' => $row['total_liters_accumulated']]);
} else {
    echo json_encode(['total_liters_accumulated' => 0, 'message' => 'No se encontraron datos para la sesión especificada.']);
}

// Cerrar la conexión y liberar recursos
mysqli_stmt_close($stmt);
mysqli_close($db_connection);
?>
