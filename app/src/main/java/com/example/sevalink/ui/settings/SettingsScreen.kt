package com.example.sevalink.ui.settings

import androidx.compose.foundation.layout.*
import androidx.compose.material3.*
import androidx.compose.runtime.*
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.unit.dp
import androidx.hilt.navigation.compose.hiltViewModel

@Composable
fun SettingsScreen(viewModel: SettingsViewModel = hiltViewModel()) {
    val smsEnabled by viewModel.smsAlertsEnabled.collectAsState()
    val callEnabled by viewModel.autoCallEnabled.collectAsState()
    val sirenEnabled by viewModel.loudSirenEnabled.collectAsState()
    val sensitivity by viewModel.sensitivityLevel.collectAsState()

    Column(
        modifier = Modifier.fillMaxSize().padding(16.dp),
        verticalArrangement = Arrangement.spacedBy(16.dp)
    ) {
        Text("Alert Options", style = MaterialTheme.typography.titleLarge, fontWeight = FontWeight.Bold)
        
        ToggleSetting("SMS Alerts", "Send SMS to caretakers on fall", smsEnabled) { viewModel.setSmsEnabled(it) }
        ToggleSetting("Auto-Call", "Automatically call primary caretaker", callEnabled) { viewModel.setAutoCallEnabled(it) }
        ToggleSetting("Loud Siren", "Play loud siren when fall is triggered", sirenEnabled) { viewModel.setSirenEnabled(it) }
        
        Divider()
        
        Text("Detection Sensitivity", style = MaterialTheme.typography.titleLarge, fontWeight = FontWeight.Bold)
        
        SensitivitySlider(sensitivity) { viewModel.setSensitivity(it) }
        
        Text(
            text = when(sensitivity) {
                0 -> "Low: Fewer false alarms, may miss soft falls."
                1 -> "Medium: Calibrated baseline performance."
                else -> "High: Catches gentler falls, more false positives."
            },
            style = MaterialTheme.typography.bodySmall,
            color = MaterialTheme.colorScheme.onSurfaceVariant
        )
    }
}

@Composable
fun ToggleSetting(title: String, description: String, checked: Boolean, onCheckedChange: (Boolean) -> Unit) {
    Row(
        modifier = Modifier.fillMaxWidth(),
        verticalAlignment = Alignment.CenterVertically
    ) {
        Column(modifier = Modifier.weight(1f)) {
            Text(title, style = MaterialTheme.typography.bodyLarge)
            Text(description, style = MaterialTheme.typography.bodySmall)
        }
        Switch(checked = checked, onCheckedChange = onCheckedChange)
    }
}

@Composable
fun SensitivitySlider(value: Int, onValueChange: (Int) -> Unit) {
    Column {
        Slider(
            value = value.toFloat(),
            onValueChange = { onValueChange(it.toInt()) },
            valueRange = 0f..2f,
            steps = 1
        )
        Row(modifier = Modifier.fillMaxWidth(), horizontalArrangement = Arrangement.SpaceBetween) {
            Text("Low")
            Text("Medium")
            Text("High")
        }
    }
}
