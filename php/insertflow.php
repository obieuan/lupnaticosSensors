<?php
// Recibir datos JSON de la solicitud POST
$json_data = file_get_contents('php://input');
$data = json_decode($json_data, true);

// Conectar a la base de datos
$db_connection = mysqli_connect("localhost", "root", "", "flujometro");

// Verificar la conexión
if (!$db_connection) {
    die("La conexión a la base de datos falló: " . mysqli_connect_error());
}

// Comprobar si ya existe una fila con la misma sesión
$sql_check_session = "SELECT * FROM flow_data WHERE sesion = ?";
$stmt_check_session = mysqli_prepare($db_connection, $sql_check_session);
mysqli_stmt_bind_param($stmt_check_session, "i", $data['sesion']);
mysqli_stmt_execute($stmt_check_session);
$result_check_session = mysqli_stmt_get_result($stmt_check_session);

// Si la sesión existe, actualizar los valores
if (mysqli_num_rows($result_check_session) > 0) {
    $row = mysqli_fetch_assoc($result_check_session);
    $sql_update = "UPDATE flow_data SET timestamp = ?, pulses_per_minute = ?, estimated_flow_min = ?, estimated_flow_max = ?, total_liters_accumulated = ? WHERE sesion = ?";
    $stmt_update = mysqli_prepare($db_connection, $sql_update);
    mysqli_stmt_bind_param($stmt_update, "sddddi", $data['timestamp'], $data['pulses_per_minute'], $data['estimated_flow_min'], $data['estimated_flow_max'], $data['total_liters_accumulated'], $data['sesion']);
    if (mysqli_stmt_execute($stmt_update)) {
        echo "Datos actualizados correctamente";
    } else {
        echo "Error al actualizar datos: " . mysqli_error($db_connection);
    }
} else { // Si la sesión no existe, insertar una nueva fila
    $sql_insert = "INSERT INTO flow_data (timestamp, pulses_per_minute, estimated_flow_min, estimated_flow_max, total_liters_accumulated, sesion) VALUES (?, ?, ?, ?, ?, ?)";
    $stmt_insert = mysqli_prepare($db_connection, $sql_insert);
    mysqli_stmt_bind_param($stmt_insert, "sddddi", $data['timestamp'], $data['pulses_per_minute'], $data['estimated_flow_min'], $data['estimated_flow_max'], $data['total_liters_accumulated'], $data['sesion']);
    if (mysqli_stmt_execute($stmt_insert)) {
        echo "Datos insertados correctamente";
    } else {
        echo "Error al insertar datos: " . mysqli_error($db_connection);
    }
}

// Cerrar la conexión y liberar recursos
mysqli_stmt_close($stmt_check_session);
mysqli_stmt_close($stmt_insert);
mysqli_stmt_close($stmt_update);
mysqli_close($db_connection);
?>
