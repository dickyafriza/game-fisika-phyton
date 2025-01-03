#reno
import pygame
import math
import random

# Inisialisasi Pygame
pygame.init()

# Dimensi layar
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Game Angry Birds Sederhana dengan Trek")

# Warna
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
BLACK = (0, 0, 0)
BLUE = (0, 0, 255)

# Font
font = pygame.font.SysFont(None, 24)

# Waktu dan gravitasi
clock = pygame.time.Clock()
g = 9.8  # gravitasi (m/s^2)

# Properti bola
x_initial, y_initial = 100, HEIGHT - 100  # Posisi awal bola
radius = 10  # Radius bola
x_new, y_new = x_initial, y_initial
velocity = 0
angle_rad = 0
flying = False

# Trek lintasan
trajectory_points = []

# Skala kecepatan (untuk memperpendek garis)
SCALE = 0.5

# Properti target
target_width, target_height = 40, 40
target_x, target_y = 600, HEIGHT - 120
target_respawn_time = 0  # Waktu untuk respawn target

# Muat gambar latar belakang
background = pygame.image.load("/Users/dicky/Documents/Github/game-fisika-phyton/bg.jpg")
background = pygame.transform.scale(background, (800, 600))  # Ubah ukuran sesuai layar

# Muat gambar angry
ball_image = pygame.image.load("/Users/dicky/Documents/Github/game-fisika-phyton/ball.png")
ball_image = pygame.transform.scale(ball_image, (radius * 4, radius * 4))  # Ubah ukuran bola

# Fungsi untuk memindahkan target ke posisi baru
def respawn_target():
    global target_x, target_y
    target_x = random.randint(400, WIDTH - target_width)
    target_y = random.randint(HEIGHT // 2, HEIGHT - target_height)

# Fungsi untuk menampilkan teks
def draw_text(text, x, y, color=BLACK):
    render = font.render(text, True, color)
    screen.blit(render, (x, y))

# Variabel untuk menyimpan jarak jatuh
fall_distance = None
#reno

#dicky
# Loop utama
running = True
while running:
    screen.blit(background, (0, 0))  # Tampilkan latar belakang

    # Gambar target jika aktif
    if pygame.time.get_ticks() > target_respawn_time:
        pygame.draw.rect(screen, BLACK, (target_x, target_y, target_width, target_height))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN and not flying:
            # Dapatkan posisi mouse saat ditekan
            start_pos = pygame.mouse.get_pos()
        if event.type == pygame.MOUSEBUTTONUP and not flying:
            # Hitung sudut dan kecepatan berdasarkan posisi mouse
            end_pos = pygame.mouse.get_pos()
            dx = end_pos[0] - x_initial
            dy = y_initial - end_pos[1]
            velocity = math.sqrt(dx**2 + dy**2) * SCALE  # Perbesar kecepatan dengan skala
            angle_rad = math.atan2(dy, dx)
            flying = True
            time = 0
            trajectory_points.clear()  # Bersihkan trek lintasan
            fall_distance = None  # Reset jarak jatuh

    # Gerak parabola saat bola meluncur
    if flying:
        x_new = x_initial + velocity * time * math.cos(angle_rad)
        y_new = y_initial - (velocity * time * math.sin(angle_rad) - 0.5 * g * time**2)

        # Tambahkan posisi ke lintasan
        trajectory_points.append((int(x_new), int(y_new)))

        # Deteksi tabrakan dengan tanah
        if y_new >= HEIGHT - radius:
            y_new = HEIGHT - radius
            flying = False
            fall_distance = x_new - x_initial  # Hitung jarak jatuh
            x_new, y_new = x_initial, y_initial  # Reset posisi bola

        # Deteksi tabrakan dengan target
        if (target_x <= x_new <= target_x + target_width and
                target_y <= y_new <= target_y + target_height):
            print("Target kena!")
            target_respawn_time = pygame.time.get_ticks() + 2000  # Respawn dalam 2 detik
            respawn_target()

        time += 0.1  # Increment waktu
#dicky
        

#alif
    # Gambar bola menggunakan gambar PNG
    screen.blit(ball_image, (int(x_new) - radius, int(y_new) - radius))

    # Gambar lintasan
    for point in trajectory_points:
        pygame.draw.circle(screen, BLUE, point, 2)

    # Gambar garis peluncuran saat mouse ditekan
    if not flying and pygame.mouse.get_pressed()[0]:
        mouse_pos = pygame.mouse.get_pos()
        pygame.draw.line(screen, BLACK, (x_initial, y_initial), mouse_pos, 2)  # Gunakan posisi bola sebagai titik awal

    # Tampilkan sudut dan kecepatan di layar
    if not flying and pygame.mouse.get_pressed()[0]:
        mouse_pos = pygame.mouse.get_pos()
        dx = mouse_pos[0] - x_initial
        dy = y_initial - mouse_pos[1]
        angle_deg = math.degrees(math.atan2(dy, dx))
        velocity_display = math.sqrt(dx**2 + dy**2) * SCALE
        draw_text(f"Sudut: {angle_deg:.1f}°", 10, 10)
        draw_text(f"Kecepatan: {velocity_display:.1f} m/s", 10, 30)

    # Tampilkan jarak jatuh jika ada
    if fall_distance is not None:
        draw_text(f"Jarak jatuh: {fall_distance:.1f} m", 10, 50)

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
#alif