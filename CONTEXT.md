# Glance Clock Home Assistant

This context describes the user-visible Glance Clock capabilities being
recreated locally through Home Assistant and BLE.

## Language

**Clock Face**:
A persistent firmware scene in a numbered slot that the clock presents through
its sequential previous/next carousel.
_Avoid_: App, screen, widget

**Clock-facing Function**:
A v2 app capability whose meaningful outcome is data or behavior on the
physical clock.
_Avoid_: App feature, Android feature

**Local-first**:
Runtime clock control that depends on Home Assistant and local BLE, not the
Glance account or cloud backend. Home Assistant may obtain source data from its
own configured integrations.
_Avoid_: Offline-only, cloud clone

**Practical Parity**:
Equivalent observable behavior on the clock, without requiring the original
Android interface or Glance backend architecture.
_Avoid_: Screen-for-screen parity, backend parity
