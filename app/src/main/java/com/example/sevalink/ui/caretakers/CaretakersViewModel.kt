package com.example.sevalink.ui.caretakers

import androidx.lifecycle.ViewModel
import androidx.lifecycle.viewModelScope
import com.example.sevalink.domain.model.Caretaker
import com.example.sevalink.domain.repository.CaretakerRepository
import dagger.hilt.android.lifecycle.HiltViewModel
import kotlinx.coroutines.flow.SharingStarted
import kotlinx.coroutines.flow.StateFlow
import kotlinx.coroutines.flow.stateIn
import kotlinx.coroutines.launch
import javax.inject.Inject

@HiltViewModel
class CaretakersViewModel @Inject constructor(
    private val repository: CaretakerRepository
) : ViewModel() {

    val caretakers: StateFlow<List<Caretaker>> = repository.getAllCaretakers()
        .stateIn(viewModelScope, SharingStarted.WhileSubscribed(5000), emptyList())

    fun addCaretaker(name: String, phone: String, relation: String) {
        viewModelScope.launch {
            repository.addCaretaker(Caretaker(name = name, phoneNumber = phone, relation = relation, isPrimary = false))
        }
    }

    fun deleteCaretaker(caretaker: Caretaker) {
        viewModelScope.launch {
            repository.deleteCaretaker(caretaker)
        }
    }

    fun setPrimary(caretaker: Caretaker) {
        viewModelScope.launch {
            repository.setPrimaryCaretaker(caretaker.id)
        }
    }
}
