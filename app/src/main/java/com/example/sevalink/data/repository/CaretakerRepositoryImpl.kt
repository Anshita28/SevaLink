package com.example.sevalink.data.repository

import com.example.sevalink.data.local.dao.CaretakerDao
import com.example.sevalink.data.local.entity.toDomain
import com.example.sevalink.data.local.entity.toEntity
import com.example.sevalink.domain.model.Caretaker
import com.example.sevalink.domain.repository.CaretakerRepository
import kotlinx.coroutines.flow.Flow
import kotlinx.coroutines.flow.map
import javax.inject.Inject
import javax.inject.Singleton

@Singleton
class CaretakerRepositoryImpl @Inject constructor(
    private val caretakerDao: CaretakerDao
) : CaretakerRepository {

    override fun getAllCaretakers(): Flow<List<Caretaker>> {
        return caretakerDao.getAllCaretakers().map { list ->
            list.map { it.toDomain() }
        }
    }

    override suspend fun addCaretaker(caretaker: Caretaker) {
        caretakerDao.insertCaretaker(caretaker.toEntity())
    }

    override suspend fun updateCaretaker(caretaker: Caretaker) {
        caretakerDao.updateCaretaker(caretaker.toEntity())
    }

    override suspend fun deleteCaretaker(caretaker: Caretaker) {
        caretakerDao.deleteCaretaker(caretaker.toEntity())
    }

    override suspend fun setPrimaryCaretaker(caretakerId: String) {
        caretakerDao.setPrimaryCaretaker(caretakerId.toLong())
    }
}
