package com.example.sevalink.ui.overlay

import android.app.KeyguardManager
import android.content.Context
import android.os.Build
import android.os.Bundle
import androidx.activity.ComponentActivity
import androidx.activity.compose.setContent
import androidx.compose.foundation.background
import androidx.compose.foundation.layout.*
import androidx.compose.material3.*
import androidx.compose.runtime.*
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp
import com.example.sevalink.ui.theme.SevaLinkTheme
import dagger.hilt.android.AndroidEntryPoint
import kotlinx.coroutines.delay

import android.view.WindowManager

@AndroidEntryPoint
class FallAlertOverlayActivity : ComponentActivity() {
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        
        if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.O_MR1) {
            setShowWhenLocked(true)
            setTurnScreenOn(true)
            val keyguardManager = getSystemService(KEYGUARD_SERVICE) as KeyguardManager
            keyguardManager.requestDismissKeyguard(this, null)
        } else {
            window.addFlags(
                WindowManager.LayoutParams.FLAG_SHOW_WHEN_LOCKED or
                WindowManager.LayoutParams.FLAG_TURN_SCREEN_ON or
                WindowManager.LayoutParams.FLAG_KEEP_SCREEN_ON or
                WindowManager.LayoutParams.FLAG_DISMISS_KEYGUARD
            )
        }

        setContent {
            SevaLinkTheme {
                FallAlertScreen(
                    onCancel = { finish() },
                    onConfirm = { /* In real app, trigger SMS/Calls immediately */ }
                )
            }
        }
    }
}

@Composable
fun FallAlertScreen(onCancel: () -> Unit, onConfirm: () -> Unit) {
    var countdown by remember { mutableIntStateOf(10) }

    LaunchedEffect(Unit) {
        while (countdown > 0) {
            delay(1000)
            countdown--
        }
        onConfirm()
    }

    Column(
        modifier = Modifier
            .fillMaxSize()
            .background(Color.Red.copy(alpha = 0.9f))
            .padding(24.dp),
        horizontalAlignment = Alignment.CenterHorizontally,
        verticalArrangement = Arrangement.Center
    ) {
        Text(
            text = "FALL DETECTED!",
            color = Color.White,
            fontSize = 32.sp,
            fontWeight = FontWeight.Bold
        )
        
        Spacer(modifier = Modifier.height(32.dp))
        
        Text(
            text = "Sending emergency alerts in",
            color = Color.White,
            fontSize = 20.sp
        )
        
        Text(
            text = "$countdown",
            color = Color.White,
            fontSize = 80.sp,
            fontWeight = FontWeight.ExtraBold
        )

        Spacer(modifier = Modifier.height(64.dp))

        Button(
            onClick = onCancel,
            modifier = Modifier.fillMaxWidth().height(80.dp),
            colors = ButtonDefaults.buttonColors(containerColor = Color.White)
        ) {
            Text("I'M OK / CANCEL", color = Color.Red, fontSize = 24.sp, fontWeight = FontWeight.Bold)
        }
    }
}
