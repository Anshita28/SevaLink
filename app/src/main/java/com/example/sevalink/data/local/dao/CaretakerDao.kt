package com.example.sevalink.data.local.dao

import androidx.room.*
import com.example.sevalink.data.local.entity.CaretakerEntity
import kotlinx.coroutines.flow.Flow

@Dao
interface CaretakerDao {
    @Query("SELECT * FROM caretakers")
    fun getAllCaretakers(): Flow<List<CaretakerEntity>>

    @Insert(onConflict = OnConflictStrategy.REPLACE)
    suspend fun insertCaretaker(caretaker: CaretakerEntity)

    @Update
    suspend fun updateCaretaker(caretaker: CaretakerEntity)

    @Delete
    suspend fun deleteCaretaker(caretaker: CaretakerEntity)

    @Query("UPDATE caretakers SET isPrimary = (id = :caretakerId)")
    suspend fun setPrimaryCaretaker(caretakerId: Long)
}
