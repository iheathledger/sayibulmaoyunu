import pygame
import random
import sys

def farkli_sayi_olustur():
    while True:
        num = random.sample(range(10), 4)
        if num[0] != 0:  
            break
    return int(''.join(map(str, num)))

def tahmin_yap(tahmin, tutulan_sayi):
    tahmin_str = str(tahmin)
    tutulan_str = str(tutulan_sayi)
    dogru_basamaklar = 0
    dogru_rakamlar = 0
    for i in range(4):
        if tahmin_str[i] == tutulan_str[i]:
            dogru_basamaklar += 1
        elif tahmin_str[i] in tutulan_str:
            dogru_rakamlar += 1
    if dogru_basamaklar == 4:
        return "+4"
    else:
        return "+" + str(dogru_basamaklar) + ",-" + str(dogru_rakamlar)

def run_game():
    pygame.init()

    WIDTH, HEIGHT = 400, 600
    ekran = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Sayı Tahmin Oyunu")

    BEYAZ = (255, 255, 255)
    SİYAH = (0, 0, 0)

    font = pygame.font.Font(None, 36)
    instructions_font = pygame.font.Font(None, 22)  

    
    background = pygame.image.load('background1.jpg')
    background = pygame.transform.scale(background, (WIDTH, HEIGHT))

    def yeni_oyun():
        nonlocal bilgisayar_sayisi, tahminler, input_text, game_started
        bilgisayar_sayisi = farkli_sayi_olustur()
        print("Bilgisayarın tuttuğu sayı:", bilgisayar_sayisi)  
        tahminler = []
        input_text = ''
        game_started = False

    bilgisayar_sayisi = farkli_sayi_olustur()
    print("Bilgisayarın tuttuğu sayı:", bilgisayar_sayisi)  

    tahminler = []

    input_box = pygame.Rect(135, 75, 140, 32)
    input_text = ''

    game_started = False
    show_instructions = False
    start_button_rect = pygame.Rect(115, 275, 170, 50)
    start_button_text = font.render("Oyuna Başla", True, SİYAH)
    restart_button_rect = pygame.Rect(115, 500, 170, 50)
    restart_button_text = font.render("Tekrar Oyna", True, SİYAH)
    instructions_button_rect = pygame.Rect(105, 350, 190, 50)
    instructions_button_text = font.render("Nasıl Oynanır?", True, SİYAH)
    back_button_rect = pygame.Rect(95, 500, 220, 50)
    back_button_text = font.render("Ana Sayfaya Dön", True, SİYAH)

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if not game_started and not show_instructions:  
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    if start_button_rect.collidepoint(event.pos):
                        game_started = True
                    elif instructions_button_rect.collidepoint(event.pos):
                        show_instructions = True
            elif show_instructions:
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    if back_button_rect.collidepoint(event.pos):
                        show_instructions = False
            else:  
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        if len(input_text) == 4 and input_text.isdigit():
                            tahmin = int(input_text)
                            sonuc = tahmin_yap(tahmin, bilgisayar_sayisi)
                            tahminler.append((tahmin, sonuc))
                            input_text = ''
                            if sonuc == "+4":
                                font_big = pygame.font.Font(None, 72)
                                message_surface = font_big.render("Tebrikler!", True, SİYAH)
                                ekran.blit(message_surface, (80, 25))
                                pygame.display.flip()
                    elif event.key == pygame.K_BACKSPACE:
                        input_text = input_text[:-1]
                    else:
                        if len(input_text) < 4 and event.unicode.isdigit():
                            input_text += event.unicode
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    if restart_button_rect.collidepoint(event.pos):
                        yeni_oyun()
        
        ekran.blit(background, (0, 0))

        if not game_started and not show_instructions:  
            title_text = font.render("SAYI BULMA OYUNU", True, SİYAH)
            title_rect = title_text.get_rect(center=(WIDTH//2, 50))
            ekran.blit(title_text, title_rect)

            pygame.draw.rect(ekran, SİYAH, start_button_rect, 2)
            ekran.blit(start_button_text, (start_button_rect.x + 10, start_button_rect.y + 10))

            pygame.draw.rect(ekran, SİYAH, instructions_button_rect, 2)
            ekran.blit(instructions_button_text, (instructions_button_rect.x + 10, instructions_button_rect.y + 10))

        elif show_instructions:
            instructions_text = [
                "1. Bilgisayar 4 basamaklı bir sayı tutar.",
                "2. Sayıyı tahmin etmeye çalışın.",
                "3. Her tahminden sonra '+x,-y' geri bildirimi alırsınız.",
                "4. '+x' x sayısı kadar doğru rakam ve", 
                "doğru basamak yerini, '-y' ise y sayısı kadar", 
                "doğru rakam ama yanlış basamak yerini ifade eder."
            ]
            ekran.fill(BEYAZ)
            y_offset = 150
            for line in instructions_text:
                instruction_surface = instructions_font.render(line, True, SİYAH)
                instruction_rect = instruction_surface.get_rect(center=(WIDTH//2, y_offset))
                ekran.blit(instruction_surface, instruction_rect)
                y_offset += 30

            pygame.draw.rect(ekran, SİYAH, back_button_rect, 2)
            ekran.blit(back_button_text, (back_button_rect.x + 10, back_button_rect.y + 10))

        else: 
            pygame.draw.rect(ekran, SİYAH, input_box, 2)
            text_surface = font.render(input_text, True, SİYAH)
            ekran.blit(text_surface, (input_box.x + 5, input_box.y + 5))

            y_offset = 125
            for tahmin, sonuc in tahminler:
                tahmin_surface = font.render(f"{tahmin}: {sonuc}", True, SİYAH)
                ekran.blit(tahmin_surface, (135, y_offset))
                y_offset += 30

            if tahminler and tahminler[-1][1] == "+4":
                pygame.draw.rect(ekran, SİYAH, restart_button_rect, 2)
                ekran.blit(restart_button_text, (restart_button_rect.x + 10, restart_button_rect.y + 10))

        pygame.display.flip()

    pygame.quit()

run_game()
