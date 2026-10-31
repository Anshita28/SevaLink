package com.example.sevalink.data.repository

import android.content.Context
import androidx.datastore.core.DataStore
import androidx.datastore.preferences.core.*
import androidx.datastore.preferences.preferencesDataStore
import com.example.sevalink.domain.repository.SettingsRepository
import dagger.hilt.android.qualifiers.ApplicationContext
import kotlinx.coroutines.flow.Flow
import kotlinx.coroutines.flow.map
import javax.inject.Inject
import javax.inject.Singleton

private val Context.dataStore: DataStore<Preferences> by preferencesDataStore(name = "settings")

@Singleton
class SettingsRepositoryImpl @Inject constructor(
    @ApplicationContext private val context: Context
) : SettingsRepository {

    private object PreferencesKeys {
        val SMS_ALERTS_ENABLED = booleanPreferencesKey("sms_alerts_enabled")
        val AUTO_CALL_ENABLED = booleanPreferencesKey("auto_call_enabled")
        val LOUD_SIREN_ENABLED = booleanPreferencesKey("loud_siren_enabled")
        val SENSITIVITY_LEVEL = intPreferencesKey("sensitivity_level")
    }

    override val smsAlertsEnabled: Flow<Boolean> = context.dataStore.data
        .map { preferences -> preferences[PreferencesKeys.SMS_ALERTS_ENABLED] ?: true }

    override val autoCallEnabled: Flow<Boolean> = context.dataStore.data
        .map { preferences -> preferences[PreferencesKeys.AUTO_CALL_ENABLED] ?: false }

    override val loudSirenEnabled: Flow<Boolean> = context.dataStore.data
        .map { preferences -> preferences[PreferencesKeys.LOUD_SIREN_ENABLED] ?: true }

    override val sensitivityLevel: Flow<Int> = context.dataStore.data
        .map { preferences -> preferences[PreferencesKeys.SENSITIVITY_LEVEL] ?: 1 }

    override suspend fun setSmsAlertsEnabled(enabled: Boolean) {
        context.dataStore.edit { preferences ->
            preferences[PreferencesKeys.SMS_ALERTS_ENABLED] = enabled
        }
    }

    override suspend fun setAutoCallEnabled(enabled: Boolean) {
        context.dataStore.edit { preferences ->
            preferences[PreferencesKeys.AUTO_CALL_ENABLED] = enabled
        }
    }

    override suspend fun setLoudSirenEnabled(enabled: Boolean) {
        context.dataStore.edit { preferences ->
            preferences[PreferencesKeys.LOUD_SIREN_ENABLED] = enabled
        }
    }

    override suspend fun setSensitivityLevel(level: Int) {
        context.dataStore.edit { preferences ->
            preferences[PreferencesKeys.SENSITIVITY_LEVEL] = level
        }
    }
}
