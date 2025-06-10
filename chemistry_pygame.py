import pygame
import random
import json

# --- Inisialisasi Pygame ---
pygame.init()

# --- Konstanta ---
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
GREY = (200, 200, 200) # Warna baru untuk teks aturan
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
MAX_QUESTIONS = 5
FEEDBACK_DURATION = 1500

# --- Pengaturan Layar & Font ---
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Game Kimia Keren by Nida & Bara")
font = pygame.font.Font('assets//fonts/sugar_crush.otf', 45) # Ganti ukurannya juga boleh
font_small = pygame.font.Font('assets/fonts/sugar_crush.otf', 32)

# --- Load Suara ---
try:
    correct_sound = pygame.mixer.Sound('assets/sounds/correct.wav')
    wrong_sound = pygame.mixer.Sound('assets/sounds/wrong.wav')
except pygame.error as e:
    print("Error: Gagal memuat file suara.", e)
    # Buat jadi None kalo gagal, biar game ga crash
    correct_sound = None
    wrong_sound = None
    
# --- Load Gambar ---
try:
    background_image = pygame.image.load('assets/images/background.jpg').convert()
    # Pastikan ukuran gambar pas dengan layar kita
    background_image = pygame.transform.scale(background_image, (SCREEN_WIDTH, SCREEN_HEIGHT))
    tick_image = pygame.image.load('assets/images/tick.png').convert_alpha()
    tick_image = pygame.transform.scale(tick_image, (100, 100))
    cross_image = pygame.image.load('assets/images/cross.png').convert_alpha()
    cross_image = pygame.transform.scale(cross_image, (100, 100))
except pygame.error as e:
    print("Error: Gagal memuat file gambar.", e)
    background_image = None # Kalo gagal, backgroundnya nanti warna putih aja

# --- Data Game ---
with open('senyawa.json', 'r') as f:
    compounds = json.load(f)

# --- Variabel Game ---
game_state = "start"
previous_game_state = "start"
running = True
current_compound = None
user_answer = ""
score = 0
total_questions = 0
feedback_message = ""
feedback_color = BLACK
feedback_start_time = 0
hint_message = "" # <<< VARIABEL BARU UNTUK HINT

# --- Fungsi Bantuan ---
def get_new_compound():
    formula = random.choice(list(compounds.keys()))
    return formula, compounds[formula]

def display_message(text, color, y_offset, current_font=font): # Update fungsi biar bisa ganti font
    text_surface = current_font.render(text, True, color)
    text_rect = text_surface.get_rect(center=(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2 + y_offset))
    screen.blit(text_surface, text_rect)

def draw_text(text, font, color, surface, x, y):
    text_obj = font.render(text, True, color)
    text_rect = text_obj.get_rect()
    text_rect.topleft = (x, y)
    surface.blit(text_obj, text_rect)

# =================================================================
# --- GAME LOOP UTAMA ---
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
                    # --- LOGIKA HINT BARU ---
                    if user_answer.lower().strip() == 'hint':
                        hint_message = current_compound[1]['sifat']
                        user_answer = "" # Kosongkan jawaban setelah minta hint
                    else:
                        correct_answer = current_compound[1]['name'].lower()
                        if user_answer.lower().strip() == correct_answer:
                            score += 1
                            feedback_message = "BENAR!"
                            feedback_color = GREEN
                            if correct_sound: correct_sound.play()
                        else:
                            feedback_message = f"SALAH! Jawaban: {current_compound[1]['name']}"
                            feedback_color = RED
                            if wrong_sound: wrong_sound.play()
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
            
            elif game_state == "result":
                if event.key == pygame.K_y:
                    game_state = "playing"
                    score = 0
                    total_questions = 0
                    user_answer = ""
                    hint_message = "" # Reset hint
                    current_compound = get_new_compound()
                elif event.key == pygame.K_n:
                    running = False

    # 2. Drawing
    if game_state == "start":
        if background_image:
            screen.blit(background_image, (0, 0))
        else:
            screen.fill(WHITE)
        display_message("Selamat Datang di Game Kimia!", BLACK, -150)
        display_message("Tekan Spasi untuk Memulai", BLACK, 180)
        
        # --- TAMPILAN ATURAN MAIN BARU ---
        display_message("Cara Bermain:", GREY, -80, font_small)
        display_message("1. Tebak nama senyawa dari rumus kimia yang diberikan.", GREY, -50, font_small)
        display_message("2. Ketik 'hint' untuk mendapatkan petunjuk.", GREY, -20, font_small)
        display_message("3. Tekan 'ESC' kapan saja untuk keluar.", GREY, 10, font_small)

        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE]:
            game_state = "playing"
            current_compound = get_new_compound()
            user_answer = ""
            hint_message = "" # Reset hint
            score = 0
            total_questions = 0

    elif game_state == "playing":
        if background_image:
            screen.blit(background_image, (0, 0))
        else:
            screen.fill(WHITE)
        pygame.draw.rect(screen, (0, 0, 0, 150), [0, 0, SCREEN_WIDTH, 60]) 
        draw_text(f"Skor: {score}", font_small, WHITE, screen, 20, 15)
        draw_text(f"Soal: {total_questions + 1}/{MAX_QUESTIONS}", font_small, WHITE, screen, SCREEN_WIDTH - 150, 15)
        if current_compound:
            formula = current_compound[0]
            display_message(f"Rumus Kimia: {formula}", BLACK, -150)
            display_message("Apa nama senyawa ini?", BLACK, -100)
            
            # --- TAMPILAN HINT BARU ---
            if hint_message:
                display_message(f"Hint: {hint_message}", GREY, -50, font_small)
            
            pygame.draw.rect(screen, BLACK, (100, SCREEN_HEIGHT / 2, 600, 50), 2)
            answer_surface = font.render(user_answer, True, BLACK)
            screen.blit(answer_surface, (110, SCREEN_HEIGHT / 2 + 10))

    elif game_state == "feedback":
        if background_image:
            screen.blit(background_image, (0, 0))
        else:
            screen.fill(WHITE)
        pygame.draw.rect(screen, (0, 0, 0, 150), [0, 0, SCREEN_WIDTH, 60])
        draw_text(f"Skor: {score}", font_small, WHITE, screen, 20, 15)
        draw_text(f"Soal: {total_questions}/{MAX_QUESTIONS}", font_small, WHITE, screen, SCREEN_WIDTH - 150, 15) # Di sini pakenya total_questions, bukan +1
        # Tentukan gambar mana yang mau ditampilkan berdasarkan warna feedback
        if feedback_color == GREEN:
            if tick_image:
                # Tampilkan gambar di tengah layar
                rect = tick_image.get_rect(center=(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2))
                screen.blit(tick_image, rect)
        else: # Berarti warnanya MERAH
            if cross_image:
                # Tampilkan gambar di tengah layar
                rect = cross_image.get_rect(center=(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2))
                screen.blit(cross_image, rect)
        
        # Tampilkan juga teks feedback-nya di bawah gambar
        display_message(feedback_message, feedback_color, 150)

        # Cek timer untuk lanjut ke soal berikutnya
        current_time = pygame.time.get_ticks()
        if current_time - feedback_start_time > FEEDBACK_DURATION:
            if total_questions >= MAX_QUESTIONS:
                game_state = "result"
            else:
                game_state = "playing"
                current_compound = get_new_compound()
                user_answer = ""
                hint_message = ""

    elif game_state == "confirm_quit":
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 150))
        screen.blit(overlay, (0, 0))
        display_message("Yakin mau keluar?", WHITE, -20)
        display_message("Tekan (Y) untuk Ya / (N) untuk Tidak", WHITE, 20)
        
    elif game_state == "result":
        if background_image:
            screen.blit(background_image, (0, 0))
        else:
            screen.fill(WHITE)
        display_message("GAME SELESAI!", BLACK, -100)
        display_message(f"Skor Akhir: {score} / {MAX_QUESTIONS}", BLACK, -20)
        display_message("Main Lagi?", BLACK, 50)
        display_message("(Y/N)", BLACK, 90)

    # 3. Update Display
    pygame.display.flip()

# --- Keluar ---
pygame.quit()