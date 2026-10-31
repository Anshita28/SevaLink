package com.example.sevalink.domain.repository

import com.example.sevalink.domain.model.Caretaker
import kotlinx.coroutines.flow.Flow

/**
 * Repository for managing caretakers who receive fall alerts.
 */
interface CaretakerRepository {
    fun getAllCaretakers(): Flow<List<Caretaker>>
    suspend fun addCaretaker(caretaker: Caretaker)
    suspend fun updateCaretaker(caretaker: Caretaker)
    suspend fun deleteCaretaker(caretaker: Caretaker)
    suspend fun setPrimaryCaretaker(caretakerId: String)
}
