import pygame as pg

import config
import moves
import notation
import state


font = pg.font.SysFont('Arial', 24)
title_font = pg.font.SysFont('Arial', 40, bold=True)
menu_font = pg.font.SysFont('Arial', 22, bold=True)
menu_body_font = pg.font.SysFont('Arial', 18)
menu_small_font = pg.font.SysFont('Arial', 16)
small_font = pg.font.SysFont('Arial', 16, bold=True)
status_font = pg.font.SysFont('Arial', 22, bold=True)

screen = pg.display.set_mode((config.screen_width, config.window_size + config.panel_height * 2))
pg.display.set_caption("Chess")

small_pieces = {}
for color in ["white", "black"]:
    for name in config.piece_dict.values():
        image = pg.image.load(config.resource_path(f"images/{color}_{name}.png"))
        image = pg.transform.scale(image, (40, 40))
        small_pieces[f"{color}_{name}"] = image

pieces = {}
for color in ["white", "black"]:
    for name in config.piece_dict.values():
        image = pg.image.load(config.resource_path(f"images/{color}_{name}.png"))
        image = pg.transform.scale(image, (config.square_size, config.square_size))
        pieces[f"{color}_{name}"] = image


def draw_board(screen, board):
    for r in range(config.board_size):
        for c in range(config.board_size):

            color = config.light_color if (r + c) % 2 == 0 else config.dark_color

            pg.draw.rect(
                screen,
                color,
                (c * config.square_size,
                 r * config.square_size + config.panel_height,
                 config.square_size,
                 config.square_size)
            )

            piece = board[r][c]

            if piece != 0:
                piece_type = config.piece_num(piece)
                piece_color = "white" if piece > 0 else "black"

                piece_image = pieces[
                    f"{piece_color}_{config.piece_dict[piece_type]}"
                ]

                screen.blit(
                    piece_image,
                    (c * config.square_size,
                     r * config.square_size + config.panel_height)
                )


def draw_board_coordinates(screen):
    for c in range(config.board_size):
        file_label = chr(ord('a') + c)
        text = small_font.render(file_label, True, (35, 35, 35))
        screen.blit(text, (c * config.square_size + 4, config.panel_height + config.window_size - 18))

    for r in range(config.board_size):
        rank_label = str(8 - r)
        text = small_font.render(rank_label, True, (35, 35, 35))
        screen.blit(text, (4, config.panel_height + r * config.square_size + 3))


def draw_overlay_square(screen, row, col, color, alpha=90):
    overlay = pg.Surface((config.square_size, config.square_size), pg.SRCALPHA)
    overlay.fill((*color, alpha))
    screen.blit(
        overlay,
        (col * config.square_size, row * config.square_size + config.panel_height)
    )


def draw_status_bar(screen, eval_score):
    status_bg = (129, 96, 66)
    status_edge = (104, 77, 54)
    accent = (247, 232, 205)
    pg.draw.rect(screen, status_bg, (0, 0, config.screen_width, config.panel_height))
    pg.draw.rect(screen, status_bg, (0, config.panel_height + config.window_size, config.screen_width, config.panel_height))
    pg.draw.line(screen, status_edge, (0, config.panel_height - 1), (config.screen_width, config.panel_height - 1), 2)
    pg.draw.line(screen, status_edge, (0, config.panel_height + config.window_size), (config.screen_width, config.panel_height + config.window_size), 2)

    turn_text = "White to move" if state.current_turn == 1 else "Black to move"
    turn_surface = status_font.render(turn_text, True, accent)
    screen.blit(turn_surface, (12, 16))

    eval_text = f"Eval: {eval_score:+d}"
    eval_surface = status_font.render(eval_text, True, (245, 240, 230))
    screen.blit(eval_surface, (config.screen_width - eval_surface.get_width() - 12, 16))

    controls = f"Click to move | U undo | P AI move | R reset | Bot depth {state.bot_search_depth}"
    controls_surface = small_font.render(controls, True, (236, 226, 214))
    screen.blit(
        controls_surface,
        (12, config.panel_height + config.window_size + 18)
    )


def depth_description(depth):
    descriptions = {
        2: "Very fast, casual moves. Best if you want near-instant replies.",
        3: "Beginner bot with very quick moves.",
        4: "Intermediate bot with slower move times and more considered moves.",
        5: "Stronger bot that thinks longer before moving.",
        6: "Advanced bot with the slowest replies in this menu.",
    }
    return descriptions.get(depth, "A balanced chess bot setting.")


def draw_start_menu(screen, selected_depth):
    menu_bg_top = config.dark_color
    menu_bg_bottom = (219, 198, 160)
    menu_card = (245, 238, 226)
    menu_card_shadow = (0, 0, 0, 55)
    menu_card_border = (137, 101, 67)
    menu_accent = (168, 121, 81)
    menu_text = (54, 38, 28)
    menu_muted = (111, 89, 72)
    menu_button = (230, 220, 204)
    menu_button_hover = (241, 232, 218)
    menu_button_selected = (125, 90, 58)
    menu_button_text = (62, 45, 34)
    menu_button_text_selected = (255, 248, 238)

    screen.fill(menu_bg_top)

    ui_width, ui_height = screen.get_size()
    bg = pg.Surface((ui_width, ui_height))
    for y in range(ui_height):
        t = y / max(1, ui_height - 1)
        r = int(menu_bg_top[0] + (menu_bg_bottom[0] - menu_bg_top[0]) * t)
        g = int(menu_bg_top[1] + (menu_bg_bottom[1] - menu_bg_top[1]) * t)
        b = int(menu_bg_top[2] + (menu_bg_bottom[2] - menu_bg_top[2]) * t)
        pg.draw.line(bg, (r, g, b), (0, y), (ui_width, y))
    screen.blit(bg, (0, 0))

    glow = pg.Surface((ui_width, ui_height), pg.SRCALPHA)
    pg.draw.circle(glow, (255, 247, 233, 30), (ui_width // 2 - 140, 140), 160)
    pg.draw.circle(glow, (157, 116, 79, 18), (ui_width // 2 + 180, 220), 180)
    screen.blit(glow, (0, 0))

    card_w = min(700, ui_width - 120)
    card_h = min(560, ui_height - 100)
    card_rect = pg.Rect(
        (ui_width - card_w) // 2,
        (ui_height - card_h) // 2,
        card_w,
        card_h
    )

    shadow = pg.Surface((card_rect.width, card_rect.height), pg.SRCALPHA)
    pg.draw.rect(shadow, menu_card_shadow, shadow.get_rect(), border_radius=24)
    screen.blit(shadow, (card_rect.x + 8, card_rect.y + 10))

    pg.draw.rect(screen, menu_card, card_rect, border_radius=24)
    pg.draw.rect(screen, menu_card_border, card_rect, width=2, border_radius=24)

    header_band = pg.Rect(card_rect.left, card_rect.top, card_rect.width, 118)
    pg.draw.rect(screen, (252, 246, 238), header_band, border_top_left_radius=24, border_top_right_radius=24)
    pg.draw.line(screen, (219, 204, 184), (card_rect.left + 24, card_rect.top + 118), (card_rect.right - 24, card_rect.top + 118), 2)

    title = title_font.render("Chess Bot Setup", True, menu_text)
    subtitle = menu_body_font.render(
        "Pick a depth, read the tradeoff, then start the game.",
        True,
        menu_muted
    )
    screen.blit(title, (card_rect.left + 28, card_rect.top + 26))
    screen.blit(subtitle, (card_rect.left + 28, card_rect.top + 74))

    chip_rect = pg.Rect(card_rect.right - 152, card_rect.top + 32, 122, 34)
    pg.draw.rect(screen, (177, 127, 82), chip_rect, border_radius=17)
    pg.draw.rect(screen, (117, 82, 54), chip_rect, width=1, border_radius=17)
    chip_text = menu_small_font.render("Ready to play", True, (255, 248, 238))
    screen.blit(chip_text, (chip_rect.centerx - chip_text.get_width() // 2, chip_rect.centery - chip_text.get_height() // 2))

    left_x = card_rect.left + 28
    section_y = card_rect.top + 148

    label = menu_font.render("Choose bot depth", True, menu_text)
    screen.blit(label, (left_x, section_y))

    depth_options = [2, 3, 4, 5, 6]
    button_rects = {}
    button_w = 82
    button_h = 64
    gap = 10
    y = section_y + 38

    for index, depth in enumerate(depth_options):
        rect = pg.Rect(left_x + index * (button_w + gap), y, button_w, button_h)
        button_rects[depth] = rect

        hovered = rect.collidepoint(pg.mouse.get_pos())
        if depth == selected_depth:
            color = menu_button_selected
            text_color = menu_button_text_selected
            border_color = (88, 61, 42)
            shadow_color = (0, 0, 0, 30)
        else:
            color = menu_button_hover if hovered else menu_button
            text_color = menu_button_text
            border_color = (184, 164, 142)
            shadow_color = (0, 0, 0, 14 if hovered else 10)

        btn_shadow = pg.Surface((rect.width, rect.height), pg.SRCALPHA)
        pg.draw.rect(btn_shadow, shadow_color, btn_shadow.get_rect(), border_radius=14)
        screen.blit(btn_shadow, (rect.x + 3, rect.y + 4))

        pg.draw.rect(screen, color, rect, border_radius=14)
        pg.draw.rect(screen, border_color, rect, width=2, border_radius=14)

        depth_text = menu_font.render(str(depth), True, text_color)
        depth_label = menu_small_font.render("Depth", True, text_color if depth == selected_depth else menu_muted)
        screen.blit(depth_text, (rect.centerx - depth_text.get_width() // 2, rect.y + 8))
        screen.blit(depth_label, (rect.centerx - depth_label.get_width() // 2, rect.y + 36))

    explainer_text = menu_body_font.render(depth_description(selected_depth), True, menu_muted)
    explainer_label = menu_small_font.render(f"Depth {selected_depth}", True, menu_text)
    screen.blit(explainer_label, (left_x, card_rect.bottom - 136))
    screen.blit(explainer_text, (left_x, card_rect.bottom - 108))

    start_rect = pg.Rect(card_rect.left + 28, card_rect.bottom - 88, card_rect.width - 56, 58)
    start_hover = start_rect.collidepoint(pg.mouse.get_pos())
    start_fill = menu_accent if not start_hover else (196, 145, 102)
    start_text_color = (255, 249, 240)
    start_shadow = pg.Surface((start_rect.width, start_rect.height), pg.SRCALPHA)
    pg.draw.rect(start_shadow, (0, 0, 0, 22), start_shadow.get_rect(), border_radius=16)
    screen.blit(start_shadow, (start_rect.x + 4, start_rect.y + 6))
    pg.draw.rect(screen, start_fill, start_rect, border_radius=16)
    pg.draw.rect(screen, (101, 72, 48), start_rect, width=2, border_radius=16)

    start_text = menu_font.render("Start Game", True, start_text_color)
    start_hint = menu_small_font.render("Press Enter or click to launch the match", True, (247, 238, 225))
    screen.blit(start_text, (start_rect.centerx - start_text.get_width() // 2, start_rect.y + 9))
    screen.blit(start_hint, (start_rect.centerx - start_hint.get_width() // 2, start_rect.y + 34))

    footer = menu_small_font.render("Tip: depth 3 is the fastest. Depth 4 feels a bit more deliberate.", True, menu_muted)
    screen.blit(footer, (card_rect.centerx - footer.get_width() // 2, card_rect.bottom - 22))

    return button_rects, start_rect


def draw_panel(screen, color, captured, eval_score):
    panel_y = 0 if color == 'black' else config.panel_height + config.window_size

    pg.draw.rect(screen, (123, 90, 62), (0, panel_y, config.screen_width, config.panel_height))
    pg.draw.line(screen, (96, 69, 46), (0, panel_y + config.panel_height - 1), (config.screen_width, panel_y + config.panel_height - 1), 2)

    for i, piece in enumerate(captured):
        piece_type = config.piece_num(piece)
        piece_color = 'white' if piece > 0 else 'black'
        image = small_pieces[f'{piece_color}_{config.piece_dict[piece_type]}']
        screen.blit(image, (i * 42, panel_y + (config.panel_height - 40) // 2))

    if color == 'white' and eval_score > 0:
        text = font.render(f'+{eval_score}', True, (255, 250, 240))
        screen.blit(text, (config.screen_width - 50, panel_y + config.panel_height // 2 - 12))
    elif color == 'black' and eval_score < 0:
        text = font.render(f'+{abs(eval_score)}', True, (255, 250, 240))
        screen.blit(text, (config.screen_width - 50, panel_y + config.panel_height // 2 - 12))


def draw_move_sidebar(screen):
    sidebar_x = config.window_size
    sidebar_y = config.panel_height
    sidebar_h = config.window_size
    sidebar_rect = pg.Rect(sidebar_x, sidebar_y, config.sidebar_width, sidebar_h)

    pg.draw.rect(screen, (242, 234, 221), sidebar_rect)
    pg.draw.line(screen, (163, 135, 105), (sidebar_x, sidebar_y), (sidebar_x, sidebar_y + sidebar_h), 3)

    header_rect = pg.Rect(sidebar_x, sidebar_y, config.sidebar_width, 58)
    pg.draw.rect(screen, (209, 179, 143), header_rect)
    pg.draw.line(screen, (145, 110, 80), (sidebar_x, sidebar_y + 57), (sidebar_x + config.sidebar_width, sidebar_y + 57), 2)

    title = menu_font.render("Move Log", True, (62, 44, 32))
    subtitle = menu_small_font.render("Chess notation", True, (96, 75, 56))
    screen.blit(title, (sidebar_x + 18, sidebar_y + 12))
    screen.blit(subtitle, (sidebar_x + 18, sidebar_y + 34))

    lines = notation.build_move_log_lines()
    line_font = menu_small_font
    line_height = 24
    max_visible = (sidebar_h - 110) // line_height
    visible_lines = lines[-max_visible:]

    if not visible_lines:
        empty = line_font.render("No moves yet.", True, (112, 92, 75))
        screen.blit(empty, (sidebar_x + 18, sidebar_y + 84))
        return

    start_y = sidebar_y + 76
    for index, line in enumerate(visible_lines):
        text = line_font.render(line, True, (61, 45, 34))
        y = start_y + index * line_height
        screen.blit(text, (sidebar_x + 18, y))

    footer = menu_small_font.render("Recent moves shown here.", True, (126, 107, 92))
    screen.blit(footer, (sidebar_x + 18, sidebar_y + sidebar_h - 26))


def show_legal_moves(screen, board, row, col):
    legal_moves = moves.get_legal_moves(board, row, col)
    for move in legal_moves:
        target_piece = board[move[0]][move[1]]
        if target_piece == 0:
            pg.draw.circle(
                screen,
                (225, 225, 225),
                (move[1] * config.square_size + config.square_size // 2, move[0] * config.square_size + config.square_size // 2 + config.panel_height),
                10
            )
        else:
            draw_overlay_square(screen, move[0], move[1], (220, 90, 90), 70)
