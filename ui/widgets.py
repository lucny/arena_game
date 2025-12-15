"""Jednoduché UI widgety pro vykreslování panelů, menu a HUD."""

import pygame


def draw_panel(
	screen,
	title,
	lines,
	hint=None,
	*,
	bg_color=(15, 15, 15),
	title_color=(255, 80, 80),
	line_color=(220, 220, 220),
	hint_color=(160, 160, 160),
	title_y=120,
	start_y=220,
	line_spacing=40,
	hint_y_offset=80,
	highlight_first=False,
	highlight_color=(255, 200, 50),
):
	"""Vykreslí panel s nadpisem, řádky textu a volitelnou nápovědou."""
	width, height = screen.get_size()

	screen.fill(bg_color)

	font_title = pygame.font.SysFont(None, 52)
	font_line = pygame.font.SysFont(None, 32)

	title_surf = font_title.render(title, True, title_color)
	screen.blit(title_surf, title_surf.get_rect(center=(width // 2, title_y)))

	for i, line in enumerate(lines):
		color = highlight_color if highlight_first and i == 0 else line_color
		line_surf = font_line.render(line, True, color)
		y = start_y + i * line_spacing
		screen.blit(line_surf, line_surf.get_rect(center=(width // 2, y)))

	if hint:
		if isinstance(hint, (list, tuple)):
			hints = list(hint)
		else:
			hints = [hint]
		for idx, h in enumerate(hints):
			y = height - hint_y_offset + idx * 25
			hint_surf = font_line.render(h, True, hint_color)
			screen.blit(hint_surf, hint_surf.get_rect(center=(width // 2, y)))


def draw_input_panel(
	screen,
	title,
	value,
	hint=None,
	*,
	bg_color=(10, 10, 10),
	box_size=(360, 60),
	title_offset=60,
	hint_offset=70,
	box_color=(40, 40, 40),
	border_color=(200, 200, 200),
	text_color=(255, 255, 100),
	title_color=(255, 255, 255),
	hint_color=(150, 150, 150),
):
	"""Vykreslí panel pro zadání textu s nadpisem, vstupním boxem a nápovědou."""
	width, height = screen.get_size()

	screen.fill(bg_color)

	font_title = pygame.font.SysFont(None, 52)
	font_hint = pygame.font.SysFont(None, 32)

	title_surf = font_title.render(title, True, title_color)
	screen.blit(title_surf, title_surf.get_rect(center=(width // 2, height // 2 - title_offset)))

	box_rect = pygame.Rect(0, 0, *box_size)
	box_rect.center = (width // 2, height // 2)
	pygame.draw.rect(screen, box_color, box_rect)
	pygame.draw.rect(screen, border_color, box_rect, 2)

	text_surf = font_title.render(value, True, text_color)
	screen.blit(text_surf, text_surf.get_rect(center=box_rect.center))

	if hint:
		hint_surf = font_hint.render(hint, True, hint_color)
		screen.blit(hint_surf, hint_surf.get_rect(center=(width // 2, height // 2 + hint_offset)))


def draw_menu(
	screen,
	title,
	options,
	selected,
	*,
	hint=None,
	bg_color=(20, 20, 20),
	title_color=(255, 255, 255),
	option_color=(200, 200, 200),
	selected_color=(255, 200, 50),
	title_y=150,
	start_y=230,
	option_spacing=40,
	hint_color=(150, 150, 150),
	hint_y_offset=50,
):
	"""Vykreslí jednoduché menu s označenou položkou a nápovědou."""
	width, height = screen.get_size()

	screen.fill(bg_color)

	font_title = pygame.font.SysFont(None, 48)
	font_option = pygame.font.SysFont(None, 32)

	title_surf = font_title.render(title, True, title_color)
	screen.blit(title_surf, title_surf.get_rect(center=(width // 2, title_y)))

	for i, option in enumerate(options):
		color = selected_color if i == selected else option_color
		option_surf = font_option.render(option, True, color)
		y = start_y + i * option_spacing
		screen.blit(option_surf, option_surf.get_rect(center=(width // 2, y)))

	if hint:
		if isinstance(hint, (list, tuple)):
			hints = list(hint)
		else:
			hints = [hint]
		for idx, h in enumerate(hints):
			y = height - hint_y_offset + idx * 22
			hint_surf = font_option.render(h, True, hint_color)
			screen.blit(hint_surf, hint_surf.get_rect(center=(width // 2, y)))


def draw_hud(screen, *, score, time_value, shoots, accuracy, shots_left=None):
	"""Vykreslí HUD se skóre, časem (mm:ss), počtem výstřelů a úspěšností.

	Ammo je barevně zvýrazněno: >5 bílá, 3–5 žlutá, ≤2 červená.
	"""
	font = pygame.font.SysFont(None, 36)
	minutes = (time_value // 60) if isinstance(time_value, int) else 0
	seconds = (time_value % 60) if isinstance(time_value, int) else 0
	time_str = f"{minutes}:{seconds:02d}"

	white = (255, 255, 255)
	labels = [
		(f"Score: {score}", (10, 10), white),
		(f"Time: {time_str}", (210, 10), white),
		(f"Shoots: {shoots}", (410, 10), white),
		(f"Accuracy: {accuracy}%", (610, 10), white),
	]

	if shots_left is not None:
		if shots_left <= 2:
			ammo_color = (255, 80, 80)
		elif shots_left <= 5:
			ammo_color = (255, 210, 80)
		else:
			ammo_color = white
		labels.append((f"Ammo: {shots_left}", (810, 10), ammo_color))

	for text, pos, color in labels:
		surf = font.render(text, True, color)
		screen.blit(surf, pos)
