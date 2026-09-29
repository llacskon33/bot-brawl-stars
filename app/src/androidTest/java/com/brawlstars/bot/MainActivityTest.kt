package com.brawlstars.bot

import androidx.test.espresso.Espresso.onView
import androidx.test.espresso.action.ViewActions.click
import androidx.test.espresso.assertion.ViewAssertions.matches
import androidx.test.espresso.matcher.ViewMatchers.isEnabled
import androidx.test.espresso.matcher.ViewMatchers.isNotEnabled
import androidx.test.espresso.matcher.ViewMatchers.withId
import androidx.test.espresso.matcher.ViewMatchers.withText
import androidx.test.ext.junit.rules.ActivityScenarioRule
import androidx.test.ext.junit.runners.AndroidJUnit4
import org.junit.Rule
import org.junit.Test
import org.junit.runner.RunWith

/**
 * Verifies the basic Start/Stop UI behaves correctly, without any bot/AI logic.
 */
@RunWith(AndroidJUnit4::class)
class MainActivityTest {

    @get:Rule
    val activityRule = ActivityScenarioRule(MainActivity::class.java)

    @Test
    fun initialState_showsStoppedStatusAndEnabledStartButton() {
        onView(withId(R.id.statusTextView))
            .check(matches(withText(R.string.status_stopped)))
        onView(withId(R.id.startButton)).check(matches(isEnabled()))
        onView(withId(R.id.stopButton)).check(matches(isNotEnabled()))
    }

    @Test
    fun clickingStart_updatesStatusAndButtonStates() {
        onView(withId(R.id.startButton)).perform(click())

        onView(withId(R.id.statusTextView))
            .check(matches(withText(R.string.status_running)))
        onView(withId(R.id.startButton)).check(matches(isNotEnabled()))
        onView(withId(R.id.stopButton)).check(matches(isEnabled()))
    }

    @Test
    fun clickingStartThenStop_returnsToStoppedState() {
        onView(withId(R.id.startButton)).perform(click())
        onView(withId(R.id.stopButton)).perform(click())

        onView(withId(R.id.statusTextView))
            .check(matches(withText(R.string.status_stopped)))
        onView(withId(R.id.startButton)).check(matches(isEnabled()))
        onView(withId(R.id.stopButton)).check(matches(isNotEnabled()))
    }

    @Test
    fun runningState_survivesActivityRecreation() {
        onView(withId(R.id.startButton)).perform(click())

        activityRule.scenario.recreate()

        onView(withId(R.id.statusTextView))
            .check(matches(withText(R.string.status_running)))
        onView(withId(R.id.startButton)).check(matches(isNotEnabled()))
        onView(withId(R.id.stopButton)).check(matches(isEnabled()))
    }
}
