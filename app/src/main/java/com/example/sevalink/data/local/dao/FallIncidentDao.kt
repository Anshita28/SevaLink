package com.example.sevalink.data.local.dao

import androidx.room.*
import com.example.sevalink.data.local.entity.FallIncidentEntity
import kotlinx.coroutines.flow.Flow

@Dao
interface FallIncidentDao {
    @Query("SELECT * FROM fall_incidents ORDER BY timestamp DESC")
    fun getAllIncidents(): Flow<List<FallIncidentEntity>>

    @Insert(onConflict = OnConflictStrategy.REPLACE)
    suspend fun insertIncident(incident: FallIncidentEntity)

    @Query("UPDATE fall_incidents SET isFalsePositive = :isFalsePositive WHERE id = :incidentId")
    suspend fun updateFalsePositiveStatus(incidentId: Long, isFalsePositive: Boolean)
}
