package com.example.sevalink.data.repository

import com.example.sevalink.data.local.dao.FallIncidentDao
import com.example.sevalink.data.local.entity.toDomain
import com.example.sevalink.data.local.entity.toEntity
import com.example.sevalink.domain.model.FallIncident
import com.example.sevalink.domain.repository.FallIncidentRepository
import kotlinx.coroutines.flow.Flow
import kotlinx.coroutines.flow.map
import javax.inject.Inject
import javax.inject.Singleton

@Singleton
class FallIncidentRepositoryImpl @Inject constructor(
    private val fallIncidentDao: FallIncidentDao
) : FallIncidentRepository {

    override fun getAllIncidents(): Flow<List<FallIncident>> {
        return fallIncidentDao.getAllIncidents().map { list ->
            list.map { it.toDomain() }
        }
    }

    override suspend fun insertIncident(incident: FallIncident) {
        fallIncidentDao.insertIncident(incident.toEntity())
    }

    override suspend fun updateFalsePositiveStatus(incidentId: String, isFalsePositive: Boolean) {
        fallIncidentDao.updateFalsePositiveStatus(incidentId.toLong(), isFalsePositive)
    }
}
