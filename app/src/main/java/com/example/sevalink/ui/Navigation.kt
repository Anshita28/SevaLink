package com.example.sevalink.ui

import androidx.compose.runtime.Composable
import androidx.compose.ui.Modifier
import androidx.navigation.NavHostController
import androidx.navigation.compose.NavHost
import androidx.navigation.compose.composable
import com.example.sevalink.ui.dashboard.DashboardScreen
import com.example.sevalink.ui.caretakers.CaretakersScreen
import com.example.sevalink.ui.history.HistoryScreen
import com.example.sevalink.ui.settings.SettingsScreen
import com.example.sevalink.ui.onboarding.OnboardingScreen

sealed class Screen(val route: String) {
    object Onboarding : Screen("onboarding")
    object Dashboard : Screen("dashboard")
    object Caretakers : Screen("caretakers")
    object History : Screen("history")
    object Settings : Screen("settings")
}

@Composable
fun AppNavigation(navController: NavHostController, startDestination: String, modifier: Modifier = Modifier) {
    NavHost(navController = navController, startDestination = startDestination, modifier = modifier) {
        composable(Screen.Onboarding.route) { OnboardingScreen(navController) }
        composable(Screen.Dashboard.route) { DashboardScreen() }
        composable(Screen.Caretakers.route) { CaretakersScreen() }
        composable(Screen.History.route) { HistoryScreen() }
        composable(Screen.Settings.route) { SettingsScreen() }
    }
}
