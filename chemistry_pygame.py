import pygame
import random

# --- Inisialisasi Pygame ---
pygame.init()

# --- Konstanta ---
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
MAX_QUESTIONS = 5

# --- Pengaturan Layar & Font ---
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Game Kimia Keren by Nida & Bara")
font = pygame.font.Font(None, 40) # Menggunakan font default Pygame

# --- Data Game ---
compounds = {
    "H2O": {"name": "air", "sifat": "Cairan tidak berwarna"},
    "CO2": {"name": "karbon dioksida", "sifat": "Gas tidak berwarna"},
    "NaCl": {"name": "natrium klorida", "sifat": "Dikenal sebagai garam dapur"},
}

# --- Variabel Game ---
game_state = "start"
previous_game_state = "start"
running = True
current_compound = None
user_answer = ""
score = 0
total_questions = 0

# --- VARIABEL BARU UNTUK FEEDBACK ---
feedback_message = ""
feedback_color = BLACK
feedback_start_time = 0
FEEDBACK_DURATION = 1500 # 1.5 detik dalam milidetik

# --- Fungsi Bantuan ---
def get_new_compound():
    formula = random.choice(list(compounds.keys()))
    return formula, compounds[formula]

def display_message(text, color, y_offset):
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect(center=(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2 + y_offset))
    screen.blit(text_surface, text_rect)

# =================================================================
# --- GAME LOOP UTAMA ---
# =================================================================
# =================================================================
# --- GAME LOOP UTAMA (VERSI FINAL V1) ---
# =================================================================
while running:
    # 1. Event Handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                if game_state == "playing" or game_state == "feedback":
                    previous_game_state = game_state
                    game_state = "confirm_quit"

            if game_state == "playing":
                if event.key == pygame.K_RETURN:
                    correct_answer = current_compound[1]['name'].lower()
                    if user_answer.lower().strip() == correct_answer:
                        score += 1
                        feedback_message = "BENAR!"
                        feedback_color = GREEN
                    else:
                        feedback_message = f"SALAH! Jawaban: {current_compound[1]['name']}"
                        feedback_color = RED
                    game_state = "feedback"
                    feedback_start_time = pygame.time.get_ticks()
                    total_questions += 1
                elif event.key == pygame.K_BACKSPACE:
                    user_answer = user_answer[:-1]
                else:
                    user_answer += event.unicode
            
            elif game_state == "confirm_quit":
                if event.key == pygame.K_y:
                    running = False 
                elif event.key == pygame.K_n:
                    game_state = previous_game_state
            
            # --- LOGIKA INPUT BARU UNTUK STATE RESULT ---
            elif game_state == "result":
                if event.key == pygame.K_y:
                    # Reset game untuk main lagi
                    game_state = "playing"
                    score = 0
                    total_questions = 0
                    user_answer = ""
                    current_compound = get_new_compound()
                elif event.key == pygame.K_n:
                    running = False

    # 2. Drawing
    if game_state == "start":
        screen.fill(WHITE)
        display_message("Selamat Datang di Game Kimia!", BLACK, -50)
        display_message("Tekan Spasi untuk Memulai", BLACK, 50)
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE]:
            game_state = "playing"
            current_compound = get_new_compound()
            user_answer = ""
            score = 0
            total_questions = 0

    elif game_state == "playing":
        screen.fill(WHITE)
        if current_compound:
            formula = current_compound[0]
            display_message(f"Rumus Kimia: {formula}", BLACK, -150)
            display_message("Apa nama senyawa ini?", BLACK, -100)
            pygame.draw.rect(screen, BLACK, (100, SCREEN_HEIGHT / 2, 600, 50), 2)
            answer_surface = font.render(user_answer, True, BLACK)
            screen.blit(answer_surface, (110, SCREEN_HEIGHT / 2 + 10))

    elif game_state == "feedback":
        screen.fill(WHITE)
        if current_compound:
            formula = current_compound[0]
            display_message(f"Rumus Kimia: {formula}", BLACK, -150)
            display_message("Apa nama senyawa ini?", BLACK, -100)
            pygame.draw.rect(screen, BLACK, (100, SCREEN_HEIGHT / 2, 600, 50), 2)
            answer_surface = font.render(user_answer, True, BLACK)
            screen.blit(answer_surface, (110, SCREEN_HEIGHT / 2 + 10))
            display_message(feedback_message, feedback_color, 150)
        
        current_time = pygame.time.get_ticks()
        if current_time - feedback_start_time > FEEDBACK_DURATION:
            if total_questions >= MAX_QUESTIONS:
                game_state = "result"
            else:
                game_state = "playing"
                current_compound = get_new_compound()
                user_answer = ""

    elif game_state == "confirm_quit":
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 150))
        screen.blit(overlay, (0, 0))
        display_message("Yakin mau keluar?", WHITE, -20)
        display_message("Tekan (Y) untuk Ya / (N) untuk Tidak", WHITE, 20)
        
    # --- TAMPILAN BARU UNTUK STATE RESULT ---
    elif game_state == "result":
        screen.fill(WHITE)
        display_message("GAME SELESAI!", BLACK, -100)
        display_message(f"Skor Akhir: {score} / {MAX_QUESTIONS}", BLACK, -20)
        display_message("Main Lagi?", BLACK, 50)
        display_message("(Y/N)", BLACK, 90)

    # 3. Update Display
    pygame.display.flip()

# --- Keluar ---
pygame.quit()