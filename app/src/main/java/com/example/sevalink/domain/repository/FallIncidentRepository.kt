package com.example.sevalink.domain.repository

import com.example.sevalink.domain.model.FallIncident
import kotlinx.coroutines.flow.Flow

/**
 * Repository for logging and managing fall incident history.
 */
interface FallIncidentRepository {
    fun getAllIncidents(): Flow<List<FallIncident>>
    suspend fun insertIncident(incident: FallIncident)
    suspend fun updateFalsePositiveStatus(incidentId: String, isFalsePositive: Boolean)
}
