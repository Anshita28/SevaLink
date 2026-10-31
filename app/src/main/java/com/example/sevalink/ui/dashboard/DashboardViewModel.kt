package com.example.sevalink.ui.dashboard

import androidx.lifecycle.ViewModel
import androidx.lifecycle.viewModelScope
import com.example.sevalink.domain.model.AppUiState
import com.example.sevalink.domain.model.SystemStatus
import com.example.sevalink.domain.repository.FallClassifier
import com.example.sevalink.domain.repository.SettingsRepository
import dagger.hilt.android.lifecycle.HiltViewModel
import kotlinx.coroutines.flow.*
import javax.inject.Inject

@HiltViewModel
class DashboardViewModel @Inject constructor(
    private val settingsRepository: SettingsRepository,
    private val fallClassifier: FallClassifier
) : ViewModel() {

    private val _uiState = MutableStateFlow(AppUiState())
    val uiState: StateFlow<AppUiState> = _uiState.asStateFlow()

    val mlEngineStatus = flowOf(fallClassifier.javaClass.simpleName)

    fun toggleMonitoring() {
        val current = _uiState.value.systemStatus
        _uiState.update { 
            it.copy(systemStatus = if (current == SystemStatus.IDLE) SystemStatus.MONITORING else SystemStatus.IDLE)
        }
    }
}
