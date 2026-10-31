package com.example.sevalink.ui.history

import androidx.lifecycle.ViewModel
import androidx.lifecycle.viewModelScope
import com.example.sevalink.domain.model.FallIncident
import com.example.sevalink.domain.repository.FallIncidentRepository
import dagger.hilt.android.lifecycle.HiltViewModel
import kotlinx.coroutines.flow.SharingStarted
import kotlinx.coroutines.flow.StateFlow
import kotlinx.coroutines.flow.stateIn
import kotlinx.coroutines.launch
import javax.inject.Inject

@HiltViewModel
class HistoryViewModel @Inject constructor(
    private val repository: FallIncidentRepository
) : ViewModel() {

    val incidents: StateFlow<List<FallIncident>> = repository.getAllIncidents()
        .stateIn(viewModelScope, SharingStarted.WhileSubscribed(5000), emptyList())

    fun toggleFalsePositive(incident: FallIncident) {
        viewModelScope.launch {
            repository.updateFalsePositiveStatus(incident.id, !incident.isFalsePositive)
        }
    }
}
