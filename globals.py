def global_init():
    global path, sel_path, start_c, end_c, fin_path, alg_s, centre_x, centre_y, alg_sp, solved_text, path_nmbr, c, percentage, time, start_t, timer_r, screen, zoom_in, zoom_out
    global setup_screen_fontsize, setup_screen_font_color, setup_screen_bg_color, sc_x, sc_y, mc_x, mc_y, gamemode_solvethemaze, gamemode_timelimited, gamemode_speedrun, gamemode_text, kbmaction_text
    path = (255, 255, 255)
    sel_path = (107, 216, 255)
    start_c = (63, 192, 76)
    end_c = (46, 100, 161)
    fin_path = (255, 0, 0)
    alg_s = (255, 150, 0)
    centre_x, centre_y = 0, 0
    alg_sp = 0
    solved_text = ""
    path_nmbr = 0
    c = 0
    percentage = 0
    time = 0
    start_t = 0
    timer_r = 0
    screen = 0
    zoom_in = False
    zoom_out = False
# Parameters for display
    setup_screen_fontsize = 30
    setup_screen_font_color = (220, 220, 220)
    setup_screen_bg_color = (0, 0, 0)
    sc_x = 0
    sc_y = 0
    mc_x = 0
    mc_y = 0
# Solver selection texts
    gamemode_solvethemaze = 'Solve the maze'
    gamemode_timelimited = 'Time limited'
    gamemode_speedrun = 'Speed run'
    gamemode_text = 'a'
# Keyboard and mouse behaviour
    kbmaction_text = "kbm_click_and_drag"