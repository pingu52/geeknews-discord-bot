import requests
from bs4 import BeautifulSoup

BASE_URL = "https://news.hada.io"


def get_all_topics():
    page = 1
    topics = []

    while True:
        url = f"{BASE_URL}/?page={page}"
        response = requests.get(url)
        if response.status_code != 200:
            print("웹페이지 접근 불가")
            break

        soup = BeautifulSoup(response.text, "html.parser")
        topic_rows = soup.find_all("div", class_="topic_row")

        # 각 토픽 정보 수집
        for topic in topic_rows:
            title, topic_link, content_link, content = get_topic_info(topic)
            if title and topic_link and content_link and content:
                topics.append({
                    "title": title,
                    "topic_link": topic_link,
                    "content_link": content_link,
                    "content": content
                })

        # "토픽 더 불러오기" 링크가 없으면 종료
        more_link = soup.find("a", class_="u", text="토픽 더 불러오기")
        if more_link is None:
            break

        page += 1  # 다음 페이지로 이동

    return topics


def get_topic_info(topic):
    # 제목과 토픽 링크
    title_tag = topic.find("div", class_="topictitle").find("a")
    title = title_tag.get_text(strip=True)
    topic_link = title_tag["href"]

    # 상대경로를 절대경로로 변환
    if not topic_link.startswith("http"):
        topic_link = BASE_URL + topic_link

    # '내용 링크'의 ID 추출 및 링크 구성
    content_link_tag = topic.find("a", href=True, class_="c99 breakall")
    if content_link_tag is None:
        print("[DEBUG] 내용 링크를 찾지 못했습니다.")
        return None, None, None, None

    topic_id = content_link_tag["href"].split("id=")[-1]
    content_link = f"{BASE_URL}/topic?id={topic_id}"

    # 디버그용으로 링크 출력
    print(f"[DEBUG] 세부 내용을 가져올 링크: {content_link}")

    # 상세 내용 가져오기
    content = get_detailed_content(content_link)

    return title, topic_link, content_link, content


def get_detailed_content(content_url):
    response = requests.get(content_url)

    # 디버그용으로 페이지 접근 상태 출력
    if response.status_code != 200:
        print(f"[DEBUG] 세부 내용 페이지 접근 불가: {content_url}")
        return None
    else:
        print(f"[DEBUG] 세부 내용 페이지 접근 성공: {content_url}")

    soup = BeautifulSoup(response.text, "html.parser")
    content_div = soup.find("span", id="topic_contents")

    if content_div is None:
        print("[DEBUG] 'topic_contents'를 포함하는 <span> 태그를 찾을 수 없습니다.")
        return None

    # 마크다운 형식으로 포맷팅
    content_text = parse_topic_contents(content_div)
    return content_text


def parse_topic_contents(content_div):
    """주어진 content_div에서 마크다운 형식으로 필요한 내용을 포맷팅하여 가져옴"""
    lines = []

    for element in content_div.find_all(['li', 'code', 'br']):
        if element.name == "li":
            # 리스트 항목은 하이픈으로 시작
            lines.append(f"- {element.get_text(strip=True)}")
        elif element.name == "code":
            # 코드 텍스트는 백틱으로 감싸기
            lines.append(f"`{element.get_text(strip=True)}`")
        elif element.name == "br":
            # 줄바꿈 추가
            lines.append("\n")

    # 최종 내용을 마크다운 형식으로 합치기
    content_text = "\n".join(lines).replace("\n\n", "\n").strip()
    return content_text
