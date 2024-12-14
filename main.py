import pygame
import sys
import random

# Initialize pygame
pygame.init()

# Set the window size
width, height = 800, 600
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Banana Clicking Game")

# Load the original banana image. Assume you have a 'banana.png' image. You can replace it with the actual image path.
original_banana_image = pygame.image.load('banana.png').convert_alpha()
banana_rect = original_banana_image.get_rect(center=(width // 2, height // 2))

# Record the number of clicks
click_count = 0
# 记录游戏分数
score = 0
# 任务目标列表，每个元素代表一个任务阶段需要达到的点击次数（现在按照分数来对应判断）
task_targets = list(range(50, 1001, 50))
# 记录当前完成的任务阶段索引
completed_task_index = 0

# Set the font for displaying the click count and store-related text
font = pygame.font.Font(None, 30)

# Define the number of animation frames. You can adjust it to change the duration of the animation.
animation_frames = 10
current_frame = 0
# Store the offsets of the banana image during the animation. Increase the offset range to enhance the shaking effect.
offset_x = 0
offset_y = 0
# The range of offsets. You can adjust this value to control the shaking amplitude.
offset_range = 10

# List related to the fireworks effect. Each element represents the properties of a firework.
fireworks = []

clock = pygame.time.Clock()

# Define the list of banana skin colors. You can expand or modify it according to your needs.
banana_skins = [(255, 255, 0), (255, 0, 0), (0, 255, 0), (0, 0, 255)]
current_skin_index = 0  # Index of the currently selected skin

# Variables related to the store interface
store_open = False
store_text = font.render("Store", True, (0, 0, 0))
store_rect = store_text.get_rect(topleft=(10, 10))
skin_preview_size = 50
skin_previews = []
for color in banana_skins:
    skin_surface = pygame.Surface((skin_preview_size, skin_preview_size))
    skin_surface.fill(color)
    skin_previews.append(skin_surface)

# 新手引导相关变量，用于控制新手引导的显示与隐藏，True表示显示引导，False表示隐藏引导
show_tutorial = True
# 新手引导提示信息，可以根据实际情况调整具体的引导文本内容
tutorial_texts = [
    "Welcome to the Banana Clicking Game!",
    "Click on the banana in the middle of the screen to increase the click count.",
    "Click on 'Store' at the top left corner to change the banana skin. Give it a try!",
    "Press Space or Enter to close this tutorial and start the game."
]
tutorial_index = 0  # 当前显示的引导信息索引

# Define the function to draw fireworks
def draw_fireworks():
    new_fireworks = []
    for firework in fireworks:
        x, y, radius, color, alpha, life = firework
        if life > 0:
            # Adjust the transparency and radius according to the remaining life.
            s = int(alpha * 255)
            pygame.draw.circle(screen, (color[0], color[1], color[2], s), (x, y), radius)
            new_radius = radius + 1 if radius < 50 else radius
            new_alpha = alpha * 0.9 if alpha > 0.1 else 0
            new_life = life - 1
            new_fireworks.append((x, y, new_radius, color, new_alpha, new_life))
    return new_fireworks

def draw_task_progress():
    global completed_task_index, task_targets, score
    # 构建显示文本内容，展示当前分数和当前任务阶段的目标点击次数对应的分数（假设每个点击次数对应1分，可按需调整）
    progress_text = f"Score Progress: {score}/{task_targets[completed_task_index]}"
    text_surface = font.render(progress_text, True, (0, 0, 0))
    x = width - text_surface.get_width() - 10  # 设置文本在屏幕右下角的x坐标，距离右边缘10像素
    y = height - text_surface.get_height() - 10  # 设置文本在屏幕右下角的y坐标，距离下边缘10像素
    screen.blit(text_surface, (x, y))


while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if store_rect.collidepoint(event.pos):
                store_open = not store_open
            elif banana_rect.collidepoint(event.pos):
                click_count += 1
                # 按照概率增加分数
                random_number = random.random()
                if random_number < 0.05:  # 5%几率加10分
                    score += 10
                elif random_number < 0.15:  # 10%几率加5分（0.05到0.15的区间）
                    score += 5
                elif random_number < 0.35:  # 20%几率加2分（0.15到0.35的区间）
                    score += 2
                else:  # 其余情况加1分
                    score += 1
                if score >= task_targets[completed_task_index]:  # 此处改为用分数判断是否完成任务阶段
                    print(f"Congratulations! You've completed the task stage {completed_task_index + 1}!")
                    completed_task_index += 1
                    if completed_task_index >= len(task_targets):
                        print("You've reached the maximum click count task limit. You're amazing!")
                        # 这里可以添加更多达到上限后的处理逻辑，比如游戏结束、展示特殊画面等，目前仅做简单提示
                current_frame = 0
                # Generate a larger range of initial offsets after each click to create a more obvious shaking effect.
                offset_x = random.randint(-offset_range, offset_range)
                offset_y = random.randint(-offset_range, offset_range)
                # Add the fireworks effect. Randomly generate the position, color, initial radius, initial transparency, and life of the fireworks.
                for _ in range(5):
                    x = random.randint(0, width)
                    y = random.randint(0, height)
                    color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
                    radius = 5
                    alpha = 1.0
                    life = 20
                    fireworks.append((x, y, radius, color, alpha, life))
            elif store_open:
                for i in range(len(banana_skins)):
                    skin_rect = pygame.Rect(10 + i * (skin_preview_size + 10), 60, skin_preview_size, skin_preview_size)
                    if skin_rect.collidepoint(event.pos):
                        current_skin_index = i
                        break
        elif event.type == pygame.KEYDOWN:
            if show_tutorial:  # 按下任意键且处于新手引导显示状态时，隐藏引导
                show_tutorial = False

    screen.fill((255, 255, 255))  # Fill the background with white. You can change the background color.

    if show_tutorial:
        # 显示新手引导信息
        for i, text in enumerate(tutorial_texts):
            tutorial_surface = font.render(text, True, (0, 0, 0))
            screen.blit(tutorial_surface, (width // 2 - tutorial_surface.get_width() // 2, height // 2 + i * 30))
    else:
        # Draw the banana image according to the current skin index.
        current_banana_image = original_banana_image.copy()
        current_banana_image.fill(banana_skins[current_skin_index], special_flags=pygame.BLEND_RGB_MULT)
        if current_frame < animation_frames:
            temp_rect = banana_rect.copy()
            temp_rect.x += offset_x
            temp_rect.y += offset_y
            screen.blit(current_banana_image, temp_rect)
            current_frame += 1
        else:
            screen.blit(current_banana_image, banana_rect)

        # Draw the fireworks effect.
        fireworks = draw_fireworks()

        # Render and display the text of the click count.
        text_surface = font.render(f"Click Count: {click_count}", True, (0, 0, 0))
        screen.blit(text_surface, (width // 2 - text_surface.get_width() // 2, 20))

        # 绘制任务进度信息
        draw_task_progress()

        # Draw the elements related to the store.
        screen.blit(store_text, store_rect)
        if store_open:
            for i, skin_preview in enumerate(skin_previews):
                pygame.draw.rect(screen, (0, 0, 0), (10 + i * (skin_preview_size + 10), 60, skin_preview_size, skin_preview_size), 2)
                screen.blit(skin_preview, (10 + i * (skin_preview_size + 10), 60))
                if i == current_skin_index:
                    selected_text = font.render("Selected", True, (0, 0, 0))
                    screen.blit(selected_text, (10 + i * (skin_preview_size + 10), 60 + skin_preview_size + 5))

    pygame.display.flip()
    clock.tick(60)  # Set the frame rate to 60.