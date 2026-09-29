package com.brawlstars.bot

import android.os.Bundle
import androidx.appcompat.app.AppCompatActivity
import com.brawlstars.bot.databinding.ActivityMainBinding

/**
 * Minimal, functional entry point of the app.
 *
 * This first phase only proves that the app installs and launches correctly
 * on Android 13, exposing a basic UI with Start/Stop controls. The bot logic
 * and AI (Pyla AI) will be added in later phases.
 */
class MainActivity : AppCompatActivity() {

    private lateinit var binding: ActivityMainBinding
    private var isRunning = false

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        binding = ActivityMainBinding.inflate(layoutInflater)
        setContentView(binding.root)

        isRunning = savedInstanceState?.getBoolean(STATE_IS_RUNNING) ?: false

        binding.startButton.setOnClickListener { onStartClicked() }
        binding.stopButton.setOnClickListener { onStopClicked() }

        updateStatus()
    }

    override fun onSaveInstanceState(outState: Bundle) {
        super.onSaveInstanceState(outState)
        outState.putBoolean(STATE_IS_RUNNING, isRunning)
    }

    private fun onStartClicked() {
        // Bot/AI logic will be implemented in a later phase.
        isRunning = true
        updateStatus()
    }

    private fun onStopClicked() {
        isRunning = false
        updateStatus()
    }

    private fun updateStatus() {
        binding.statusTextView.setText(
            if (isRunning) R.string.status_running else R.string.status_stopped
        )
        binding.startButton.isEnabled = !isRunning
        binding.stopButton.isEnabled = isRunning
    }

    private companion object {
        const val STATE_IS_RUNNING = "state_is_running"
    }
}
