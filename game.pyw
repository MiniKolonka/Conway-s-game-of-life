import numpy
import pygame
from pygame import gfxdraw
from random import randint

class Game:
	def __init__(self) -> None:
		self.display = pygame.display.set_mode((1200, 1000))
		self.continue_simulation = True
		self.speed = 60 #frame rate
		self.field = Field((100,100))
		self.clock = pygame.time.Clock()

		pygame.init()
		pygame.display.set_caption("Conway's Game of Life")

	def menu(self) -> None:
		while True:
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					pygame.quit()
					quit()
				if event.type == pygame.KEYDOWN:
					return

			self.draw_menu()
			self.clock.tick(self.speed)

	def game(self) -> None:
		while True:
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					pygame.quit()
					quit()

				if event.type == pygame.KEYDOWN:
					if event.key == pygame.K_SPACE:
						self.continue_simulation = not self.continue_simulation
					if event.key == pygame.K_ESCAPE:
						return

					if event.key == pygame.K_UP:
						self.speed = self.speed + 1 if self.speed != 72 else self.speed
					elif event.key == pygame.K_DOWN:
						self.speed = self.speed - 1 if self.speed != 1 else 1

					if event.key == pygame.K_r:
						self.field.random_fill()
					elif event.key == pygame.K_c:
						self.field.clear_field()

				pressed = pygame.mouse.get_pressed()
				mouse_position = pygame.mouse.get_pos()
				if mouse_position[0] < 1001 and mouse_position[1] < 1001:
					if pressed[0]:
						self.field.field[mouse_position[1] // 10][mouse_position[0] // 10] = True
					if pressed[2]:
						self.field.field[mouse_position[1] // 10][mouse_position[0] // 10] = False			

			if self.continue_simulation:
				self.field.update_state()
			self.draw_game(self.field.field)

			self.clock.tick(self.speed)

	def draw_game(self, field: numpy.array) -> None:
		self.display.fill((49,49,49))
		number_of_cells =  0

		#Drawing all cells
		for diagonal_index, diagonal in enumerate(field):
			for cell_index, cell in enumerate(diagonal):
				if cell:
					gfxdraw.box(self.display, ((cell_index * 10, diagonal_index * 10), (10, 10)), (255, 255, 255))
					number_of_cells += 1

		#Draving stats
		gfxdraw.box(self.display, ((1000, 0), (200, 1000)), (40, 40, 40))
		gfxdraw.box(self.display, ((1000, 0), (20, 1000)), (35, 35, 35))
		gfxdraw.box(self.display, ((1000, 35), (200, 20)), (35, 35, 35))


		font = pygame.font.Font(None, 28)

		if not self.continue_simulation:
			text = font.render('Pause', 1, (255, 255, 255))
			self.display.blit(text, (1025, 5))

		text = font.render(str(self.speed), 1, (255, 255, 255))
		self.display.blit(text, (1165, 5))

		text = font.render("Population", 1, (255, 255, 255))
		self.display.blit(text, (1025, 68))

		number_of_cells = font.render(str(number_of_cells), 1, (255, 255, 255))
		self.display.blit(number_of_cells, (1070, 98))

		pygame.display.update()

	def draw_menu(self) -> None:
		self.display.fill((40,40,40))

		gfxdraw.box(self.display, ((0, 0), (1200, 215)), (49, 49, 49))
		gfxdraw.box(self.display, ((0, 440), (1200, 560)), (49, 49, 49))
		gfxdraw.box(self.display, ((1040, 215), (235, 345)), (49, 49, 49))
		gfxdraw.box(self.display, ((0, 215), (235, 345)), (49, 49, 49))
		gfxdraw.box(self.display, ((310, 850), (580, 85)), (40,40,40))

		title = pygame.font.Font(None, 72)
		text = title.render("Кнопки:", 1, (255, 255, 255))
		self.display.blit(text, (500, 155))

		paragraph = pygame.font.Font(None, 42)
		text = paragraph.render("• R - заполнить поле случайными клетками.", 1, (255, 255, 255))
		text_2 = paragraph.render("• С -  очистить поле.", 1, (255, 255, 255))
		text_3 = paragraph.render("• Space -  остановить время.", 1, (255, 255, 255))
		text_4 = paragraph.render("• Добавлять/Удалять клетки можно кликами мышки.", 1, (255, 255, 255))
		text_5 = paragraph.render("(Используйте вместе с остановкой времени)", 1, (255, 255, 255))

		self.display.blit(text, (275, 230))
		self.display.blit(text_2, (275, 270))
		self.display.blit(text_3, (275, 310))
		self.display.blit(text_4, (275, 350))
		self.display.blit(text_5, (325, 390))

		mini_paragraph = pygame.font.Font(None, 36)
		text = mini_paragraph.render("Прочитал? Гуд, жмякни на любую кнопку", 1, (255, 255, 255))
		self.display.blit(text, (340, 880))

		pygame.display.update()

	def start(self) -> None:
		while True:
			self.menu()
			self.game()







class Field:
	def __init__(self, size: tuple = (100, 100)) -> None:
		#Поле может быть только квадратом, т.е. создать поле 100x120 не выйдет.
		self.size = size
		#Field и matrix_of_neighbors  - вложенные массивы.
		self.field = numpy.array([False] * size[0] * size[0]).reshape(size[0], size[1])
		self.matrix_of_neighbors = numpy.array([0] * size[0] * size[0]).reshape(size[0], size[1])

	def random_fill(self) -> None:
		for diagonal_index in range(self.size[1]):
			for cell_index in range(self.size[0]):
				self.field[diagonal_index][cell_index] = bool(randint(0, 1))

	def clear_field(self) -> None:
		self.field = numpy.array([False] * self.size[0] * self.size[0]).reshape(self.size[0], self.size[1])		

	def count_of_neighbors(self, diagonal_index: int, cell_index: int) -> int:
		#Функция возвращает количество соседей у определённой клетки
		#field представлен в виде фигуры тор. Т.е. если клетка будет пересекать верхнюю границу - она попадает в низ и так дальше.
		upper_diagonal = diagonal_index + 1 if diagonal_index + 1 != self.size[1] else 0
		upper_cell = cell_index + 1 if cell_index + 1 != self.size[0] else 0

		lower_diahonal = diagonal_index - 1
		lower_cell = cell_index - 1

		upper_neighbors = [self.field[upper_diagonal][upper_cell], self.field[upper_diagonal][lower_cell], self.field[upper_diagonal][cell_index]]
		lower_neighbors = [self.field[lower_diahonal][upper_cell], self.field[lower_diahonal][lower_cell], self.field[lower_diahonal][cell_index]]
		middle_neighbors = [self.field[diagonal_index][upper_cell], self.field[diagonal_index][lower_cell]]

		return sum(map(int, upper_neighbors + lower_neighbors + middle_neighbors))

	def update_state(self) -> None:
		#Updates field
		#Переменная matrix_of_neighbors нужна для "одновременного" обновления всех ячеек.
		#Если реализовать поочерёдное обновление - результаты будут в корне отличается.
		self.matrix_of_neighbors = numpy.array([0] * self.size[0] * self.size[0]).reshape(self.size[0], self.size[1])

		for index_of_diagonal, diagonal  in enumerate(self.field):
			for index_of_cell, cell in enumerate(diagonal):
				neighbors = self.count_of_neighbors(index_of_diagonal, index_of_cell)
				self.matrix_of_neighbors[index_of_diagonal][index_of_cell] = neighbors

		for index_of_diagonal, diagonal  in enumerate(self.field):
			for index_of_cell, cell in enumerate(diagonal):
				if not cell and self.matrix_of_neighbors[index_of_diagonal][index_of_cell] == 3:
					self.field[index_of_diagonal][index_of_cell] = True
				elif cell and self.matrix_of_neighbors[index_of_diagonal][index_of_cell] not in (2,3):
					self.field[index_of_diagonal][index_of_cell] = False

game = Game()
game.start()
