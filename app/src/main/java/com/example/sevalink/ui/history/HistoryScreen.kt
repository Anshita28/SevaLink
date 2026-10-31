package com.example.sevalink.ui.history

import androidx.compose.foundation.layout.*
import androidx.compose.foundation.lazy.LazyColumn
import androidx.compose.foundation.lazy.items
import androidx.compose.material3.*
import androidx.compose.runtime.*
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.unit.dp
import androidx.hilt.navigation.compose.hiltViewModel
import com.example.sevalink.domain.model.FallIncident
import java.text.SimpleDateFormat
import java.util.*

@Composable
fun HistoryScreen(viewModel: HistoryViewModel = hiltViewModel()) {
    val incidents by viewModel.incidents.collectAsState()

    LazyColumn(
        modifier = Modifier.fillMaxSize().padding(16.dp),
        verticalArrangement = Arrangement.spacedBy(8.dp)
    ) {
        items(incidents) { incident ->
            IncidentItem(
                incident = incident,
                onToggleFalsePositive = { viewModel.toggleFalsePositive(incident) }
            )
        }
    }
}

@Composable
fun IncidentItem(incident: FallIncident, onToggleFalsePositive: () -> Unit) {
    val sdf = remember { SimpleDateFormat("MMM dd, yyyy HH:mm", Locale.getDefault()) }
    val dateString = sdf.format(Date(incident.timestamp))

    Card(
        modifier = Modifier.fillMaxWidth(),
        colors = CardDefaults.cardColors(
            containerColor = if (incident.isFalsePositive) Color.Gray.copy(alpha = 0.1f) else MaterialTheme.colorScheme.surfaceVariant
        )
    ) {
        Row(
            modifier = Modifier.padding(16.dp),
            verticalAlignment = Alignment.CenterVertically
        ) {
            Column(modifier = Modifier.weight(1f)) {
                Text(text = "Fall Detected", style = MaterialTheme.typography.titleMedium)
                Text(text = dateString, style = MaterialTheme.typography.bodySmall)
                Text(text = "Severity: ${incident.severity}", style = MaterialTheme.typography.bodyMedium)
            }
            
            Column(horizontalAlignment = Alignment.End) {
                Text(text = if (incident.isFalsePositive) "FALSE ALARM" else "CONFIRMED", 
                    style = MaterialTheme.typography.labelSmall,
                    color = if (incident.isFalsePositive) Color.Gray else Color.Red
                )
                Switch(
                    checked = !incident.isFalsePositive,
                    onCheckedChange = { onToggleFalsePositive() }
                )
            }
        }
    }
}
