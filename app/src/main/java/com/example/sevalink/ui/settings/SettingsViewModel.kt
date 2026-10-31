package com.example.sevalink.ui.settings

import androidx.lifecycle.ViewModel
import androidx.lifecycle.viewModelScope
import com.example.sevalink.domain.repository.SettingsRepository
import dagger.hilt.android.lifecycle.HiltViewModel
import kotlinx.coroutines.flow.SharingStarted
import kotlinx.coroutines.flow.StateFlow
import kotlinx.coroutines.flow.stateIn
import kotlinx.coroutines.launch
import javax.inject.Inject

@HiltViewModel
class SettingsViewModel @Inject constructor(
    private val repository: SettingsRepository
) : ViewModel() {

    val smsAlertsEnabled: StateFlow<Boolean> = repository.smsAlertsEnabled
        .stateIn(viewModelScope, SharingStarted.WhileSubscribed(5000), true)

    val autoCallEnabled: StateFlow<Boolean> = repository.autoCallEnabled
        .stateIn(viewModelScope, SharingStarted.WhileSubscribed(5000), false)

    val loudSirenEnabled: StateFlow<Boolean> = repository.loudSirenEnabled
        .stateIn(viewModelScope, SharingStarted.WhileSubscribed(5000), true)

    val sensitivityLevel: StateFlow<Int> = repository.sensitivityLevel
        .stateIn(viewModelScope, SharingStarted.WhileSubscribed(5000), 1)

    fun setSmsEnabled(enabled: Boolean) {
        viewModelScope.launch { repository.setSmsAlertsEnabled(enabled) }
    }

    fun setAutoCallEnabled(enabled: Boolean) {
        viewModelScope.launch { repository.setAutoCallEnabled(enabled) }
    }

    fun setSirenEnabled(enabled: Boolean) {
        viewModelScope.launch { repository.setLoudSirenEnabled(enabled) }
    }

    fun setSensitivity(level: Int) {
        viewModelScope.launch { repository.setSensitivityLevel(level) }
    }
}
