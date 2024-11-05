import discord
from discord.ext import tasks, commands
import os
from dotenv import load_dotenv
from geeknews_check import get_all_topics
from datetime import datetime

load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")
GUILD_ID = int(os.getenv("GUILD_ID"))
CHANNEL_ID = int(os.getenv("CHANNEL_ID"))
CATEGORY_NAME = "CS"
CHANNEL_NAME = "geeknews"


intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)
last_titles = []
first_run = True


@bot.event
async def on_ready():
    print(f"{bot.user.name} 이 서버에 연결되었습니다.")

    guild = bot.get_guild(GUILD_ID)
    if not guild:
        print(f"서버 {GUILD_ID}를 찾을 수 없습니다.")
        return

    target_channel = None
    for category in guild.categories:
        if category.name == CATEGORY_NAME:
            for channel in category.channels:
                if channel.name == CHANNEL_NAME:
                    target_channel = channel
                    break
            if target_channel:
                break

    if target_channel:
        print(f"카테고리 '{CATEGORY_NAME}'의 채널 '{CHANNEL_NAME}'을 찾았습니다.")
        check_for_new_topics.start(target_channel)
    else:
        print(f"카테고리 '{CATEGORY_NAME}' 내에 '{CHANNEL_NAME}' 채널을 찾을 수 없습니다.")


@tasks.loop(minutes=10)
async def check_for_new_topics(channel):
    global last_titles, first_run

    # 모든 페이지의 최신 토픽들을 가져옴
    current_topics = get_all_topics()
    if not current_topics:
        print("[DEBUG] 최신 토픽을 가져오지 못했습니다.")
        return

    # 현재 날짜 및 시간 포맷
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    timestamp_message = f"##############################\n######## {current_time} ########\n##############################"

    # 첫 실행 시 최신 토픽 하나만 전송하고 이후에만 비교
    if first_run:
        first_topic = current_topics[0]
        message = (f"{timestamp_message}\n\n"
                   f"### 새로운 토픽이 올라왔습니다! ###\n\n"
                   f"**{first_topic['title']}**  \n"
                   f"[토픽 링크]({first_topic['topic_link']})  \n"
                   f"[AI요약내용 링크]({first_topic['content_link']})  \n"
                   f"\n\n"
                   f"\n"
                   f"\n\n")  # 여러 줄의 구분선 추가
        await channel.send(message)
        last_titles = [topic["title"]
                       for topic in current_topics]  # 전체 토픽 제목 저장
        first_run = False
    else:
        # 새로운 토픽 필터링
        new_topics = []
        for topic in current_topics:
            if topic["title"] not in last_titles:
                new_topics.append(topic)

        # 새로운 토픽이 있을 때만 알림 전송
        if new_topics:
            for topic in new_topics:
                # 각 토픽의 제목, 토픽 링크, 내용 링크를 전송
                message = (f"{timestamp_message}\n\n"
                           f"### 새로운 토픽이 올라왔습니다! ###\n\n"
                           f"**{topic['title']}**  \n"
                           f"[토픽 링크]({topic['topic_link']})  \n"
                           f"[AI요약내용 링크]({topic['content_link']})  \n"
                           f"\n\n"
                           f"\n"
                           f"\n\n")  # 여러 줄의 구분선 추가
                await channel.send(message)

            # 새로운 토픽들을 포함해 전체 제목을 업데이트
            last_titles = [topic["title"] for topic in current_topics]


def run_discord_bot():
    bot.run(TOKEN)
