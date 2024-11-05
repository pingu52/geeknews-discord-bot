# GeekNews Discord Bot

이 봇은 GeekNews의 최신 토픽을 자동으로 가져와 지정된 Discord 채널에 게시하는 기능을 제공합니다.

## 기능

-   GeekNews에서 최신 토픽을 자동으로 가져옵니다.
-   지정된 Discord 채널에 토픽 세부 정보를 게시합니다.
-   주기적으로 새로운 토픽을 확인하여 실시간으로 업데이트합니다.

## 요구 사항

-   Python 3.8 이상
-   `discord.py` 라이브러리
-   `requirements.txt` 파일에 있는 기타 필요한 라이브러리

## 설치 방법

1. **저장소 클론**

```shell
git clone https://github.com/your-username/geeknews-discord-bot.git
cd geeknews-discord-bot
```

2. **의존성 설치**

```shell
pip install -r requirements.txt
```

3. **환경 변수 설정**

-   .env 파일을 생성하고, Discord 봇 토큰을 추가합니다.

```
DISCORD_TOKEN=your_discord_token_here
```

4. **봇 실행**

```shell
python main.py
```

## 파일 설명

-   `main.py`: 봇을 실행하는 메인 파일입니다.
-   `discord_bot.py`: Discord와 상호작용하는 봇의 주요 기능과 명령이 포함된 파일입니다.
-   `geeknews_check.py`: GeekNews에서 최신 토픽을 스크래핑하여 가져오는 로직을 포함합니다.

## 사용 방법

1. 봇을 Discord 서버에 초대합니다.
2. 새로운 토픽이 발견될 때마다 지정된 채널에 업데이트 내용을 게시합니다.
