def setup():
    import badge
    import easydraw
    import machine

    easydraw.msg("Setting weather overview as boot app")
    badge.nvs_set_str('boot', 'splash', 'WeekWeather')
    machine.deepsleep(1)
