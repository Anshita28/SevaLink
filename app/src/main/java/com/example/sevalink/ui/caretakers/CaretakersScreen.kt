package com.example.sevalink.ui.caretakers

import androidx.compose.foundation.layout.*
import androidx.compose.foundation.lazy.LazyColumn
import androidx.compose.foundation.lazy.items
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.filled.Add
import androidx.compose.material.icons.filled.Delete
import androidx.compose.material.icons.filled.Star
import androidx.compose.material3.*
import androidx.compose.runtime.*
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.unit.dp
import androidx.hilt.navigation.compose.hiltViewModel
import com.example.sevalink.domain.model.Caretaker

@Composable
fun CaretakersScreen(viewModel: CaretakersViewModel = hiltViewModel()) {
    val caretakers by viewModel.caretakers.collectAsState()
    var showAddDialog by remember { mutableStateOf(false) }

    Scaffold(
        floatingActionButton = {
            FloatingActionButton(onClick = { showAddDialog = true }) {
                Icon(Icons.Default.Add, contentDescription = "Add Caretaker")
            }
        }
    ) { padding ->
        LazyColumn(
            modifier = Modifier.fillMaxSize().padding(padding).padding(16.dp),
            verticalArrangement = Arrangement.spacedBy(8.dp)
        ) {
            items(caretakers) { caretaker ->
                CaretakerItem(
                    caretaker = caretaker,
                    onDelete = { viewModel.deleteCaretaker(caretaker) },
                    onSetPrimary = { viewModel.setPrimary(caretaker) }
                )
            }
        }

        if (showAddDialog) {
            AddCaretakerDialog(
                onDismiss = { showAddDialog = false },
                onAdd = { name, phone, relation ->
                    viewModel.addCaretaker(name, phone, relation)
                    showAddDialog = false
                }
            )
        }
    }
}

@Composable
fun CaretakerItem(caretaker: Caretaker, onDelete: () -> Unit, onSetPrimary: () -> Unit) {
    Card(modifier = Modifier.fillMaxWidth()) {
        Row(
            modifier = Modifier.padding(16.dp),
            verticalAlignment = Alignment.CenterVertically
        ) {
            Column(modifier = Modifier.weight(1f)) {
                Text(text = caretaker.name, style = MaterialTheme.typography.titleLarge)
                Text(text = "${caretaker.relation} • ${caretaker.phoneNumber}", style = MaterialTheme.typography.bodyMedium)
            }
            if (caretaker.isPrimary) {
                Icon(Icons.Default.Star, contentDescription = "Primary", tint = Color(0xFFFFB300))
            } else {
                IconButton(onClick = onSetPrimary) {
                    Icon(Icons.Default.Star, contentDescription = "Set Primary", tint = Color.Gray)
                }
            }
            IconButton(onClick = onDelete) {
                Icon(Icons.Default.Delete, contentDescription = "Delete", tint = Color.Red)
            }
        }
    }
}

@Composable
fun AddCaretakerDialog(onDismiss: () -> Unit, onAdd: (String, String, String) -> Unit) {
    var name by remember { mutableStateOf("") }
    var phone by remember { mutableStateOf("") }
    var relation by remember { mutableStateOf("") }

    AlertDialog(
        onDismissRequest = onDismiss,
        title = { Text("Add Caretaker") },
        text = {
            Column(verticalArrangement = Arrangement.spacedBy(8.dp)) {
                OutlinedTextField(value = name, onValueChange = { name = it }, label = { Text("Name") })
                OutlinedTextField(value = phone, onValueChange = { phone = it }, label = { Text("Phone") })
                OutlinedTextField(value = relation, onValueChange = { relation = it }, label = { Text("Relation") })
            }
        },
        confirmButton = {
            Button(onClick = { onAdd(name, phone, relation) }) { Text("Add") }
        },
        dismissButton = {
            TextButton(onClick = onDismiss) { Text("Cancel") }
        }
    )
}
