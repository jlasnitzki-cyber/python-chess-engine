import sys

import pygame as pg

import config
import engine
import moves
import state


def main():
    pg.init()

    import ui

    while state.running == True:

        menu_depth_buttons = {}
        menu_start_button = None

        if state.menu_active:
            menu_depth_buttons, menu_start_button = ui.draw_start_menu(ui.screen, state.bot_search_depth)

        for event in pg.event.get():

            if event.type == pg.QUIT:
                pg.quit()
                sys.exit()

            if state.menu_active:
                if event.type == pg.KEYDOWN and event.key == pg.K_RETURN:
                    state.reset_game()
                    state.menu_active = False
                elif event.type == pg.MOUSEBUTTONDOWN and event.button == 1:
                    clicked_depth = None
                    for depth, rect in menu_depth_buttons.items():
                        if rect.collidepoint(event.pos):
                            clicked_depth = depth
                            break

                    if clicked_depth is not None:
                        state.bot_search_depth = clicked_depth
                    elif menu_start_button is not None and menu_start_button.collidepoint(event.pos):
                        state.reset_game()
                        state.menu_active = False
                continue

            elif event.type == pg.KEYDOWN:
                if event.key == pg.K_u:
                    print("undo")
                    state.undo_move()
                elif event.key == pg.K_p:
                    if state.current_turn == -1:
                        print("ai move")
                        engine.get_best_move()
                elif event.key == pg.K_r:
                    state.reset_game()

            elif event.type == pg.MOUSEBUTTONDOWN:
                mouse_pos = pg.mouse.get_pos()
                if not (0 <= mouse_pos[0] < config.window_size and config.panel_height <= mouse_pos[1] < config.panel_height + config.window_size):
                    continue
                col = mouse_pos[0] // config.square_size
                row = (mouse_pos[1] - config.panel_height) // config.square_size

                if state.selected_square is not None:

                    if (row, col) in moves.get_legal_moves(
                        state.board,
                        state.selected_square[0],
                        state.selected_square[1]
                    ):
                        state.make_move(
                            state.selected_square[0],
                            state.selected_square[1],
                            row,
                            col
                        )
                        state.move_count += 1
                        if moves.check_pawn_promotion(state.board, row, col):
                            piece = state.board[row][col]
                            if abs(piece) == 6:
                                state.board[row][col] = 2 * state.current_turn * -1

                        color = 'white' if state.current_turn == 1 else 'black'
                        state.game_over = moves.check_endgame(state.board, color)

                        state.selected_square = None
                    else:
                        piece = state.board[row][col]
                        if piece * state.current_turn > 0:
                            state.selected_square = (row, col)
                        else:
                            state.selected_square = None
                else:
                    piece = state.board[row][col]

                    if piece * state.current_turn > 0:
                        state.selected_square = (row, col)

        if state.menu_active:
            pg.display.flip()
            continue

        ui.draw_status_bar(ui.screen, state.evaluation(state.captured_pieces))

        ui.draw_board(ui.screen, state.board)

        if state.last_move is not None:
            start, end = state.last_move
            ui.draw_overlay_square(ui.screen, start[0], start[1], (70, 140, 230), 70)
            ui.draw_overlay_square(ui.screen, end[0], end[1], (70, 140, 230), 100)

        if state.current_turn in (1, -1):
            color_to_check = 'white' if state.current_turn == 1 else 'black'
            if moves.is_in_check(state.board, color_to_check):
                king_pos = moves.find_king(state.board, color_to_check)
                if king_pos is not None:
                    ui.draw_overlay_square(ui.screen, king_pos[0], king_pos[1], (220, 60, 60), 100)

        ui.draw_board_coordinates(ui.screen)
        eval_score = state.evaluation(state.captured_pieces)
        ui.draw_panel(ui.screen, 'black', state.captured_pieces['black'], eval_score)
        ui.draw_panel(ui.screen, 'white', state.captured_pieces['white'], eval_score)
        ui.draw_move_sidebar(ui.screen)

        if state.game_over == 'checkmate':
            text = ui.font.render('CHECKMATE!', True, (0, 0, 0))
            x = config.window_size // 2 - text.get_width() // 2
            y = config.panel_height + config.window_size // 2 - text.get_height() // 2
            ui.screen.blit(text, (x, y))
        if state.game_over == 'stalemate':
            text = ui.font.render('STALEMATE!', True, (0, 0, 0))
            x = config.window_size // 2 - text.get_width() // 2
            y = config.panel_height + config.window_size // 2 - text.get_height() // 2
            ui.screen.blit(text, (x, y))

        if state.selected_square is not None:
            ui.draw_overlay_square(ui.screen, state.selected_square[0], state.selected_square[1], (255, 235, 120), 85)
            ui.show_legal_moves(
                ui.screen,
                state.board,
                state.selected_square[0],
                state.selected_square[1]
            )

        pg.display.flip()


if __name__ == "__main__":
    main()
