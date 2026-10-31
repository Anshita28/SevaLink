package com.example.sevalink.ui.dashboard

import androidx.compose.foundation.layout.*
import androidx.compose.material3.*
import androidx.compose.runtime.*
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp
import androidx.hilt.navigation.compose.hiltViewModel
import com.example.sevalink.domain.model.SystemStatus

@Composable
fun DashboardScreen(viewModel: DashboardViewModel = hiltViewModel()) {
    val uiState by viewModel.uiState.collectAsState()
    val mlStatus by viewModel.mlEngineStatus.collectAsState("Unknown")

    Column(
        modifier = Modifier
            .fillMaxSize()
            .padding(16.dp),
        horizontalAlignment = Alignment.CenterHorizontally
    ) {
        StatusHeader(uiState.systemStatus)
        
        Spacer(modifier = Modifier.height(24.dp))
        
        Button(
            onClick = { viewModel.toggleMonitoring() },
            modifier = Modifier.fillMaxWidth().height(64.dp),
            colors = ButtonDefaults.buttonColors(
                containerColor = if (uiState.systemStatus == SystemStatus.IDLE) Color(0xFF4CAF50) else Color(0xFFF44336)
            )
        ) {
            Text(
                if (uiState.systemStatus == SystemStatus.IDLE) "START MONITORING" else "STOP MONITORING",
                fontSize = 18.sp,
                fontWeight = FontWeight.Bold
            )
        }

        Spacer(modifier = Modifier.height(24.dp))

        Card(modifier = Modifier.fillMaxWidth()) {
            Column(modifier = Modifier.padding(16.dp)) {
                Text("ML Engine Status", fontWeight = FontWeight.Bold)
                Text(
                    text = if (mlStatus.contains("Mock")) "Pending Integration (Mock)" else "Active (TFLite)",
                    color = if (mlStatus.contains("Mock")) Color.Gray else Color(0xFF4CAF50)
                )
            }
        }

        Spacer(modifier = Modifier.height(16.dp))

        Card(modifier = Modifier.fillMaxWidth()) {
            Column(modifier = Modifier.padding(16.dp)) {
                Text("Live Telemetry", fontWeight = FontWeight.Bold)
                Text("Accelerometer: ${uiState.liveSensorData?.ax ?: 0f}, ${uiState.liveSensorData?.ay ?: 0f}, ${uiState.liveSensorData?.az ?: 0f}")
                Text("Gyroscope: ${uiState.liveSensorData?.gx ?: 0f}, ${uiState.liveSensorData?.gy ?: 0f}, ${uiState.liveSensorData?.gz ?: 0f}")
            }
        }
    }
}

@Composable
fun StatusHeader(status: SystemStatus) {
    val color = when (status) {
        SystemStatus.IDLE -> Color.Gray
        SystemStatus.MONITORING -> Color(0xFF4CAF50)
        SystemStatus.TRIGGERED -> Color(0xFFFF9800)
        SystemStatus.FALL_DETECTED -> Color(0xFFF44336)
    }

    Surface(
        modifier = Modifier.fillMaxWidth().height(120.dp),
        color = color,
        shape = MaterialTheme.shapes.medium
    ) {
        Box(contentAlignment = Alignment.Center) {
            Text(
                text = status.name,
                color = Color.White,
                fontSize = 28.sp,
                fontWeight = FontWeight.Black
            )
        }
    }
}
