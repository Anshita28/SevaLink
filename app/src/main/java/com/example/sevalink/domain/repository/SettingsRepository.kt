package com.example.sevalink.domain.repository

import kotlinx.coroutines.flow.Flow

/**
 * Repository for persisting and retrieving user preferences.
 */
interface SettingsRepository {
    val smsAlertsEnabled: Flow<Boolean>
    val autoCallEnabled: Flow<Boolean>
    val loudSirenEnabled: Flow<Boolean>
    val sensitivityLevel: Flow<Int>

    suspend fun setSmsAlertsEnabled(enabled: Boolean)
    suspend fun setAutoCallEnabled(enabled: Boolean)
    suspend fun setLoudSirenEnabled(enabled: Boolean)
    suspend fun setSensitivityLevel(level: Int)
}
