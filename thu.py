import pygame
import sys
import random

# Khởi tạo Pygame
pygame.init()
# Khởi tạo hệ thống âm thanh
pygame.mixer.init()

# Tải nhạc nền
pygame.mixer.music.load("nhacnen.mp3")  # Thay "background_music.mp3" bằng file nhạc nền của bạn
pygame.mixer.music.set_volume(0.5)  # Âm lượng từ 0.0 đến 1.0
pygame.mixer.music.play(-1)  # Phát nhạc nền lặp vô tận (-1)


# Thiết lập màn hình
screen_width, screen_height = 800, 400
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Con đường học tập")

# Màu sắc
WHITE = (255, 255, 255)
GROUND_COLOR = (150, 75, 0)

# Khởi tạo font
font = pygame.font.SysFont(None, 55)

# Tải ảnh nhân vật
chay_images = [
    pygame.image.load("nv1.png"),
    pygame.image.load("nv3.png")
]
chay_images = [pygame.transform.scale(img, (50,80)) for img in chay_images] #kích thước các ảnh
current_run_frame = 0 #khung hoạt ảnh hiện tại
frame_delay = 5 #độ trễ khung hình
frame_counter = 0 # bộ đếm khung hình
nv_image = chay_images[0]
nv_rect = nv_image.get_rect()
nv_rect.topleft = (100, 290)
# Cấu hình trò chơi (thêm điểm cố định cho mỗi vật phẩm)
levels = [
    {  # Level 1
        "background": "bg1.png",
        "obstacles": [("meo.png", 60, 75), ("den.png", 60, 60), ("cay.png", 60, 60), ("ban.png", 60, 60)],
        "items": [
            ("but.png", 60, 60, 12),
            ("wifi.png", 60, 60, 15),
            ("vo.png", 60, 60, 30),
            ("sach.png", 60, 60, 49.5),
            ("laptop.png", 60, 60, 75),
        ],
        "obstacle_limits": [3, 2, 2, 3],
        "item_limits": [3, 2, 2, 2, 1],
    },
    {  # Level 2
        "background": "bg2.png",
        "obstacles": [("SKY.png", 60, 60), ("J97.png", 60, 60)],
        "items": [
            ("pin.png", 40, 40, 12),
            ("chuot.png", 40, 40, 15),
            ("usb.png", 40, 40, 30),
            ("machdien.png", 40, 40, 49.5),
            ("chip.png", 40, 40, 75),
        ],
        "obstacle_limits": [7, 5],
        "item_limits": [3, 2, 2, 2, 1],
    },
    {  # Level 3
        "background": "9.png",
        "obstacles": [("C+.png", 60, 60), ("C.png", 60, 60),("D+.png", 60, 60),("D.png", 60, 60)],
        "items": [
            ("A+.png", 60, 60, 82.5),
            ("A.png", 60, 60, 57),
            ("B+.png", 60, 60, 36.5),
            ("B.png", 60, 60, 20.5),
        ],
        "obstacle_limits": [2, 2,4,5],
        "item_limits": [ 2, 2, 3, 3],
    },
]

# Lớp quản lý đối tượng
class GameObject:
    def __init__(self, image_path, width, height, speed, limit, point_value=0):
        self.image = pygame.transform.scale(pygame.image.load(image_path), (width, height))
        self.rect = self.image.get_rect()
        self.rect.topleft = (screen_width, 300)
        self.speed = speed
        self.spawn_limit = limit
        self.spawn_count = 0
        self.point_value = point_value  # Giá trị điểm của vật phẩm
# Tải hiệu ứng âm thanh
jump_sound = pygame.mixer.Sound("nhay.mp3")  # Âm thanh khi nhảy
pickup_sound = pygame.mixer.Sound("anvatpham.mp3")  # Âm thanh khi nhặt vật phẩm
crash_sound = pygame.mixer.Sound("vacham.mp3")  # Âm thanh khi va chạm

# Đặt âm lượng cho từng hiệu ứng
jump_sound.set_volume(0.7)
pickup_sound.set_volume(0.5)
crash_sound.set_volume(0.8)

# Hàm tạo đối tượng dựa trên cấu hình
def create_objects(config):
    objects = {"obstacles": [], "items": []}
    for i, (img, w, h) in enumerate(config["obstacles"]):
        objects["obstacles"].append(GameObject(img, w, h, random.randint(10, 15), config["obstacle_limits"][i]))
    for i, (img, w, h, point_value) in enumerate(config["items"]):
        objects["items"].append(GameObject(img, w, h, random.randint(15, 20), config["item_limits"][i], point_value))
    return objects

# Hàm hiển thị màn hình bắt đầu
def show_start_screen():
    start_background = pygame.image.load("start.png")
    start_background = pygame.transform.scale(start_background, (screen_width, screen_height))
    screen.blit(start_background, (0, 0))
    instruction_text = font.render("Press SPACE to start", True, (0, 0, 0))
    screen.blit(instruction_text, (screen_width // 2 - instruction_text.get_width() // 2, 200))
    pygame.display.flip()
    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                waiting = False
def show_congratulation_screen():
    congrat_background = pygame.image.load("bg3.png")
    congrat_background = pygame.transform.scale(congrat_background, (screen_width, screen_height))
    screen.blit(congrat_background, (0, 0))
    pygame.mixer.music.stop()  # Dừng nhạc nền hiện tại
    pygame.mixer.music.load("traogiai.mp3")
    pygame.mixer.music.set_volume(0.7)
    pygame.mixer.music.play(-1)  # Lặp nhạc chiến thắng

    button_text = font.render("Winner", True, (255, 255, 255))
    button_rect = pygame.Rect(screen_width // 2 - 150, 250, 300, 70)
    pygame.draw.rect(screen, (0, 128, 0), button_rect)
    screen.blit(button_text, (button_rect.x + 50, button_rect.y + 15))

    pygame.display.flip()

    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if button_rect.collidepoint(event.pos):
                    waiting = False  # Chuyển sang màn hình tốt nghiệp
                    show_graduation_screen()


# Hàm hiển thị màn hình Bằng    Tốt Nghiệp
def show_graduation_screen():
    screen.fill(WHITE)
    # Tải ảnh chúc mừng tốt nghiệp
    graduation_image = pygame.image.load("kisu.png")
    graduation_image = pygame.transform.scale(graduation_image, (800, 400))  # Điều chỉnh kích thước của ảnh
    screen.blit(graduation_image, (0, 0)) # Vẽ ảnh lên màn hình

    # Vẽ nút "END" ở góc phải dưới màn hình
    end_button_text = font.render("END", True, (255, 0, 0))  # Tạo chữ "END"
    end_button_rect = pygame.Rect(screen_width - end_button_text.get_width() - 20, screen_height - end_button_text.get_height() - 20, end_button_text.get_width(), end_button_text.get_height())
    pygame.draw.rect(screen, (0, 0, 255), end_button_rect)  # Vẽ hình chữ nhật màu xanh
    screen.blit(end_button_text, (end_button_rect.x + 10, end_button_rect.y + 10))  # Vẽ chữ "END" lên nút

    pygame.display.flip()

    # Chờ cho người chơi nhấn nút "END" để thoát
    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if end_button_rect.collidepoint(event.pos):  # Kiểm tra nếu nhấn vào nút "END"
                    waiting = False

# Hàm hiển thị tùy chọn sau màn 1 và màn 2
def show_level_end_screen(level):
    if level == 1:
        transition_bg = pygame.image.load("12.png")
    elif level == 2:
        transition_bg = pygame.image.load("23.png")
    transition_bg = pygame.transform.scale(transition_bg, (screen_width, screen_height))
    screen.blit(transition_bg, (0, 0))

    message_text = font.render(f"Hoàn thành màn {level}!", True, (0, 0, 0))
    option1_text = font.render("Press 1: Get The Engineering Degree ", True, (0, 0, 0))
    option2_text = font.render("Press 2: Continue", True, (0, 0, 0)) 
    screen.blit(message_text, (screen_width // 2 - message_text.get_width() // 2, 100))
    screen.blit(option1_text, (screen_width // 2 - option1_text.get_width() // 2, 200))
    screen.blit(option2_text, (screen_width // 2 - option2_text.get_width() // 2, 300))
    pygame.display.flip()
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    show_graduation_screen()
                    return False
                if event.key == pygame.K_2:
                    return True
    

# Biến trạng thái
current_level = 0
score = 0
total_score = 0
objects = create_objects(levels[current_level])
background = pygame.image.load(levels[current_level]["background"])
background = pygame.transform.scale(background, (screen_width, screen_height))
screen.blit(background, (0, 0))
# Biến chuyển động của Mario
speed_x = 5
jump_power = 15
gravity = 1
is_jumping = False
y_velocity = 0

# Biến điều khiển
running = True
object_active = False
current_object = None
clock = pygame.time.Clock()

# Hiển thị màn hình bắt đầu
show_start_screen()

# Vòng lặp chính
while running:
    # Kiểm tra sự kiện
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and not is_jumping:
                jump_sound.play() # phát âm thanh khi nhảy
                is_jumping = True
                y_velocity = -jump_power

    # Điều khiển Mario
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] or keys[pygame.K_RIGHT]:
        frame_counter +=1
        if frame_counter >= frame_delay:#đổi khung hình
            frame_counter=0
            current_run_frame= (current_run_frame + 1) % len(chay_images) # vòng lặp các khung hình
        nv_image=chay_images[current_run_frame] #cập nhật hình ảnh hoạt ảnh
        if keys[pygame.K_LEFT]:
            nv_rect.x -= speed_x
        if keys[pygame.K_RIGHT]:
            nv_rect.x += speed_x 
    else:
        nv_image=chay_images[0] #trạng thái đứng yên

    # Trọng lực
    if is_jumping:
        nv_rect.y += y_velocity
        y_velocity += gravity
        if nv_rect.bottom >= 360:
            nv_rect.bottom = 360
            is_jumping = False
            y_velocity = 0

    # Giới hạn Mario trong màn hình
    nv_rect.left = max(0, nv_rect.left)
    nv_rect.right = min(screen_width, nv_rect.right)

    # Quản lý đối tượng
    if not object_active:
      # Lấy các đối tượng có thể tạo ra, bao gồm các vật phẩm và chướng ngại vật
      available_objects = objects["obstacles"] + [item for item in objects["items"] if item.spawn_count < item.spawn_limit]
      if available_objects:
        # Chọn ngẫu nhiên một đối tượng để tạo mới
        current_object = random.choice(available_objects)
        current_object.rect.x = screen_width  # Đặt đối tượng ở vị trí bên phải màn hình
        current_object.spawn_count += 1
        object_active = True

    # Di chuyển đối tượng
    if object_active:
      current_object.rect.x -= current_object.speed  # Di chuyển đối tượng sang trái
      if current_object.rect.right < 0:  # Kiểm tra xem đối tượng đã ra khỏi màn hình chưa
        object_active = False  # Ngừng vẽ đối tượng khi ra ngoài màn hình

     # Va chạm
    if object_active and nv_rect.colliderect(current_object.rect):  # Kiểm tra va chạm
        if current_object in objects["obstacles"]:  # Nếu va chạm với chướng ngại vật
          crash_sound.play() #Phát âm thanh va chạm
          print("Game Over!")
          running = False
        else:  # Nếu va chạm với vật phẩm
          pickup_sound.play() #phát âm thanh khi ăn vật phẩm
          score += current_object.point_value  # Cộng điểm cho vật phẩm
          object_active = False  # Ngừng vẽ vật phẩm sau khi va chạm

     # Vẽ lại màn hình
    screen.fill(WHITE)  # Xóa màn hình cũ để tránh nhiễu
    screen.blit(background, (0, 0))  # Vẽ lại nền
    pygame.draw.rect(screen, GROUND_COLOR, (0, 360, screen_width, 40))  # Vẽ lại mặt đất
    screen.blit(nv_image, nv_rect)  # Vẽ lại nhân vật Mario

     # Nếu có đối tượng đang di chuyển, vẽ nó lên màn hình
    if object_active:
     screen.blit(current_object.image, current_object.rect)

     # Hiển thị điểm số
    score_text = font.render(f"Score: {total_score + score}", True, (0, 0, 0))
    screen.blit(score_text, (10, 10))

    pygame.display.flip()  # Cập nhật màn hình sau khi vẽ lại

    # Kiểm tra hoàn thành màn chơi
    if score >= 300:
        total_score += score
        if current_level < len(levels) - 1:
            if not show_level_end_screen(current_level + 1):
                running = False
            else:
                current_level += 1
                objects = create_objects(levels[current_level])
                background = pygame.image.load(levels[current_level]["background"])
                score = 0
        else: 
            #hiển thị màn hình chúc mừng
            show_congratulation_screen()
            break  

    # Vẽ màn hình
    screen.blit(background, (0, 0))
    pygame.draw.rect(screen, GROUND_COLOR, (0, 360, screen_width, 40))
    screen.blit(nv_image, nv_rect)
    if object_active:
        screen.blit(current_object.image, current_object.rect)

    # Hiển thị điểm số
    score_text = font.render(f"Score: {total_score + score}", True, (0, 0, 0))
    screen.blit(score_text, (10, 10))
    pygame.display.flip()

    # Cập nhật FPS
    clock.tick(30)

pygame.quit()
sys.exit()
      